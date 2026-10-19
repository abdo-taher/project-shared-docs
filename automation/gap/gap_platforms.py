"""Minimal GitHub (intake repository) and GitLab (backend project) adapters.

Only the calls the coordinator needs. Every read of user-controlled content
(issue bodies, comments, notes) returns plain data; callers decide trust from
platform-reported identities (authors, label-event actors, permissions), never
from text inside the content.
"""

from __future__ import annotations

import urllib.parse

from gap_http import ApiError, Http

GITHUB_LABELS = {
    "api-gap": ("5319e7", "Structured API gap request (capitalix.api-gap.v1)"),
    "gap:submitted": ("c5def5", "Gap: submitted, not yet processed by the coordinator"),
    "gap:validating": ("c5def5", "Gap: the coordinator is validating it"),
    "gap:needs-triage": ("fbca04", "Gap: waiting for a trusted maintainer (gap:triage-approved)"),
    "gap:accepted": ("0e8a16", "Gap: accepted; backend work is tracked"),
    "gap:duplicate": ("cfd3d7", "Gap: same consumer already reported this gap"),
    "gap:rejected": ("b60205", "Gap: rejected (see the coordinator comment)"),
    "gap:in-progress": ("1d76db", "Gap: backend change in progress"),
    "gap:contract-published": ("0e8a16", "Gap: an approved contract containing the fix is published"),
    "gap:consumer-verified": ("0e8a16", "Gap: the consumer verified the published fix"),
    "gap:resolved": ("0e8a16", "Gap: resolved"),
    "gap:blocked": ("d93f0b", "Gap: blocked (decision needed or permanent failure)"),
    # Input labels: applied by trusted maintainers only; the coordinator never sets them.
    "gap:triage-approved": ("5319e7", "Maintainer approval for an untrusted or flagged gap request"),
    "gap:triage-rejected": ("5319e7", "Maintainer rejection of a gap request"),
}
STATE_LABELS = [name for name in GITHUB_LABELS if name.startswith("gap:") and not name.startswith("gap:triage-")]

GITLAB_LABELS = {
    "api-gap": "#5319e7",
    "gap::accepted": "#0e8a16",
    "gap::in-progress": "#1d76db",
    "gap::contract-published": "#0e8a16",
    "gap::resolved": "#0e8a16",
    "gap::blocked": "#d93f0b",
    "gap-sensitive": "#b60205",
    # Input labels (trusted backend roles; verified through label events and member access).
    "gap-dispatch::approved": "#5319e7",
    "gap-owner::approved": "#5319e7",
    "gap-triage::not-backend": "#5319e7",
    "gap-triage::needs-decision": "#5319e7",
    "gap-dispatch::failed": "#d93f0b",
}
GITLAB_STATE_LABELS = ["gap::accepted", "gap::in-progress", "gap::contract-published", "gap::resolved",
                       "gap::blocked"]


class GitHub:
    def __init__(self, repo: str, token: str | None, http: Http | None = None,
                 base: str = "https://api.github.com"):
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.repo = repo
        self.can_write = bool(token)
        self.http = http or Http(base, headers)
        if http is not None and token:
            self.http.headers.update(headers)

    def _r(self, path: str) -> str:
        return f"repos/{self.repo}/{path}"

    def viewer(self) -> str | None:
        return self.http.get("user").get("login") if self.can_write else None

    def open_issues(self) -> list[dict]:
        # Every open issue: requests created through the API by outside users lose their labels.
        return [i for i in self.http.paginate(self._r("issues"), {"state": "open"}) if "pull_request" not in i]

    def issue(self, number: int) -> dict:
        return self.http.get(self._r(f"issues/{number}"))

    def comments(self, number: int) -> list[dict]:
        return self.http.paginate(self._r(f"issues/{number}/comments"))

    def label_events(self, number: int) -> list[dict]:
        return [e for e in self.http.paginate(self._r(f"issues/{number}/events"))
                if e.get("event") in ("labeled", "unlabeled")]

    def permission(self, login: str) -> str:
        """admin | maintain | write | triage | read | none (the platform's answer, not the issue's)."""
        try:
            data = self.http.get(self._r(f"collaborators/{urllib.parse.quote(login)}/permission"))
        except ApiError as exc:
            if exc.status in (403, 404):
                return "none"
            raise
        return data.get("role_name") or data.get("permission") or "none"

    def ensure_labels(self) -> None:
        existing = {l["name"] for l in self.http.paginate(self._r("labels"))}
        for name, (color, description) in GITHUB_LABELS.items():
            if name not in existing:
                self.http.request("POST", self._r("labels"),
                                  body={"name": name, "color": color, "description": description})

    def set_labels(self, number: int, add: list[str], remove: list[str]) -> None:
        for name in remove:
            try:
                self.http.request("DELETE", self._r(f"issues/{number}/labels/{urllib.parse.quote(name)}"))
            except ApiError as exc:
                if exc.status != 404:
                    raise
        if add:
            self.http.request("POST", self._r(f"issues/{number}/labels"), body={"labels": add})

    def comment(self, number: int, body: str) -> dict:
        return self.http.request("POST", self._r(f"issues/{number}/comments"), body={"body": body})[0]

    def edit_comment(self, comment_id: int, body: str) -> None:
        self.http.request("PATCH", self._r(f"issues/comments/{comment_id}"), body={"body": body})

    def close(self, number: int, reason: str = "completed") -> None:
        self.http.request("PATCH", self._r(f"issues/{number}"), body={"state": "closed", "state_reason": reason})


class GitLab:
    def __init__(self, project: str, token: str | None, http: Http | None = None,
                 base: str = "https://gitlab.com/api/v4"):
        # Bearer works for project/personal access tokens and OAuth tokens alike.
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        self.project = urllib.parse.quote(project, safe="")
        self.http = http or Http(base, headers)
        if http is not None and token:
            self.http.headers.update(headers)
        self._access: dict[int, int] = {}

    def _p(self, path: str) -> str:
        return f"projects/{self.project}/{path}"

    def find_by_fingerprint(self, fingerprint: str) -> list[dict]:
        found = self.http.paginate(self._p("issues"), {"search": fingerprint[:16], "in": "title",
                                                        "state": "all", "order_by": "created_at", "sort": "asc"})
        marker = f"capitalix-gap fingerprint={fingerprint}"
        return sorted((i for i in found if marker in (i.get("description") or "")), key=lambda i: i["iid"])

    def issue(self, iid: int) -> dict:
        return self.http.get(self._p(f"issues/{iid}"))

    def gap_issues(self, state: str = "opened") -> list[dict]:
        return self.http.paginate(self._p("issues"), {"labels": "api-gap", "state": state})

    def create_issue(self, title: str, description: str, labels: list[str]) -> dict:
        return self.http.request("POST", self._p("issues"), body={
            "title": title, "description": description, "labels": ",".join(labels)})[0]

    def update_issue(self, iid: int, **fields) -> dict:
        return self.http.request("PUT", self._p(f"issues/{iid}"), body=fields)[0]

    def notes(self, iid: int) -> list[dict]:
        return self.http.paginate(self._p(f"issues/{iid}/notes"), {"sort": "asc"})

    def add_note(self, iid: int, body: str) -> dict:
        return self.http.request("POST", self._p(f"issues/{iid}/notes"), body={"body": body})[0]

    def label_events(self, iid: int) -> list[dict]:
        return self.http.paginate(self._p(f"issues/{iid}/resource_label_events"))

    def access_level(self, user_id: int) -> int:
        """Effective project access level (inherited membership included); 0 when not a member."""
        if user_id not in self._access:
            try:
                self._access[user_id] = int(self.http.get(self._p(f"members/all/{user_id}")).get("access_level", 0))
            except ApiError as exc:
                if exc.status != 404:
                    raise
                self._access[user_id] = 0
        return self._access[user_id]

    def related_merge_requests(self, iid: int) -> list[dict]:
        return self.http.paginate(self._p(f"issues/{iid}/related_merge_requests"))

    def create_merge_request(self, source: str, title: str, description: str, target: str = "main") -> dict:
        return self.http.request("POST", self._p("merge_requests"), body={
            "source_branch": source, "target_branch": target, "title": title, "description": description,
            "remove_source_branch": False, "labels": "api-gap"})[0]

    def pipelines(self, sha: str) -> list[dict]:
        return self.http.paginate(self._p("pipelines"), {"sha": sha, "ref": "main"}, limit=50)

    def pipeline_jobs(self, pipeline_id: int) -> list[dict]:
        return self.http.paginate(self._p(f"pipelines/{pipeline_id}/jobs"), {"include_retried": "false"})

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        if ancestor == descendant:
            return True
        query = urllib.parse.urlencode([("refs[]", ancestor), ("refs[]", descendant)])
        base = self.http.get(self._p(f"repository/merge_base?{query}"))
        return (base or {}).get("id") == ancestor

    def file_at(self, path: str, ref: str) -> bytes | None:
        try:
            return self.http.request("GET", self._p(f"repository/files/{urllib.parse.quote(path, safe='')}/raw"),
                                     params={"ref": ref}, raw=True)[0]
        except ApiError as exc:
            if exc.status == 404:
                return None
            raise

    def ensure_labels(self) -> None:
        existing = {l["name"] for l in self.http.paginate(self._p("labels"))}
        for name, color in GITLAB_LABELS.items():
            if name not in existing:
                self.http.request("POST", self._p("labels"), body={"name": name, "color": color})

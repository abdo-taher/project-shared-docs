"""GitHub backend-tracking adapter: the backend issues and pull requests live in the development repository.

The coordinator, dispatcher and worker were written against a small tracker interface (issues with `iid`,
`state` opened/closed, label names, notes, label events, access levels, related change requests). This adapter
implements exactly that interface on top of GitHub Issues and Pull Requests of the backend repository, so no
decision logic had to change. All answers are normalized to plain data; trust is derived from GitHub-reported
identities (label-event actors and repository permissions), never from issue text.
"""

from __future__ import annotations

import urllib.parse

from gap_http import ApiError, Http

LABELS = {
    "api-gap": "5319e7",
    "gap::accepted": "0e8a16",
    "gap::in-progress": "1d76db",
    "gap::contract-published": "0e8a16",
    "gap::resolved": "0e8a16",
    "gap::blocked": "d93f0b",
    "gap-sensitive": "b60205",
    # Input labels (trusted writers/owner; verified through label events and repository permission).
    "gap-dispatch::approved": "5319e7",
    "gap-owner::approved": "5319e7",
    "gap-triage::not-backend": "5319e7",
    "gap-triage::needs-decision": "5319e7",
    "gap-dispatch::failed": "d93f0b",
}
STATE_LABELS = ["gap::accepted", "gap::in-progress", "gap::contract-published", "gap::resolved", "gap::blocked"]
# repository role -> the numeric levels the policy uses (reporter 20, developer 30, maintainer 40, owner 50)
ROLE_LEVEL = {"admin": 50, "maintain": 40, "write": 30, "triage": 20, "read": 10}


class GitHubBackend:
    def __init__(self, repo: str, token: str | None, http: Http | None = None, base: str = "https://api.github.com"):
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.repo = repo
        self.http = http or Http(base, headers)
        if http is not None and token:
            self.http.headers.update(headers)
        self._logins: dict[int, str] = {}
        self._levels: dict[str, int] = {}

    def _r(self, path: str) -> str:
        return f"repos/{self.repo}/{path}"

    @staticmethod
    def _issue(raw: dict) -> dict:
        return {"iid": raw["number"], "title": raw.get("title", ""), "description": raw.get("body") or "",
                "state": "opened" if raw.get("state") == "open" else "closed",
                "labels": [l["name"] if isinstance(l, dict) else l for l in raw.get("labels", [])],
                "web_url": raw.get("html_url", ""), "created_at": raw.get("created_at", ""),
                "author": (raw.get("user") or {}).get("login", "")}

    # ------------------------------------------------------------------ issues

    def gap_issues(self, state: str = "opened") -> list[dict]:
        wanted = {"opened": "open", "closed": "closed", "all": "all"}[state]
        raw = self.http.paginate(self._r("issues"), {"labels": "api-gap", "state": wanted})
        return [self._issue(i) for i in raw if "pull_request" not in i]

    def find_by_fingerprint(self, fingerprint: str) -> list[dict]:
        marker = f"capitalix-gap fingerprint={fingerprint}"
        found = [i for i in self.gap_issues("all") if marker in i["description"]]
        return sorted(found, key=lambda i: i["iid"])

    def issue(self, iid: int) -> dict:
        return self._issue(self.http.get(self._r(f"issues/{iid}")))

    def create_issue(self, title: str, description: str, labels: list[str]) -> dict:
        return self._issue(self.http.request("POST", self._r("issues"), body={
            "title": title, "body": description, "labels": labels})[0])

    def update_issue(self, iid: int, **fields) -> dict:
        add = [l for l in fields.get("add_labels", "").split(",") if l]
        remove = [l for l in fields.get("remove_labels", "").split(",") if l]
        for name in remove:
            try:
                self.http.request("DELETE", self._r(f"issues/{iid}/labels/{urllib.parse.quote(name)}"))
            except ApiError as exc:
                if exc.status != 404:
                    raise
        if add:
            self.http.request("POST", self._r(f"issues/{iid}/labels"), body={"labels": add})
        if fields.get("state_event") == "close":
            self.http.request("PATCH", self._r(f"issues/{iid}"), body={"state": "closed", "state_reason": "not_planned"})
        return self.issue(iid)

    def notes(self, iid: int) -> list[dict]:
        return self.http.paginate(self._r(f"issues/{iid}/comments"))

    def add_note(self, iid: int, body: str) -> dict:
        return self.http.request("POST", self._r(f"issues/{iid}/comments"), body={"body": body})[0]

    def label_events(self, iid: int) -> list[dict]:
        out = []
        for event in self.http.paginate(self._r(f"issues/{iid}/events")):
            if event.get("event") not in ("labeled", "unlabeled"):
                continue
            actor = event.get("actor") or {}
            if actor.get("id"):
                self._logins[int(actor["id"])] = actor.get("login", "")
            out.append({"action": "add" if event["event"] == "labeled" else "remove",
                        "label": {"name": (event.get("label") or {}).get("name", "")},
                        "user": {"id": actor.get("id", 0), "username": actor.get("login", "")}})
        return out

    def access_level(self, user_id: int) -> int:
        """Repository permission of the account with this id (0 when it is not a collaborator)."""
        login = self._logins.get(user_id)
        if login is None:
            try:
                login = self.http.get(f"user/{user_id}").get("login", "")
            except ApiError:
                login = ""
            self._logins[user_id] = login
        if not login:
            return 0
        if login not in self._levels:
            try:
                data = self.http.get(self._r(f"collaborators/{urllib.parse.quote(login)}/permission"))
                self._levels[login] = ROLE_LEVEL.get(data.get("role_name") or data.get("permission") or "", 0)
            except ApiError as exc:
                if exc.status not in (403, 404):
                    raise
                self._levels[login] = 0
        return self._levels[login]

    # ------------------------------------------------------------------ pull requests

    def related_merge_requests(self, iid: int) -> list[dict]:
        """Pull requests that reference this issue (cross-references), normalized to opened/merged/closed."""
        numbers: list[int] = []
        for event in self.http.paginate(self._r(f"issues/{iid}/timeline")):
            source = (event.get("source") or {}).get("issue") or {}
            if event.get("event") == "cross-referenced" and "pull_request" in source:
                repo = (source.get("repository") or {}).get("full_name", self.repo)
                if repo == self.repo and source["number"] not in numbers:
                    numbers.append(source["number"])
        out = []
        for number in numbers:
            pr = self.http.get(self._r(f"pulls/{number}"))
            state = "merged" if pr.get("merged") else ("opened" if pr.get("state") == "open" else "closed")
            out.append({"iid": number, "state": state, "target_branch": (pr.get("base") or {}).get("ref"),
                        "merge_commit_sha": pr.get("merge_commit_sha"), "sha": (pr.get("head") or {}).get("sha"),
                        "merged_at": pr.get("merged_at"), "draft": bool(pr.get("draft")),
                        "web_url": pr.get("html_url", "")})
        return out

    def file_at(self, path: str, ref: str) -> bytes | None:
        try:
            return self.http.request("GET", self._r(f"contents/{urllib.parse.quote(path)}"), params={"ref": ref},
                                     raw=True, headers={"Accept": "application/vnd.github.raw+json"})[0]
        except ApiError as exc:
            if exc.status == 404:
                return None
            raise

    def ensure_labels(self) -> None:
        existing = {l["name"] for l in self.http.paginate(self._r("labels"))}
        for name, color in LABELS.items():
            if name not in existing:
                self.http.request("POST", self._r("labels"), body={"name": name, "color": color})

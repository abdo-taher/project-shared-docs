#!/usr/bin/env python3
"""Read-only audit of the development -> production (GitLab main) relationship for API gap fixes.

  python3 scripts/gap/promotion_audit.py --dev-repo ~/projects/capitalix \\
      --dev-ref origin/integration/E01-FOUNDATION-SAAS --prod-ref refs/prod/main [--json]

Uses only git plumbing on the given local clone (no fetch, no checkout, no
write, no network); safe while agents are running. Reports:

  - whether the development and production histories share an ancestor
    (today they do not: GitLab main is an independent snapshot, so promotion
    cannot rely on git ancestry);
  - every API gap resolution evidence file on the development ref and whether
    the same file (same bytes) is present on the production ref;
  - evidence files present on production but not on development (would be lost
    by a development-led promotion).

Exit codes: 0 audited; 1 something would be lost by promotion or is missing;
3 input error.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

RESOLUTION_DIR = "docs/api-gap/resolutions"


def git(repo: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(f"git {args[0]} failed: {result.stderr.strip()[:200]}")
    return result


def evidence(repo: str, ref: str) -> dict[str, str]:
    listing = git(repo, "ls-tree", "-r", ref, "--", RESOLUTION_DIR, check=False)
    out = {}
    for line in listing.stdout.splitlines():
        meta, _, path = line.partition("\t")
        if path.endswith(".json"):
            out[path.rsplit("/", 1)[-1]] = meta.split()[2]  # blob id
    return out


def audit(repo: str, dev_ref: str, prod_ref: str) -> dict:
    dev_sha = git(repo, "rev-parse", "--verify", dev_ref).stdout.strip()
    prod_sha = git(repo, "rev-parse", "--verify", prod_ref).stdout.strip()
    base = git(repo, "merge-base", dev_ref, prod_ref, check=False)
    related = base.returncode == 0 and bool(base.stdout.strip())
    dev, prod = evidence(repo, dev_ref), evidence(repo, prod_ref)
    return {
        "dev_ref": dev_ref, "dev_commit": dev_sha, "prod_ref": prod_ref, "prod_commit": prod_sha,
        "shared_ancestor": base.stdout.strip() if related else None,
        "promotion_by_ancestry_possible": related,
        "dev_only": sorted(n for n in dev if n not in prod),
        "prod_only": sorted(n for n in prod if n not in dev),
        "different": sorted(n for n in dev if n in prod and dev[n] != prod[n]),
        "in_both": sorted(n for n in dev if n in prod and dev[n] == prod[n]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dev-repo", required=True, help="local clone containing both refs")
    parser.add_argument("--dev-ref", required=True)
    parser.add_argument("--prod-ref", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = audit(args.dev_repo, args.dev_ref, args.prod_ref)
    problems = bool(report["prod_only"] or report["different"] or report["dev_only"])
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"development {report['dev_ref']} @ {report['dev_commit'][:12]}")
        print(f"production  {report['prod_ref']} @ {report['prod_commit'][:12]}")
        print("shared ancestor: " + (report["shared_ancestor"][:12] if report["shared_ancestor"] else
              "NONE — histories are unrelated; promotion cannot use git ancestry"))
        for key, text in (("in_both", "present on both (identical)"),
                          ("dev_only", "on development, not yet promoted"),
                          ("prod_only", "on production only — a development-led promotion would LOSE these"),
                          ("different", "different content on the two refs")):
            print(f"{text}: {len(report[key])}" + "".join(f"\n  - {n}" for n in report[key]))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Fail when a recorded API gap resolution is no longer true of this tree's contract.

  python3 scripts/gap/check_resolutions.py [--dir docs/api-gap/resolutions] [--contract docs/api/openapi.json]

Every `<fp16>.json` resolution evidence file declares checks (operation exists,
field present/required/typed, parameter present/required). This guard re-runs
them against the committed contract of the tree being merged or promoted, so a
later merge or promotion that drops a fix fails its pipeline instead of
silently re-opening a gap that consumers were told is resolved.

Exit codes: 0 all hold (or no evidence files); 1 a check fails or a file is invalid; 3 input error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gap_contract import evaluate_check  # noqa: E402
from gap_coordinator import RESOLUTION_SCHEMA, parse_resolution  # noqa: E402


def check_tree(directory: Path, contract_path: Path) -> list[str]:
    problems: list[str] = []
    files = sorted(p for p in directory.glob("*.json") if p.is_file())
    if not files:
        return problems
    try:
        document = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{contract_path}: cannot read the contract ({type(exc).__name__})"]
    for path in files:
        raw = path.read_bytes()
        try:
            fingerprint = json.loads(raw).get("fingerprint", "")
            iid = json.loads(raw).get("backend_issue")
        except (json.JSONDecodeError, AttributeError):
            problems.append(f"{path.name}: not a JSON object")
            continue
        if not isinstance(fingerprint, str) or fingerprint[:16] != path.stem:
            problems.append(f"{path.name}: file name must be the first 16 characters of its fingerprint")
            continue
        evidence, problem = parse_resolution(raw, fingerprint, iid)
        if problem:
            problems.append(f"{path.name}: {problem}")
            continue
        for check in evidence.get("checks", []):
            failure = evaluate_check(document, check)
            if failure:
                problems.append(f"{path.name}: {failure}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dir", default="docs/api-gap/resolutions")
    parser.add_argument("--contract", default="docs/api/openapi.json")
    parser.add_argument("--expect-failure", action="store_true",
                        help="negative control: succeed only if at least one check FAILS on this contract (use it with the "
                             "currently published contract, to prove the evidence demonstrates the fix)")
    args = parser.parse_args(argv)
    directory = Path(args.dir)
    if not directory.is_dir():
        print(f"no resolution directory at {directory}: nothing to check")
        return 0
    problems = check_tree(directory, Path(args.contract))
    if args.expect_failure:
        for problem in problems:
            print(f"fails on {args.contract} (good): {problem}")
        if not problems:
            print(f"VACUOUS: every check already holds on {args.contract}; the evidence does not show what the fix "
                  "changes. Add a check that fails there and holds on the contract your change generates.",
                  file=sys.stderr)
        return 0 if problems else 1
    for problem in problems:
        print(f"REGRESSION: {problem}", file=sys.stderr)
    count = len(list(directory.glob("*.json")))
    if problems:
        print(f"{len(problems)} problem(s) in {count} resolution file(s)", file=sys.stderr)
        return 1
    print(f"{count} gap resolution file(s) hold on {args.contract}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

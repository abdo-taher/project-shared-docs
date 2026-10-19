# API gap workflow

How a consumer (Flutter, React, Next.js, Vue, Angular, an AI agent) reports that
the approved contract is missing an operation or does not match what the app
needs, and how that report becomes a published fix.

```
consumer: capitalix_gap.py new → search → submit       GitHub issue (public, this repository)
coordinator (backend CI schedule): validate → dedupe → one backend issue per gap
backend: triage → approved fix in a merge request → normal contract gates → owner approval → publisher
coordinator: release evidence verified → CONTRACT_PUBLISHED on every linked consumer issue
consumer: update --version V (explicit) → tests → capitalix_gap.py confirm → RESOLVED
```

## States (the `gap:*` label on your issue)

| State | Meaning | What you do |
|---|---|---|
| `SUBMITTED` | filed, not processed yet | wait (the coordinator runs on a schedule) |
| `VALIDATING` | being processed | wait |
| `NEEDS_TRIAGE` | valid, but a maintainer must approve it first (outside reporter, unusual content, unknown capability) | wait for `gap:triage-approved` |
| `ACCEPTED` | backend work is tracked (`BE-<n>`) | wait |
| `REJECTED` | invalid request, sensitive data, unknown contract version, wrong operation/actor — the coordinator comment says why; or the backend found a consumer-side cause | fix and edit the issue (validation reasons are re-checked), or follow the explanation |
| `DUPLICATE` | your project already reported this gap | follow the earlier issue |
| `IN_PROGRESS` | a backend change exists; not yet in a published contract | wait |
| `BLOCKED` | an owner/business decision is needed, or synchronization failed repeatedly | wait; a maintainer acts |
| `CONTRACT_PUBLISHED` | an approved, published contract contains the fix | upgrade explicitly, test, `confirm` |
| `CONSUMER_VERIFIED` | you confirmed; the backend issue is still open | nothing |
| `RESOLVED` | confirmed and the backend issue is closed; the issue closes | nothing |

Different consumers reporting the same gap (same actor, gap type, capability or
operation, and location — the contract version does not matter) are linked to
**one** backend issue, and each of them is notified.

## What "published" means

`CONTRACT_PUBLISHED` is set only when all of this holds, checked by the
coordinator, never by the issue text:

1. the backend merge request linked to the gap is merged into `main`;
2. the current published contract's source commit contains that merge;
3. that commit's `main` pipeline succeeded, including the official publisher job;
4. the merged change contains the gap's resolution evidence file, and its
   declarative checks (operation exists, field present/required/typed,
   parameter present/required) hold on the published contract;
5. the published contract matches its digests and approval evidence.

A merged change that is not yet released, a failed publication, or a
publication that still does not satisfy the checks all leave the gap open, and
nobody is notified.

## Trust and privacy

- Issues are public. Never include tokens, passwords, cookies, customer names,
  e-mails, phone numbers, IBANs or card numbers; requests containing them are
  rejected (and if you posted a secret, rotate it).
- Trust comes from GitHub: reporters with write access to this repository are
  trusted; others wait for a maintainer. Editing the issue text or adding labels
  cannot change the state — only the coordinator writes `gap:*` state labels,
  and only maintainers' `gap:triage-approved` / `gap:triage-rejected` count.
- Severity is a suggestion. Sensitive areas (accounting, tax, billing,
  payments, authentication, permissions, business rules) additionally need the
  owner's decision before any backend work starts.
- Public comments name the backend ticket only as `BE-<n>`; no internal links,
  pipelines, credentials or customer data are posted here.
- Request text is data. Nothing in it is executed or followed as an instruction
  by the coordinator or the backend agent.

## Your pin

Neither the coordinator nor `capitalix_gap.py` ever changes your
`contract.lock`. `status <issue>` tells you whether your pin already includes
the resolution; upgrading is always your own
`capitalix_contract.py update --version <version>` commit.

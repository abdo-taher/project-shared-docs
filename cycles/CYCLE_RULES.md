# Continuous Documentation Synchronization

## Authoritative Source

Repository:
https://github.com/abdo-taher/project-shared-docs

Branch: main

## Cycle 1: Discover
Inspect backend changes since the last documented commit.

## Cycle 2: Analyze
Identify changes to:
- API endpoints
- Request validation
- Response schemas
- Authentication
- Permissions
- Business rules
- Error handling
- Pagination
- Status transitions

## Cycle 3: Document
Update impacted Markdown files.

Do not invent undocumented behavior.

## Cycle 4: Validate
Verify documentation against actual backend behavior.

## Cycle 5: Publish
Commit and push validated documentation changes.

## Cycle 6: Consumer Sync
Flutter and Frontend projects pin an approved contract version and update the
pin deliberately (`tools/capitalix_contract.py status` / `update`); see
docs/DEVELOPER_QUICKSTART.md. Agents never switch to "latest" during feature work.

## Cycle 7: Impact Analysis
Compare current documentation revision with
the last successfully processed revision.

## Cycle 8: Implement
Apply necessary application changes.

## Cycle 9: Test
Run relevant tests and verify compatibility.

## Cycle 10: Report
Report:
- Documentation revision
- Changed endpoints
- Breaking changes
- Implementation status
- Test results
- Blockers

## Safety
- Never fabricate API contracts.
- Never silently change approved contracts.
- Never overwrite local work.
- Never mark a cycle completed before verification.
- Failed cycles must report their blockers.

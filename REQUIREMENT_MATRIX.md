# Readiness ledger

| Gate | Contract path | Executable proof | Status |
| --- | --- | --- | --- |
| Full and public sources use distinct origins | `audit_release` | source guard test | PASS |
| Owner cannot act as auditor | `register_record` | role guard test | PASS |
| Every omission receives a disposition | `_audit` | consensus surface test | PASS |
| All stored findings and digests reach validator agreement | `_audit` | exact principle assertion | PASS |
| Exposure outranks over-redaction | `release_state` | three-outcome test | PASS |
| Reviewed source deployed and exercised on StudioNet | deployment evidence | added after network verification | UNVERIFIED |

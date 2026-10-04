# REDACTION MARGIN

```text
FULL RECORD  ── compare ──  PUBLIC RELEASE
      │                         │
      └── allowed reasons ──────┘
                  ↓
       MINIMAL | OVERREDACTED | LEAKING
```

Public disclosure has two opposite failure modes: hiding too much and exposing what the release rule protects. Redaction Margin makes both visible.

The owner registers a numbered full record, its clause labels, and a closed list of allowed redaction reasons. A different auditor submits the public release from another source origin. Validators retrieve both documents and agree on every omitted clause, every unsupported omission, every exposed sensitive clause, the reason mapping, and both content digests. Contract code rejects incomplete attribution and derives the final state without another model call.

## States

- `MINIMAL`: every omission has an allowed reason and no sensitive clause remains exposed.
- `OVERREDACTED`: at least one omission lacks an allowed reason.
- `LEAKING`: protected material remains visible. This state takes priority over over-redaction.

Duplicate identifiers, self-auditing, same-origin full and public records, replayed audits, malformed URLs, and unclassified omissions fail closed.

## Local checks

```text
python -m pytest -q
genvm-lint check contracts/contract.py
```

The included documents are operator-authored technical fixtures. They demonstrate source retrieval and classification, not an actual confidential disclosure.

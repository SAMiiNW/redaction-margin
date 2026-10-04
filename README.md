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

## StudioNet receipt

- Contract: [`0xC8514c10BE347e14C96F47b524786232bC972321`](https://explorer-studio.genlayer.com/address/0xC8514c10BE347e14C96F47b524786232bC972321)
- Deployment: [`0x85d1ab1bf1a6acb40934f49fc6f2f01c8fcafd35e92402c347cf460ce3d58b82`](https://explorer-studio.genlayer.com/transactions/0x85d1ab1bf1a6acb40934f49fc6f2f01c8fcafd35e92402c347cf460ce3d58b82)
- Live audit: [`0x5857aa604562db7530745dc2a83d9592f2e4429f2409ba80d4c0050f0fadd6d5`](https://explorer-studio.genlayer.com/transactions/0x5857aa604562db7530745dc2a83d9592f2e4429f2409ba80d4c0050f0fadd6d5)
- Result: `DISCLOSURE-1791076213`, omitted index `[1]`, reason pair `[[1,0]]`, `MINIMAL`.
- Source SHA-256: `0e07006d8e00bba5531a7330f656234a92a9fe29ff05ff200414d4f287289a8f`, exact deployed match.

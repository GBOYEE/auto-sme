# AGENTS.md — auto-sme V1 discipline (non-negotiable)

- Contract first: docs/00-v1-contract.md + docs/ROADMAP.md (18 criteria) override any conflicting instruction.
- No SaaS, no TPT/FEM import (patterns only). Church Pack is v1.1 discussion only.
- Smallest diff per milestone; no drive-by refactors. Verify before acting (read/grep before edit).
- Never commit secrets (keys, tokens, .env). `.env.example` only.
- Report every milestone as: Completed X/18 — Z% + files + tests + evidence + remaining.
- QA gates block merge: pytest green, content QA PASS, visual target >= 80 / styled >= 90, footer stamp present.
- Prefer counts, filenames, concise diffs, test summaries, SHAs. No full-file dumps, no huge logs.

# Vericoding: Getting It Right!
## A Python concurrency workshop with TLA+

**Format:** 120 minutes of instruction and exercises, followed by 45 minutes of questions. A five-minute break sits inside the first 120 minutes. Intended for developers who can read Python; no TLA+ experience required. Work in pairs. Installation happens before the workshop.

We operate a tiny ticket reservation service. Two clients compete for one ticket. Each client sends one request through a FIFO queue. The server dispatches a task per request and replies through a separate mailbox for each client. An asynchronous audit operation splits a stock check from its update. Both requests can succeed.

The core is a real, runnable **in-process message-passing client/server**, using Python's standard library. It deliberately excludes sockets, HTTP and a database to keep the code/model correspondence visible. An HTTP version is a follow-up, not a hidden prerequisite.

Run the commands from the repository root. With Nix, `nix develop` provides Python, Java, and the pinned TLC jar and sets `TLA_JAR`. Without Nix, follow `SETUP.md` to install Python and Java and fetch the pinned jar.

## Branches

- `main` is the participant and LLM task branch: specification, buggy starter, Python reference and tests, and the extraction prompt.
- `reference` adds the answer key: `models/Reservation.tla`, its TLC configurations, `tools/run_tlc.py`, TLC evidence, `facilitator/`, `OUTLINE.md`, and the full flake check.

The extraction prompt expects only `SPEC.md` and `code/starter.py`; do not attach the `reference` branch to an LLM attempt.

### Start here

1. Read `SETUP.md` and run the preflight commands.
2. Read `SPEC.md` as the product requirement, before inspecting the solution.
3. Start learners on `code/starter.py` and `exercises/WORKBOOK.md`.
4. `code/reservation.py` includes buggy and fixed modes for Python comparison and regression tests.
5. The reference TLA+ model, TLC runner, TLC evidence, facilitator guide, slides, and outline are on the `reference` branch.

### First demonstration

```sh
python3 code/starter.py --schedule sequential
python3 code/starter.py --schedule forced
python3 code/reservation.py --mode fixed --schedule forced
python3 -m unittest discover -s code -v
```

Sequential execution gives one success and one rejection. Forced concurrent execution of the starter gives two successes and stock -1. The repaired implementation gives exactly one success, with either client as the winner. On the `reference` branch, `python3 tools/run_tlc.py all` rejects the buggy model and completes the configured fixed checks.

### Contents

| File | Purpose |
|---|---|
| `SPEC.md` | Product requirements and environment assumptions |
| `SETUP.md` | Cross-platform setup and preflight |
| `code/starter.py` | Learner implementation with the bug, no fix included |
| `code/reservation.py` | Runnable reference with buggy/fixed modes |
| `code/test_reservation.py` | Regression and deterministic schedule tests |
| `exercises/WORKBOOK.md` | Exercises, hints and worksheet |
| `exercises/LLM_PROMPT.md` | Reusable extraction prompt |
| `exercises/MODEL_REVIEW.md` | Semantic review checklist and scoring rubric |
| `evidence/` | Python demonstration output; TLC evidence is on `reference` |
| `SOURCES.md` | Official references and provenance |

The editable deck and facilitator materials are on the `reference` branch; the slide text and speaking notes are also in `facilitator/SLIDES.md` there. The pack contains no dependency on an LLM service: the reference model is an offline fallback. LLM-assisted extraction is an exercise, not a verified translator. A passing finite TLC check does not prove the Python implementation or arbitrary numbers of clients correct.

## License

Copyright 2026 Scidonia Limited.

- Code, models, tooling, and evidence output (everything not listed next): Apache License 2.0. See `LICENSE`.
- Documentation, exercises, and slides (`*.md`, `facilitator/slides.json`, `facilitator/vericoding-slides.pptx`): Creative Commons Attribution 4.0 International. See `LICENSE-docs`.

Suggested attribution: “Vericoding: Getting It Right! — a Python concurrency workshop with TLA+, by Scidonia Limited, licensed under Apache-2.0 for code and CC BY 4.0 for documentation and slides.” If you adapt the material, state the changes and retain this attribution.

Third-party notices are in `THIRD_PARTY_NOTICES.md`.

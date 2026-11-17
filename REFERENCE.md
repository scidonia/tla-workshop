# Reference branch

This branch is the facilitator and answer branch. The participant and LLM task
branch is `main`.

It adds:

- `models/Reservation.tla` and the TLC configurations.
- `tools/run_tlc.py`.
- `evidence/` with the Python and TLC output.
- `facilitator/` with the guide, mapping, trace, slides, and deck.
- `OUTLINE.md`.
- The full flake check, covering both the Python suite and the TLC cases.

Do not use this branch as the LLM input. Use `main` with
`exercises/LLM_PROMPT.md`, which expects only `SPEC.md` and
`code/starter.py`.

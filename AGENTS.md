# Repository conventions

## Toolchain

Run Python and TLC commands through the nix dev shell:

```sh
nix develop -c <command>
```

The shell provides Python 3.12, Java 21, and `TLA_JAR` pointing at the pinned
TLA+ tools 1.7.4 jar from nixpkgs. Outside Nix, `SETUP.md` documents the
Python, Java, and jar-download route.

## Branches

- `main` is the participant and LLM task branch. It does not contain the
  reference TLA+ model or the facilitator answer key.
- `reference` adds the reference model, TLC configurations and runner, TLC
  evidence, facilitator materials, and outline; its flake check runs both the
  Python suite and the TLC cases.

## Tests

- Python standard-library `unittest` only. Do not add third-party Python
  dependencies or a second test runner.
- On `main`, run the Python suite:
  `nix develop -c python3 -m unittest discover -s code -v`
- On `reference`, also run:
  `nix develop -c python3 tools/run_tlc.py all`
- Run the branch's flake check:
  `nix build .#checks.<system>.default` (for example
  `nix build .#checks.x86_64-linux.default`)
- The buggy TLC case is expected to violate `NoOversell`; `run_tlc.py` treats
  that as success and exits nonzero on any other result. Do not "fix" the
  buggy configuration.

## Layout

- `code/` contains the learner program, the reference implementation, and the
  regression tests.
- `exercises/` contains the workbook and extraction prompt. Those are the
  task inputs for an LLM attempt.
- The `reference` branch contains `models/`, `tools/run_tlc.py`,
  `facilitator/`, `OUTLINE.md`, and the TLC evidence.

## Generated files

`code/__pycache__/`, `models/states/`, `.direnv/`, and
`tools/tla2tools.jar` are not committed. `evidence/tlc-*.txt` on `reference`
are committed snapshots; re-running `run_tlc.py` rewrites them.

## Licensing

Code, models, tooling, and evidence output are Apache-2.0 (`LICENSE`).
Documentation, exercises, and slides are CC BY 4.0 (`LICENSE-docs`,
`NOTICE`). Third-party notices are in `THIRD_PARTY_NOTICES.md`.

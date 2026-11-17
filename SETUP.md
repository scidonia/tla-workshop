# Setup and reproducible runs

Run commands from the repository root. Python code uses the standard library only.

## Requirements

- Python 3.11 or later. On Windows substitute `py -3` for `python3`.
- Java 11 or later. Check `java -version`.
- TLC from TLA+ tools release **v1.7.4**, pinned for this pack.
- Optional: Nix with flakes, which provides Python, Java, and the pinned jar.
- Optional: VS Code with the TLA+ extension. CLI commands below are the reference route.

This repository does not commit `tools/tla2tools.jar`. With Nix, `nix develop` sets `TLA_JAR` to the pinned TLA+ tools 1.7.4 jar from nixpkgs. Without Nix, download the jar into `tools/tla2tools.jar` and verify its hash. The runner also honours an absolute `TLA_JAR` path; other versions may report different counts or traces.

To download the pinned jar:

```sh
curl -L --fail https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar -o tools/tla2tools.jar
(cd tools && sha256sum -c TLC-SHA256.txt)
```

On macOS, use `(cd tools && shasum -a 256 -c TLC-SHA256.txt)`.

PowerShell:

```powershell
Invoke-WebRequest https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar -OutFile tools/tla2tools.jar
(Get-FileHash tools/tla2tools.jar -Algorithm SHA256).Hash
```

The expected SHA-256 is in `tools/TLC-SHA256.txt`.

## Preflight

With Nix:

```sh
nix develop
```

Then, inside the shell (or with Python, Java, and the jar available):

```sh
python3 --version
java -version
python3 code/starter.py --schedule sequential
python3 code/starter.py --schedule forced
python3 code/reservation.py --mode fixed --schedule forced
python3 -m unittest discover -s code -v
python3 tools/run_tlc.py all
```

The same checks are available as a flake check: `nix build .#checks.<system>.default`, for example `nix build .#checks.x86_64-linux.default`.

`starter.py --schedule forced` should print `OVERSOLD`. This is an expected demonstration, not a setup error. Its exit code is zero because the outcome is returned as data. Tests assert that the buggy case fails its safety predicate. `run_tlc.py` verifies the expected invariant failure for the buggy case and exits nonzero on unexpected output.

### Raw TLC commands

From `models/`:

```sh
java -cp ../tools/tla2tools.jar tlc2.TLC -workers 1 -config buggy.cfg Reservation.tla
java -cp ../tools/tla2tools.jar tlc2.TLC -workers 1 -config fixed.cfg Reservation.tla
java -cp ../tools/tla2tools.jar tlc2.TLC -workers 1 -config fixed-3clients.cfg Reservation.tla
java -cp ../tools/tla2tools.jar tlc2.TLC -workers 1 -config live.cfg Reservation.tla
```

Inside `nix develop`, substitute `"$TLA_JAR"` for `../tools/tla2tools.jar`.

The first raw command intentionally returns an invariant error. Do not chain it with `&&` and assume later commands will run. The runner handles expected failure explicitly.

### VS Code

Open `models/Reservation.tla`. Use the extension's model-check command and select the intended `.cfg` when prompted. If configuration selection differs in your extension release, use the raw CLI. Do not accidentally check `fixed.cfg` while demonstrating the bug.

## Schedule modes

- `sequential`: send the next request only after receiving the previous reply. It conceals this race.
- `natural`: let audit calls yield without a gate. Useful exploration, but not the reproducibility contract.
- `forced`: hold eligible handlers at audit until all clients arrive. Positive capacity is required. This deterministically makes every client check before any can commit.

The gate lives in the test audit dependency. The service is not repaired by the gate. A different repair that takes a lock around audit will deadlock with this all-clients gate; test that alternative with a suitable scheduler rather than changing the model to hide the blockage.

## Offline and troubleshooting

No LLM is required. Use the reference model after attempting the worksheet. Once the jar is present, TLC is available offline. Python's ten-second watchdog reports mistakes such as a stranded gate instead of hanging the workshop. If Java fails, use saved TLC output while the facilitator runs the model. TLC writes disposable state directories; the runner uses a temporary metadata directory.

"""Run TLC, retain logs, and check expected outcomes. No third-party Python deps."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument("case", choices=["buggy", "fixed", "fixed-3clients", "live", "all"], default="all", nargs="?")
args = p.parse_args()
jar = Path(os.environ.get("TLA_JAR", str(root / "tools" / "tla2tools.jar"))).resolve()
if not jar.is_file():
    sys.exit("Missing TLC jar. Follow SETUP.md or set TLA_JAR to an absolute path.")
cases = ["buggy", "fixed", "fixed-3clients", "live"] if args.case == "all" else [args.case]
for case in cases:
    with tempfile.TemporaryDirectory(prefix="tla-tlc-") as metadir:
        r = subprocess.run(["java", "-XX:+UseParallelGC", "-cp", str(jar), "tlc2.TLC",
                            "-workers", "1", "-metadir", metadir,
                            "-config", f"{case}.cfg", "Reservation.tla"],
                           cwd=root / "models", text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    (root / "evidence").mkdir(exist_ok=True)
    (root / "evidence" / f"tlc-{case}.txt").write_text(r.stdout)
    print(r.stdout)
    expected = "Invariant NoOversell is violated" if case == "buggy" else "Model checking completed. No error has been found."
    if expected not in r.stdout or (case != "buggy" and r.returncode != 0):
        sys.exit(f"Unexpected result for {case}: exit={r.returncode}")
    print(f"EXPECTED RESULT: {case}\n")

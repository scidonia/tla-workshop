# Preparation results

Prepared 17 November 2026. These are actual local runs, not predicted output.

| Check | Result |
|---|---|
| Python regression suite | 5 test methods passed, including capacity/client matrix |
| Buggy Python, forced schedule | Two ok replies, remaining -1 |
| Fixed Python, same forced schedule | One ok, one full, remaining 0 |
| TLC buggy, 2 clients / capacity 1 | NoOversell violation at state 9 |
| TLC fixed, 2 clients / capacity 1 | 41 distinct states, no error |
| TLC fixed, 3 clients / capacity 2 | 252 distinct states, no error |
| TLC fixed + weak fairness, 2 clients / capacity 1 | AllReplied checked, no error |

Runtime: Python 3.12.14; OpenJDK 21.0.13; tla2tools release v1.7.4, TLC 2.19 (08 August 2024).

Logs are included. Their timestamp display reflects the tool environment, and absolute paths inside them are preparation-container paths, not repository paths. Exact trace order and search metadata can differ on another run. A finite model check does not mechanically establish the implementation/model correspondence or arbitrary-size correctness.

No separate LLM extraction experiment was performed in preparation. The reference model is authored and checked; participants use the prompt to produce and audit their own extraction.

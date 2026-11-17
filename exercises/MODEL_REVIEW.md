# Extraction review and rubric

A model that parses is only a candidate. Review the mapping before interpreting a green TLC result.

| Review item | Acceptance criterion | Common failure |
|---|---|---|
| Source fidelity | Models the supplied implementation | Models the intended specification instead |
| Shared state | All handlers refer to one stock variable | Separate inventory per client |
| Control flow | Successful check survives across audit | Adds a fresh guard accidentally |
| Atomicity | Check and commit are separate actions | Entire handler becomes atomic |
| Request channel | FIFO sequence, explicit nonempty guard | Unexplained unordered set |
| Reply channels | Client-indexed mailboxes and receive guard | Replies disappear or reach wrong client |
| State updates | Every variable constrained each action | Missing UNCHANGED permits arbitrary changes |
| Properties | Invariants are checked independently | NoOversell inserted into Next as a guard |
| Completion | Intended terminal state can stutter | Globally disables deadlock checking |
| Scope | States limits and excluded failures | Claims all Python behaviour is verified |

Score each of these ten rows 0 (absent/incorrect), 1 (partly justified), or 2 (explicit and correct), for 20 points. A draft is ready to interpret only when the source fidelity, atomicity, state updates and properties rows score 2. A total score cannot compensate for hiding the race.

Record whether the generated model: parses, detects the reference bug, accepts the mapped repair, and preserves source correspondence. Retain rejected drafts as learning evidence. Do not report an LLM success rate without actually running multiple recorded attempts.

## Mutation challenge

After obtaining a failing model, combine Check and Commit into an atomic reservation action. It will likely make the invariant pass. Explain why this is a changed implementation model rather than a repair to the original Python.

## Honest result wording

“Under the stated abstraction, TLC found a reachable state with two reservations and capacity one. The deterministic Python run reproduces the same stale-check pattern.”

“For the fixed model with two clients and capacity one, TLC exhaustively explored the reachable finite state space and found no violation of the configured invariants. A separate three-client case also passed. We have not mechanically proved the Python-to-TLA+ correspondence or correctness for all client counts.”

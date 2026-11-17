# Pedagogical counterexample

This is a valid illustrative schedule, not a promise that TLC will pick these client names or this ordering. See `evidence/tlc-buggy.txt` for the actual checker trace.

| Step | Action | Remaining | Booked | Relevant observation |
|---:|---|---:|---|---|
| 0 | Init | 1 | {} | Both clients ready |
| 1 | Send(c1) | 1 | {} | Request queue [c1] |
| 2 | Send(c2) | 1 | {} | Request queue [c1,c2] |
| 3 | Dispatch | 1 | {} | c1 handler enabled |
| 4 | Dispatch | 1 | {} | c2 handler enabled |
| 5 | Check(c1) | 1 | {} | c1 enters audit |
| 6 | Check(c2) | 1 | {} | c2 also enters audit |
| 7 | Commit(c1) | 0 | {c1} | ok published for c1 |
| 8 | Commit(c2) | -1 | {c1,c2} | NoOversell fails |

The bug exists at reservation commit, before either client needs to read its reply. If execution continues, both receive ok. In the repaired model, the second Commit publishes full and leaves stock and bookings unchanged.

Ask learners whether Accounting fails. It does not: -1 + 2 = 1. This is a useful example of why a plausible invariant may be too weak.

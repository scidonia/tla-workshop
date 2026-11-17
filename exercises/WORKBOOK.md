# Participant workbook

## Exercise 1: two clients, one ticket (15 minutes)

Read `SPEC.md` and `code/starter.py`. Before running it, predict the results for sequential and concurrent requests.

```sh
python3 code/starter.py --schedule sequential
python3 code/starter.py --schedule forced
```

Record the two check events and two commit events. Why does the second successful check fail to guarantee a ticket? Identify the exact await that lets another handler act. Which requirements fail? Does the accounting equation also fail?

Hint 1: the relevant shared state is `inventory.remaining`.

Hint 2: ask whether the decision `eligible` is recomputed after suspension.

Deliverable: a four-row interleaving and one sentence explaining why the sequential test misses it.

## Exercise 2: extract the implementation (20 minutes)

Use `LLM_PROMPT.md`, or construct the same model manually. Fill in:

| Python entity or operation | TLA+ representation | Guard / atomicity explanation |
|---|---|---|
| Shared inventory | | |
| Request queue | | |
| Reply queue | | |
| Client send | | |
| Server dispatch | | |
| Availability branch | | |
| Audit completion and reservation | | |
| Client receive | | |

The draft must preserve the branch decision across audit. Review it with `MODEL_REVIEW.md`. At minute 75 the facilitator supplies `models/Reservation.tla` so all pairs can continue even if their generated model has syntax errors.

Deliverable: model plus mapping, with at least two explicit abstraction assumptions.

## Exercise 3: read the counterexample (15 minutes)

```sh
python3 tools/run_tlc.py buggy
```

Find the first state violating `NoOversell`. Read backwards until you find both workers in the audit phase. Translate the trace into Python operations. Explain why TLC can stop before clients consume replies. Does that weaken the finding?

Deliverable: a trace explanation, the failing invariant, and a code reproduction. A screenshot of red output alone is not enough.

## Exercise 4: repair both artifacts (15 minutes)

Edit a copy of `starter.py`. Keep the asynchronous audit. Make the final availability check and reservation indivisible on the specified event loop. Ensure rejection still publishes `full`.

In the reference model, the `Fixed` switch enables the repaired commit guard. Inspect the actual changed action; do not just trust the name.

```sh
python3 code/reservation.py --mode fixed --schedule forced
python3 tools/run_tlc.py fixed
python3 tools/run_tlc.py fixed-3clients
python3 -m unittest discover -s code -v
```

Run the forced demo on your edited starter as well: the reference regression suite tests `reservation.py`, not your edited file. Count replies and stock; do not test which client wins.

Deliverable: patch, successful run of your patch under the forced schedule, and TLC result for the repaired model.

## Exit exercise (last 5 minutes of teaching)

1. Why would a model containing only an atomic `Reserve` action miss this bug?
2. What new assumption would fail if two worker processes shared a database?
3. Complete: “For ___, TLC explored ___ and found ___. This does not establish ___.”

## Optional extensions

- Change to three clients and one ticket, then capacity zero. Inspect state counts.
- Check `live.cfg`. Remove fairness and determine whether eventual response is still established.
- Make a write-only lock repair. Explain why an unlocked earlier check is still stale.
- Model a bounded request queue. Add its capacity guard explicitly.
- Add retries with request IDs. Decide how repeated IDs alter the state space before implementing them.
- Replace the queues with real network transport and list exactly which new failure modes must enter the model.

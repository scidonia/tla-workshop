# Vericoding: Getting It Right!

Slide text and speaker notes. The editable deck is `facilitator/vericoding-slides.pptx`.

## 1. Vericoding: Getting It Right!

**Timing:** 00–02

Finding a Python concurrency bug with TLA+

Two-hour workshop + 45-minute discussion

**Speaker notes:** Welcome. This session assumes Python familiarity but no TLA+ background. Tools should already be installed. We will connect one implementation bug to a model counterexample and then a repair.

## 2. One ticket. Two clients.

**Timing:** 02–05

A community workshop has one place left.

Two clients request that place.

What outcomes should the server permit?

**Speaker notes:** Ask the audience before showing code. Either client may win. Two successes violate the business requirement. The audit is diagnostic, not payment. Keep the scenario concrete.

## 3. The service contract

**Timing:** 05–08

*Assuming the service, clients and audit continue to make progress.

Property | Requirement
--- | ---
No overselling | Bookings never exceed capacity
Stock | Remaining tickets never become negative
Replies | An ok reply corresponds to a booking
Progress | Every request eventually gets a reply*

**Speaker notes:** SPEC.md contains the full contract, including accounting and justified rejection. Distinguish safety from eventual response. Do not promise completion without environmental assumptions.

## 4. Today’s investigation

**Timing:** 08–10

Minutes | Activity
--- | ---
00–40 | Python, sequential tests and the race
40–60 | TLA+ essentials and a short break
60–95 | Extract, review and model-check
95–120 | Repair, retest and qualify the result
120–165 | Questions and extensions

**Speaker notes:** Give pairs the pack. The first two hours include exercises and a five-minute break. There is a separate 45-minute discussion. The reference model is available if an LLM or installation fails.

## 5. A server inside one process

**Timing:** 10–13

Component | Role
--- | ---
Clients | Send one request each
Request queue | Reliable, unbounded FIFO
Dispatcher | Start a handler for each request
Handlers | Share inventory and await audit
Reply queues | One mailbox per client

**Speaker notes:** This is runnable message-passing architecture, not a socket simulation. The deliberately small transport lets us see channels and guards. No crashes, retries, threads or cancellation. Source: https://docs.python.org/3/library/asyncio-queue.html

## 6. The reservation handler

**Timing:** 13–17

```text
eligible = inventory.remaining > 0
if eligible:
    await audit.record_attempt(client)
    inventory.remaining -= 1
    inventory.booked.add(client)
    outcome = "ok"
else:
    outcome = "full"
replies[client].put_nowait(outcome)
```

**Speaker notes:** Excerpt from code/starter.py, with tracing removed. Ask which objects are shared and which values are local. eligible records an earlier observation. Do not reveal the repair yet.

## 7. Where another task can run

**Timing:** 17–21

The availability check reads shared stock.

The audit call can suspend this handler.

Another handler can change stock before this one resumes.

**Speaker notes:** Use the exact audit stub in the source. asyncio.sleep(0) deliberately yields. Not every await must suspend, but this one can. Synchronous check/update spans do not yield to another task in the stated environment. Source: https://docs.python.org/3/library/asyncio-task.html

## 8. The sequential test passes

**Timing:** 21–25

```text
python3 code/starter.py --schedule sequential

check c1: remaining=1, eligible=True
commit c1: remaining=0
check c2: remaining=0, eligible=False

replies=["ok", "full"]
SAFE
```

**Speaker notes:** Run the real command. The slide abbreviates the full trace and uses JSON-style quote marks for readability. Ask what schedules this test never exercised. A passing test is useful evidence but only for the tested execution.

## 9. Exercise 1: force the race

**Timing:** 25–31

Predict first. Then run.
Record both checks and both commits.
Which requirement fails?

```text
python3 code/starter.py --schedule forced
```

**Speaker notes:** Allow pairs about six minutes before debriefing. The test audit waits until all clients have arrived before releasing them. The model later abstracts arbitrary audit completion instead of carrying this test gate.

## 10. Both clients saw one ticket

**Timing:** 31–36

The successful check becomes stale while the handler awaits audit.

Operation | Remaining | Bookings
--- | --- | ---
Client A checks | 1 | 0
Client B checks | 1 | 0
Client A commits | 0 | 1
Client B commits | −1 | 2

**Speaker notes:** Client names are illustrative; the supplied forced Python run normally releases the second arriver first. The winner is not specified. This is a check-then-act race, not a lost-update example.

## 11. Accounting can still look right

**Timing:** 36–40

Conservation alone does not forbid overselling.

```text
remaining + number_of_bookings == capacity

       -1 + 2 == 1
```

**Speaker notes:** Ask whether the accounting invariant catches the failure. It does not. Both NoOversell and StockNonnegative express constraints that accounting alone misses. This motivates deriving properties from the actual requirement.

## 12. TLA+: states and actions

**Timing:** 40–43

A state assigns values to variables.

An action relates a state to its possible next states.

TLC explores reachable states and checks the invariants.

**Speaker notes:** Avoid teaching all of temporal logic. Explain that actions are predicates rather than imperative functions. TLC checks the finite configured model. Source: https://github.com/tlaplus/tlaplus/blob/master/USE.md

## 13. Notation for this workshop

**Timing:** 43–46

Notation | Read it as
--- | ---
x' | x in the next state
/\   and   \/ | and   /   or
UNCHANGED x | x keeps its current value
[c \in Clients |-> value] | A function indexed by client
Append(q, c), Head(q), Tail(q) | FIFO sequence operations

**Speaker notes:** Type the backslash operators in an editor while explaining. A disabled guard is not an exception. Function update syntax uses EXCEPT; the model provides examples. Source: https://learntla.com/

## 14. The model’s state

**Timing:** 46–49

Variable | Meaning
--- | ---
remaining, booked | Shared stock and successful client IDs
requests | FIFO sequence of client IDs
clientPC, workerPC | Per-client control phases
reply, result | Pending reply and consumed outcome

**Speaker notes:** A set of booked IDs supports reply identity checks. One reply slot per client is sufficient only because the exercise allows one request per client. workerPC=audit remembers a successful check without an extra eligible variable.

## 15. One complete action

**Timing:** 49–52

```text
Send(c) ==
    /\ clientPC[c] = "ready"
    /\ requests' = Append(requests, c)
    /\ clientPC' =
           [clientPC EXCEPT ![c] = "waiting"]
    /\ UNCHANGED <<remaining, booked,
                   workerPC, reply, result>>
```

**Speaker notes:** Read each conjunct. The first is a guard. Two variables change and all others are constrained to stay equal. TLA+ does not implicitly preserve variables omitted from an action.

## 16. The crucial action boundary

**Timing:** 52–55

Check reads availability and enters the audit phase.

Commit resumes after audit and allocates the ticket.

The model must preserve the state between them.

**Speaker notes:** An atomic reserve model would encode a stronger implementation. Check and Commit must be separate because another handler can act during audit. Commit includes reply publication because there is no further await before put_nowait.

## 17. Five-minute break

**Timing:** 55–60

Resume at minute 60

Next: extract the model from code and requirements

**Speaker notes:** Use this break to help pairs whose tooling failed. Prepare the LLM prompt and reference model, but do not overwrite participant drafts.

## 18. Exercise 2: extraction

**Timing:** 60–63

Input: SPEC.md + code/starter.py

Output: state, guards, atomic actions, channels

Then a runnable TLA+ module and configuration

**Speaker notes:** Use exercises/LLM_PROMPT.md. Give three minutes for the state table, five for drafting, seven for review and five to reconcile. No LLM access is needed: pairs can use the worksheet and reference skeleton.

## 19. A repeatable LLM prompt

**Timing:** 63–68

Preserve the actual implementation, including mistakes.

Explain each atomic action with a code span.

Keep requirements as independent invariants.

List every abstraction and environmental assumption.

**Speaker notes:** The full copyable prompt is in the pack. Save the exact input and model version. This pack has not measured an extraction success rate. Repeatability concerns the controlled inputs and review procedure, not identical generated text.

## 20. The model review

**Timing:** 68–75

Check | Failure to reject
--- | ---
Atomicity | Check and commit merged
Guard fidelity | Fresh stock check invented
Channels | FIFO silently becomes an unordered set
Next-state values | Variables left unconstrained
Requirements | NoOversell inserted as an action guard

**Speaker notes:** Have pairs exchange drafts. A green result for the wrong model is not useful. Correct parser errors without casually changing semantics. The rubric has ten rows and explicit critical checks.

## 21. The reference action map

**Timing:** 75–80

Code | TLA+ action
--- | ---
Client sends request | Send(c)
Server creates handler | Dispatch
Check, then enter audit await | Check(c)
Resume, reserve, publish reply | Commit(c)
Client consumes reply | Receive(c)

**Speaker notes:** Supply the reference now so all pairs can progress. Explain the abstraction of dispatcher scheduling and audit completion. It is not a mechanically verified translation. The test gate is not part of the reference service model.

## 22. Exercise 3: run TLC

**Timing:** 80–84

Find the first bad state.
Then work backwards to both successful checks.

```text
python3 tools/run_tlc.py buggy

Error: Invariant NoOversell is violated.
```

**Speaker notes:** Actual result from evidence/tlc-buggy.txt. The runner regards this failure as expected. Show the raw log so learners see control state, channels and bookings rather than only the error line.

## 23. The checker finds the stale decisions

**Timing:** 84–90

Both ok replies exist before either client consumes them.

State | Worker A | Worker B | Stock
--- | --- | --- | ---
After both checks | audit | audit | 1
After first commit | done | audit | 0
After second commit | done | done | −1

**Speaker notes:** These rows summarise states 7, 8 and 9 in the recorded TLC trace. The bad state has booked={c1,c2}. Exact client names and search order may vary. A violation at commit is sufficient; we need not wait for reply consumption.

## 24. Model counterexample, code witness

**Timing:** 90–95

The model permits both checks before either commit.

The forced audit schedule reproduces that pattern.

Review extra model schedules before accepting other findings.

**Speaker notes:** The abstract scheduler permits more orders than the concrete Python ready queue in some places. We demonstrate this relevant failure in code. This is not a proof of exact trace correspondence, and not every future model counterexample is automatically a real implementation bug.

## 25. Exercise 4: repair the boundary

**Timing:** 95–99

Keep the asynchronous audit.

Check current stock after it returns.

Perform the check and update without suspension.

**Speaker notes:** Allow learners to propose a patch before revealing the next slide. Ask what a lock around only the decrement would protect. The key is stale eligibility, not concurrent arithmetic instructions.

## 26. The repaired commit

**Timing:** 99–102

```text
await audit.record_attempt(client)
if inventory.remaining > 0:
    inventory.remaining -= 1
    inventory.booked.add(client)
    outcome = "ok"
else:
    outcome = "full"
replies[client].put_nowait(outcome)
```

**Speaker notes:** Excerpt of the post-audit repair. The initial availability check remains in the complete program. This is atomic only relative to other tasks on the one event loop with no await in the check/update span. A multi-process database deployment requires a different argument.

## 27. One model change

**Timing:** 102–105

Fixed = FALSE preserves the bug.
Fixed = TRUE checks stock at commit.

```text
Commit(c) ==
    /\ workerPC[c] = "audit"
    /\ IF ~Fixed \/ remaining > 0
          THEN ... reserve and publish ok ...
          ELSE ... preserve stock, publish full ...
```

**Speaker notes:** This slide is an abbreviated excerpt, not a runnable replacement. Open the complete action in Reservation.tla. Inspect the unchanged variables and reply branch. Do not just change the config and assume the code matches.

## 28. The same schedule after repair

**Timing:** 105–110

One ok reply. One full reply. Stock zero.

```text
python3 code/reservation.py --mode fixed
python3 tools/run_tlc.py fixed
python3 tools/run_tlc.py fixed-3clients
python3 -m unittest discover -s code -v
```

**Speaker notes:** The default schedule is forced, clients=2, capacity=1. Also run each learner’s edited starter: the provided regression tests exercise the reference file, not their patch. Either client may win.

## 29. What we checked

**Timing:** 110–113

Configuration | Observed result
--- | ---
Buggy: 2 clients, capacity 1 | NoOversell violation
Fixed: 2 clients, capacity 1 | 41 distinct reachable states, no error
Fixed: 3 clients, capacity 2 | 252 distinct reachable states, no error
Fixed + fairness: 2 clients | AllReplied checked, no error

**Speaker notes:** Actual preparation runs, TLC tools release v1.7.4, TLC 2.19. See evidence logs. Counts describe these exact configurations and model, not a universal proof. The buggy search stopped at its first violation.

## 30. The remaining obligations

**Timing:** 113–115

Review the code-to-model correspondence.

Revisit the model when the environment changes.

Finite instances do not establish arbitrary client counts.

A specification still needs to express the intended service.

**Speaker notes:** Ask participants to name excluded features: retries, crashes, audit failures, cancellation, processes, database isolation, network loss. A useful method can have an explicit scope without claiming end-to-end verification.

## 31. Exit exercise

**Timing:** 115–120

Why would atomic Reserve hide this bug?

What changes with two server processes?

What does our passing TLC run establish?

**Speaker notes:** Collect responses before giving the answers. Good answers identify the intermediate stale-check state, loss of the one-event-loop assumption, and a finite model result rather than a Python correctness theorem.

## 32. Questions and discussion

**Timing:** 120–165

The trace and TLA+ notation

Model fidelity and LLM extraction

Applying the method to your systems

**Speaker notes:** 45-minute discussion. Suggested split: 15 minutes trace/syntax, 15 minutes model fidelity, 15 minutes applications. The next slides are optional supporting material, not additional required teaching time.

## 33. Optional: safety and progress

**Timing:** Q&A

Eventual response assumes audit completion and scheduling.

```text
Spec == Init /\ [][Next]_vars

AllReplied == <>Done

FairSpec adds weak fairness to
dispatch and each per-client action.
```

**Speaker notes:** Run python3 tools/run_tlc.py live if relevant. Weak fairness of Commit represents the audit eventually completing when a handler awaits it. Remove fairness to expose indefinite stuttering. Safety required no such assumption. Source: https://learntla.com/

## 34. Optional: the lock alternative

**Timing:** Q&A

A lock around only the write leaves the check stale.

A lock around check and audit serializes the whole operation.

The all-clients audit gate then needs a different test design.

**Speaker notes:** Source: https://docs.python.org/3/library/asyncio-sync.html. A lock can be a valid repair but the forced test barrier will deadlock if the first handler holds the lock while waiting for all others. Distinguish the production protocol from test instrumentation. A local asyncio lock cannot coordinate separate processes.

## 35. Optional: the next tutorial

**Timing:** Q&A

Retries require request identities and deduplication.

Crashes require recovery and durable state.

A database requires transaction semantics.

Each change adds concrete modelling obligations.

**Speaker notes:** Use participant examples. Avoid promising automatic translation. The reusable workflow is to name the requirement, expose shared state and boundaries, draft a model, review correspondence, inspect a trace, reproduce it and validate a repair. References are in SOURCES.md.

# Workshop outline

## Audience and prerequisites

Developers comfortable with functions, shared state and basic Python. Explain asyncio during the session; no temporal logic background required. Pair participants so every pair has a working Python 3.11+ and Java 11+ installation. Ask them to run setup at least one day before the workshop. A presenter-only demo is the fallback for installations that cannot run Java.

## Outcomes

Participants will be able to reproduce a check-then-act race, identify suspension points, translate code into guarded TLA+ actions and explicit channels, check an invariant with TLC, trace a counterexample back to code, repair the atomicity boundary, and audit an LLM-generated model for accidental strengthening.

## Schedule: 120 minutes + 45 minutes

| Minutes | Duration | Activity | Slides | Evidence of learning |
|---|---:|---|---|---|
| 00–10 | 10 | Scenario, requirements, prediction | 1–4 | State what must never happen |
| 10–25 | 15 | Read Python and run sequential demo | 5–8 | Identify shared state and the await |
| 25–40 | 15 | Exercise 1: force and explain the race | 9–11 | Produce two successful reservations |
| 40–55 | 15 | TLA+ essentials and state mapping | 12–16 | Write one guarded transition |
| 55–60 | 5 | Break | 17 | — |
| 60–80 | 20 | Exercise 2: extract and review a model | 18–21 | Annotated code-to-model mapping |
| 80–95 | 15 | Exercise 3: TLC and counterexample | 22–24 | Explain both stale checks |
| 95–110 | 15 | Exercise 4: repair code and model | 25–28 | Same schedule fails before, passes after |
| 110–120 | 10 | Bounds, transfer and exit exercise | 29–31 | Correctly qualify the result |
| 120–165 | 45 | Questions and optional deeper examples | 32–35 | Apply the method to participants' systems |

For the 20-minute extraction block: 3 minutes to identify state, 5 minutes for an LLM draft or manual skeleton, 7 minutes for review, 5 minutes to reconcile with the reference. Do not spend the whole block repairing generated syntax. Switch to the supplied reference at minute 75 if needed.

## Pedagogical choices

**Why this bug?** Check-then-act races recur in quotas, stock allocation and admission checks. This is an approachable example of that family, not a claim that it is statistically the most common concurrency bug. The business failure is immediately visible and two clients suffice. A deadlock needs more lock-state machinery; retries and duplicate processing introduce failure assumptions before learners understand atomic actions.

**Why Python asyncio?** The await makes the vulnerable scheduling boundary visible. Single-threaded execution still permits a logical race between tasks. There is no need to teach CPU memory models or the GIL.

**Why message queues?** Explicit FIFO requests and per-client replies make channels and guards concrete. They avoid network setup and HTTP libraries. Explain that this is a server architecture inside one process.

**Why direct TLA+?** Learners see guards, primed variables and UNCHANGED directly. PlusCal is an alternative follow-up, not an extra notation to master today.

**Why a recheck repair?** The shared-state check and update can run together without an await in this single event loop. A lock is useful when the critical section must suspend, but is not needed for this exact repair. A process-local lock would not fix a multi-process database deployment.

## Preparation and materials

Projector, editor with a large font, terminal, pack extracted locally, and optionally an LLM. Prepare three terminal tabs for Python, TLC and source. Keep `evidence/` available if a live run fails. Do not give learners the reference answer until they have identified the race. The starter and specification are sufficient for the extraction prompt.

## Assessment

Each pair hands in: one runnable model, one counterexample explanation, a code/action mapping, the repaired code or patch, and a two-sentence statement of what the finite check establishes and what it leaves unproved.

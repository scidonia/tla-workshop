# Facilitator guide and answer key

## Before the room arrives

Run every command in SETUP.md. Keep the terminal font readable. Open starter.py, SPEC.md and Reservation.tla. Keep the reference fixed implementation closed until exercise 4. Save a clean copy before learners edit. The two hours assumes pre-installed tools, not a live install party.

## 00–10: start with the obligation

Say: “We have one ticket and two clients. Which outcomes should the service allow?” Accept either winner, reject two successes. Ask for both a safety statement and a progress statement. Explain the single-process scope early so nobody assumes the queues model a failure-prone network.

## 10–25: inspect the implementation

Walk through the client, request queue, dispatcher, handler and reply queue. Run the sequential starter. Ask whether this result establishes safety under concurrency. Point to eligible being computed before await. Explain that a coroutine can suspend while another coroutine operates on the same inventory. The GIL is irrelevant to this logical race.

## 25–40: reproduce it

Pairs run the forced schedule. The barrier makes all clients arrive at audit before any resumes. It is test instrumentation in the dependency, not part of the service's product specification. It does not invent a shared-state operation; it selects an adversarial completion schedule. Demonstrate the same gate with the repaired code later.

Answer: both clients read stock 1, both remember eligibility, both decrement. NoOversell and StockNonnegative fail. Accounting holds. ReplySound holds because each ok really has a corresponding booking, even though too many bookings exist.

## 40–55: teach only the needed TLA+

A state assigns values to variables. An action relates the current state to the next state. `x'` means next-state x. `/\` means and, `\/` means or. A guard must hold before the action can occur. A disabled action is not an exception. `UNCHANGED` constrains variables not updated by that action. Explain a function indexed by client IDs and a FIFO sequence. `Init /\ [][Next]_vars` allows steps satisfying Next or stuttering. An invariant is checked in every reachable state.

Use Send as the first complete example. Then show Check and Commit separately. Ask learners which code boundary requires that separation. Do not spend this session teaching arbitrary temporal logic or PlusCal syntax.

## 60–80: draft and audit

Use the fixed extraction prompt with code and specification only. Each pair marks guard boundaries before asking an LLM. Pairs with no model access use the mapping worksheet. Review generated actions before running TLC. Look especially for invented fresh availability checks and an atomic Reserve action. Parser errors are normal; semantic drift during a syntax fix is the more consequential risk. Supply the reference at minute 75.

## 80–95: read a trace

Run the buggy configuration. Find the violating state, identify the last successful operation, and trace back to both checks. A counterexample is an execution explanation, not simply a red status. Require the link to the forced Python run. Exact trace order may differ between TLC versions or search settings.

## 95–110: repair and compare

Let pairs propose repairs first. The provided fix performs a fresh availability check after audit and immediately updates shared stock. There is no await in that critical span. Keep the initial check as an optional fast path. Run identical forced scheduling before and after. Check fixed.cfg and fixed-3clients.cfg. Tests assert the number of successful replies, not the identity of the winner.

A lock around only the decrement is insufficient: both requests may already have passed the stale check. A lock around check+audit+commit can serialize correctly, but the forced audit gate would then deadlock waiting for contenders that cannot enter the critical section. Use this to distinguish production synchronization from test scheduling. It also shows why changing a repair requires changing the test harness thoughtfully.

## 110–120: limits and transfer

Ask what a green finite TLC result means. Accept the wording in MODEL_REVIEW.md. The tutorial does not prove that an LLM extracts correct semantics, prove arbitrary-size correctness, establish database behaviour, or handle network failures. It does produce a model-level bug with a concrete implementation witness and a checked repair under stated assumptions.

## 120–165: question session

Use 120–135 for questions about the trace and syntax, 135–150 for model fidelity and AI-assisted extraction, and 150–165 for applying the method to participants' systems. These are prompts, not mandatory lectures. Slides 33–35 are optional answers.

### Likely questions

**Can async code have races on one thread?** Yes. A decision can depend on state that changes while the task is suspended. This is a logical race rather than simultaneous unsynchronised CPU memory access.

**Is every await a context switch?** No. An awaited operation can complete immediately. Our audit stub deliberately suspends. A general model must consider whether suspension is possible and may allow both immediate and delayed completion.

**Why not just add a unit test?** The forced test is valuable and remains in the pack. Model checking searches the abstract schedules without our having to guess a single interleaving. Tests also help determine whether a model counterexample corresponds to the implementation.

**Can the LLM be trusted to translate?** Treat its output as a candidate. Use source mapping, invariant separation, mutation challenges and executable witnesses. This pack contains a human-authored reference and reusable prompt, not an evaluated extraction benchmark.

**Does TLC prove it for any number of users?** No. These configurations are finite instances. A parameterised proof needs additional reasoning or a proof system.

**Does correct accounting prove correct allocation?** No. Negative stock still satisfies the accounting equation. Use properties that express the actual business prohibition.

**Is the model's scheduler exactly Python's?** No. It abstracts scheduling and audit completion. It allows broader interleavings in some places. The selected failing schedule is concretely reproduced. A general preservation theorem is outside scope.

**Why not include a lock in the reference model?** The chosen fix has no suspension in its check/update region. If the repaired region must await, introduce lock ownership and acquire/release guards explicitly.

**What if the audit fails?** The exercise assumes successful completion. If exceptions are introduced, model handler failure, replies and any compensation. This audit is diagnostic; do not re-label it a payment service without changing the requirements.

**What happens with retries?** Client identity no longer uniquely identifies one attempt. Add request IDs, in-flight and completed records, and duplicate semantics. Exactly-once processing is a different exercise.

**What if we add a database?** Reassess atomicity at the database boundary. A read followed by a write can race across processes even if each process has a local lock. Model the transaction or conditional update actually used.

## Answer key for exit exercise

1. Atomic Reserve removes the intermediate state where both workers have passed their guards; it represents a stronger implementation.
2. One event loop controlling all inventory updates is no longer true. Shared database semantics matter.
3. Name the concrete configuration, reachable finite states, checked properties, and missing general correspondence/parameterised proof.

## Recovery plan

Python error: switch to the reference file, preserve the learner's patch for later. TLC parser error: compare action-by-action against the reference, watching primed variables and backslashes. Java unavailable: use the actual saved log and ask the pair to reconstruct the trace. LLM unavailable: complete the state/action table manually. Running late: skip live.cfg and use the supplied fixed model, but retain the code/model mapping discussion.

# Reusable extraction prompt

Start a fresh chat. Attach only `SPEC.md` and `code/starter.py`. Do not attach the reference model, fixed implementation, trace, or this pack's answers. Save the exact prompt, model name/version, settings if available, date, and unedited answer. Repeatability means reproducible review and checking, not guaranteed identical LLM text.

Copy the following:

---

Extract an implementation model in executable TLA+ from the attached Python code and specification. The goal is to discover whether the code satisfies the specification. Preserve the code's actual behaviour, including mistakes. Do not repair it during extraction.

Environment: one asyncio event loop, one request per uniquely identified client, reliable unbounded FIFO request queue, a per-client reply mailbox, no exceptions, retries, cancellation or crashes. Audit can suspend and later complete. Model arbitrary completion order rather than wall-clock time. Model the ungated service, not the test-only forced barrier. Use two clients and capacity one initially.

Before generating TLA+, produce:
1. A table of shared state, per-client control state and channels.
2. Every relevant guard and every actual or possible suspension point.
3. Proposed atomic actions with a corresponding code span and rationale.
4. Explicit abstraction choices and assumptions, especially scheduler behaviour.

Then return a complete module `Extracted.tla` and `Extracted.cfg`, using only standard modules such as Integers, Sequences and FiniteSets. Include Init, Next, Spec, TypeOK, NoOversell and StockNonnegative. Use a sequence for requests and a function for per-client reply mailboxes. Give every variable a next-state assignment or UNCHANGED clause in every action. Represent control flow explicitly so a branch decision made before an await survives the await.

Do not invent a lock, transaction, post-await recheck, duplicate suppression or fairness assumption for safety. Do not merge code on opposite sides of the audit await into one atomic transition. Do not encode NoOversell as a guard that prevents the implementation from violating it. Allow intended completion without suppressing all deadlock checking.

Finally, give the TLC command and a code/action correspondence review. Report any ambiguity. Do not say the model passes, fails or proves the Python code correct unless supported by an actual checker run. Do not change the specification to make it pass.

---

## Follow-up after a parser error

Attach the exact TLC output. Ask for a syntax-only repair and a diff. Re-review guards and atomicity after every edit. If a semantic change is necessary, require an explanation rather than accepting it as a syntax fix.

## Follow-up after a counterexample

Ask: “Map each transition to the original Python. Is this schedule compatible with the stated environment? Identify any abstraction that might make this a false positive. Propose a deterministic code-level reproduction before suggesting a repair.”

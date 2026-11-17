# Product specification: the last ticket

## Story

A community workshop has a limited number of tickets. Clients request one ticket each. The reservation service should allocate tickets without selling more than it has. The service records an asynchronous audit attempt before completing an eligible reservation. The audit is diagnostic, not a payment or a durable reservation record.

## Supported environment

- One Python process and one asyncio event loop. No threads mutate inventory.
- A finite, nonempty set of clients, each with a unique integer ID.
- Each client makes exactly one request. IDs are not reused within the run.
- Capacity is a nonnegative integer. No cancellation, restock, refund or expiry.
- Reliable, unbounded, in-memory FIFO request queue. Each client has its own reply queue.
- The server dispatches one task per request. Tasks share the inventory.
- The audit may suspend. In normal runs it eventually returns successfully.
- No task cancellation, exceptions, process crashes or communication loss within the exercise.

## Safety requirements

S1. **No overselling:** the number of successful reservations never exceeds initial capacity.

S2. **Nonnegative stock:** remaining stock is never negative.

S3. **Accounting:** remaining stock plus successful reservations always equals initial capacity.

S4. **Honest replies:** an `ok` reply corresponds to a recorded reservation for that client.

S5. **Justified rejection:** a `full` reply means no tickets remain. Since there is no restock, stock remains exhausted after that reply.

S6. **One outcome:** each request receives at most one reply and each client obtains at most one ticket. The one-request-per-client protocol must enforce this structurally; checking duplicates/retries is a separate extension.

The winner of the last ticket is unspecified. FIFO dispatch does not promise FIFO completion. The audit does not itself allocate a ticket. There is no requirement that a check performed earlier entitles a client to a later reservation.

## Progress requirement

P1. If the service, clients and audit continue to make progress, every request eventually receives either `ok` or `full`.

Safety is the main workshop exercise. P1 needs explicit scheduling and audit-completion assumptions and is checked in an optional fair model.

## Acceptance examples

| Clients | Capacity | Required final outcome, assuming completion |
|---|---:|---|
| 2 | 1 | Exactly one `ok`, one `full`, remaining 0 |
| 3 | 2 | Exactly two `ok`, one `full`, remaining 0 |
| 2 | 0 | Both `full`, remaining 0 |
| 2 | 3 | Both `ok`, remaining 1 |

Write the model of the implementation, including any faulty behaviour, separately from these requirements. Do not silently implement these requirements inside the model and then claim to have checked the supplied program.

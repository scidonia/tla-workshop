"""One-process message-passing client/server, Python 3.11+, standard library only.

This intentionally buggy program is for teaching. No network, database or payments.
Each client sends exactly one request. See SPEC.md for the supported environment.
"""
import argparse
import asyncio
import json
from dataclasses import dataclass, field


@dataclass
class Inventory:
    capacity: int
    remaining: int = field(init=False)
    booked: set[int] = field(default_factory=set)

    def __post_init__(self):
        self.remaining = self.capacity


class Audit:
    """A yielding audit dependency; the optional gate controls a test schedule."""
    def __init__(self, parties=0):
        self.parties = parties
        self.arrived = 0
        self.release = asyncio.Event()

    async def record_attempt(self, client):
        if self.parties:
            self.arrived += 1
            if self.arrived == self.parties:
                self.release.set()
            await self.release.wait()
        else:
            # Represents an external operation that can suspend the handler.
            await asyncio.sleep(0)


async def handle(client, inventory, replies, audit, trace):
    # CHECK: this decision remains live across an await.
    eligible = inventory.remaining > 0
    trace.append(f"check c{client}: remaining={inventory.remaining}, eligible={eligible}")
    if eligible:
        # AUDIT: another handler can check or commit while this task waits.
        await audit.record_attempt(client)
        # COMMIT: reserve the item after recording the attempt.
        inventory.remaining -= 1
        inventory.booked.add(client)
        outcome = "ok"
        trace.append(f"commit c{client}: remaining={inventory.remaining}")
    else:
        outcome = "full"
    # PUBLISH: one reply mailbox per client, unbounded, reliable in this exercise.
    replies[client].put_nowait(outcome)


async def server(requests, replies, inventory, audit, count, trace):
    handlers = []
    for _ in range(count):
        client_id = await requests.get()
        trace.append(f"dispatch c{client_id}")
        handlers.append(asyncio.create_task(
            handle(client_id, inventory, replies, audit, trace)))
    await asyncio.gather(*handlers)


async def client(client_id, requests, replies, trace):
    requests.put_nowait(client_id)
    trace.append(f"send c{client_id}")
    outcome = await replies[client_id].get()
    trace.append(f"receive c{client_id}: {outcome}")
    return outcome


async def run(clients=2, capacity=1, schedule="forced"):
    if clients < 1 or capacity < 0:
        raise ValueError("clients must be positive and capacity nonnegative")
    if schedule == "forced" and capacity == 0:
        raise ValueError("forced schedule needs positive capacity")
    if schedule not in {"forced", "natural", "sequential"}:
        raise ValueError("unknown schedule")
    inventory = Inventory(capacity)
    requests = asyncio.Queue()
    replies = {c: asyncio.Queue() for c in range(1, clients + 1)}
    audit = Audit(clients if schedule == "forced" else 0)
    trace = []
    service = asyncio.create_task(server(
        requests, replies, inventory, audit, clients, trace))
    try:
        if schedule == "sequential":
            results = [await client(c, requests, replies, trace)
                       for c in replies]
        else:
            results = await asyncio.gather(*(
                client(c, requests, replies, trace) for c in replies))
        await service
    finally:
        if not service.done():
            service.cancel()
            await asyncio.gather(service, return_exceptions=True)
    return {"schedule": schedule, "capacity": capacity,
            "clients": clients, "remaining": inventory.remaining,
            "booked": sorted(inventory.booked), "replies": results,
            "safe": len(inventory.booked) <= capacity and inventory.remaining >= 0,
            "trace": trace}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clients", type=int, default=2)
    parser.add_argument("--capacity", type=int, default=1)
    parser.add_argument("--schedule", choices=["forced", "natural", "sequential"], default="forced")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = asyncio.run(asyncio.wait_for(run(
        args.clients, args.capacity, args.schedule), timeout=10))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n".join(result["trace"]))
        print(f"remaining={result['remaining']} booked={result['booked']} replies={result['replies']}")
        print("SAFE" if result["safe"] else "OVERSOLD")
    # Deliberate failure is data. Tests decide what outcome is expected.


if __name__ == "__main__":
    main()

import asyncio
import unittest
from reservation import run


class ReservationTests(unittest.IsolatedAsyncioTestCase):
    async def scenario(self, **kwargs):
        return await asyncio.wait_for(run(**kwargs), timeout=3)

    async def test_sequential_tests_miss_the_bug(self):
        for mode in ("buggy", "fixed"):
            r = await self.scenario(mode=mode, schedule="sequential")
            self.assertTrue(r["safe"])
            self.assertEqual(r["replies"], ["ok", "full"])

    async def test_forced_schedule_exposes_bug(self):
        r = await self.scenario(mode="buggy")
        self.assertFalse(r["safe"])
        self.assertEqual(r["remaining"], -1)
        self.assertEqual(r["replies"], ["ok", "ok"])

    async def test_fix_survives_same_schedule(self):
        r = await self.scenario(mode="fixed")
        self.assertTrue(r["safe"])
        self.assertEqual(r["remaining"], 0)
        self.assertCountEqual(r["replies"], ["ok", "full"])

    async def test_capacity_and_client_matrix(self):
        for n in (1, 2, 3, 5, 10):
            for k in (1, 2, 4):
                r = await self.scenario(mode="fixed", clients=n, capacity=k)
                self.assertTrue(r["safe"])
                self.assertEqual(len(r["booked"]), min(n, k))
                self.assertEqual(r["remaining"] + len(r["booked"]), k)

    async def test_empty_stock(self):
        r = await self.scenario(mode="fixed", clients=3, capacity=0, schedule="natural")
        self.assertEqual(r["replies"], ["full"] * 3)
        self.assertTrue(r["safe"])


if __name__ == "__main__":
    unittest.main()

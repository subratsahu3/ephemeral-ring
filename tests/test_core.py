import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from ephemeral_ring.core import SPSCRingBuffer


class TestSPSCRingBuffer(unittest.TestCase):
    def test_non_power_of_two_raises(self):
        with self.assertRaises(ValueError):
            SPSCRingBuffer(capacity=7)

    def test_fifo_ordering(self):
        rb = SPSCRingBuffer(capacity=4)
        self.assertTrue(rb.push("alpha"))
        self.assertTrue(rb.push("beta"))
        self.assertEqual(rb.size(), 2)

        self.assertEqual(rb.pop(), "alpha")
        self.assertEqual(rb.pop(), "beta")
        self.assertIsNone(rb.pop())
        self.assertTrue(rb.is_empty())

    def test_buffer_full_rejection(self):
        rb = SPSCRingBuffer(capacity=2)
        self.assertTrue(rb.push(1))
        self.assertTrue(rb.push(2))
        self.assertTrue(rb.is_full())
        self.assertFalse(rb.push(3))  # Rejected

    def test_circular_wrap_around(self):
        rb = SPSCRingBuffer(capacity=4)
        for i in range(20):
            self.assertTrue(rb.push(i))
            self.assertEqual(rb.pop(), i)
        self.assertTrue(rb.is_empty())


if __name__ == "__main__":
    unittest.main()

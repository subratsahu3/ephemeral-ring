"""EphemeralRing: Lock-Free Single-Producer Single-Consumer Circular Buffer."""

from typing import Any, List, Optional


class SPSCRingBuffer:
    """
    Lock-free Single-Producer Single-Consumer (SPSC) queue.
    Uses bitwise circular masking over power-of-two capacity for ultra-fast throughput.
    """

    def __init__(self, capacity: int):
        if capacity <= 0 or (capacity & (capacity - 1)) != 0:
            raise ValueError("Capacity must be a positive power of two (e.g., 8, 16, 64, 1024).")
        self.capacity = capacity
        self.mask = capacity - 1
        self.buffer: List[Optional[Any]] = [None] * capacity
        self.head = 0  # Write cursor
        self.tail = 0  # Read cursor

    def push(self, item: Any) -> bool:
        """
        Appends an item to the ring.
        Returns: True if queued, False if buffer is currently full.
        """
        if (self.head - self.tail) >= self.capacity:
            return False
        self.buffer[self.head & self.mask] = item
        self.head += 1
        return True

    def pop(self) -> Optional[Any]:
        """
        Consumes the next item in FIFO order.
        Returns: Item or None if buffer is currently empty.
        """
        if self.head == self.tail:
            return None
        item = self.buffer[self.tail & self.mask]
        self.buffer[self.tail & self.mask] = None  # Release reference for GC
        self.tail += 1
        return item

    def is_empty(self) -> bool:
        return self.head == self.tail

    def is_full(self) -> bool:
        return (self.head - self.tail) >= self.capacity

    def size(self) -> int:
        return self.head - self.tail

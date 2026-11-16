# EphemeralRing: Lock-Free SPSC Circular Buffer

A high-performance Single-Producer Single-Consumer (SPSC) circular ring buffer implementing branch-free bitwise masking over power-of-two capacity for zero-allocation streaming.

## Features
- **Zero Allocations on Hot Paths:** Pre-allocated circular memory array.
- **Lock-Free Semantics:** Separate head and tail cursor pointers eliminate mutex contention.
- **Bitwise Masking:** Replaces expensive modulo operations with `index & mask`.

## Run Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Author
Subrat Sahu (@subratsahu3) — subratsahu195@gmail.com

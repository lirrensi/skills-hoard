# 🤖 ML / AI Domain

> **Layer 3: Domain Constraints** — *Zero-copy tensors, GPU utilization, model portability*

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| Large data | Efficient memory | Zero-copy, streaming |
| GPU acceleration | CUDA/Metal support | `candle`, `tch-rs` |
| Model portability | Standard formats | ONNX |
| Batch processing | Throughput over latency | Batched inference |
| Numerical precision | Float handling | `ndarray`, careful f32/f64 |
| Reproducibility | Deterministic results | Seeded random, versioning |

## Critical Constraints

### Memory Efficiency

```
RULE: Avoid copying large tensors
WHY: Memory bandwidth is the bottleneck
RUST: References, views, in-place operations
```

### GPU Utilization

```
RULE: Batch operations for GPU efficiency
WHY: GPU overhead per kernel launch
RUST: Batch sizes 32/64/128, async data loading
```

### Model Portability

```
RULE: Use standard model formats
WHY: Train in Python, deploy in Rust
RUST: ONNX via tract or candle
```

## Use Case → Framework

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Inference only | `tract` (ONNX) | Lightweight, portable |
| Training + inference | `candle`, `burn` | Pure Rust, GPU support |
| PyTorch models | `tch-rs` | Direct C++ bindings |
| Data pipelines | `polars` | Fast, lazy evaluation |

## Key Crates

| Purpose | Crate |
|---------|-------|
| Deep learning | `candle`, `burn`, `tch-rs` |
| ONNX runtime | `tract` |
| DataFrames | `polars` |
| Numerical arrays | `ndarray` |
| Computer vision | `image` |

## Common Mistakes in ML Domain

- Copying large tensors unnecessarily
- Using Python for inference in production (use Rust with ONNX)
- Single-instance inference (always batch!)
- Not using lazy/streaming data loading
- Ignoring numerical precision issues

## Related References

- [09-performance](../references/09-performance.md) — zero-copy, streaming, batching
- [07-concurrency](../references/07-concurrency.md) — async data loading
- [13-lifecycle](../references/13-lifecycle.md) — lazy model loading, caching

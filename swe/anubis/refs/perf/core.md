# Performance: Core

> First-pass triage, general bottlenecks, and language-agnostic performance fundamentals.
>
> Load this first for any performance review, then add a service or client/runtime module if needed.

---

## 🧭 QUICK REFERENCE: "USER SAYS X → CHECK Y"

| User Says | First Places to Look |
|-----------|----------------------|
| *"App is slow"* | Profile first → DB queries (N+1, missing index) → Caching |
| *"Slow under load"* | Connection pools → Async bottlenecks → Scaling config → Lock contention |
| *"Page loads slowly"* | Bundle size → Render waterfall → Image optimization → CDN |
| *"API times out"* | External I/O timeouts → N+1 queries → Missing pagination |
| *"Uses too much memory"* | Unbounded collections → Cache eviction → Object allocation in loops |
| *"Database is slow"* | EXPLAIN ANALYZE → Missing indexes → N+1 → Connection pool exhaustion |
| *"Works fine locally, slow in prod"* | Cold starts → Resource limits → Geographic latency → Missing env config |
| *"Gets slow over time"* | Memory leak → Cache without eviction → DB table bloat → Log accumulation |
| *"High variance / bad P99"* | Queues/locks/GC/downstream → Trace waterfall → GC metrics |
| *"Slow only on first request after deploy"* | Cold start/cache → Warmup metrics → Lazy initialization |

---

## 🔍 SYMPTOM → LIKELY AREA → FIRST TOOL

| Symptom | Likely Area | First Tool |
|---------|-------------|------------|
| Slow only on certain endpoints | Backend/DB | Trace + DB query timings |
| Slow only on first request after deploy | Cold start/cache | Trace + warmup metrics |
| Gets worse with concurrency | Contention/pools | Saturation metrics + load test |
| UI feels janky (scroll/input lag) | Frontend main thread | DevTools Performance + INP |
| High variance / bad P99 | Queues/locks/GC/downstream | Trace waterfall + GC metrics |
| Memory grows unbounded | Leaks / unbounded cache | Memory profiler + heap dump |
| Spikes in error rate | Downstream failures / timeouts | Distributed trace + error logs |

---

## 📈 SCALING DECISION TREE — OPTIMIZE OR SCALE?

Ask these questions:

| Signal | Action |
|--------|--------|
| ✅ CPU consistently >80%? | Optimize code or scale vertically |
| ✅ RAM usage growing unbounded? | Fix leaks or add memory |
| ✅ Disk I/O saturated? | Optimize queries, add SSD, or read replicas |
| ✅ Network bandwidth maxed? | Compress payloads, CDN, paginate |
| ✅ Hitting connection limits? | Tune pools, add replicas, async I/O |

**Key insight:**
- 🛑 If P99 latency is high but CPU/RAM are low → You have an I/O or algorithmic bottleneck → **OPTIMIZE FIRST**
- 🚀 If optimizing yields <10% gain and cost of eng time > cost of infra → **Just scale it** (for now)

---

## ⚖️ LATENCY vs THROUGHPUT — OPTIMIZE FOR WHAT?

| Metric | What It Means | How to Improve |
|--------|---------------|----------------|
| **Latency** | Time for one operation to complete (e.g., API response time) | Reduce round trips, cache, optimize algorithms, edge compute |
| **Throughput** | Operations per second the system can handle (e.g., req/sec) | Parallelize, batch, scale horizontally, optimize resource usage |

**Examples:**
- User says "page loads slow" → optimize **latency** (LCP, TTFB, reduce render blocking)
- Ops says "we're dropping requests at peak" → optimize **throughput** (scale workers, tune pools, queue backpressure)

---

## 🛠️ PERFORMANCE TOOLBOX — BY STACK

### Python
| Category | Tools |
|----------|-------|
| CPU Profiler | `python -m cProfile`, `py-spy`, `scalene` |
| Memory | `tracemalloc`, `memory_profiler`, `memray` |
| Async | `aiomonitor`, `yappi` |
| DB | `django-debug-toolbar`, `sqlalchemy echo=True`, `pg_stat_statements` |

### Node.js
| Category | Tools |
|----------|-------|
| CPU Profiler | `node --prof`, `clinic.js`, `0x` |
| Heap | `node --inspect`, Chrome DevTools Memory tab |
| APM | `dd-trace`, `OpenTelemetry` |
| Load Test | `autocannon`, `k6` |

### React / Frontend
| Category | Tools |
|----------|-------|
| Bundle | `webpack-bundle-analyzer`, `source-map-explorer` |
| Render | React DevTools Profiler, `why-did-you-render` |
| Metrics | `web-vitals`, Lighthouse CI, CrUX dashboard |
| Virtualize | `react-window`, `react-virtualized` |

### Go
| Category | Tools |
|----------|-------|
| CPU/Heap | `pprof` |
| Trace | `go tool trace` |
| Race Detector | `go run -race` |

### JVM (Java/Scala/Kotlin)
| Category | Tools |
|----------|-------|
| CPU Profiler | `async-profiler` |
| Memory | Eclipse MAT, `jmap` |
| Production | JFR (Java Flight Recorder), Pyroscope |

### PostgreSQL
| Category | Tools |
|----------|-------|
| Slow queries | `log_min_duration_statement = 200ms` |
| Index advice | `pg_qualstats`, `hypopg` |
| Bloat | `pg_bloat_check`, `pg_repack` |
| Explain | `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` |

---

## 🚩 QUICK SCAN: TOP PERFORMANCE RED FLAGS

*Fast visual cues during code review — see the anti-patterns section later in this module for the longer list.*

| Red Flag | Quick Fix |
|----------|-----------|
| `SELECT *` in production | Select only needed columns |
| No timeout on external HTTP call | Always set `timeout=(connect, read)` |
| `requests.get()` / ORM query inside a loop | Classic N+1 — use batch/join |
| `result += string` inside a loop | Use `"".join(items)` |
| `new Connection()` per request | Use connection pooling |
| Rendering 1000+ DOM nodes | Use virtualization |
| `fs.readFileSync()` in async handler | Use async/streams |

---

## 🧮 Algorithmic Complexity

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Big-O audit every hot path** | Profile before assuming. Then check: is this O(n²) hiding in a loop? Could it be O(n log n) or O(n)? |
| 🔴 CRITICAL | **Choose the right sort algorithm** | Built-in sorts (Timsort, introsort) are usually best. Hand-rolled bubble sort for 100k items = crime. |
| 🟡 HIGH | **Avoid sorting the same data repeatedly** | Sort once and maintain order, or use a sorted data structure (heap, sorted list). Sorting inside a loop is a red flag. |
| 🟡 HIGH | **Use binary search on sorted data** | Linear scan on sorted data is wasteful. If data is sorted, binary search gives O(log n) for free. |
| 🟡 HIGH | **Short-circuit and early exit** | Break out of loops as soon as the answer is found. Evaluating the full collection when you only need the first match is wasteful. |
| 🟡 HIGH | **Audit space complexity alongside time complexity** | Sometimes you trade time for space intentionally — make it explicit. O(n) memory for O(1) lookup? Worth it? |
| 🟢 MEDIUM | **Understand amortized complexity** | `list.append()` is amortized O(1), not pure O(1). Important for pre-allocation decisions in hot loops. |
| 🟢 MEDIUM | **Reduce recursion depth with iteration or tail-call** | Deep recursion is both slower (stack frames) and risky (stack overflow). Prefer iterative solutions for linear traversal. |
| 🟢 MEDIUM | **Use lazy evaluation / generators** | Don't compute the entire result if only the first N items are needed. Generators avoid building giant collections in memory. |

```python
# Algorithmic Complexity Examples

# BAD: nested loop searching → O(n²)
# GOOD: hashmap lookup → O(1)

# BAD: bubble_sort(items)     # O(n²) always
# GOOD: sorted(items)         # Timsort O(n log n), O(n) if nearly sorted

# BAD: for query in queries: results.sort()
# GOOD: results.sort()  # once before the loop

import bisect
# GOOD: bisect.bisect_left(sorted_list, target)  # O(log n)

# BAD: found = any_match(items); return found
# GOOD: for item in items: if match(item): return True

# Pre-allocate when size is known (amortized complexity)
result = [None] * n  # avoids repeated resizing
for i in range(n):
    result[i] = compute(i)

# BAD: results = [expensive(x) for x in huge_list]
# GOOD: results = (expensive(x) for x in huge_list)  # lazy
```

---

## 🚫 Performance Anti-Patterns Hall Of Shame

*Complete list - pair with Quick Scan at the top of this module for a condensed view.*

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| `SELECT *` in production | Wastes bandwidth, memory, blocks schema evolution |
| ORM query inside a for loop | Classic N+1 - fires 1000 queries instead of 1 |
| `requests.get()` with no timeout | Can hang thread forever, cascade failures |
| `new Connection()` per request | 20-100ms overhead per request, exhausts DB |
| `re.compile()` inside a loop | Compiles same regex 1000s of times |
| `cache[key] = value` with no eviction | Memory leak disguised as optimization |
| `result += string` inside a loop | O(n^2) allocations, kills GC |
| `.sort()` inside a `.map()`/.forEach() | Sorting same data N times |
| `console.log()` in hot path | Yes, it's slow - I/O blocks event loop |
| `JSON.parse(JSON.stringify(obj))` for deep clone | Extremely expensive, loses types |
| `setInterval()` never cleared | Memory leak, keeps running after component unmount |
| Promise chains instead of `Promise.all()` | Serial execution when parallel possible |
| `fs.readFileSync()` in async handler | Blocks event loop, kills throughput |
| Unbounded retry with no backoff | Thundering herd when service recovers |
| `try/catch` for expected conditions | Exceptions are expensive, use return values |
| Logging entire request/response bodies | Disk I/O, memory, sometimes security issue |
| Using regex for simple string contains | Overhead of regex engine for literal match |
| Creating date formatter in loop | Date parsing is expensive, reuse formatters |

---

## 🚀 Critical Performance Rules

- Profile before optimizing - measure first, then act
- N+1 queries will destroy you - use joins/batch fetches
- Paginate everything - unbounded queries are time bombs
- String concat in loops means O(n^2) allocations - use `join()`
- Index your `WHERE`/`JOIN` columns - unindexed means full table scan
- Parallelize independent async calls - don't await in series
- Never render 10k DOM nodes - virtualize
- Compile regex outside loops - not inside
- Cache hot reads - define invalidation strategy upfront
- Offload CPU/I/O-heavy work to queues - don't block the event loop
- Set timeouts on all external I/O - no hanging forever
- Use connection pooling - never open a connection per request
- Circuit breakers on external dependencies - fail fast
- Rate limit inbound traffic - protect yourself from clients
- Stream large files - never buffer in memory

---

## 🗂️ Data Structure Choices

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Use a set/hashmap for membership tests** | Checking "is X in this list?" in a loop is O(n) per check. Convert to a set first for O(1) lookups. |
| 🔴 CRITICAL | **Use a min/max heap for top-K problems** | Sorting everything to get the top 10 is O(n log n). A heap gives you top-K in O(n log k), much better for large n. |
| 🟡 HIGH | **Use deque for queue operations** | `list.pop(0)` on a Python list is O(n) because it shifts everything. `collections.deque.popleft()` is O(1). |
| 🟡 HIGH | **Prefer arrays over linked lists for cache locality** | Linked list nodes scatter across memory — cache misses hurt. Arrays are contiguous in memory; iteration is ~10x faster in practice. |
| 🟡 HIGH | **Use memoization / dynamic programming for repeated subproblems** | If the same inputs produce the same output and you call it many times, cache the result. Don't recompute. |
| 🟢 MEDIUM | **Counter/defaultdict instead of manual frequency maps** | Manual frequency counting with `dict.get()` and conditional assignments is verbose and slower than Counter. |

```python
# Data Structure Examples

# BAD: if user_id in list_of_ids    # O(n)
# GOOD: if user_id in set_of_ids    # O(1)

import heapq
# GOOD: top10 = heapq.nlargest(10, items, key=lambda x: x.score)

from collections import deque
# BAD: queue.pop(0)     # O(n)
# GOOD: dq.popleft()    # O(1)

# Sequential array access = CPU prefetcher happy
# Linked list traversal = pointer chase = cache thrash

from functools import lru_cache
@lru_cache(maxsize=1024)
def expensive(n): ...

from collections import Counter
# GOOD: freq = Counter(items)  # clean and fast
```

---

## 🧠 Memory & Allocation

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **String concatenation in loops — use join()** | Strings are immutable. Concatenating in a loop creates a new string object every iteration. O(n²) total allocations. |
| 🔴 CRITICAL | **Don't build unbounded in-memory collections** | Loading 1M rows into a list to filter 3 is both slow and memory-explosive. Stream or filter at the source. |
| 🔴 CRITICAL | **Avoid object allocation inside tight loops** | Creating new objects in a hot loop stresses the garbage collector. Reuse objects or use primitives where possible. |
| 🟡 HIGH | **Use streaming/chunked processing for large data** | Process large files or query results in chunks rather than loading everything at once. Memory stays flat regardless of input size. |
| 🟡 HIGH | **Unbounded caches need eviction policies** | An in-memory cache that only grows is a memory leak with good PR. Add TTL, LRU eviction, or max size limits. |
| 🟡 HIGH | **Close closures that capture large objects** | A lambda or callback holding a reference to a huge data structure keeps it alive in memory indefinitely. |
| 🟡 HIGH | **Use \_\_slots\_\_ for small, numerous objects (Python)** | `__slots__` eliminates the per-instance `__dict__`, reducing memory by ~40-60% for classes with many instances. |
| 🟢 MEDIUM | **Prefer typed arrays (numpy, typed arrays in JS)** | Native lists/arrays store boxed objects. NumPy/typed arrays store raw values — 10-100x less memory, much faster iteration. |

```python
# Memory Examples

# BAD: result = ""; for s in items: result += s
# GOOD: result = "".join(items)

# BAD: all_orders = db.query("SELECT * FROM orders")  # 500k rows
# GOOD: db.query("SELECT * FROM orders WHERE status='pending' LIMIT 100")

# BAD: for i in range(1_000_000): result.append({"id": i, "val": i*2})
# Consider: pre-allocate, use numpy arrays, or yield instead

# BAD: data = file.read()            # entire file in RAM
# GOOD: for chunk in file.chunks(8192): process(chunk)

# BAD: cache = {}; cache[key] = value  # grows forever
# GOOD: cache = LRUCache(maxsize=1000, ttl=300)

# BAD: fn = lambda: print(len(huge_df))  # holds entire df
# GOOD: n = len(huge_df); fn = lambda: print(n)  # only captures int

# GOOD for data classes with 1M+ instances:
class Point:
    __slots__ = ["x", "y"]

# BAD: data = [1.0, 2.0, 3.0]  # list of Python float objects
# GOOD: data = np.array([1.0, 2.0, 3.0], dtype=np.float64)
```

---

## 🖥️ CPU & Compute Optimization

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Profile before optimizing — measure, don't guess** | Gut feel is almost always wrong. Use a profiler (cProfile, async-profiler, Chrome DevTools) to find actual hotspots before touching code. |
| 🔴 CRITICAL | **Compile regex patterns outside of loops** | Compiling the same regex 100,000 times per second is embarrassing. Compile once at module level. |
| 🟡 HIGH | **Use vectorized operations instead of Python loops** | Python loops are slow. NumPy / pandas vectorized ops run in compiled C — orders of magnitude faster for numerical work. |
| 🟡 HIGH | **Avoid repeated attribute lookups in tight loops** | Python attribute lookup (`obj.method`) traverses the MRO every time. Cache the method reference outside the loop. |
| 🟡 HIGH | **Use appropriate number types — avoid float where int suffices** | Float arithmetic is slower than integer arithmetic, especially in tight loops. Use integers for counts, IDs, and integer math. |
| 🟢 MEDIUM | **Short-circuit boolean evaluation aggressively** | Put the cheapest and most likely to fail condition first in AND chains. Python/JS will skip the rest. |
| 🟢 MEDIUM | **Consider JIT-compiled alternatives for hot Python code** | PyPy, Numba, or Cython can give 10-100x speedup for numerical hot paths without rewriting in C. |

> 💡 **See also:** [Serialization & Parsing](#-serialization--parsing) for JSON performance, faster serializers, and response sizing.

```python
# CPU & Compute Examples

# Python: python -m cProfile -s cumtime script.py
# Node: node --prof app.js && node --prof-process isolate-*.log
# Go: go test -cpuprofile cpu.prof && go tool pprof cpu.prof

# BAD: for line in lines: re.search(r'\d{4}', line)
# GOOD: YEAR = re.compile(r'\d{4}')
#        for line in lines: YEAR.search(line)

# BAD: result = [x * 2 for x in data]  # Python loop
# GOOD: result = np_array * 2           # NumPy vectorized, C speed

# BAD: for x in data: results.append(transform(x))
# GOOD: app = results.append  # cache reference
#        for x in data: app(transform(x))

# BAD: total = 0.0; for x in items: total += x.count  # float
# GOOD: total = 0; for x in items: total += x.count   # int

# BAD: if expensive_check() and cheap_check():
# GOOD: if cheap_check() and expensive_check():  // cheap first

# Numba JIT for numeric hot loops:
from numba import jit
@jit(nopython=True)
def hot_function(arr): ...
```

---

## 📊 Performance Observability

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Instrument latency at every service boundary** | You can't optimize what you can't measure. Add timing spans around every DB call, external API, and cache operation. |
| 🔴 CRITICAL | **Track P50/P95/P99 latency — not just average** | Average latency hides slow outliers. A P99 of 5 seconds means 1% of users wait 5 seconds. That's catastrophic at scale. |
| 🔴 CRITICAL | **Use distributed tracing — not just metrics** | Metrics tell you *something* is slow; traces tell you *where*. Trace across all services. |
| 🟡 HIGH | **Add performance budgets to CI/CD** | Set hard limits: bundle size < 200KB, LCP < 2.5s, API latency P99 < 500ms. Fail the build if budgets are exceeded. |
| 🟡 HIGH | **Benchmark before and after every optimization** | Without before/after benchmarks, you don't know if your optimization actually helped, regressed, or made no difference. |
| 🟡 HIGH | **Track error rate as a performance signal** | Errors are infinite latency from the user's perspective. High error rate = performance problem. |
| 🟡 HIGH | **Use synthetic monitoring** | Monitor from outside your infra — catches what internal metrics miss. Run periodic checks from multiple regions. |
| 🟡 HIGH | **Profile in production** | Continuous profiling (Pyroscope, Datadog profiler) catches things load tests don't. Real traffic reveals real hotspots. |
| 🟢 MEDIUM | **Use flame graphs to find actual hotspots** | Flame graphs visualize where CPU time is spent across the call stack. They're the fastest way to find non-obvious bottlenecks. |

```python
# Observability Examples

# OpenTelemetry / Datadog / Jaeger traces
# with tracer.start_span("db.query"): result = db.execute(sql)

# Use histograms, not averages
# Alert on P99 > threshold, not avg > threshold

# Lighthouse CI: assert: [{ metric: lcp, maxValue: 2500 }]
# Bundlesize: { "src/main.js": "< 200 kB" }

# Python: timeit, pytest-benchmark
# Node: autocannon, k6
# Always run in conditions matching production

# Python: py-spy top --pid <PID>
# Node: clinic flame -- node app.js
# JVM: async-profiler
```

---

## 🔄 Serialization & Parsing

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Measure JSON serialization cost** | JSON encode/decode is often a top CPU consumer in API servers. Profile it. |
| 🟡 HIGH | **Avoid double-encoding / repeated parsing** | Parse once, reuse structured form. Don't JSON.parse → JSON.stringify in a loop. |
| 🟡 HIGH | **Use faster serializers when warranted** | `orjson`/`ujson` for Python (5-10x faster), `simdjson` for C++, Protocol Buffers for internal services. |
| 🟡 HIGH | **Cap response size + enforce projections** | Don't let a single API call return 100MB of JSON. Enforce max response size and field projections. |
| 🟢 MEDIUM | **Avoid expensive logging of whole payloads** | Logging entire JSON payloads on every request is a performance killer. Log IDs, not bodies. |

```python
# Serialization Examples

# Profile JSON cost:
import cProfile
cProfile.run("json.dumps(huge_dict)")

# Faster JSON serializers:
import orjson  # 5-10x faster than stdlib
data = orjson.dumps(payload)  # returns bytes
parsed = orjson.loads(data)

# Or ujson:
import ujson
data = ujson.dumps(payload)

# Avoid double-parsing:
# BAD:
for item in items:
    parsed = json.loads(item.json_blob)  # parse every iteration
    
# GOOD:
cached_parses = {item.id: json.loads(item.json_blob) for item in items}

# Cap response size:
@app.get("/users")
def get_users():
    users = db.query("SELECT * FROM users LIMIT 1000")  # hard limit
    if len(users) > 500:
        users = users[:500]  # enforce cap
        response.headers["X-Truncated"] = "true"
    return users

# Better: field projections
@app.get("/users")
def get_users(fields: str = "id,name"):
    allowed = {"id", "name", "email"}
    selected = set(fields.split(",")) & allowed
    return db.query(f"SELECT {','.join(selected)} FROM users LIMIT 100")
```

---

## ⚠️ Code Anti-Patterns (Hidden Performance Killers)

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Never use exceptions for control flow** | Throwing/catching an exception is incredibly expensive (stack unwinding). Never use try/catch for logic you expect to happen (e.g., "UserNotFound"). Use return values or Result types. |
| 🔴 CRITICAL | **Avoid reflection at runtime in hot paths** | Reflection (Java/C#) or heavy metaprogramming (Python getattr) defeats compiler optimizations. Cache the result of reflection, don't do it every request. |
| 🟡 HIGH | **Fix incorrect locking / lock contention** | Using a broad lock (locking the whole object) when you only need to protect one field serializes all threads. Use fine-grained locks or atomics. |
| 🟡 HIGH | **Don't re-create heavy objects in loops** | Date formatters, regex patterns, JSON serializers — create once, reuse. Re-creating them in a loop is a classic CPU hog. |
| 🟡 HIGH | **Avoid premature optimization** | Profile first. Optimizing the wrong thing is worse than no optimization. |
| 🟢 MEDIUM | **Don't use regex for simple string operations** | `string.contains()` is faster than `regex.match()` for literal strings. Use the right tool. |
| 🟢 MEDIUM | **Be careful with string operations in loops** | String splitting, trimming, and formatting in tight loops add up. Cache results when possible. |

```python
# Code Anti-Pattern Examples

# BAD: Exceptions as control flow
try:
    user = db.get_user(user_id)
except UserNotFoundError:
    user = None

# GOOD: Return value / Optional
user = db.get_user(user_id)  # Returns None if not found
if user is None:
    ...

# BAD: Reflection in hot path
for obj in objects:
    method = getattr(obj, 'process')  # Reflection every iteration
    method()

# GOOD: Cache reflection result
PROCESS_METHOD = operator.methodcaller('process')
for obj in objects:
    PROCESS_METHOD(obj)

# Or even better: use a protocol/interface
# BAD: Broad lock
lock = threading.Lock()

def increment_a():
    with lock:
        global_a += 1

def increment_b():
    with lock:  # Blocks if increment_a is running!
        global_b += 1

# GOOD: Per-field locks
lock_a = threading.Lock()
lock_b = threading.Lock()

# BAD: Re-create date formatter in loop
for log in logs:
    formatter = SimpleDateFormat("yyyy-MM-dd")  # Expensive!
    date = formatter.parse(log.date)

# GOOD: Create once
FORMATTER = SimpleDateFormat("yyyy-MM-dd")
for log in logs:
    date = FORMATTER.parse(log.date)

# BAD: Regex for simple string check
import re
if re.match(r"error", message):  # Overhead of regex engine
    ...

# GOOD: Simple string method
if message.startswith("error"):  # Much faster
    ...
```

---

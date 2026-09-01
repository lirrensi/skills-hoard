# Performance: Services And Data

> Backend latency, databases, caches, queues, network paths, contention, and distributed-system throughput.
>
> Load this for APIs, workers, data pipelines, or any service that spends time waiting on other systems.

---

## 🗄️ Database & Query Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Eliminate N+1 query problems** | Fetching users then looping to fetch each user's orders one-by-one is catastrophic. Use JOINs or batch fetches. |
| 🔴 CRITICAL | **Index foreign keys and WHERE clause columns** | Without indexes, every query is a full table scan. An unindexed join on a 10M row table will make you famous for the wrong reason. |
| 🔴 CRITICAL | **SELECT only what you need — never SELECT \*** | Fetching 50 columns when you need 3 wastes network, memory, and parse time. Especially painful on wide tables or with ORMs. |
| 🔴 CRITICAL | **Paginate — never load unbounded result sets** | SELECT without LIMIT is a time bomb. One table growing to millions of rows will eventually OOM your app server. |
| 🔴 CRITICAL | **EXPLAIN ANALYZE every new query before shipping** | Make this a habit. Look for: Seq Scan on large tables, high row estimates vs actual, missing indexes. |
| 🔴 CRITICAL | **Avoid long transactions** | They block vacuum/cleanup and increase lock contention. Keep transactions as short as possible. |
| 🟡 HIGH | **Use batch inserts / upserts instead of row-by-row** | Inserting 10,000 rows one at a time is 10,000 round trips. Batch them into a single statement. |
| 🟡 HIGH | **Use covering indexes to avoid table lookups** | A covering index contains all columns the query needs, so the DB never touches the actual table rows — fastest possible read. |
| 🟡 HIGH | **Avoid functions on indexed columns in WHERE clauses** | Wrapping a column in a function prevents index usage. The DB has to compute the function for every row. |
| 🟡 HIGH | **Use connection pooling — don't open a new connection per request** | Opening a DB connection takes 20–100ms. Without pooling, every request pays this cost. Use pgBouncer, HikariCP, or built-in pool. |
| 🟡 HIGH | **Prefer keyset/seek pagination over OFFSET for large offsets** | `OFFSET 100000` still scans 100k rows. Keyset pagination (`WHERE id > last_id`) is O(1). |
| 🟡 HIGH | **Partition large tables** | Range/hash partitioning on time-series data — queries skip irrelevant partitions entirely. |
| 🟡 HIGH | **Use prepared statements for high-QPS repeated queries** | Parameterized queries reuse query plans; string-concatenated queries don't. |
| 🟡 HIGH | **Tune/verify DB stats maintenance** | `ANALYZE`/`VACUUM`/auto stats must run. Bloated tables from deletes slow everything; autovacuum tuning matters. |
| 🟡 HIGH | **Avoid soft deletes on hot tables** | `is_deleted=true` rows bloat indexes and slow queries. Consider hard deletes + archive table instead. |
| 🟢 MEDIUM | **Use read replicas for read-heavy workloads** | Write to primary, read from replicas. Doubles (or more) your read capacity with zero schema changes. |
| 🟢 MEDIUM | **Beware ORM "helpfulness"** | Implicit joins, eager loads, and hidden extra queries can reintroduce N+1 problems silently. |

```sql
-- Database Examples

-- BAD: users.forEach(u => fetchOrders(u.id))  -- 1 + N queries
-- GOOD: fetchUsersWithOrders()                -- 1 query with join

-- GOOD habit before shipping any new query:
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT ...;
-- Look for: Seq Scan on large tables, high row estimates vs actual

-- Fix: CREATE INDEX idx_orders_user_id ON orders(user_id)

-- BAD: SELECT * FROM users
-- GOOD: SELECT id, name, email FROM users

-- BAD: SELECT * FROM orders WHERE status = 'pending'
-- GOOD: SELECT * FROM orders WHERE status = 'pending' LIMIT 100 OFFSET :cursor

-- EVEN BETTER (keyset pagination):
-- SELECT * FROM orders WHERE id > :last_id AND status = 'pending' LIMIT 100

-- BAD: for row in data: db.execute("INSERT ...", row)
-- GOOD: db.bulk_insert(data)  -- single round trip

-- If query always selects (user_id, email, created_at)
-- CREATE INDEX idx_cov ON users(user_id) INCLUDE (email, created_at)

-- BAD: WHERE YEAR(created_at) = 2024     -- no index used
-- GOOD: WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'

-- Configure pool: min_connections=5, max_connections=20
-- Never: new Connection() on every request handler

-- Route reads: db.execute(query, use_replica=True)
-- Route writes: db.execute(query, use_primary=True)

-- Partition example (PostgreSQL):
-- CREATE TABLE orders (id bigint, created_at timestamp, ...)
-- PARTITION BY RANGE (created_at);
```

---

## 💾 Caching Strategy

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Identify and cache hot, expensive reads** | Profile first. Then cache the reads that are: expensive to compute, called frequently, and return stable data. |
| 🔴 CRITICAL | **Define cache invalidation explicitly** | "We cache it" is not a strategy. Define: what triggers invalidation? TTL? Write-through? Cache-bust on update? |
| 🔴 CRITICAL | **Design cache keys carefully** | Bad key design causes collisions or unbounded key spaces. Include version, tenant, and all distinguishing attributes. |
| 🟡 HIGH | **Pre-warm caches for predictable hot keys** | Cold start after a deploy means your first N requests hit the DB hard. Pre-warm for known hot keys at startup. |
| 🟡 HIGH | **Use local in-process cache before distributed cache** | Redis is fast but still involves a network hop. An in-process LRU cache for extremely hot data is 10-100x faster. |
| 🟡 HIGH | **Avoid cache stampede (dogpile effect)** | When a cached key expires and 1000 requests simultaneously try to recompute it, you get a thundering herd. Use locks or probabilistic early expiry. |
| 🟡 HIGH | **Implement negative caching** | Cache "this user doesn't exist" to avoid repeated DB misses on non-existent keys. |
| 🟡 HIGH | **Use stale-while-revalidate pattern** | Serve stale data instantly, refresh in background — zero latency penalty for users. |
| 🟢 MEDIUM | **HTTP cache headers for static/semi-static responses** | Set Cache-Control, ETag, and Last-Modified appropriately. Free caching at CDN and browser layer with zero infrastructure. |

```python
# Caching Examples

# Pattern: cache-aside
def get_product(id):
    cached = cache.get(f"product:{id}")
    return cached if cached else cache.set(f"product:{id}", db.fetch(id))

# Bad: "we cache user profiles for... some time?"
# Good: TTL=300s + explicit invalidation on profile update

# On deploy: pre_warm_cache(top_1000_products)

# L1: in-process LRU (0.01ms)
# L2: Redis (0.5ms)
# L3: Database (5-50ms)

# Pattern: mutex/lock on cache miss
# Or: jitter TTL = base_ttl + random(0, 30)

# Negative cache example:
result = cache.get(key)
if result is CACHE_MISS:
    result = db.fetch(key)
    # Cache even None results to avoid repeated DB hits
    cache.set(key, result or SENTINEL_NOT_FOUND, ttl=60)

# HTTP Headers:
# Cache-Control: public, max-age=3600, stale-while-revalidate=86400
# ETag: "abc123xyz"
```

---

## ⚡ Concurrency & Async

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Parallelize independent async operations** | Sequential awaits for independent operations means you pay the latency of each one, in series. Use `Promise.all()` or `asyncio.gather()`. |
| 🔴 CRITICAL | **Offload CPU-heavy work to worker threads / processes** | Image processing, PDF generation, ML inference on the main event loop blocks all other requests. Use a worker pool. |
| 🔴 CRITICAL | **Set timeouts on all external I/O** | Without timeouts, a slow external service holds your thread/connection forever. Set connect + read timeouts on every HTTP/DB call. |
| 🟡 HIGH | **Batch and debounce high-frequency operations** | Writing a DB row or sending a metric on every single event is expensive. Batch them up and flush periodically. |
| 🟡 HIGH | **Use async I/O — don't block threads on I/O waits** | Synchronous file or network I/O blocks the whole thread. Async I/O lets one thread handle thousands of concurrent I/O waits. |
| 🟡 HIGH | **Tune thread pool and connection pool sizes together** | Threadpool of 100 with a DB connection pool of 5 means 95 threads are always waiting. Match sizes to actual bottleneck. |
| 🟡 HIGH | **Profile lock contention under load** | Locks that look fine at low concurrency can serialize at scale. Measure, don't guess. |
| 🟡 HIGH | **Avoid global locks — prefer per-key locks** | Global mutex = single-threaded under contention. Use fine-grained locks keyed by resource ID. |
| 🟡 HIGH | **Propagate async context (trace IDs, user IDs)** | Async code loses request context without explicit propagation. Use contextvars or AsyncLocalStorage. |

> 💡 **See also:** [Contention, Locking & Saturation](#-contention-locking--saturation) for backpressure, pool exhaustion, and queue management.

```python
# Concurrency Examples

# BAD: 2s total
const users = await fetchUsers();   // 1s
const orders = await fetchOrders(); // 1s

# GOOD: 1s total
const [users, orders] = await Promise.all([fetchUsers(), fetchOrders()])

# BAD: app.post("/resize", (req, res) => resizeImage(req))  // blocks event loop
# GOOD: queue.add("resize-job", req.data)  // worker picks it up async

# BAD: response = requests.get(url)  # hangs forever
# GOOD: response = requests.get(url, timeout=(3.05, 10))  # connect, read

# BAD: on_event(e): db.insert(e)         // 10k inserts/sec
# GOOD: on_event(e): buffer.add(e)       // flush every 100ms

# BAD (Flask sync): return requests.get(url).json()
# GOOD (FastAPI async): return await httpx.get(url).json()

# Rule of thumb: pool_size ≈ (cpu_cores * 2) + effective_spindle_count
# Always load-test and measure before tuning

# Per-key locking pattern:
from contextlib import contextmanager
import threading
_locks = {}
_global_lock = threading.Lock()

@contextmanager
def key_lock(key):
    with _global_lock:
        if key not in _locks:
            _locks[key] = threading.Lock()
        lock = _locks[key]
    with lock:
        yield
```

---

## 🌐 Network & I/O Efficiency

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Enable HTTP/2 and connection keep-alive** | HTTP/1.1 opens a new TCP connection per request. HTTP/2 multiplexes dozens of requests over a single connection. |
| 🔴 CRITICAL | **Compress responses — enable gzip/brotli** | A 500KB JSON response becomes 50KB with gzip. Almost free CPU cost for 10x bandwidth savings. |
| 🟡 HIGH | **Use a CDN for static assets and cacheable content** | Serve assets from edge locations close to the user. Cuts latency from 200ms to 5ms. Take static load off your origin entirely. |
| 🟡 HIGH | **Minimize payload size — send only what's needed** | REST APIs often return entire objects when clients need 2 fields. Use sparse fieldsets, projections, or GraphQL. |
| 🟡 HIGH | **Use binary protocols for internal services (gRPC, MessagePack)** | JSON is human-readable but slow to parse and bloated. For internal service-to-service calls, use gRPC or MessagePack. |
| 🟡 HIGH | **Reduce DNS lookups — reuse HTTP sessions/clients** | Creating a new HTTP client per request re-does DNS resolution, TCP handshake, and TLS handshake every time. |
| 🟢 MEDIUM | **Use ETags and conditional requests** | If data hasn't changed, don't transmit it. ETags let clients ask "give me this only if it changed" — returns 304 Not Modified otherwise. |

> 💡 **See also:** `./perf/frontend_and_runtime.md` -> Storage & File I/O for streaming large files, disk I/O optimization, and object storage.

```
# Network Examples

# Nginx: http2 on;
# Requests: session = requests.Session()  # reuses connection

# Nginx: gzip on; gzip_types application/json text/html;
# Express: app.use(compression())

# Route: /static/* → CDN (CloudFront, Cloudflare, Fastly)
# Route: /api/* → origin server

# BAD: GET /user/123 → { id, name, bio, avatar, history, preferences, ... }
# GOOD: GET /user/123?fields=id,name → { id, name }

# JSON: 200 bytes, ~2ms parse for complex objects
# Protobuf: 50 bytes, 0.2ms parse

# BAD: axios.get(url)  // new client every call
# GOOD: const client = axios.create(); client.get(url)  // reused

# Server: ETag: "abc123"
# Client: If-None-Match: "abc123"  → 304 Not Modified (zero body)
```

---

## 🏗️ Infrastructure & Deployment

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Set container resource limits (CPU/memory)** | Under-provisioned containers throttle and OOM. Always set requests AND limits. |
| 🔴 CRITICAL | **Optimize cold starts (Lambda/serverless)** | Serverless cold starts can add 2-5s latency. Minimize bundle size, avoid heavy imports at module level, use provisioned concurrency. |
| 🔴 CRITICAL | **Implement graceful shutdown** | Dropped connections during deploys = invisible errors. Drain connections before killing pods. |
| 🟡 HIGH | **Horizontal vs vertical scaling decision** | Know when to add instances vs add resources. CPU-bound → vertical. I/O-bound → horizontal. |
| 🟡 HIGH | **Configure auto-scaling thresholds correctly** | Scale too late = degraded service. Scale too early = wasted money. Base on P95 latency + CPU, not just CPU. |
| 🟡 HIGH | **Geographic distribution / multi-region** | Speed of light is real. Put compute near users. Use edge locations for latency-sensitive paths. |
| 🟡 HIGH | **Increase file descriptor limits** | Default Linux `ulimit -n` is often 1024. High-concurrency servers need 65k+ for open sockets. |
| 🟢 MEDIUM | **Use immutable infrastructure** | Pets vs cattle. Immutable infrastructure means consistent performance across deploys. |

```yaml
# Container: always set resource requests AND limits
resources:
  requests: { cpu: "250m", memory: "256Mi" }
  limits:   { cpu: "1000m", memory: "512Mi" }

# Lambda cold start optimization:
# - Minimize deployment package size
# - Use provisioned concurrency for latency-sensitive paths
# - Lazy-load heavy dependencies

# Graceful shutdown (Kubernetes):
# lifecycle:
#   preStop:
#     exec:
#       command: ["/bin/sh", "-c", "sleep 10"]

# Increase file descriptors:
# ulimit -n 65535
# Or in systemd: LimitNOFILE=65535
```

---

## 📦 Queue & Background Job Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Make jobs idempotent** | Retried jobs that duplicate work = silent bugs + wasted load. Design for at-least-once delivery. |
| 🔴 CRITICAL | **Use dead letter queues** | Failed jobs that retry forever starve the queue. Move them to DLQ after N retries for investigation. |
| 🟡 HIGH | **Implement priority queues** | All jobs equal means urgent work waits behind bulk exports. Separate queues by priority. |
| 🟡 HIGH | **Batch job fetching at worker level** | Worker fetching 1 job at a time = queue overhead dominates. Fetch multiple jobs per network round trip. |
| 🟡 HIGH | **Use fan-out patterns for parallel processing** | One event triggers 50 workers efficiently vs sequentially. Publish to multiple consumers. |
| 🟡 HIGH | **Measure queue lag and processing rate** | Queue depth growing = consumers can't keep up. Alert before it becomes critical. |
| 🟢 MEDIUM | **Choose the right queue backend** | Redis for simple, RabbitMQ for complex routing, Kafka for high-throughput streaming. |

```python
# Queue Examples

# Idempotent job design:
@job
def process_order(order_id):
    # Check if already processed
    if Order.get(order_id).status == 'processed':
        return  # skip, already done
    # ... process ...

# Dead letter queue pattern:
@job(retries=3, retry_backoff=True, retry_jitter=True)
def risky_job(data):
    ...
# After 3 retries → DLQ for investigation

# Priority queues:
# HIGH: queue.process('email:urgent', handler)
# LOW:  queue.process('email:digest', handler)

# Batch job fetching (BullMQ example):
worker = Worker('my-queue', {
  limiter: {
    max: 1000,    # max jobs per duration
    duration: 1000  # per millisecond
  }
})

# Fan-out (Redis pub/sub or Kafka):
# Publisher sends to "orders.created" topic
# Multiple consumers: email-service, inventory-service, analytics-service
```

---

## 🛡️ Rate Limiting & Overload Protection

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Implement circuit breakers on external dependencies** | Slow downstream drags everything — fail fast instead. Open circuit after N failures, retry with backoff. |
| 🔴 CRITICAL | **Rate limit inbound traffic** | Runaway client hammering your API kills everyone else. Per-user, per-IP, per-API-key limits. |
| 🔴 CRITICAL | **Shed load gracefully (429 > 504)** | Rejecting excess load fast is better than queuing forever. Return 429 early, don't let requests pile up. |
| 🟡 HIGH | **Implement request coalescing / deduplication** | 1000 requests for same uncached resource = 1000 DB hits. Coalesce into one DB call, serve result to all waiters. |
| 🟡 HIGH | **Use the bulkhead pattern** | Isolate slow consumers so they don't starve fast paths. Separate thread pools / connections per downstream. |
| 🟡 HIGH | **Set concurrency limits per route** | Not all endpoints are equal. Limit expensive endpoints separately from cheap ones. |
| 🟢 MEDIUM | **Implement graceful degradation** | When overloaded, serve cached/stale data or simplified responses rather than errors. |

```python
# Rate Limiting Examples

# Circuit breaker (pybreaker, resilience4j, etc.)
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
def call_external_api():
    return requests.get(url, timeout=5)

# OPEN state: fail immediately instead of waiting 30s to time out
# HALF-OPEN: try one request, close if success, open if fail
# CLOSED: normal operation

# Request coalescing (asyncio):
from asyncio import Lock
_cache_locks = {}

async def get_with_coalescing(key):
    if key not in _cache_locks:
        _cache_locks[key] = Lock()
    
    async with _cache_locks[key]:
        # Double-check after acquiring lock
        cached = cache.get(key)
        if cached:
            return cached
        result = await fetch_from_db(key)
        cache.set(key, result)
        return result

# Bulkhead pattern (separate pools):
# api_pool = ConnectionPool(size=10)  # for API calls
# db_pool = ConnectionPool(size=20)   # for DB calls
# Slow DB won't starve API calls

# Rate limiting (Redis token bucket):
# RATE_LIMIT = 100 requests per minute per user
# redis.incr(f"ratelimit:{user_id}")
# redis.expire(f"ratelimit:{user_id}", 60)
```

---

## 🌍 System Architecture & Distributed Systems

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Reduce chattiness between services** | Making 50 internal HTTP calls to Service B to build one response is a latency death spiral. Consolidate into 1 batch call. |
| 🔴 CRITICAL | **Apply data locality — move compute to data** | Don't pull 10GB of data over the network to process it. Push the processing logic (stored proc, Spark job) to where the data lives. |
| 🟡 HIGH | **Use async/event-driven for non-critical paths** | Sending an email, updating analytics, or generating a PDF should never block the user's HTTP response. Push to a queue. |
| 🟡 HIGH | **Use content negotiation for media** | Don't send a high-res PNG to a mobile phone. Support Accept headers for requesting specific sizes/formats. |
| 🟡 HIGH | **Design for partial failure** | Distributed systems fail. Use timeouts, retries with backoff, and fallbacks. Assume any call can fail. |
| 🟢 MEDIUM | **Use service mesh for observability** | Istio, Linkerd provide automatic tracing, metrics, and traffic management without code changes. |
| 🟢 MEDIUM | **Implement health checks at every layer** | Load balancer health checks, container health probes, service health endpoints. Enable automatic recovery. |

```python
# Architecture Examples

# BAD: 50 HTTP calls to build one response
for user_id in user_ids:
    user = user_service.get(user_id)       # 50 calls
    
# GOOD: Batch API
users = user_service.get_batch(user_ids)   # 1 call

# Data locality:
# BAD: Pull 10GB to app server, process, push 10GB back
# GOOD: Run Spark job where data lives (S3/Databricks)
# BETTER: Stored procedure for simple aggregations

# Async non-critical path:
def create_order(order):
    order = db.save(order)
    # Don't block on these!
    queue.enqueue(send_confirmation_email, order.id)
    queue.enqueue(update_analytics, order.id)
    queue.enqueue(inventory.update, order.items)
    return order  # Return immediately

# Content negotiation:
@app.route("/images/<id>")
def get_image(id):
    accept = request.headers.get("Accept", "")
    if "image/webp" in accept:
        return send_file(f"{id}.webp", mimetype="image/webp")
    return send_file(f"{id}.jpg", mimetype="image/jpeg")

# Partial failure handling:
async def get_user_with_fallback(user_id):
    try:
        return await user_service.get(user_id, timeout=2)
    except TimeoutError:
        return await cache.get(f"user:{user_id}")  # fallback
```

---

## 🔒 Contention, Locking & Saturation

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Monitor pool exhaustion** | DB pool, thread pool, HTTP client pool — when exhausted, requests queue indefinitely. Alert before saturation. |
| 🔴 CRITICAL | **Profile database lock contention** | Long transactions, `SELECT ... FOR UPDATE`, hot rows, missing indexes causing lock amplification. |
| 🟡 HIGH | **Measure queue buildup** | Background jobs piling up? Measure lag and processing rate. Alert before backlog becomes critical. |
| 🟡 HIGH | **Fix tail latency amplifiers** | Retries without jitter, synchronized cache expiry — these cause thundering herds that spike P99. |
| 🟡 HIGH | **Implement internal backpressure** | When internal queues fill up, slow down producers. Use bounded queues and propagate pressure upstream. |
| 🟢 MEDIUM | **Use lock-free data structures when appropriate** | For extremely high-contention scenarios, consider lock-free queues, atomic operations, or concurrent collections. |

> 💡 **See also:** [Rate Limiting & Overload Protection](#-rate-limiting--overload-protection) for circuit breakers, load shedding, and external traffic control.

```python
# Contention Examples

# Monitor pool exhaustion:
# Prometheus metric: db_pool_active_connections / db_pool_max_connections
# Alert when > 80%

# Database lock contention:
# PostgreSQL: SELECT * FROM pg_locks WHERE NOT granted;
# Find blocked queries and what's blocking them

# Internal backpressure with bounded queues:
import asyncio

async def producer(queue, data):
    if queue.full():
        # Apply backpressure: slow down or drop
        await asyncio.sleep(0.1)  # rate limit self
    await queue.put(data)

async def consumer(queue):
    while True:
        item = await queue.get()
        process(item)

queue = asyncio.Queue(maxsize=1000)  # bounded!

# Fix tail latency with jitter:
import random

def get_with_jitter(key):
    # Add jitter to TTL to prevent synchronized expiry
    base_ttl = 300
    jitter = random.randint(0, 30)
    cache.set(key, value, ttl=base_ttl + jitter)

# Retry with jitter to prevent thundering herd:
def retry_with_jitter(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception:
            if attempt < max_retries - 1:
                sleep((2 ** attempt) + random.random())  # exponential + jitter
```

---

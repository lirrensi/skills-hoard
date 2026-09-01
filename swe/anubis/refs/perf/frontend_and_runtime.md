# Performance: Frontend And Runtime

> Client-side rendering, storage/file paths, startup costs, runtime tuning, and mobile constraints.
>
> Load this for frontends, local-first apps, CLIs, desktop apps, mobile clients, or cold-start-heavy runtimes.

---

## 🌟 Frontend Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Code-split and lazy-load — don't ship everything upfront** | A 5MB JavaScript bundle on initial load blocks rendering. Code-split by route and lazy-load components that aren't immediately visible. |
| 🔴 CRITICAL | **Avoid render waterfalls — parallelize data fetching** | Parent component fetches, renders child, child fetches — sequential. Move to parallel fetches at the route level. |
| 🔴 CRITICAL | **Virtualize long lists — never render 10k DOM nodes** | Rendering 10,000 list items is an instant jank machine. Virtualization renders only visible items. |
| 🟡 HIGH | **Preload / prefetch critical resources** | `<link rel="preload">` for fonts, critical CSS, key API calls. `<link rel="preconnect">` for critical origins. |
| 🟡 HIGH | **Avoid render-blocking scripts** | Use `async`/`defer` on non-critical scripts. Put critical CSS in `<head>`, non-critical at end of body. |
| 🟡 HIGH | **Memoize expensive React renders** | Components re-render on every parent render, even if their props didn't change. Memoize pure components and callbacks. |
| 🟡 HIGH | **Debounce and throttle event handlers** | A scroll or resize handler firing 60 times/second on every pixel change is unnecessary. Debounce and throttle aggressive events. |
| 🟡 HIGH | **Optimize images — correct format, size, and lazy loading** | Use WebP/AVIF over JPEG. Serve appropriately sized images. Lazy-load offscreen images. Use srcset for responsive images. |
| 🟡 HIGH | **Audit third-party scripts** | Analytics, chat widgets, A/B tools — often 40% of page weight. Lazy-load, defer, or remove unused. |
| 🟡 HIGH | **Measure Core Web Vitals — LCP, FID/INP, CLS** | LCP (largest contentful paint), INP (interaction to next paint), CLS (cumulative layout shift). These directly impact SEO and UX. |
| 🟡 HIGH | **Optimize font loading** | Use `font-display: swap`, subset fonts, WOFF2 format. Preload critical fonts. |
| 🟢 MEDIUM | **Avoid layout thrashing — batch DOM reads and writes** | Interleaving DOM reads and writes forces the browser to recalculate layout repeatedly. Batch reads together, then writes. |
| 🟢 MEDIUM | **Use Service Worker for offline + cache** | Cache static assets aggressively at edge of browser. Enables offline access and faster repeat visits. |

```jsx
// Frontend Examples

// BAD: import HugeModal from "./HugeModal"  // always bundled
// GOOD: const HugeModal = lazy(() => import("./HugeModal"))

// BAD: Component renders, triggers fetch, child renders, triggers fetch
// GOOD: Route loader fetches all data in parallel before render

// BAD: data.map(item => <Row key={item.id} />)  // 10k DOM nodes
// GOOD: <VirtualList items={data} rowHeight={40} />  // ~20 DOM nodes

<!-- Preload critical path -->
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
<link rel="preconnect" href="https://api.example.com">

<!-- Non-critical JS -->
<script src="analytics.js" defer></script>

// React.memo: skips re-render if props unchanged
// useMemo: memoizes expensive computed values
// useCallback: memoizes function references

// BAD: window.addEventListener("scroll", fetchData)
// GOOD: window.addEventListener("scroll", debounce(fetchData, 200))

<img src="img.webp" loading="lazy" width="400" height="300"
     srcset="img-sm.webp 400w, img-lg.webp 800w"
     sizes="(max-width: 600px) 400px, 800px" />

// Tools: Lighthouse, PageSpeed Insights, web-vitals npm package
// Targets: LCP < 2.5s, INP < 200ms, CLS < 0.1

// BAD (thrashing): el.style.width = x + "px"; h = el.clientHeight; ...
// GOOD: const h = el.clientHeight; requestAnimationFrame(() => el.style.width = x)

/* Font optimization */
@font-face {
  font-family: 'Main';
  src: url('/fonts/main.woff2') format('woff2');
  font-display: swap;
}
```

---

## 💾 Storage & File I/O

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Stream large file uploads/downloads** | Buffering a 1GB upload in memory before processing = OOM. Stream directly to disk or object storage. |
| 🟡 HIGH | **Avoid disk I/O on hot paths** | Disk is ~1000x slower than RAM. Log writes, temp files, and config reads should not be in hot paths. |
| 🟡 HIGH | **Use object storage (S3) for blobs** | Don't serve large files through your app server. Use CDN-backed object storage. |
| 🟡 HIGH | **Compress stored data** | Parquet vs CSV for analytics, gzip stored JSON. Storage is cheap but I/O isn't. |
| 🟡 HIGH | **Use connection pooling for object storage** | Reuse HTTP connections to S3/GCS. Don't open a new connection per file. |
| 🟢 MEDIUM | **Choose the right storage class** | Hot data on SSD, cold data on HDD/archive. S3 Standard vs S3 Glacier for access patterns. |

```python
# Storage Examples

# Stream file upload (don't buffer in memory):
@app.post("/upload")
async def upload(file: UploadFile):
    async with aiofiles.open(f"/tmp/{file.filename}", "wb") as f:
        while chunk := await file.read(65536):  # 64KB chunks
            await f.write(chunk)
    return {"status": "ok"}

# Stream to S3 (don't load into memory):
import boto3
s3 = boto3.client('s3')

def upload_stream(file_obj, bucket, key):
    s3.upload_fileobj(file_obj, bucket, key)

# Compress stored data:
import pandas as pd
df.to_parquet("data.parquet")  # vs df.to_csv("data.csv")
# Parquet: 10x smaller, columnar, faster queries

# Storage class decision:
# Hot data: S3 Standard (ms latency)
# Infrequent access: S3 IA (cheaper, retrieval fee)
# Archive: S3 Glacier (hours to retrieve)
```

---

## 🔧 Runtime & GC Tuning

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Tune garbage collection parameters** | In Java/Go/Node, frequent "Stop-the-World" pauses kill latency. Tune heap size and generation sizing to minimize full GCs. |
| 🔴 CRITICAL | **Avoid GC thrashing** | Creating short-lived objects in a tight loop forces the GC to run constantly. Reuse buffers/objects to keep memory pressure stable. |
| 🟡 HIGH | **Warm up the JIT / runtime before routing traffic** | Java/C# need warmup time to JIT compile hot paths. Node.js needs time to optimize V8 paths. Don't route 100% traffic to a cold instance immediately. |
| 🟡 HIGH | **Disable unused runtime features in production** | Turn off debug logging, disable assertion checks, run Python with `-O` to strip assert statements. |
| 🟡 HIGH | **Monitor GC pause times** | If GC pauses exceed your latency budget, you have a problem. Track pause duration and frequency. |
| 🟢 MEDIUM | **Use object pools for hot paths** | Pool and reuse expensive-to-create objects (database connections, thread pools, buffers) instead of creating new ones. |

```bash
# Runtime Tuning Examples

# JVM GC tuning:
java -Xms4g -Xmx4g \           # Fixed heap size (no resize overhead)
     -XX:+UseG1GC \            # G1 garbage collector (low pause)
     -XX:MaxGCPauseMillis=200 \ # Target max pause time
     -XX:+AlwaysPreTouch \     # Touch heap pages at startup
     -jar app.jar

# Node.js --max-old-space-size:
node --max-old-space-size=4096 app.js  # 4GB heap

# Python optimization:
python -O app.py  # Strip assert statements
python -OO app.py # Strip assert AND docstrings

# Go GOGC:
GOGC=100 ./app  # Default, trigger GC when heap doubles
GOGC=off ./app  # Disable GC (only for short-lived CLI tools)

# Warm up before routing traffic:
# Kubernetes: readinessProbe initialDelaySeconds
# Load balancer: gradual traffic shift (10% → 50% → 100%)
```

---

## 📱 Mobile & Battery Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Batch network requests** | Waking up the cellular radio costs battery. Batching uploads/syncs instead of firing every 30 seconds is battery-friendly. |
| 🔴 CRITICAL | **Offload heavy processing to server** | Don't process large datasets or heavy ML models on a mid-range Android phone. Send data up, process, send result down. |
| 🟡 HIGH | **Respect "Low Power Mode"** | Check if the OS is in battery saver mode. If so, disable auto-play videos, reduce fetch frequency, disable animations. |
| 🟡 HIGH | **Optimize overdraw** | Rendering layers on top of invisible layers wastes GPU cycles. Flatten view hierarchies. |
| 🟡 HIGH | **Minimize wake locks** | Holding a wake lock prevents the device from sleeping. Release as soon as possible. |
| 🟢 MEDIUM | **Use efficient image formats** | WebP is 25-35% smaller than JPEG. Smaller downloads = less radio time = less battery. |

```kotlin
// Mobile Examples (Android/Kotlin)

// Batch network requests
// BAD: Upload immediately on every user action
fun onUserAction(event: Event) {
    api.upload(event)  // Wakes radio every time
}

// GOOD: Batch and upload every 5 minutes
val eventBuffer = mutableListOf<Event>()
fun onUserAction(event: Event) {
    eventBuffer.add(event)
    if (eventBuffer.size >= 100) flush()
}

fun flush() {
    api.uploadBatch(eventBuffer)
    eventBuffer.clear()
}

// Check power save mode
val powerManager = getSystemService(Context.POWER_SERVICE) as PowerManager
if (powerManager.isPowerSaveMode) {
    // Reduce polling frequency, disable animations
    fetchInterval = 60_000L  // 1 minute instead of 10 seconds
}

// Reduce overdraw (Android)
// Use Layout Inspector to find overlapping backgrounds
// Remove unnecessary backgrounds from containers
```

```swift
// iOS Examples

// Batch network requests
// Use BGAppRefreshTask for periodic background fetch
// Batch multiple items into single API call

// Check low power mode
if ProcessInfo.processInfo.isLowPowerModeEnabled {
    // Reduce refresh frequency
    refreshInterval = 300  // 5 minutes instead of 30 seconds
}

// Minimize wake locks
// Use URLSessionConfiguration.background for uploads
// Let system decide when to execute
```

---

## 🔨 Build & Startup Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🟡 HIGH | **Lazy imports / deferred initialization** | Import time adds to cold start and test suite time. Lazy-load heavy modules when possible. |
| 🟡 HIGH | **Enable tree-shaking and dead code elimination** | Ships less JS = parses faster. Configure bundler to remove unused code. |
| 🟡 HIGH | **Audit dependencies** | Are you importing lodash for `_.get()`? That's 70KB for one function. Use lighter alternatives. |
| 🟡 HIGH | **Use build caching** | Rebuilding unchanged layers wastes minutes per deploy. Enable CI/CD layer caching. |
| 🟢 MEDIUM | **Parallelize test execution** | Tests running serially? Use parallel test runners to speed up feedback loop. |
| 🟢 MEDIUM | **Measure import time** | Use tools to profile which modules slow down startup. Optimize the slowest ones. |

```python
# Build & Startup Examples

# Lazy imports (Python):
def expensive_function():
    import heavy_module  # Only imported when function is called
    return heavy_module.process()

# Lazy imports (JavaScript):
// Static import at top = always loaded
import { heavy } from 'heavy-module'

// Dynamic import = loaded on demand
async function doHeavy() {
    const { heavy } = await import('heavy-module')
    return heavy()
}

# Tree-shaking (JavaScript):
// BAD: Imports entire library
import _ from 'lodash'
_.get(obj, 'path')

// GOOD: Imports only what you need
import get from 'lodash/get'
get(obj, 'path')

// EVEN BETTER: Use native or lighter alternative
obj?.path  // Native optional chaining

# Build caching (Docker):
# BAD: Copy everything first
COPY . .
RUN pip install -r requirements.txt

# GOOD: Copy requirements first, cache that layer
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # Source changes don't invalidate pip install layer

# Measure import time (Python):
python -X importtime your_script.py 2>&1 | grep "import time"
# Or use: pip install tuna && python -X importtime script.py 2> tuna.log && tuna tuna.log
```

---

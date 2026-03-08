# Runbook Index

This index describes all available runbooks. Read this file first to
determine which runbook matches the current incident, then retrieve
the matching runbook file.

## Available Runbooks

### cpu-high-runbook.md
- **Category:** Infrastructure
- **Symptoms:** CPU utilization sustained above 85%, process slowdown, increased response times, thread pool exhaustion
- **Keywords:** cpu, processor, utilization, load average, throttling, compute
- **Applicable service types:** Any compute workload (APIs, batch processors, workers)

### error-rate-spike-runbook.md
- **Category:** Application
- **Symptoms:** HTTP 5xx error rate exceeds baseline by 2x+, authentication failures, upstream dependency errors, circuit breaker trips
- **Keywords:** error rate, 5xx, 500, 503, failures, exceptions, error spike, error budget
- **Applicable service types:** Web services, APIs, authentication services, middleware

### disk-space-runbook.md
- **Category:** Infrastructure
- **Symptoms:** Disk utilization above 85%, write failures, log rotation failures, database WAL growth, inode exhaustion
- **Keywords:** disk, storage, filesystem, capacity, inode, volume, disk full, no space
- **Applicable service types:** Any service with local storage (databases, log aggregators, file processors)

### latency-degradation-runbook.md
- **Category:** Application
- **Symptoms:** P95/P99 response time exceeds SLO, request queuing, connection pool saturation, downstream timeout increases
- **Keywords:** latency, response time, slow, timeout, p95, p99, degradation, performance
- **Applicable service types:** Customer-facing APIs, gateway services, proxy layers

### memory-exhaustion-runbook.md
- **Category:** Infrastructure
- **Symptoms:** Memory utilization above 90%, OOM kills, swap usage increasing, GC pause times elevated, heap exhaustion
- **Keywords:** memory, RAM, OOM, out of memory, heap, garbage collection, swap, memory leak
- **Applicable service types:** JVM-based services, in-memory caches, batch processing engines

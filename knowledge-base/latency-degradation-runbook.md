# Runbook: Latency Degradation

## Overview
This runbook covers diagnosis and remediation of service latency
degradation. Use when P95 or P99 response times exceed SLO thresholds
or when sustained latency increase is detected.

## Symptoms
- P95/P99 response time exceeds SLO threshold
- Request queue depth increasing
- Connection pool utilization approaching capacity
- Downstream service timeout rate increasing
- User-reported slowness or timeouts

## Diagnostic Steps

### Step 1: Identify the latency source
Determine whether latency is introduced at the application layer,
network layer, or by a downstream dependency. Use distributed
tracing to identify the slowest span in the request path.

### Step 2: Check downstream dependency response times
Review response times for all downstream services, databases,
caches, and external APIs. A single slow dependency can increase
latency for all requests that traverse it.

### Step 3: Analyze connection pool and thread pool metrics
Check connection pool utilization for databases and HTTP clients.
Pool exhaustion forces requests to queue, adding latency. Review
thread pool active counts and queue depths.

### Step 4: Review garbage collection and resource utilization
Check GC pause times, CPU utilization, and memory pressure. High
GC frequency or long GC pauses directly increase response latency.
Memory pressure can cause the OS to swap, severely impacting
performance.

### Step 5: Compare traffic volume to capacity
Determine if the current request rate exceeds the service's tested
capacity. Compare current throughput against load test baselines.
Check if auto-scaling policies (if configured) are responding.

### Step 6: Check for network-level issues
Review network metrics: packet loss, retransmissions, DNS resolution
time, and TLS handshake duration. Network issues can cause latency
spikes that appear intermittent and are difficult to reproduce.

## Remediation Options

### Option A: Scale the bottleneck
If latency is caused by resource saturation (CPU, memory, connections),
add capacity at the bottleneck. Scale the service horizontally or
increase resource limits for the constrained resource.

### Option B: Restart degraded instances
If latency is caused by a degraded instance (GC thrashing, connection
pool corruption, memory fragmentation), restart the affected
instances in a rolling fashion.

### Option C: Enable or adjust caching
If latency is caused by repeated expensive operations (database
queries, external API calls), enable or tune caching. Verify that
cache invalidation is correct before enabling.

### Option D: Shed non-critical traffic
If the service is overloaded, enable load shedding or rate limiting
for non-critical traffic. Prioritize traffic based on business
criticality.

## Escalation Criteria
- P99 latency exceeds 5x the SLO threshold
- Latency affects a customer-facing transaction path
- The root cause involves a shared infrastructure component
  (database, network, DNS)
- Latency does not improve within 15 minutes of remediation
- Multiple services show correlated latency increases

## Rollback Guidance
Latency remediation typically does not require rollback. If a
configuration change (cache settings, pool sizes, timeouts) made
the issue worse:
- Revert the configuration change to the previous value
- Monitor latency for 10 minutes to confirm improvement
- If a deployment is correlated, follow the standard deployment
  rollback procedure

# Runbook: Memory Exhaustion

## Overview
This runbook covers diagnosis and remediation of memory exhaustion
events. Use when memory utilization exceeds 90%, OOM kills are
detected, or swap usage is increasing significantly.

## Symptoms
- Memory utilization sustained above 90%
- OOM (Out of Memory) killer invocations
- Swap usage increasing (indicates physical memory exhaustion)
- Garbage collection pause times elevated
- Heap utilization approaching configured maximum
- Process restarts with exit code 137 (SIGKILL from OOM killer)

## Diagnostic Steps

### Step 1: Identify the memory-consuming process
Determine which process is consuming the most memory. Check both
resident set size (RSS) and virtual memory size (VSZ). Compare
current memory usage against the process's historical baseline.

### Step 2: Analyze memory growth pattern
Determine if memory usage is growing linearly (leak), stepped
(periodic allocation), or spiked (sudden event). A linear growth
pattern over hours or days strongly suggests a memory leak.

### Step 3: Check for recent deployments or configuration changes
Review deployment history for changes that could affect memory
usage: new features, increased cache sizes, new batch jobs,
changes to connection pool settings, or JVM heap configuration.

### Step 4: Review heap dumps or memory profiles
If the service supports it, capture a heap dump or memory profile.
Identify the object types consuming the most memory and trace
them to the responsible code path.

### Step 5: Check for external factors
Review whether increased traffic, larger request payloads, or
a change in data volume could explain the memory increase. A
new batch job processing larger datasets than expected is a
common cause.

## Remediation Options

### Option A: Restart the affected service
If the memory issue is caused by a leak, restarting the service
will reclaim memory. This is a temporary fix — the leak will
recur. Schedule a root cause investigation.

### Option B: Roll back recent deployment
If memory exhaustion correlates with a recent deployment, roll
back to the previous version. Monitor memory usage for 30 minutes
post-rollback to confirm the leak is resolved.

### Option C: Adjust memory limits
If the service legitimately requires more memory (new feature,
increased data volume), increase the memory limit. Ensure the
host or container orchestrator has sufficient capacity.

### Option D: Reduce memory-intensive workload
If a batch job or background process is consuming excessive
memory, throttle or pause it. Reduce batch sizes or processing
concurrency to lower peak memory usage.

## Escalation Criteria
- OOM kills are occurring on a production service
- Memory exhaustion affects a stateful service (database, cache)
- The memory leak rate suggests the service will OOM within 1 hour
- Multiple instances of the same service show identical growth patterns
- The affected service has no redundancy (single instance)

## Rollback Guidance
If a deployment rollback is performed:
- Verify the previous version's memory baseline is known and stable
- Monitor memory usage for at least 30 minutes post-rollback
  (memory leaks may take time to manifest)
- If the service uses a JVM, monitor GC metrics to confirm heap
  utilization returns to baseline
- Document the memory growth rate from the failed deployment to
  aid the development team's investigation

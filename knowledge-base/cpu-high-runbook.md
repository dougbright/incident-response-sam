# Runbook: High CPU Utilization

## Overview
This runbook covers diagnosis and remediation of sustained high CPU
utilization on compute workloads. Use when CPU exceeds 85% for more
than 5 minutes.

## Symptoms
- CPU utilization sustained above 85%
- Increased response latency correlated with CPU
- Thread pool exhaustion or request queuing
- Load average exceeds available core count

## Diagnostic Steps

### Step 1: Identify top CPU-consuming processes
Check which processes are consuming the most CPU on the affected host.
Sort by CPU percentage and review the top 20 processes.

### Step 2: Check for recent configuration or code changes
Determine if any deployments, configuration changes, or feature flag
toggles occurred in the 2 hours preceding the alert. Correlate
timestamps between the change and the onset of high CPU.

### Step 3: Analyze thread and connection pool utilization
Review thread pool metrics and active connection counts. High CPU
often correlates with thread pool exhaustion or connection pool
saturation when the service is under unexpected load.

### Step 4: Check for runaway queries or batch jobs
Look for long-running queries, stuck batch processes, or infinite
loops. Review application logs for repeated error patterns that
may indicate a tight retry loop.

### Step 5: Review traffic patterns
Compare current request volume against baseline. Determine if the
CPU spike correlates with a traffic surge (organic or synthetic)
versus an internal process issue.

## Remediation Options

### Option A: Restart the affected service
If the root cause is a transient issue (memory leak causing CPU
thrashing, stuck thread), restart the service. Verify the service
is stateless or has proper state persistence before restarting.
Monitor CPU for 10 minutes post-restart.

### Option B: Roll back recent deployment
If a recent deployment correlates with the CPU spike, initiate
a rollback to the previous known-good version. Verify the rollback
completes and CPU returns to baseline within 15 minutes.

### Option C: Scale horizontally
If the CPU spike is caused by legitimate traffic growth, add
additional instances to distribute load. Update load balancer
configuration to include new instances.

## Escalation Criteria
- CPU remains above 90% after initial remediation attempt
- Multiple hosts in the same service tier are affected simultaneously
- The service is classified as Tier 1 (customer-facing, revenue-impacting)
- Root cause cannot be identified within 15 minutes

## Rollback Guidance
If a deployment rollback is performed, ensure:
- The previous version's artifacts are available in the artifact repository
- Database migrations (if any) are backward-compatible
- Feature flags associated with the new version are disabled
- Post-rollback health checks pass before declaring the incident resolved

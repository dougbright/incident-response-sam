# Runbook: Error Rate Spike

## Overview
This runbook covers diagnosis and remediation of sudden increases in
application error rates. Use when the HTTP 5xx error rate exceeds
the baseline by 2x or more, or when error budget burn rate triggers
an alert.

## Symptoms
- HTTP 5xx error rate exceeds baseline by 2x or more
- Authentication or authorization failure rate spike
- Circuit breakers tripping on downstream dependencies
- Error budget consumption rate exceeds SLO threshold

## Diagnostic Steps

### Step 1: Classify the error type
Determine whether errors are server-side (5xx), client-side (4xx
spike from a specific caller), or dependency-related (upstream
service returning errors). Check HTTP status code distribution
for the affected service.

### Step 2: Check for recent deployments or configuration changes
Review deployment history for the affected service and its direct
dependencies. Configuration changes, feature flag toggles, and
certificate rotations are common root causes.

### Step 3: Identify the failing code path
Review application logs for stack traces and error messages. Determine
if errors are concentrated in a specific endpoint, handler, or
integration point.

### Step 4: Check downstream dependency health
Verify health and response times of all downstream services,
databases, caches, and external APIs. A single degraded dependency
can cascade errors through multiple upstream services.

### Step 5: Review recent credential or certificate changes
Check if API keys, database credentials, TLS certificates, or
OAuth tokens have expired or been rotated. Authentication-related
errors often spike simultaneously across all endpoints.

## Remediation Options

### Option A: Roll back recent deployment
If errors correlate with a recent deployment to the affected service,
roll back to the previous version. Monitor error rate for 10 minutes
post-rollback to confirm resolution.

### Option B: Disable or roll back feature flag
If the error is isolated to a specific code path gated by a feature
flag, disable the flag. This is lower risk than a full rollback.

### Option C: Fix or bypass failing dependency
If errors are caused by a downstream dependency failure, enable
circuit breaker fallbacks or route traffic to a healthy replica.
Coordinate with the dependency team for their remediation.

### Option D: Restart the affected service
If errors are caused by corrupted in-memory state (stale cache,
connection pool poisoning), restart the service instances in a
rolling fashion to avoid downtime.

## Escalation Criteria
- Error rate exceeds 10% of total requests
- Errors affect authentication or authorization (security implication)
- Multiple independent services show correlated error spikes
- Error rate does not decrease within 10 minutes of remediation
- The affected service processes financial transactions or PII

## Rollback Guidance
If a deployment rollback is performed, ensure:
- The rollback target version is confirmed stable (ran without errors
  for at least 24 hours previously)
- Any database schema changes are backward-compatible
- Dependent services are notified if API contracts changed
- Monitor error rate for 30 minutes post-rollback before closing

# Runbook: Disk Space Critical

## Overview
This runbook covers diagnosis and remediation of critical disk space
utilization. Use when disk usage exceeds 85% or when write failures
are detected.

## Symptoms
- Disk utilization exceeds 85% on any mounted volume
- Application write failures or "no space left on device" errors
- Log rotation failures
- Database write-ahead log (WAL) growth
- Inode exhaustion (disk shows space available but writes fail)

## Diagnostic Steps

### Step 1: Identify the largest consumers of disk space
Check disk usage by directory to identify which directories are
consuming the most space. Focus on log directories, temporary files,
data directories, and core dumps.

### Step 2: Check log file sizes and rotation status
Review log file sizes and verify that log rotation is functioning
correctly. Failed log rotation is a common cause of disk exhaustion.
Check for compressed log archives that should have been cleaned up.

### Step 3: Review temporary file accumulation
Check temporary directories for accumulated files from failed
processes, incomplete uploads, or orphaned session files. Temporary
files that are not cleaned up by application shutdown can accumulate
over weeks.

### Step 4: Check database storage growth
If the host runs a database, review table sizes, WAL segment
accumulation, and backup retention. Uncontrolled WAL growth often
indicates a replication lag or failed backup process.

### Step 5: Verify inode availability
Even with available disk space, inode exhaustion can prevent new
file creation. Check inode utilization if write failures occur
despite reported free space.

## Remediation Options

### Option A: Clean up known safe targets
Remove or archive files that are safe to delete: old log archives,
temporary files older than 24 hours, core dumps, and expired cache
files. Do not delete active log files — truncate them instead.

### Option B: Extend volume capacity
If the disk is a managed volume (cloud block storage, LVM), extend
the volume and resize the filesystem. This is non-destructive and
does not require downtime on most modern filesystems.

### Option C: Fix log rotation
If log rotation is broken, fix the rotation configuration and
manually rotate the current log files. Verify the fix by checking
that rotation runs successfully on the next cycle.

### Option D: Move data to alternative storage
If a specific data directory is consuming disproportionate space,
move it to a larger volume or to object storage. Update application
configuration to reference the new path.

## Escalation Criteria
- Disk utilization exceeds 95%
- Database write failures are occurring (data integrity risk)
- The issue affects multiple hosts in the same tier
- Root cause is unknown (unexpected disk growth pattern)
- The affected host runs a stateful service with no replica

## Rollback Guidance
Disk space remediation is generally additive (freeing space, extending
volumes) and does not require rollback. If files were deleted in error:
- Check if deleted files are still held open by a process (recoverable
  via /proc on Linux)
- Restore from the most recent backup
- If database files were affected, initiate point-in-time recovery

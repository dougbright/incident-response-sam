"""Deployment lookup tool for the Triage Agent.

Reads simulated deployment history from data/deployments.json and
returns recent deployments for a given service, with a correlation
flag if a deploy happened within the alert time window.
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional

from solace_agent_mesh.agent.tools import ToolResult


async def lookup_recent_deployments(
    service_name: str,
    hours: int = 24,
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None,
) -> ToolResult:
    """Look up recent deployments for a service to check for deploy correlation.

    Use this tool when triaging an alert to determine if a recent deployment
    to the affected service could be the root cause. Returns deployment
    details and a correlation flag.

    Args:
        service_name: The name of the service to look up deployments for.
        hours: How many hours back to search for deployments. Defaults to 24.
    """
    # Resolve the path to deployments.json relative to the project root.
    # tool_config can override this, but defaults to data/deployments.json
    # in the project directory.
    data_path = "data/deployments.json"
    if tool_config and tool_config.get("data_path"):
        data_path = tool_config["data_path"]

    if not os.path.isabs(data_path):
        # Resolve relative to the project root (two levels up from this file)
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        data_path = os.path.join(project_root, data_path)

    # Load deployment data
    try:
        with open(data_path, "r") as f:
            all_deployments = json.load(f)
    except FileNotFoundError:
        return ToolResult.error(f"Deployment data file not found: {data_path}")
    except json.JSONDecodeError:
        return ToolResult.error(f"Invalid JSON in deployment data file: {data_path}")

    # Filter by service name (case-insensitive)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    matching = []

    for deploy in all_deployments:
        if deploy["service_name"].lower() != service_name.lower():
            continue

        deploy_time = datetime.fromisoformat(deploy["timestamp"])
        if deploy_time >= cutoff:
            matching.append(deploy)

    # Sort by timestamp descending (most recent first)
    matching.sort(key=lambda d: d["timestamp"], reverse=True)

    # Build the result
    if not matching:
        return ToolResult.ok(
            f"No deployments found for '{service_name}' in the last {hours} hours.",
            data={
                "service_name": service_name,
                "hours_searched": hours,
                "deployments_found": 0,
                "deploy_correlation": False,
                "deployments": [],
            },
        )

    most_recent = matching[0]
    deploy_time = datetime.fromisoformat(most_recent["timestamp"])
    age_minutes = int((datetime.now(timezone.utc) - deploy_time).total_seconds() / 60)

    return ToolResult.ok(
        f"Found {len(matching)} deployment(s) for '{service_name}' in the last "
        f"{hours} hours. Most recent: version {most_recent['version']} deployed "
        f"{age_minutes} minutes ago. Change: {most_recent['change_summary']}",
        data={
            "service_name": service_name,
            "hours_searched": hours,
            "deployments_found": len(matching),
            "deploy_correlation": True,
            "most_recent_deploy": {
                "deployment_id": most_recent["deployment_id"],
                "version": most_recent["version"],
                "previous_version": most_recent["previous_version"],
                "timestamp": most_recent["timestamp"],
                "age_minutes": age_minutes,
                "commit_sha": most_recent["commit_sha"],
                "change_summary": most_recent["change_summary"],
                "change_ticket": most_recent["change_ticket"],
                "rollback_version": most_recent["rollback_version"],
            },
            "all_deployments": matching,
        },
    )

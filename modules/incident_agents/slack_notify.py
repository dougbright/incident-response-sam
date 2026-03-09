"""Slack notification tool for the Notification Agent.

Posts incident sitreps to a Slack channel via an Incoming Webhook URL.
"""

import json
import os
import urllib.request
import urllib.error
from typing import Any, Dict, Optional

from solace_agent_mesh.agent.tools import ToolResult


async def post_to_slack(
    message: str,
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None,
) -> ToolResult:
    """Post a message to the incident Slack channel.

    Use this tool to send the stakeholder sitrep to Slack after generating it.

    Args:
        message: The sitrep text to post to Slack.
    """
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
    if tool_config and tool_config.get("webhook_url"):
        webhook_url = tool_config["webhook_url"]

    if not webhook_url:
        return ToolResult.error("SLACK_WEBHOOK_URL environment variable is not set.")

    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return ToolResult.ok("Sitrep posted to Slack successfully.")
    except urllib.error.HTTPError as e:
        return ToolResult.error(f"Slack webhook returned HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        return ToolResult.error(f"Failed to reach Slack: {e.reason}")

#!/usr/bin/env python3
"""
Alert Generator — sends simulated Datadog webhook alerts.

Supports two modes:
  --mode broker   Publish directly to Solace broker topics (picked up by Event Mesh Gateway)
  --mode webui    Submit via the SAM Web UI REST API (original behavior)

Usage:
    python alert_generator.py --scenario cpu
    python alert_generator.py --scenario cpu --mode webui
    python alert_generator.py --all
"""

import argparse
import json
import sys
import time
import uuid
from datetime import datetime, timezone

import requests


# Scenarios use Datadog webhook payload format.
# See https://docs.datadoghq.com/integrations/webhooks/ for variable reference.
SCENARIOS = {
    "cpu": {
        "topic": "monitoring/alerts/infra/cpu",
        "alert": {
            "title": "[Triggered] CPU utilization critical on payment-processor in us-east-1",
            "host": "prod-pp-07.us-east-1.internal",
            "alert_metric": "system.cpu.utilization",
            "alert_query": "avg(last_10m):avg:system.cpu.utilization{service:payment-processor, host:prod-pp-07.us-east-1.internal} > 85",
            "body": (
                "The monitor 'payment-processor CPU utilization' was triggered.\n\n"
                "Metric value: 94.2% (threshold: 85%)\n"
                "Duration: 12 minutes above threshold\n\n"
                "Host: prod-pp-07.us-east-1.internal\n"
                "Service: payment-processor\n"
                "Region: us-east-1\n"
                "Environment: production\n\n"
                "Top CPU consumers:\n"
                "- java (PID 4821): 67.3% — payment-processor main process\n"
                "- java (PID 4955): 18.1% — connection pool health checker\n\n"
                "Related signals: Thread count elevated (847, baseline: 200), "
                "error rate 2.3% (baseline: 0.1%)"
            ),
            "tags": "service:payment-processor,host:prod-pp-07.us-east-1.internal,region:us-east-1,env:production,team:payments,tier:1,pci-scope:yes",
            "alert_status": "Triggered",
            "alert_transition": "Triggered",
            "priority": "normal",
            "link": "https://app.datadoghq.com/monitors/18294701",
            "date": None,  # filled at runtime
            "last_updated": None,
            "event_type": "metric_alert_monitor",
            "id": "18294701",
            "org_name": "ABC Financial",
        },
    },
    "error-rate": {
        "topic": "monitoring/alerts/app/error-rate",
        "alert": {
            "title": "[Triggered] Error rate spike on auth-service in us-east-1",
            "host": "prod-auth-03.us-east-1.internal",
            "alert_metric": "trace.http.request.errors.by_http_status",
            "alert_query": "avg(last_10m):sum:trace.http.request.errors{service:auth-service, region:us-east-1, http.status_class:5xx} / sum:trace.http.request.hits{service:auth-service, region:us-east-1} > 0.02",
            "body": (
                "The monitor 'auth-service error rate' was triggered.\n\n"
                "Metric value: 8.7% (threshold: 2%)\n"
                "Baseline (7d avg): 0.3%\n"
                "Duration: 8 minutes above threshold\n\n"
                "Host: prod-auth-03.us-east-1.internal\n"
                "Service: auth-service\n"
                "Region: us-east-1\n"
                "Environment: production\n\n"
                "Top errors:\n"
                "- HTTP 500: 78% of errors — InvalidTokenException in JWTValidator.validate()\n"
                "- HTTP 503: 22% of errors — upstream connect timeout to user-store\n\n"
                "Affected endpoints: /api/v2/authenticate (62%), /api/v2/token/refresh (38%)\n"
                "347 errors in last 5 minutes"
            ),
            "tags": "service:auth-service,host:prod-auth-03.us-east-1.internal,region:us-east-1,env:production,team:identity,tier:1,pci-scope:yes",
            "alert_status": "Triggered",
            "alert_transition": "Triggered",
            "priority": "normal",
            "link": "https://app.datadoghq.com/monitors/18294732",
            "date": None,
            "last_updated": None,
            "event_type": "metric_alert_monitor",
            "id": "18294732",
            "org_name": "ABC Financial",
        },
    },
    "disk": {
        "topic": "monitoring/alerts/infra/disk",
        "alert": {
            "title": "[Triggered] Disk utilization warning on log-aggregator in us-east-1",
            "host": "prod-log-02.us-east-1.internal",
            "alert_metric": "system.disk.in_use",
            "alert_query": "avg(last_5m):avg:system.disk.in_use{service:log-aggregator, host:prod-log-02.us-east-1.internal, device:/data} > 0.85",
            "body": (
                "The monitor 'log-aggregator disk utilization' was triggered.\n\n"
                "Metric value: 91.3% (threshold: 85%)\n"
                "Duration: 45 minutes above threshold\n\n"
                "Host: prod-log-02.us-east-1.internal\n"
                "Service: log-aggregator\n"
                "Region: us-east-1\n"
                "Environment: production\n"
                "Volume: /data\n\n"
                "Disk growth rate: 2.1 GB/hour\n"
                "Estimated time to full: 6 hours\n"
                "Current usage: 1.83 TB / 2.0 TB\n\n"
                "Top space consumers:\n"
                "- /data/logs/settlement-engine: 487 GB (log rotation may be stalled)\n"
                "- /data/logs/payment-processor: 312 GB\n"
                "- /data/logs/auth-service: 298 GB"
            ),
            "tags": "service:log-aggregator,host:prod-log-02.us-east-1.internal,region:us-east-1,env:production,team:platform,tier:2,device:/data",
            "alert_status": "Triggered",
            "alert_transition": "Triggered",
            "priority": "normal",
            "link": "https://app.datadoghq.com/monitors/18294755",
            "date": None,
            "last_updated": None,
            "event_type": "metric_alert_monitor",
            "id": "18294755",
            "org_name": "ABC Financial",
        },
    },
    "latency": {
        "topic": "monitoring/alerts/app/latency",
        "alert": {
            "title": "[Triggered] P99 latency degradation on order-gateway in us-east-1",
            "host": "prod-og-05.us-east-1.internal",
            "alert_metric": "trace.http.request.duration.by_service.p99",
            "alert_query": "avg(last_10m):p99:trace.http.request.duration{service:order-gateway, region:us-east-1} > 1500",
            "body": (
                "The monitor 'order-gateway P99 latency' was triggered.\n\n"
                "Metric value: 4200ms (threshold: 1500ms)\n"
                "Baseline (7d avg): 450ms\n"
                "Duration: 15 minutes above threshold\n\n"
                "Host: prod-og-05.us-east-1.internal\n"
                "Service: order-gateway\n"
                "Region: us-east-1\n"
                "Environment: production\n\n"
                "Latency breakdown (p99):\n"
                "- /api/v1/orders: 4200ms (baseline: 380ms)\n"
                "- /api/v1/orders/{id}/status: 2800ms (baseline: 120ms)\n"
                "- /api/v1/health: 45ms (normal)\n\n"
                "23% of requests exceeding 5s client timeout\n"
                "Downstream: settlement-engine response times normal"
            ),
            "tags": "service:order-gateway,host:prod-og-05.us-east-1.internal,region:us-east-1,env:production,team:trading,tier:1,pci-scope:yes",
            "alert_status": "Triggered",
            "alert_transition": "Triggered",
            "priority": "normal",
            "link": "https://app.datadoghq.com/monitors/18294778",
            "date": None,
            "last_updated": None,
            "event_type": "metric_alert_monitor",
            "id": "18294778",
            "org_name": "ABC Financial",
        },
    },
    "memory": {
        "topic": "monitoring/alerts/infra/memory",
        "alert": {
            "title": "[Triggered] Memory utilization critical on settlement-engine in us-east-1",
            "host": "prod-se-01.us-east-1.internal",
            "alert_metric": "system.mem.pct_usable",
            "alert_query": "avg(last_5m):avg:system.mem.pct_usable{service:settlement-engine, host:prod-se-01.us-east-1.internal} < 0.10",
            "body": (
                "The monitor 'settlement-engine memory utilization' was triggered.\n\n"
                "Metric value: 96.1% used (threshold: 90%)\n"
                "Duration: 20 minutes above threshold\n\n"
                "Host: prod-se-01.us-east-1.internal\n"
                "Service: settlement-engine\n"
                "Region: us-east-1\n"
                "Environment: production\n\n"
                "JVM heap utilization: 94.7% (12.1 GB / 12.8 GB)\n"
                "GC pause avg: 850ms (baseline: 45ms)\n"
                "Full GC events in last 10m: 14 (baseline: 0-1)\n\n"
                "OOM risk: HIGH — if trend continues, OOMKill expected within 15 minutes\n\n"
                "Related signals: End-of-day batch reconciliation job started 25 minutes ago, "
                "processing 2.3M cross-border transactions"
            ),
            "tags": "service:settlement-engine,host:prod-se-01.us-east-1.internal,region:us-east-1,env:production,team:settlements,tier:1,sox-scope:yes",
            "alert_status": "Triggered",
            "alert_transition": "Triggered",
            "priority": "normal",
            "link": "https://app.datadoghq.com/monitors/18294791",
            "date": None,
            "last_updated": None,
            "event_type": "metric_alert_monitor",
            "id": "18294791",
            "org_name": "ABC Financial",
        },
    },
}


def _fill_timestamps(alert: dict) -> dict:
    """Set date/last_updated to current epoch time."""
    alert = alert.copy()
    epoch = str(int(datetime.now(timezone.utc).timestamp()))
    alert["date"] = epoch
    alert["last_updated"] = epoch
    return alert


def publish_via_broker(scenario_name: str, broker_url: str = "ws://localhost:8008"):
    """Publish alert JSON directly to a Solace broker topic.

    The Event Mesh Gateway subscribes to monitoring/alerts/> and forwards
    the payload to the OrchestratorAgent automatically.
    """
    from solace.messaging.messaging_service import MessagingService
    from solace.messaging.resources.topic import Topic

    scenario = SCENARIOS[scenario_name]
    alert = _fill_timestamps(scenario["alert"])
    topic_str = scenario["topic"]

    # Parse broker URL into host/port for the Solace PubSub+ SDK
    broker_props = {
        "solace.messaging.transport.host": broker_url,
        "solace.messaging.service.vpn-name": "default",
        "solace.messaging.authentication.scheme.basic.username": "default",
        "solace.messaging.authentication.scheme.basic.password": "default",
    }

    service = MessagingService.builder().from_properties(broker_props).build()
    service.connect()

    publisher = service.create_direct_message_publisher_builder().build()
    publisher.start()

    payload = json.dumps(alert, indent=2)
    topic = Topic.of(topic_str)

    print(f"Publishing {scenario_name} alert to broker topic: {topic_str}")
    print(f"  Title: {alert['title']}")
    print(f"  Host: {alert['host']}")

    publisher.publish(message=payload, destination=topic)

    print(f"  -> Published. The Event Mesh Gateway will pick this up.")
    print(f"  -> Watch progress in the web UI: http://127.0.0.1:8000")

    publisher.terminate()
    service.disconnect()


def publish_via_webui(scenario_name: str, api_url: str = "http://127.0.0.1:8000", watch: bool = True):
    """Send alert via the SAM Web UI streaming API."""
    scenario = SCENARIOS[scenario_name]
    alert = _fill_timestamps(scenario["alert"])

    alert_text = f"DATADOG WEBHOOK ALERT:\n{json.dumps(alert, indent=2)}"

    session_id = f"alert-session-{uuid.uuid4().hex[:8]}"

    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/stream",
        "params": {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": alert_text,
                    }
                ],
                "messageId": str(uuid.uuid4()),
                "contextId": session_id,
                "metadata": {
                    "agent_name": "OrchestratorAgent",
                },
            }
        },
    }

    print(f"Sending {scenario_name} alert via streaming API...")
    print(f"  Service: {alert.get('host', 'unknown')}")
    print(f"  Priority: {alert.get('priority', 'unknown')}")
    print(f"  Title: {alert['title']}")

    resp = requests.post(
        f"{api_url}/api/v1/message:stream",
        json=payload,
        headers={"Content-Type": "application/json"},
    )

    if resp.status_code != 200:
        print(f"  -> Failed: {resp.status_code} {resp.text}")
        return

    result = resp.json()
    task_id = None

    if "result" in result:
        task_obj = result["result"]
        if isinstance(task_obj, dict):
            task_id = task_obj.get("id")

    if not task_id:
        print(f"  -> Sent but could not extract task ID from response: {result}")
        return

    print(f"  -> Task created: {task_id} (session: {session_id})")
    print(f"  -> View in web UI: {api_url}")

    if not watch:
        return

    print(f"\n  Monitoring task progress (Ctrl+C to stop)...\n")
    try:
        sse_resp = requests.get(
            f"{api_url}/api/v1/sse/subscribe/{task_id}",
            stream=True,
            timeout=600,
        )

        event_type = None
        for line in sse_resp.iter_lines(decode_unicode=True):
            if line is None:
                continue

            if line.startswith("event:"):
                event_type = line[6:].strip()
            elif line.startswith("data:"):
                data_str = line[5:].strip()
                try:
                    data = json.loads(data_str)
                except (json.JSONDecodeError, ValueError):
                    continue

                _print_event(event_type, data)

                if _is_final_event(event_type, data):
                    print("\n  Task completed.")
                    return
            elif line.startswith(":"):
                pass

    except KeyboardInterrupt:
        print("\n  Stopped monitoring.")
    except requests.exceptions.ConnectionError:
        print("  -> Lost connection to server.")


def _print_event(event_type: str, data: dict):
    """Pretty-print an SSE event."""
    if event_type == "status_update":
        status = data.get("status", {})
        state = status.get("state", "unknown")
        message = status.get("message", {})
        if isinstance(message, dict):
            text = message.get("text", "")
        else:
            text = str(message)
        if text:
            if len(text) > 200:
                text = text[:200] + "..."
            print(f"  [{state}] {text}")

    elif event_type == "final_response":
        result = data.get("result", {})
        status = result.get("status", {})
        state = status.get("state", "unknown")
        message = status.get("message", {})
        if isinstance(message, dict):
            text = message.get("text", "")
        else:
            text = str(message)
        if text:
            print(f"\n  === FINAL RESPONSE ({state}) ===")
            print(f"  {text[:1000]}")
        else:
            print(f"\n  === TASK FINISHED ({state}) ===")

    elif event_type == "artifact_update":
        artifact = data.get("artifact", {})
        name = artifact.get("name", "unknown")
        print(f"  [artifact] {name}")


def _is_final_event(event_type: str, data: dict) -> bool:
    """Check if this SSE event indicates the task is done."""
    if event_type == "final_response":
        return True
    if event_type == "status_update":
        status = data.get("status", {})
        state = status.get("state", "")
        if state in ("completed", "failed", "canceled"):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Publish simulated Datadog webhook alerts")
    parser.add_argument(
        "--scenario",
        choices=list(SCENARIOS.keys()),
        help="Alert scenario to publish",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Publish all scenarios with a 3-second delay between each",
    )
    parser.add_argument(
        "--mode",
        choices=["broker", "webui"],
        default="broker",
        help="Delivery mode: 'broker' publishes to Solace topic (default), 'webui' uses REST API",
    )
    parser.add_argument(
        "--api-url",
        default="http://127.0.0.1:8000",
        help="SAM Web UI API URL for webui mode (default: http://127.0.0.1:8000)",
    )
    parser.add_argument(
        "--broker-url",
        default="ws://localhost:8008",
        help="Solace broker URL for broker mode (default: ws://localhost:8008)",
    )
    parser.add_argument(
        "--no-watch",
        action="store_true",
        help="Don't monitor SSE stream (webui mode only)",
    )

    args = parser.parse_args()

    if not args.scenario and not args.all:
        parser.print_help()
        return

    scenarios = list(SCENARIOS.keys()) if args.all else [args.scenario]

    for i, name in enumerate(scenarios):
        if args.mode == "broker":
            publish_via_broker(name, args.broker_url)
        else:
            publish_via_webui(name, args.api_url, watch=not args.no_watch)

        if args.all and i < len(scenarios) - 1:
            print("  Waiting 3 seconds...")
            time.sleep(3)


if __name__ == "__main__":
    main()

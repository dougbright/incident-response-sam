
{
  "title": "[Triggered] P99 latency degradation on order-gateway in us-east-1",
  "host": "prod-og-05.us-east-1.internal",
  "alert_metric": "trace.http.request.duration.by_service.p99",
  "alert_query": "avg(last_10m):p99:trace.http.request.duration{service:order-gateway, region:us-east-1} > 1500",
  "body": "The monitor 'order-gateway P99 latency' was triggered.\n\nMetric value: 4200ms (threshold: 1500ms)\nBaseline (7d avg): 450ms\nDuration: 15 minutes above threshold\n\nHost: prod-og-05.us-east-1.internal\nService: order-gateway\nRegion: us-east-1\nEnvironment: production\n\nLatency breakdown (p99):\n- /api/v1/orders: 4200ms (baseline: 380ms)\n- /api/v1/orders/{id}/status: 2800ms (baseline: 120ms)\n- /api/v1/health: 45ms (normal)\n\n23% of requests exceeding 5s client timeout\nDownstream: settlement-engine response times normal",
  "tags": "service:order-gateway,host:prod-og-05.us-east-1.internal,region:us-east-1,env:production,team:trading,tier:1,pci-scope:yes",
  "alert_status": "Triggered",
  "alert_transition": "Triggered",
  "priority": "normal",
  "link": "https://app.datadoghq.com/monitors/18294778",
  "date": "1741459200",
  "last_updated": "1741459200",
  "event_type": "metric_alert_monitor",
  "id": "18294778",
  "org_name": "ABC Financial"
}

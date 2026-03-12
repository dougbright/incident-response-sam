DATADOG WEBHOOK ALERT:
{
  "title": "[Triggered] Memory utilization critical on settlement-engine in us-east-1",
  "host": "prod-se-01.us-east-1.internal",
  "alert_metric": "system.mem.pct_usable",
  "alert_query": "avg(last_5m):avg:system.mem.pct_usable{service:settlement-engine, host:prod-se-01.us-east-1.internal} < 0.10",
  "body": "The monitor 'settlement-engine memory utilization' was triggered.\n\nMetric value: 96.1% used (threshold: 90%)\nDuration: 20 minutes above threshold\n\nHost: prod-se-01.us-east-1.internal\nService: settlement-engine\nRegion: us-east-1\nEnvironment: production\n\nJVM heap utilization: 94.7% (12.1 GB / 12.8 GB)\nGC pause avg: 850ms (baseline: 45ms)\nFull GC events in last 10m: 14 (baseline: 0-1)\n\nOOM risk: HIGH — if trend continues, OOMKill expected within 15 minutes\n\nRelated signals: End-of-day batch reconciliation job started 25 minutes ago, processing 2.3M cross-border transactions",
  "tags": "service:settlement-engine,host:prod-se-01.us-east-1.internal,region:us-east-1,env:production,team:settlements,tier:1,sox-scope:yes",
  "alert_status": "Triggered",
  "alert_transition": "Triggered",
  "priority": "normal",
  "link": "https://app.datadoghq.com/monitors/18294791",
  "date": "1741459200",
  "last_updated": "1741459200",
  "event_type": "metric_alert_monitor",
  "id": "18294791",
  "org_name": "ABC Financial"
}

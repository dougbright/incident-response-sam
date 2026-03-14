
{
  "title": "[Triggered] Disk utilization warning on log-aggregator in us-east-1",
  "host": "prod-log-02.us-east-1.internal",
  "alert_metric": "system.disk.in_use",
  "alert_query": "avg(last_5m):avg:system.disk.in_use{service:log-aggregator, host:prod-log-02.us-east-1.internal, device:/data} > 0.85",
  "body": "The monitor 'log-aggregator disk utilization' was triggered.\n\nMetric value: 91.3% (threshold: 85%)\nDuration: 45 minutes above threshold\n\nHost: prod-log-02.us-east-1.internal\nService: log-aggregator\nRegion: us-east-1\nEnvironment: production\nVolume: /data\n\nDisk growth rate: 2.1 GB/hour\nEstimated time to full: 6 hours\nCurrent usage: 1.83 TB / 2.0 TB\n\nTop space consumers:\n- /data/logs/settlement-engine: 487 GB (log rotation may be stalled)\n- /data/logs/payment-processor: 312 GB\n- /data/logs/auth-service: 298 GB",
  "tags": "service:log-aggregator,host:prod-log-02.us-east-1.internal,region:us-east-1,env:production,team:platform,tier:2,device:/data",
  "alert_status": "Triggered",
  "alert_transition": "Triggered",
  "priority": "normal",
  "link": "https://app.datadoghq.com/monitors/18294755",
  "date": "1741459200",
  "last_updated": "1741459200",
  "event_type": "metric_alert_monitor",
  "id": "18294755",
  "org_name": "ABC Financial"
}

{
  "title": "[Triggered] CPU utilization critical on payment-processor in us-east-1",
  "host": "prod-pp-07.us-east-1.internal",
  "alert_metric": "system.cpu.utilization",
  "alert_query": "avg(last_10m):avg:system.cpu.utilization{service:payment-processor, host:prod-pp-07.us-east-1.internal} > 85",
  "body": "The monitor 'payment-processor CPU utilization' was triggered.\n\nMetric value: 94.2% (threshold: 85%)\nDuration: 12 minutes above threshold\n\nHost: prod-pp-07.us-east-1.internal\nService: payment-processor\nRegion: us-east-1\nEnvironment: production\n\nTop CPU consumers:\n- java (PID 4821): 67.3% — payment-processor main process\n- java (PID 4955): 18.1% — connection pool health checker\n\nRelated signals: Thread count elevated (847, baseline: 200), error rate 2.3% (baseline: 0.1%)",
  "tags": "service:payment-processor,host:prod-pp-07.us-east-1.internal,region:us-east-1,env:production,team:payments,tier:1,pci-scope:yes",
  "alert_status": "Triggered",
  "alert_transition": "Triggered",
  "priority": "normal",
  "link": "https://app.datadoghq.com/monitors/18294701",
  "date": "1741459200",
  "last_updated": "1741459200",
  "event_type": "metric_alert_monitor",
  "id": "18294701",
  "org_name": "ABC Financial"
}

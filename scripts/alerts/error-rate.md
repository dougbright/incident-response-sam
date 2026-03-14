
{
  "title": "[Triggered] Error rate spike on auth-service in us-east-1",
  "host": "prod-auth-03.us-east-1.internal",
  "alert_metric": "trace.http.request.errors.by_http_status",
  "alert_query": "avg(last_10m):sum:trace.http.request.errors{service:auth-service, region:us-east-1, http.status_class:5xx} / sum:trace.http.request.hits{service:auth-service, region:us-east-1} > 0.02",
  "body": "The monitor 'auth-service error rate' was triggered.\n\nMetric value: 8.7% (threshold: 2%)\nBaseline (7d avg): 0.3%\nDuration: 8 minutes above threshold\n\nHost: prod-auth-03.us-east-1.internal\nService: auth-service\nRegion: us-east-1\nEnvironment: production\n\nTop errors:\n- HTTP 500: 78% of errors — InvalidTokenException in JWTValidator.validate()\n- HTTP 503: 22% of errors — upstream connect timeout to user-store\n\nAffected endpoints: /api/v2/authenticate (62%), /api/v2/token/refresh (38%)\n347 errors in last 5 minutes",
  "tags": "service:auth-service,host:prod-auth-03.us-east-1.internal,region:us-east-1,env:production,team:identity,tier:1,pci-scope:yes",
  "alert_status": "Triggered",
  "alert_transition": "Triggered",
  "priority": "normal",
  "link": "https://app.datadoghq.com/monitors/18294732",
  "date": "1741459200",
  "last_updated": "1741459200",
  "event_type": "metric_alert_monitor",
  "id": "18294732",
  "org_name": "ABC Financial"
}

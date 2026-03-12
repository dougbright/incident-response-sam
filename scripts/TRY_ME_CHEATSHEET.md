# Try Me! Quick Reference

## Broker Password

```
oanbh8b5452m50qj6lnf7m8hk1
```

## Subscriber (final response only)

Topic: `incident-response/a2a/v1/gateway/response/>`

## Publisher

Topic: `monitoring/alerts/infra/cpu`

Message:

```
{"title":"[Triggered] CPU critical on payment-processor us-east-1","host":"prod-pp-07.us-east-1.internal","alert_metric":"system.cpu.utilization","body":"Metric: 94.2% (threshold 85%), 12min above threshold. Service: payment-processor, Region: us-east-1, Env: production. Top CPU: java PID 4821 67.3% (main process), java PID 4955 18.1% (conn pool health checker). Related: thread count 847 (baseline 200), error rate 2.3% (baseline 0.1%)","tags":"service:payment-processor,region:us-east-1,env:production,team:payments,tier:1,pci-scope:yes","alert_status":"Triggered","priority":"normal","id":"18294701","org_name":"ABC Financial"}
```

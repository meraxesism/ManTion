# 🏭 Enterprise Deployment Guide

Guidance for deploying ManTion in production-like environments.

## Docker
- Build and run with docker-compose: `docker-compose up`
- Mount `models/` and `logs/` as volumes
- Configure environment variables for ports, logging level, model paths

## Kubernetes
- Separate Deployments for API and Frontend
- Use NodeSelectors/Taints to bind camera access to designated nodes
- PersistentVolume for `logs/` and `models/`
- Liveness/Readiness probes on API
- NetworkPolicies to restrict traffic

## PLC/MES Integration
- Use `line_control.py` (PLC-ready) for Modbus/OPC-UA adapters
- Implement webhooks from API to MES for event logging
- Validate emergency stop paths out-of-band

## Observability
- Structured logs (JSON) forwarded to ELK/Datadog
- Metrics: request latency, frame processing time, detection counts
- Traces for critical paths (API -> Camera -> AI -> Control)

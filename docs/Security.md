# 🔒 Security Hardening

Guidance for deploying ManTion securely.

## Network & Transport
- Enforce HTTPS (TLS 1.2+) via reverse proxy/ingress
- Prefer RTSP over TLS or VPN for camera streams
- Restrict egress; segment camera networks; apply firewall rules / NetworkPolicies

## AuthN & AuthZ
- Protect API with JWT or mTLS; rotate secrets regularly
- Use role-based access (operator/supervisor/admin)
- Enable audit logging for critical actions

## Secrets & Data
- Store secrets in env vars or secret managers (KMS/Vault); never commit
- Mask PII/credentials in logs; set log retention policies

## Hardening Checklist
- Disable unused endpoints; rate-limit APIs
- Health probes and liveness/readiness checks
- Regular dependency updates and vulnerability scans

## Compliance Considerations
- ISO 13849: Designed to support safety-integrity practices; certification not included
- Keep an audit trail of detection and control events for regulatory reviews

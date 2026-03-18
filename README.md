# HELL (Active Defense Honeypot) - PROJECT EVANGELION
## Version: 16.5.6-STABLE (ASCII EDITION)

### Overview
HELL is a high-interaction, active defense infrastructure designed to neutralize botnets and capture forensic intelligence through deception.

### Key Changes (March 18, 2026)
- **Infrastructure Upgrade:** Droplet resized to 8GB RAM / 2 vCPUs to prevent OOM-Killer.
- **Shadow Log Protocol:** Core writes to `hell_activity.log`, Dashboard reads from `dashboard_live.log` (copy every 5s) to prevent file locking in Host Mode.
- **Consolidated Architecture:** Dashboard is now an internal thread of the Core process.
- **Zero-Emoji Policy:** Compliance with GEMINI.md protocol. All UI and logs use ASCII/Text indicators only.
- **Lethal Modules:** 51 ports active + VOID redirect (20101-65534).

### Deployment
```bash
export DOCKER_API_VERSION=1.41
docker-compose up -d --build --force-recreate
```

### Rollback Point
Commit: `d9a5731`
Status: PRODUCTIVE / STABLE

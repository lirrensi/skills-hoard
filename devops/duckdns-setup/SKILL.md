---
name: duckdns-setup
description: Set up DuckDNS for a server, keep the hostname updated, and hand it off to HTTPS/self-hosting when the user has no domain. Use whenever the user says DuckDNS, dynamic DNS, free hostname, stable URL, no domain, or needs a server reachable by name without buying a domain.
---

# duckdns-setup

Create or update a DuckDNS hostname and keep it synced to the server's public IP.

## Platform

- Primary target: Linux/macOS shell with `bash`
- Also practical on Windows with PowerShell or Task Scheduler

## Quick scout

Check only what matters for this job:

```bash
curl -4 https://api.ipify.org
command -v curl
command -v caddy
```

## Workflow

1. Ask for the DuckDNS subdomain and token if they are missing.
2. Store the token in a `.env` file or environment variable, not in shell history or process args.
3. Update the DuckDNS record over HTTPS.
4. Verify DNS resolves to the intended current public IP.
5. If the user wants HTTPS, hand the hostname to Caddy.
6. If they need wildcard/DNS-01, mention the DuckDNS Caddy DNS module as the current official path.

## Core update command

```bash
export DUCKDNS_TOKEN='...'
curl "https://www.duckdns.org/update?domains=SUBNAME&token=$DUCKDNS_TOKEN&ip="
```

For IPv6:

```bash
curl "https://www.duckdns.org/update?domains=SUBNAME&token=$DUCKDNS_TOKEN&ipv6=$IPV6"
```

Example `.env` file:

```bash
DUCKDNS_TOKEN=replace_me
DUCKDNS_SUBDOMAIN=mybox
```

## Optional automation

Run the updater every few minutes with cron or a timer. Keep the token out of logs and shell history.

Windows Task Scheduler quick shape:

```powershell
powershell -File .\update-duckdns.ps1
```

## Validate

```bash
dig +short mybox.duckdns.org A
dig +short mybox.duckdns.org AAAA
```

- Compare resolved records with the intended public IPs.
- If DNS is correct but the service is unreachable, check firewall, port forwarding, CGNAT, or hoster filtering.

## Troubleshooting

- Update says OK but the name still points elsewhere: wait for propagation, then compare DNS again.
- DNS is correct but HTTPS fails: the service or proxy is not listening, or ports 80/443 are blocked.
- Works on LAN only: likely missing router forwarding or the ISP/hoster blocks inbound ports.
- Frequent IP drift: use a timer/cron job and verify the machine can reach DuckDNS reliably.

## Cleanup / rollback

- Remove the timer/cron/task-scheduler job.
- Delete the env file or revoke access to it if the token is no longer needed.
- If abandoning the hostname, remove the DNS record from DuckDNS and any related proxy config.

## Output

Return:

- DuckDNS hostname
- update command or timer command
- current public IP
- verification command
- any HTTPS handoff note for Caddy
- troubleshooting hint if validation fails

## Notes

- DuckDNS uses the subname, not the full `.duckdns.org` suffix, in its update API.
- Do not log or paste the token into public configs or process arguments.
- Prefer HTTPS for the update call.

## Bundled helper

Use `scripts/update_duckdns.sh` for the stable update path when you want one loud, repeatable command.

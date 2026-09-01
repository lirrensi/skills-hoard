---
name: exposure-check
description: Diagnose whether a self-hosted service is reachable the way the user thinks it is, including local bind issues, firewall/NAT trouble, DNS mismatch, TLS fingerprint mismatch, blocked ports, and hoster restrictions. Use whenever the user says debug exposure, why is my site unreachable, check if this port is open, LAN works but public fails, DNS looks wrong, or help me figure out what network mess I created.
---

# exposure-check

Diagnose reachability, routing, DNS, and TLS issues for a self-hosted service.

## Platform

- Linux server flow: first-class
- Windows desktop flow: supported for quick local diagnostics

## What this skill is for

Use this when something is supposed to be reachable but acts cursed:

- works on localhost but not LAN
- works on LAN but not public internet
- DNS resolves but the app still fails
- HTTPS warns or the fingerprint changed
- router, firewall, hoster, VPN, or bind-address choices may be sabotaging things

## Gather first

- intended URL, hostname, IP, and port
- whether the target should be localhost-only, LAN, VPN-only, or public internet
- whether a reverse proxy is involved
- whether the service uses HTTP, HTTPS, or a custom TCP/UDP port

## Workflow

1. Identify the target service, port, and intended audience.
2. Check whether the process is actually listening on the expected interface.
3. Check local firewall and host firewall rules.
4. Check DNS resolution if a hostname is involved.
5. Check TLS identity or fingerprint if HTTPS is involved.
6. Separate localhost-only failure, LAN failure, and public-internet failure.
7. Return the most likely break point and the next fix.

## Linux checks

Listening sockets:

```bash
ss -ltnp
ss -lunp
```

HTTP/HTTPS probe:

```bash
curl -I http://127.0.0.1:PORT/
curl -kI https://127.0.0.1:PORT/
```

DNS:

```bash
dig +short HOSTNAME A
dig +short HOSTNAME AAAA
```

TLS fingerprint:

```bash
echo | openssl s_client -connect HOST:PORT -servername HOST 2>/dev/null | openssl x509 -noout -fingerprint -sha256
```

## Windows checks

Listening sockets:

```powershell
Get-NetTCPConnection -State Listen
Get-NetUDPEndpoint
```

HTTP/HTTPS probe:

```powershell
Invoke-WebRequest "http://127.0.0.1:PORT/" -Method Head
Invoke-WebRequest "https://127.0.0.1:PORT/" -Method Head -SkipCertificateCheck
```

DNS:

```powershell
Resolve-DnsName HOSTNAME
```

Port reachability:

```powershell
Test-NetConnection HOSTNAME -Port PORT
```

## Decision tree

- Not listening at all: the service never started, crashed, or bound to the wrong port.
- Listening only on `127.0.0.1`: localhost works, LAN/public fails by design.
- Listening on `0.0.0.0` or LAN IP, but LAN fails: local firewall, Wi-Fi isolation, VLAN, or client-side routing issue.
- LAN works, public fails: router forwarding, CGNAT, ISP/hoster filtering, or cloud security-group issue.
- DNS wrong: the name points elsewhere or propagation is incomplete.
- HTTPS mismatch: cert SAN or fingerprint does not match the host the client used.
- Reverse proxy works, backend path fails: likely subpath/base-path misconfiguration upstream.

## Validate

- Test from the host itself.
- Test from another LAN device.
- Test from an actually external network when public access is intended.
- Compare all three results before claiming the internet is broken.

## Troubleshooting cues

- If `curl` works locally but not from LAN, stop staring at DNS and check bind/firewall first.
- If DNS is correct but the port is closed, the problem is exposure, not naming.
- If the fingerprint changed, assume cert rotation until proven otherwise.
- If only mobile fails, suspect captive portal, mobile network filtering, or certificate trust UX.

## Output

Return:

- what is listening and where
- whether DNS matches the intended target
- whether TLS identity matches
- whether localhost, LAN, and public tests each passed
- most likely failure point
- next recommended fix

## Notes

- This is a diagnostic skill, not a deployment skill.
- Prefer evidence over guessing; separate bind, firewall, DNS, and TLS as different layers.
- Public testing may require a truly external vantage point; localhost and LAN are not enough.

---
name: ipfs-host
description: >
  Host a directory or static site on Kubo-backed IPFS, keep the daemon running, and return a
  shareable CID plus optional IPNS handoff. Use whenever the user says host on IPFS, deploy to
  IPFS, give me a CID, keep this IPFS content alive, publish via IPNS, or wants a self-hosted IPFS
  workflow without relying on pinning services.
---

# ipfs-host

Deploy a local directory to Kubo IPFS, keep it pinned, and return gateway links.

## Platform

- Linux server flow: first-class, with optional `systemd`
- Windows desktop flow: supported for personal workstation publishing

---

## Assumptions

- Content is a local directory or static build output
- User can run Kubo locally and keep the daemon alive long enough to publish and serve
- `systemd` steps apply only when a Linux service is actually being used

---

## Quick scout

Linux:

```bash
command -v ipfs
ipfs --version
systemctl status ipfs 2>/dev/null || true
```

Windows PowerShell:

```powershell
Get-Command ipfs -ErrorAction SilentlyContinue
ipfs --version
```

## Workflow

1. Install or verify Kubo.
2. Initialize the node with the server profile if needed.
3. Keep the daemon running as a service.
4. Add the directory with wrap-with-directory enabled.
5. Pin the CID and return gateway links.
6. If the user wants a mutable name, offer IPNS.
7. Validate local gateway access and explain what to do if public gateways lag.

## Initialize and run

```bash
ipfs init --profile server
ipfs daemon
```

Windows desktop quick path:

```powershell
ipfs init
ipfs daemon
```

Leave that terminal running, or use a Windows service manager if the user wants persistence on their own machine.

---

## Persistent service

Use a system service only if one exists already or you create one explicitly. Do not assume `ipfs.service` magically came with every install.

```bash
sudo systemctl enable ipfs
sudo systemctl restart ipfs
```

If the service unit is missing, either create one intentionally or run the daemon manually for short-lived publishing.

## Add and pin content

```bash
CID=$(ipfs add -r -Q --cid-version 1 --wrap-with-directory "dist")
ipfs pin add "$CID"
```

## Optional mutable name

```bash
ipfs name publish "/ipfs/$CID"
```

---

## Return links

Return:

- CID
- local gateway link
- at least one public gateway link if appropriate
- pin status
- daemon status
- optional IPNS name and resolve hint
- troubleshooting hint if a gateway does not resolve yet

## Notes

- `ipfs add` already pins by default; pin again explicitly if you want the intent clear.
- Use `--wrap-with-directory` so `index.html` resolves correctly.
- Treat gateways as retrieval surfaces; the CID is the real content address.
- Do not expose the RPC API publicly.
- Public gateways can lag or rate-limit; verify the local gateway first.

## Useful checks

```bash
ipfs pin ls --type=recursive | grep "$CID"
ipfs repo stat
ipfs swarm peers | head -5
```

## Update note

New content means a new CID. Add the new directory, pin it, and publish a new IPNS name only if the user needs mutability.

## Validate

```bash
curl -I "http://127.0.0.1:8080/ipfs/$CID/"
ipfs pin ls --type=recursive | grep "$CID"
```

- Confirm the local gateway works before blaming public gateways.
- If using IPNS, resolve it after publish and expect propagation delay.

## Troubleshooting

- `systemctl enable ipfs` fails: the service unit does not exist; create one or run manually.
- Local gateway fails: the daemon is not running or the API/gateway ports were changed.
- Public gateway 404/timeout: give it a moment, keep the node online, or try another gateway.
- Content updates but link stays old: that is normal; new content means a new CID unless the user switches to IPNS.

## Cleanup / rollback

- Stop the daemon if this was only a one-off publish.
- Unpin the CID if the user intentionally no longer wants to retain it locally.
- Remove any service unit only if it was created just for this workflow.

## Bundled helper

Use `scripts/add_pin_publish.sh` for the stable add/pin/print flow, and leave install/service decisions in the main workflow.

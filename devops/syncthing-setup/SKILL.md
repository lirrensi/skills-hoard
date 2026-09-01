---
name: syncthing-setup
description: Set up Syncthing for server, local machine, phone, and agent collaboration with secure defaults. Use whenever the user says Syncthing, share folders, sync server and laptop, phone-friendly workspace, headless sync, remote GUI, SSH tunnel, or needs a private file collaboration channel that is richer than chat.
---

# syncthing-agent-collab

Set up Syncthing so a server, a workstation, phones, and an agent can share folders safely.

## Platform

- Linux server flow: first-class, with `systemd`
- Windows desktop flow: explicitly supported for personal workstation use

## Quick scout

Check only the pieces relevant to sync and access:

Linux:

```bash
command -v syncthing
systemctl status syncthing@${USER}.service 2>/dev/null || true
```

Windows PowerShell:

```powershell
Get-Command syncthing -ErrorAction SilentlyContinue
```

## Workflow

1. Keep the GUI local by default.
2. Use SSH tunneling for remote GUI access unless the user explicitly wants public HTTPS.
3. Pair devices with their device IDs.
4. Choose the right folder role: sendreceive, sendonly, receiveonly, or receiveencrypted.
5. For phones, make acceptance easy and avoid exposing more than needed.
6. Return device IDs, folder paths, and the exact access method.
7. Validate that devices are actually connected, not merely configured.

## Connectivity modes

- LAN-only: easiest path; devices only need local reachability and firewall allowance.
- Internet via relays/discovery: lowest-friction remote option when direct inbound ports are not available.
- Direct internet-reachable: best performance, but requires firewall/NAT/hoster rules to allow Syncthing traffic.

## Secure defaults

- Device IDs are public keys, not secrets.
- Do not expose the GUI on `0.0.0.0:8384` without auth and firewalling.
- Syncthing is not a backup tool.

## Useful commands

Start as a service:

```bash
systemctl enable syncthing@myuser.service
```

SSH tunnel to the GUI:

```bash
ssh -L 9999:localhost:8384 user@server
```

Set GUI credentials:

```bash
syncthing generate --gui-user=admin --gui-password=STRONGPASSWORD
```

Windows desktop quick path:

```powershell
syncthing.exe
```

- Open the local GUI, usually on `http://127.0.0.1:8384/`.
- Use Windows Firewall prompts carefully; allow private-network access when intended.
- For a persistent desktop setup, add Syncthing to startup or install it with its Windows service wrapper if desired.

## Folder roles

- `sendreceive` for normal shared workspaces
- `sendonly` when the server is the source of truth
- `receiveonly` when the device is a mirror
- `receiveencrypted` for an untrusted endpoint with encryption on the trusted side

## Output

Return:

- device IDs
- folder IDs and paths
- service or SSH tunnel instructions
- GUI access method
- folder role recommendation
- any mobile-specific onboarding note
- validation result or next diagnostic step

## Notes

- Prefer SSH tunneling over public GUI exposure.
- Keep folder structure simple; one clear workspace beats nested sync spaghetti.
- If the user wants phone collaboration, optimize for fast acceptance and easy file drop-in.
- Device pairing alone is not success; check that devices show as connected and folder state is up to date.

## Validate

- Confirm each device appears as connected in the GUI.
- Confirm at least one test file syncs in the expected direction.
- For remote peers, confirm whether the connection is direct or relay-backed.

## Troubleshooting

- Devices added but never connect: check firewall, NAT, discovery, relay availability, or hoster restrictions.
- GUI unreachable remotely: use SSH tunneling first; do not start by exposing `0.0.0.0:8384` publicly.
- Folder stays out of sync: check path permissions, disk space, ignore patterns, or conflicting folder types.
- Phone setup is flaky: keep the folder count small and acceptance flow simple.

## Cleanup / rollback

- Remove the shared folder from both sides if the collaboration is temporary.
- Remove the device from trusted peers when access should end.
- Disable the service or startup entry if Syncthing should no longer stay resident.

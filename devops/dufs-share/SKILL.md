---
name: dufs-share
description: Share any server folder with dufs, including mobile-friendly upload/download links, auth, search, archive downloads, and standalone TLS when there is no domain or proxy. Use whenever the user says dufs, share a folder, serve a directory, file share, upload/download links, folder zip download, LAN share, or wants a quick folder server right now.
---

# dufs-share

Expose a folder with dufs and return a link the user can open immediately.

## Platform

- Primary target: Linux/macOS shell with `bash`
- Also works on Windows when `dufs` is installed and launched from PowerShell, but the bundled helper is bash-first

## Quick scout

Check only the folder server pieces you actually need:

```bash
command -v dufs
command -v openssl
```

## Workflow

1. Decide whether the share is read-only, authenticated writable, or temporary.
2. Start dufs directly on the folder.
3. If no proxy/domain exists, generate a self-signed cert and run dufs with TLS.
4. If a proxy exists, optionally register a route there.
5. Return the URL plus any auth or fingerprint detail the recipient needs.
6. Validate the URL locally and from the intended client side.
7. Tell the user how to shut it down or rotate the cert if needed.

## Common modes

Read-only:

```bash
dufs /share
```

Authenticated upload/search/archive:

```bash
dufs /share --allow-upload --allow-archive --allow-search -a user:pass@/:rw
```

Broader write access, if the operator intentionally wants it, must be enabled explicitly with the matching dufs allow flags for that version. Do not call a share "read-write" unless the chosen flags truly allow the mutations the user expects.

Standalone TLS:

```bash
dufs /share --tls-cert cert.pem --tls-key key.pem -p 8443
```

Windows PowerShell quick start:

```powershell
dufs "D:\share" --tls-cert cert.pem --tls-key key.pem -p 8443
```

## Validate

Local:

```bash
curl -I http://127.0.0.1:5000/
curl -kI https://127.0.0.1:8443/
```

Remote/LAN:

- Confirm the advertised host is the address the recipient can actually reach.
- If using a self-signed cert, verify the browser shows the same SHA-256 fingerprint returned by the helper.
- Test one upload/download action when write access is intended.

## Troubleshooting

- Wrong URL returned: set an explicit advertised host instead of relying on `127.0.0.1`.
- Works locally but not from phone/LAN: check host firewall, router isolation, VPN, or bind address.
- Browser certificate warning: expected for self-signed mode; compare the fingerprint before trusting.
- Upload button missing: `--allow-upload` is required even when auth is configured.
- Reverse-proxy path weirdness: some backends need a path prefix stripped upstream; prefer dedicated hostnames or clean subpaths behind Caddy.

## Cleanup / rollback

- Stop the dufs process.
- Remove any temporary cert/key created just for this share.
- Remove any temporary reverse-proxy route that was added.
- If credentials were generated for a one-off share, discard them after the session.

## Useful URL forms

- `?zip` for folder download
- `?json` for JSON listings
- `?hash` for file hash
- `?q=...` for search

## Output

Return:

- share URL
- whether it is read-only or read-write
- auth, if any
- TLS fingerprint, if using a self-signed cert
- any browser/mobile note the user should know
- shutdown or cleanup note

## Notes

- Keep the skill self-contained; do not assume another proxy or domain exists.
- Dufs is usable on phones, but the stock UI is not magic on tiny screens.
- Upload requires `--allow-upload` even when auth is configured.
- Distinguish bind address from advertised URL; they are often not the same thing.

## Bundled helper

Use `scripts/run_dufs_share.sh` for the repeatable launch path; keep unusual topology choices in the skill steps.

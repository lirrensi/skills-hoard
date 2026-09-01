---
name: selfsigned-proxy
description: Build a no-domain reverse proxy with one self-signed certificate, one SHA-256 fingerprint, and multiple local services behind Caddy. Use whenever the user says no domain, self-signed cert, fingerprint pinning, Caddy admin API, one cert many services, or wants a stable server identity without ACME.
---

# selfsigned-proxy

Create one self-signed certificate, print its fingerprint, and serve multiple backends through Caddy.

## Platform

- Primary target: Linux/macOS shell with `bash`
- Caddy itself also works on Windows, but the bundled helper is bash-first

## Quick scout

Check only the proxy and cert tools:

```bash
command -v openssl
command -v caddy
```

## Workflow

1. Generate a leaf cert with SANs for the actual host/IP.
2. Print the SHA-256 fingerprint as the server identity.
3. Start Caddy with that cert/key or add routes through the local admin API.
4. Keep the admin API local only.
5. Return one URL and one fingerprint.
6. Validate both the certificate identity and backend reachability.
7. Tell the user how to remove routes or rotate the cert.

## Generate cert

```bash
openssl req -x509 -newkey rsa:2048 -noenc \
  -keyout key.pem -out cert.pem -days 365 \
  -subj "/CN=proxy.local" \
  -addext "subjectAltName=IP:127.0.0.1,DNS:localhost"
```

## Print identity

```bash
openssl x509 -in cert.pem -noout -fingerprint -sha256
```

## Simple Caddyfile shape

```caddyfile
:8443 {
	tls cert.pem key.pem

	handle_path /files/* {
		reverse_proxy 127.0.0.1:8080
	}

	handle_path /app/* {
		reverse_proxy 127.0.0.1:3000
	}
}
```

Use `handle_path` when the upstream expects requests at `/`. If the upstream is path-aware already, plain `handle` may be fine. Say which case you are using instead of assuming subpaths will just work by magic.

## Validate

```bash
curl -kI https://127.0.0.1:8443/
openssl x509 -in cert.pem -noout -fingerprint -sha256
```

- Open one routed path per backend and confirm assets/redirects resolve correctly.
- If clients connect by IP, confirm the cert SAN includes that IP.
- If using the admin API, confirm it only listens on localhost or another trusted local socket.

## Troubleshooting

- Browser says hostname mismatch: regenerate the cert with the real DNS name or IP in SAN.
- Root page works but `/app/` is broken: likely a subpath/base-path issue; use `handle_path` or configure the upstream base URL.
- Admin API refused: verify Caddy admin is enabled locally and not firewalled off from localhost.
- Fingerprint changed unexpectedly: the cert was rotated or replaced; recipients must re-verify.

## Cleanup / rollback

- Remove the route from Caddy or restore the previous config snapshot.
- Stop Caddy if this proxy was temporary.
- Securely keep or intentionally destroy `cert.pem` and `key.pem`; recreating them changes the fingerprint.

## Output

Return:

- HTTPS URL
- SHA-256 fingerprint
- local listen address
- route list
- note that the fingerprint changes if the cert is regenerated
- cleanup note if the setup is temporary

## Notes

- Do not expose Caddy's admin API to untrusted networks.
- The fingerprint is for that exact certificate only.
- This skill is for no-domain HTTPS, not DNS or ACME setup.
- Prefer explicit route behavior over ambiguous subpath forwarding.

## Bundled helper

Use `scripts/generate_selfsigned_cert.sh` for the deterministic cert/fingerprint step, then keep route wiring in the main instructions.

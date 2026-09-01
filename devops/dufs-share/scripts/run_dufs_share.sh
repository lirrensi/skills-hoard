#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'EOF'
Usage: run_dufs_share.sh <folder> [port] [bind-address]

Starts dufs with optional TLS from DUFS_TLS_CERT and DUFS_TLS_KEY.
If DUFS_SELF_SIGNED_HOST is set and TLS files are missing, a temporary cert is created.
Set DUFS_PUBLIC_HOST to control the advertised URL returned to the caller.
EOF
}

if [[ $# -lt 1 ]]; then
	usage
	exit 2
fi

FOLDER="$1"
PORT="${2:-${DUFS_PORT:-5000}}"
BIND_ADDRESS="${3:-${DUFS_BIND:-0.0.0.0}}"
PUBLIC_HOST="${DUFS_PUBLIC_HOST:-}"
TLS_CERT="${DUFS_TLS_CERT:-}"
TLS_KEY="${DUFS_TLS_KEY:-}"

if [[ ! -d "$FOLDER" ]]; then
	echo "Folder not found: $FOLDER" >&2
	exit 1
fi

if [[ -z "$PUBLIC_HOST" ]]; then
	if [[ "$BIND_ADDRESS" == "127.0.0.1" || "$BIND_ADDRESS" == "localhost" ]]; then
		PUBLIC_HOST="127.0.0.1"
	else
		PUBLIC_HOST="$BIND_ADDRESS"
		echo "warning=DUFS_PUBLIC_HOST not set; advertising bind address ${BIND_ADDRESS}. Override for LAN/public sharing." >&2
	fi
fi

TEMP_DIR=""
if [[ -z "$TLS_CERT" || -z "$TLS_KEY" ]]; then
	if [[ -n "${DUFS_SELF_SIGNED_HOST:-}" ]]; then
		TEMP_DIR="$(mktemp -d)"
		SAN_ENTRY="${DUFS_SELF_SIGNED_HOST}"
		if [[ "$SAN_ENTRY" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || [[ "$SAN_ENTRY" == *:* ]]; then
			SAN_ENTRY="IP:${SAN_ENTRY}"
		else
			SAN_ENTRY="DNS:${SAN_ENTRY}"
		fi
		openssl req -x509 -newkey rsa:2048 -noenc \
			-keyout "$TEMP_DIR/key.pem" -out "$TEMP_DIR/cert.pem" \
			-days 365 \
			-subj "/CN=${DUFS_SELF_SIGNED_HOST}" \
			-addext "subjectAltName=${SAN_ENTRY},IP:127.0.0.1"
		TLS_CERT="$TEMP_DIR/cert.pem"
		TLS_KEY="$TEMP_DIR/key.pem"
		TLS_FINGERPRINT="$(openssl x509 -in "$TLS_CERT" -noout -fingerprint -sha256 | sed 's/^.*=//')"
		echo "tls_fingerprint=$TLS_FINGERPRINT"
	else
		echo "Running without TLS certs; set DUFS_TLS_CERT/DUFS_TLS_KEY or DUFS_SELF_SIGNED_HOST." >&2
	fi
fi

echo "folder=$FOLDER"
echo "bind_address=$BIND_ADDRESS"
echo "advertised_host=$PUBLIC_HOST"
echo "url=http${TLS_CERT:+s}://${PUBLIC_HOST}:${PORT}/"

ARGS=("$FOLDER" -b "$BIND_ADDRESS" -p "$PORT")
if [[ -n "$TLS_CERT" && -n "$TLS_KEY" ]]; then
	ARGS+=(--tls-cert "$TLS_CERT" --tls-key "$TLS_KEY")
fi

exec dufs "${ARGS[@]}"

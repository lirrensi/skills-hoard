#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'EOF'
Usage: generate_selfsigned_cert.sh <common-name> [output-dir] [SAN...]

Creates cert.pem and key.pem, then prints the SHA-256 fingerprint.
SAN arguments may be hostnames or IPs. Hostnames become DNS: entries, IPs become IP: entries.
EOF
}

if [[ $# -lt 1 ]]; then
	usage
	exit 2
fi

COMMON_NAME="$1"
OUTPUT_DIR="${2:-.}"

if [[ $# -ge 2 ]]; then
	shift 2
else
	shift 1
fi

mkdir -p "$OUTPUT_DIR"

if [[ "$COMMON_NAME" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || [[ "$COMMON_NAME" == *:* ]]; then
	SAN_ENTRIES=("IP:${COMMON_NAME}")
else
	SAN_ENTRIES=("DNS:${COMMON_NAME}")
fi

for item in "$@"; do
	if [[ "$item" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || [[ "$item" == *:* ]]; then
		SAN_ENTRIES+=("IP:${item}")
	else
		SAN_ENTRIES+=("DNS:${item}")
	fi
done

CERT_PATH="$OUTPUT_DIR/cert.pem"
KEY_PATH="$OUTPUT_DIR/key.pem"
SAN_VALUE="$(IFS=,; echo "${SAN_ENTRIES[*]}")"

openssl req -x509 -newkey rsa:2048 -noenc \
	-keyout "$KEY_PATH" \
	-out "$CERT_PATH" \
	-days 365 \
	-subj "/CN=${COMMON_NAME}" \
	-addext "subjectAltName=${SAN_VALUE}"

echo "cert=$CERT_PATH"
echo "key=$KEY_PATH"
openssl x509 -in "$CERT_PATH" -noout -fingerprint -sha256

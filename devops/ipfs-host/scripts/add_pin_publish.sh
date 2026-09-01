#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'EOF'
Usage: add_pin_publish.sh <directory> [--ipns]

Adds a directory to IPFS with wrap-with-directory, pins the CID, and prints the links.
Pass --ipns to also publish the CID under the current IPNS identity.
EOF
}

if [[ $# -lt 1 ]]; then
	usage
	exit 2
fi

TARGET_DIR="$1"
PUBLISH_IPNS="${2:-}"

if [[ ! -d "$TARGET_DIR" ]]; then
	echo "Directory not found: $TARGET_DIR" >&2
	exit 1
fi

CID="$(ipfs add -r -Q --cid-version 1 --wrap-with-directory "$TARGET_DIR")"
ipfs pin add "$CID" >/dev/null

echo "cid=$CID"
echo "local_gateway=http://127.0.0.1:8080/ipfs/${CID}/"
echo "public_gateway=https://ipfs.io/ipfs/${CID}/"
echo "pin=added"
echo "note=verify the local gateway first; public gateways can lag or rate-limit"

if [[ "$PUBLISH_IPNS" == "--ipns" ]]; then
	IPNS_LINE="$(ipfs name publish "/ipfs/${CID}")"
	echo "ipns=${IPNS_LINE}"
fi

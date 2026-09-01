#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'EOF'
Usage: DUCKDNS_TOKEN=token update_duckdns.sh <subdomain> [ipv6]

Updates DuckDNS over HTTPS, prints the response, and warns if DNS does not yet resolve
to the current public IP. Requires curl; dig is optional for verification.
EOF
}

if [[ $# -lt 1 ]]; then
	usage
	exit 2
fi

SUBDOMAIN="$1"
IPV6="${2:-}"
TOKEN="${DUCKDNS_TOKEN:-}"

if [[ -z "$TOKEN" ]]; then
	echo "DUCKDNS_TOKEN is required in the environment." >&2
	exit 2
fi

PUBLIC_IPV4=""
if [[ -z "$IPV6" ]]; then
	PUBLIC_IPV4="$(curl -fsS4 https://api.ipify.org)"
fi

if [[ -n "$IPV6" ]]; then
	RESP="$(curl -fsS "https://www.duckdns.org/update?domains=${SUBDOMAIN}&token=${TOKEN}&ipv6=${IPV6}")"
else
	RESP="$(curl -fsS "https://www.duckdns.org/update?domains=${SUBDOMAIN}&token=${TOKEN}&ip=${PUBLIC_IPV4}")"
fi

if [[ "$RESP" != OK* ]]; then
	echo "DuckDNS update failed: $RESP" >&2
	exit 1
fi

echo "duckdns_update=$RESP"
echo "hostname=${SUBDOMAIN}.duckdns.org"
if [[ -n "$PUBLIC_IPV4" ]]; then
	echo "public_ipv4=$PUBLIC_IPV4"
fi
if [[ -n "$IPV6" ]]; then
	echo "public_ipv6=$IPV6"
fi

if command -v dig >/dev/null 2>&1; then
	RESOLVED_IPV4="$(dig +short "${SUBDOMAIN}.duckdns.org" A | tr '\n' ' ' | sed 's/ $//')"
	if [[ -n "$RESOLVED_IPV4" ]]; then
		echo "resolved_ipv4=$RESOLVED_IPV4"
		if [[ -n "$PUBLIC_IPV4" && "$RESOLVED_IPV4" != *"$PUBLIC_IPV4"* ]]; then
			echo "warning=DNS A record does not yet match ${PUBLIC_IPV4}" >&2
		fi
	fi
	if [[ -n "$IPV6" ]]; then
		RESOLVED_IPV6="$(dig +short "${SUBDOMAIN}.duckdns.org" AAAA | tr '\n' ' ' | sed 's/ $//')"
		if [[ -n "$RESOLVED_IPV6" ]]; then
			echo "resolved_ipv6=$RESOLVED_IPV6"
			if [[ "$RESOLVED_IPV6" != *"$IPV6"* ]]; then
				echo "warning=DNS AAAA record does not yet match ${IPV6}" >&2
			fi
		fi
	fi
else
	echo "warning=dig not installed; DNS verification skipped" >&2
fi

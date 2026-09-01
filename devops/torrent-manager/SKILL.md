---
name: torrent-manager
description: >
  Manage torrent downloads using qBittorrent (Web API + Python client) or aria2c
  (lightweight CLI). Use this skill when the user wants to download torrents, manage
  seeding, check download status, add/remove trackers, set categories, or automate
  any torrent-related workflow. Supports both full-featured daemon-based management
  (qBittorrent) and fire-and-forget single-shot downloads (aria2c).
---

# Torrent Manager Skill

Two contenders, two philosophies. Pick your fighter:

| Tool | Vibe | Best For |
|------|------|----------|
| **qBittorrent** | Full-service daemon with REST API | Managing many torrents, categories, trackers, automation |
| **aria2c** | Lightweight single-binary wildcard | Quick downloads, HTTP/FTP/BT multifetch, minimal setup |

---

## Platform notes

- Linux server/headless flow: excellent for `qbittorrent-nox`
- Windows desktop flow: fully viable for personal-machine use, especially qBittorrent portable mode or `aria2c`
- Validate connectivity and storage path permissions before assuming the client is broken

---

## Installation Check

### qBittorrent

```powershell
# Check if qbittorrent-nox daemon is available
Get-Command qbittorrent-nox -ErrorAction SilentlyContinue

# Check for the Python API client (preferred for automation)
python -c "import qbittorrentapi" 2>$null
```

**If not installed:**

```powershell
# Windows: Install via Chocolatey
choco install qbittorrent

# Portable mode: extract from installer with 7-Zip, create 'profile' folder
#   (see "Portable Mode" section below — no system install needed!)

# Or grab the Python API client (no daemon needed if connecting to remote)
uv pip install qbittorrent-api
```

> **Note:** qBittorrent runs as a background daemon (`qbittorrent-nox`). The Web API
> listens on port 8080 by default. The Python client can talk to it locally or remotely.
>
> **qBittorrent v5.x support:** The `qbittorrent-api` Python package **v2026.5.1**
> supports qBittorrent **v5.2.0** (Web API v2.15.1, released May 2026) — fully
> compatible. Cookie management, web seeds, API key auth — all covered.

### aria2c

```powershell
# Already installed? Check:
aria2c --version
```

**If not installed:**

```powershell
# Windows (Chocolatey):
choco install aria2

# Or download the binary from:
# https://github.com/aria2/aria2/releases
```

> aria2c is a single binary — no daemon needed for basic use. Just point it at a URI
> and it goes. For persistent management, enable the RPC mode.

---

# qBittorrent — Full-Service Torrent Manager

## Architecture

```
┌─────────────────┐     HTTP API (8080)     ┌──────────────┐
│  qbittorrent-nox │ ◄─────────────────────► │  Your Code   │
│  (daemon process) │                        │  (curl/Python)│
└─────────────────┘                        └──────────────┘
```

qBittorrent's Web API is at `/api/v2/` — all endpoints require authentication (except login).

### Official Documentation

| Resource | Link |
|----------|------|
| Wiki Home | [github.com/qbittorrent/qBittorrent/wiki](https://github.com/qbittorrent/qBittorrent/wiki/) |
| WebUI API (v5.0+) | [WebUI API (qBittorrent 5.0)](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-5.0)) |
| WebUI API (v4.1 - v4.6.x) | [WebUI API (qBittorrent 4.1)](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)) |
| Portable Mode | [How to use portable mode](https://github.com/qbittorrent/qBittorrent/wiki/How-to-use-portable-mode) |
| API Key Auth (≥v5.2.0) | [API Key Authentication](https://github.com/qbittorrent/qBittorrent/wiki/API-Key-Authentication-(%E2%89%A5v5.2.0)) |
| Python Client | [qbittorrent-api on Read the Docs](https://qbittorrent-api.readthedocs.io/) |

### 1. Start the Daemon

```powershell
# Start in background (headless)
qbittorrent-nox --webui-port=8080

# Or run as a background job with the bg skill
bg run "qbittorrent-nox --webui-port=8080"
```

Default WebUI credentials: `admin` / `adminadmin`

> **Note on v4.6.1+:** Newer versions generate a one-time password on first launch
> instead of using `adminadmin`. Check the daemon's console output for the temporary password.

### 🔄 Portable Mode (No System Install)

qBittorrent supports **portable mode** (v4.2.1+) — all configs live in a local `profile`
folder, so no system files are touched and the whole thing runs from a USB stick or
any directory. Works on both Windows and Linux.

**Windows:**
1. Extract `qbittorrent.exe` and `qbittorrent.pdb` from the installer using 7-Zip
   (installers are just self-extracting archives).
2. Create a folder called `profile` next to the EXE.
3. Run `qbittorrent.exe` — it initializes config files inside `profile/` automatically.
4. Move the whole folder anywhere, including to another machine. Configs travel with it.

**Linux:**
```powershell
# Point to a portable config directory
qbittorrent-nox --profile=/path/to/portable/config --relative-fastresume

# Or create a 'profile' folder next to the binary (same as Windows behavior)
```

**How it interacts with the API:** Portable or not — the Web API is identical.
The `--webui-port` flag still works, the Python client doesn't care where configs
live. You can run portable mode on a headless server:
```powershell
bg run "qbittorrent-nox --profile=D:/qbt-portable --webui-port=8080"
```

Multiple instances via `--configuration=NAME`:
```powershell
# Each gets its own config directory (~/.config/qbittorrent_NAME)
qbittorrent-nox --configuration=media
qbittorrent-nox --configuration=games
```

### 2. Authentication (curl)

```bash
# Login and capture the SID cookie
curl -c cookies.txt -X POST \
  --header 'Referer: http://localhost:8080' \
  --data 'username=admin&password=adminadmin' \
  http://localhost:8080/api/v2/auth/login

# Use the cookie for authenticated requests
curl -b cookies.txt http://localhost:8080/api/v2/torrents/info
```

> **Important:** The `Referer` header must match the host:port exactly, otherwise
> qBittorrent drops the request.

### 3. Python Client (Preferred for Automation)

```python
# Quick one-shot:
uv run --with qbittorrent-api python -c "
import qbittorrentapi

qbt = qbittorrentapi.Client(
    host='localhost:8080',
    username='admin',
    password='adminadmin'
)

# This will auto-login and handle cookie refresh
print(f'qBittorrent: {qbt.app.version}')
print(f'Web API: {qbt.app.web_api_version}')

# List all torrents
for t in qbt.torrents_info():
    print(f'{t.hash[-8:]}: {t.name} ({t.state}) [{t.progress*100:.1f}%]')
"
```

Or use it as a managed script:

```python
import qbittorrentapi
from pathlib import Path

conn_info = dict(
    host="localhost",
    port=8080,
    username="admin",
    password="adminadmin",
)

with qbittorrentapi.Client(**conn_info) as qbt:
    # --- Add torrents ---
    # From URL
    qbt.torrents_add(urls="magnet:?xt=urn:btih:...")

    # From local .torrent file
    qbt.torrents_add(torrent_files=[str(Path("file.torrent"))])

    # From torrent file data (bytes)
    qbt.torrents_add(torrent_files=[torrent_bytes])

    # With options
    qbt.torrents_add(
        urls="magnet:...",
        save_path="D:/Downloads",
        category="movies",
        tags=["4k", "hdr"],
        paused=True,
        ratio_limit=2.0,
        seeding_time_limit=1440,  # minutes
    )

    # --- List torrents (with filtering) ---
    all_torrents = qbt.torrents_info()
    downloading = qbt.torrents_info(filter="downloading")
    completed = qbt.torrents_info(filter="completed")
    active = qbt.torrents_info(filter="active")
    inactive = qbt.torrents_info(filter="inactive")
    stalled = qbt.torrents_info(filter="stalled_downloading")
    tagged = qbt.torrents_info(tag="4k")

    # --- Control torrents ---
    hashes = [t.hash for t in all_torrents]

    # Pause / Resume
    qbt.torrents_pause(torrent_hashes=hashes)
    qbt.torrents_resume(torrent_hashes=hashes)

    # Delete (also remove files from disk)
    qbt.torrents_delete(delete_files=True, torrent_hashes=hashes)

    # Recheck
    qbt.torrents_recheck(torrent_hashes=hashes)

    # Reannounce
    qbt.torrents_reannounce(torrent_hashes=hashes)

    # Set force start
    qbt.torrents_set_force_start(torrent_hashes=hashes)

    # --- Trackers ---
    torrent_hash = all_torrents[0].hash

    # Get trackers for a torrent
    trackers = qbt.torrents_trackers(torrent_hash=torrent_hash)
    for tr in trackers:
        print(f'{tr.url}: {tr.status} (seeds: {tr.num_seeds})')

    # Add trackers
    qbt.torrents_add_trackers(
        torrent_hash=torrent_hash,
        urls="udp://tracker.opentrackr.org:1337\nudp://tracker.coppersurfer.tk:6969"
    )

    # Edit tracker
    qbt.torrents_edit_tracker(
        torrent_hash=torrent_hash,
        orig_url="http://old-tracker.com/announce",
        new_url="http://new-tracker.com/announce"
    )

    # Remove trackers
    qbt.torrents_remove_trackers(
        torrent_hash=torrent_hash,
        urls="http://dead-tracker.com/announce"
    )

    # --- Categories ---
    # List all categories
    cats = qbt.torrents_categories()

    # Create category
    qbt.torrents_create_category(category="movies", save_path="D:/Torrents/Movies")

    # Edit category
    qbt.torrents_edit_category(category="movies", save_path="D:/Media/Movies")

    # Remove categories
    qbt.torrents_remove_categories(categories="movies")

    # Set torrent category
    qbt.torrents_set_category(torrent_hashes=hashes, category="movies")

    # --- Tags ---
    qbt.torrents_create_tags(tags="4k,hdr,remux")
    qbt.torrents_add_tags(torrent_hashes=hashes, tags="4k")
    qbt.torrents_remove_tags(torrent_hashes=hashes, tags="4k")
    qbt.torrents_delete_tags(tags="old-tag")

    # --- Speed Limits ---
    # Per-torrent (bytes/sec)
    qbt.torrents_set_download_limit(torrent_hashes=hashes, limit=0)     # 0 = unlimited
    qbt.torrents_set_upload_limit(torrent_hashes=hashes, limit=102400)  # 100 KiB/s

    # Global
    qbt.transfer_set_download_limit(limit=0)
    qbt.transfer_set_upload_limit(limit=512000)  # 500 KiB/s

    # Toggle alt speed limits
    qbt.transfer_toggle_speed_limits_mode()

    # --- Share Limits ---
    qbt.torrents_set_share_limits(
        torrent_hashes=hashes,
        ratio_limit=2.0,      # stop seeding at ratio 2.0
        seeding_time_limit=1440  # or after 1440 minutes
    )

    # --- Priority ---
    qbt.torrents_increase_priority(torrent_hashes=hashes)
    qbt.torrents_decrease_priority(torrent_hashes=hashes)
    qbt.torrents_top_priority(torrent_hashes=hashes)
    qbt.torrents_bottom_priority(torrent_hashes=hashes)

    # --- Files within torrent ---
    files = qbt.torrents_files(torrent_hash=torrent_hash)
    for f in files:
        print(f'{f.index}: {f.name} ({f.size} bytes, priority={f.priority})')

    # Set file priority (0=skip, 1=normal, 6=high, 7=max)
    qbt.torrents_file_priority(
        torrent_hash=torrent_hash,
        file_ids=[0, 1],      # file indices
        priority=0              # skip these files
    )

    # --- Rename ---
    qbt.torrents_rename(torrent_hash=torrent_hash, new_name="New Name")
    qbt.torrents_rename_file(torrent_hash=torrent_hash, old_path="ep1.mkv", new_path="Episode_1.mkv")
    qbt.torrents_rename_folder(torrent_hash=torrent_hash, old_path="Season1", new_path="Season_01")

    # --- Torrent Properties ---
    props = qbt.torrents_properties(torrent_hash=torrent_hash)
    print(f'Save path: {props.save_path}')
    print(f'Total size: {props.total_size}')
    print(f'Added on: {props.addition_date}')
    print(f'Downloaded: {props.total_downloaded}')
    print(f'Ratio: {props.ratio}')
    print(f'Seeding time: {props.seeding_time}s')
```

### 🆕 qBittorrent v5.x — What Changed

qBittorrent **v5.0+** uses Web API **v2.9.3+**. The latest release **v5.2.0**
(May 3, 2026) ships Web API **v2.15.1**. Most v4.x API endpoints remain the same,
but there are additions and removals:

| Change | Version | Detail |
|--------|---------|--------|
| `reannounce` field in `/torrents/info` | API v2.9.3 | Each torrent now reports `reannounce` timestamp |
| Cookie management APIs | API v2.11.3 | New `app/cookies` (GET) and `app/setCookies` (POST) |
| `cookie` field removed from `/torrents/add` | API v2.11.3 | Use the cookie management APIs instead |
| API Key Authentication | ≥v5.2.0 | New auth method — generate API keys for script access instead of sharing passwords. See [wiki](https://github.com/qbittorrent/qBittorrent/wiki/API-Key-Authentication-(%E2%89%A5v5.2.0)). |
| WebSeed management endpoints | Added | `torrents/addWebSeeds`, `torrents/editWebSeed`, `torrents/removeWebSeeds` |
| Tracker status additions | v5.2.0 | New tracker status values |

**Python client compatibility:** The `qbittorrent-api` package **v2026.5.1** supports
qBittorrent **v5.2.0** (Web API v2.15.1) — so yes, the Python client fully covers
v5.x including the new cookie and web seed endpoints. Install/upgrade with:
```powershell
uv pip install --upgrade qbittorrent-api
```

### 4. curl Cheat Sheet (if Python isn't available)

```bash
# Variables
SID="SID=your_cookie_here"
BASE="http://localhost:8080/api/v2"

# Login
SID=$(curl -s -c - -X POST \
  --header 'Referer: http://localhost:8080' \
  --data 'username=admin&password=adminadmin' \
  "$BASE/auth/login" | grep SID | awk '{print $NF}')

# List torrents
curl -s --cookie "$SID" "$BASE/torrents/info"

# Filter by state
curl -s --cookie "$SID" "$BASE/torrents/info?filter=downloading"

# Add torrent from URL (magnet or http)
curl -s -X POST --cookie "$SID" \
  --header 'Referer: http://localhost:8080' \
  --data 'urls=magnet:?...' \
  "$BASE/torrents/add"

# Add torrent with category & save path
curl -s -X POST --cookie "$SID" \
  --header 'Referer: http://localhost:8080' \
  -F 'torrents=@file.torrent' \
  -F 'category=movies' \
  -F 'savepath=D:/Downloads' \
  -F 'paused=false' \
  "$BASE/torrents/add"

# Pause all
curl -s -X POST --cookie "$SID" \
  --header 'Referer: http://localhost:8080' \
  --data 'hashes=all' \
  "$BASE/torrents/pause"

# Resume all
curl -s -X POST --cookie "$SID" \
  --header 'Referer: http://localhost:8080' \
  --data 'hashes=all' \
  "$BASE/torrents/resume"

# Delete with files
curl -s -X POST --cookie "$SID" \
  --header 'Referer: http://localhost:8080' \
  --data 'hashes=all&deleteFiles=true' \
  "$BASE/torrents/delete"

# Get global transfer info (speed, etc.)
curl -s --cookie "$SID" "$BASE/transfer/info"

# Set global download limit (bytes/sec)
curl -s -X POST --cookie "$SID" \
  --header 'Referer: http://localhost:8080' \
  --data 'limit=1048576' \
  "$BASE/transfer/setDownloadLimit"

# Get application preferences
curl -s --cookie "$SID" "$BASE/app/preferences"

# Set preference (e.g., enable DHT)
curl -s -X POST --cookie "$SID" \
  --header 'Referer: http://localhost:8080' \
  --data 'json={"dht":true}' \
  "$BASE/app/setPreferences"
```

### 5. Key qBittorrent API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v2/auth/login` | Login, get SID cookie |
| POST | `/api/v2/auth/logout` | Logout |
| GET | `/api/v2/app/version` | App version string |
| GET | `/api/v2/app/webapiVersion` | API version string |
| GET | `/api/v2/app/buildInfo` | Build info (Qt, libtorrent, etc.) |
| POST | `/api/v2/app/shutdown` | Stop the daemon |
| GET | `/api/v2/app/preferences` | Get all preferences |
| POST | `/api/v2/app/setPreferences` | Set preferences (JSON) |
| GET | `/api/v2/torrents/info` | List torrents (with filter/sort/tag) |
| POST | `/api/v2/torrents/add` | Add torrent (URL, file, or magnet) |
| POST | `/api/v2/torrents/pause` | Pause torrent(s) |
| POST | `/api/v2/torrents/resume` | Resume torrent(s) |
| POST | `/api/v2/torrents/delete` | Delete torrent(s) (+ files) |
| POST | `/api/v2/torrents/recheck` | Recheck torrent(s) |
| POST | `/api/v2/torrents/reannounce` | Reannounce to trackers |
| POST | `/api/v2/torrents/setCategory` | Set torrent category |
| POST | `/api/v2/torrents/addTrackers` | Add trackers to torrent |
| POST | `/api/v2/torrents/editTracker` | Replace tracker URL |
| POST | `/api/v2/torrents/removeTrackers` | Remove trackers |
| GET | `/api/v2/torrents/trackers` | List torrent trackers |
| GET | `/api/v2/torrents/files` | List files in torrent |
| POST | `/api/v2/torrents/filePrio` | Set file priority |
| POST | `/api/v2/torrents/setShareLimits` | Set ratio/time share limits |
| POST | `/api/v2/torrents/setLocation` | Change save path |
| POST | `/api/v2/torrents/rename` | Rename torrent |
| POST | `/api/v2/torrents/renameFile` | Rename file within torrent |
| POST | `/api/v2/torrents/addTags` | Add tags |
| POST | `/api/v2/torrents/removeTags` | Remove tags |
| GET | `/api/v2/torrents/categories` | List all categories |
| POST | `/api/v2/torrents/createCategory` | Create category |
| POST | `/api/v2/torrents/removeCategories` | Remove categories |
| POST | `/api/v2/torrents/setDownloadLimit` | Per-torrent DL limit |
| POST | `/api/v2/torrents/setUploadLimit` | Per-torrent UL limit |
| POST | `/api/v2/torrents/setForceStart` | Force start toggle |
| POST | `/api/v2/torrents/setSuperSeeding` | Super seeding toggle |
| POST | `/api/v2/torrents/toggleSequentialDownload` | Sequential download |
| POST | `/api/v2/torrents/setFirstLastPiecePrio` | First/last piece priority |
| GET | `/api/v2/transfer/info` | Global transfer stats |
| POST | `/api/v2/transfer/setDownloadLimit` | Global DL limit |
| POST | `/api/v2/transfer/setUploadLimit` | Global UL limit |
| POST | `/api/v2/transfer/toggleSpeedLimitsMode` | Toggle alt speed |
| GET | `/api/v2/app/cookies` | List cookies (v2.11.3+) |
| POST | `/api/v2/app/setCookies` | Set cookies (v2.11.3+) |
| POST | `/api/v2/torrents/addWebSeeds` | Add web seeds to torrent |
| POST | `/api/v2/torrents/editWebSeed` | Edit web seed URL |
| DELETE | `/api/v2/torrents/removeWebSeeds` | Remove web seeds |
| GET | `/api/v2/sync/maindata` | Sync main data (polling) |
| GET | `/api/v2/log/main` | Get event log |

### 6. Torrent State Values

| State | Meaning |
|-------|---------|
| `downloading` | Actively downloading |
| `uploading` | Seeding (download complete) |
| `pausedDL` | Paused while downloading |
| `pausedUP` | Paused while seeding |
| `queuedDL` | Queued for download |
| `queuedUP` | Queued for seeding |
| `checkingDL` | Checking/resuming download |
| `checkingUP` | Checking/resuming seed |
| `stalledDL` | No peers, waiting to download |
| `stalledUP` | No leechers, idle seeding |
| `metaDL` | Fetching magnet metadata |
| `missingFiles` | Files not found |
| `error` | Error state |
| `moving` | Moving files to new location |

### 7. Complete PowerShell Automation Example

```powershell
# qbt.ps1 — one-liner status check
$cred = @{ host = 'localhost:8080'; username = 'admin'; password = 'adminadmin' }

uv run --with qbittorrent-api python -c @"
import qbittorrentapi, json
qbt = qbittorrentapi.Client(**$(@{ $cred | ConvertTo-Json -Compress }))
for t in qbt.torrents_info():
    print(f'{t.hash[-8:]} | {t.name[:40]:40s} | {t.state:15s} | {t.progress*100:5.1f}%')
"@
```

---

# aria2c — The Lightweight Torrent Sniper

## Philosophy

One binary, zero config. `aria2c torrent.torrent` — done. Want HTTP too? Same command.
No daemon needed for one-shots. Want management? Enable RPC mode.

### 1. Basic Torrent Downloads

```powershell
# Download from a .torrent file
aria2c ubuntu-24.04-desktop.torrent

# Download from magnet link
aria2c "magnet:?xt=urn:btih:..."

# Download from trackerless magnet (DHT)
aria2c --enable-dht --dht-listen-port=6881 "magnet:?xt=urn:btih:..."

# Download a .torrent from a URL (auto-follows if .torrent)
aria2c "https://example.com/file.torrent"

# Specify download directory
aria2c -d "D:/Downloads" "magnet:?xt=urn:btih:..."

# Continue an interrupted download
aria2c -c "magnet:?xt=urn:btih:..."
```

### 2. HTTP/FTP Downloads (Bonus)

```powershell
# Simple HTTP download
aria2c "https://example.com/large-file.iso"

# Download from multiple mirrors (fast!)
aria2c -x 16 -s 16 "https://mirror1/file.iso" "https://mirror2/file.iso"

# Download with 16 connections per server
aria2c -x 16 -s 16 "https://example.com/big-file.zip"

# With speed limit
aria2c --max-overall-download-limit=5M "https://example.com/file.iso"

# Multiple files in parallel
aria2c -j 3 "https://example.com/file1.iso" "https://example.com/file2.iso"

# From file list (URIs separated by newline)
aria2c -i uris.txt
```

### 3. BitTorrent Seeding Control

```powershell
# Seed until ratio 2.0, then stop
aria2c --seed-ratio=2.0 "file.torrent"

# Seed for 60 minutes, then stop
aria2c --seed-time=60 "file.torrent"

# Both conditions (whichever hits first)
aria2c --seed-ratio=2.0 --seed-time=120 "file.torrent"

# No seeding at all
aria2c --seed-time=0 "file.torrent"

# Upload speed limit per torrent
aria2c -u 500K "file.torrent"

# Overall upload limit
aria2c --max-overall-upload-limit=2M "file.torrent"

# Only download, don't seed (immediate stop after completion)
aria2c --seed-time=0 "file.torrent"
```

### 4. Select Specific Files

```powershell
# First, see what's in the torrent
aria2c -S "file.torrent"

# Output shows file indices — download only specific files
aria2c --select-file=1,3,5-7 "file.torrent"
```

### 5. Tracker Management

```powershell
# Add extra trackers
aria2c --bt-tracker="udp://tracker.opentrackr.org:1337,udp://tracker.coppersurfer.tk:6969" "file.torrent"

# Exclude specific trackers
aria2c --bt-exclude-tracker="http://dead-tracker.com/announce" "file.torrent"

# Remove ALL trackers and use DHT only
aria2c --bt-exclude-tracker="*" --enable-dht "file.torrent"

# Connect to DHT network
aria2c --enable-dht --dht-listen-port=6881 "file.torrent"
```

### 6. RPC Mode (Persistent Daemon)

For continuous management, run aria2 with RPC enabled:

```powershell
# Start as RPC daemon (listens on localhost:6800)
aria2c --enable-rpc --rpc-listen-all=true --rpc-listen-port=6800 `
  --rpc-secret=mysecret `
  --continue=true `
  --max-concurrent-downloads=5 `
  --max-connection-per-server=16 `
  --split=16 `
  --min-split-size=10M `
  --seed-ratio=2.0 `
  --enable-dht `
  --dht-listen-port=6881 `
  --listen-port=6881-6999 `
  --dir="D:/Downloads"

# Or with a config file
aria2c --conf-path="C:/Users/rx/.aria2/aria2.conf"
```

**Sample `aria2.conf`:**

```
enable-rpc=true
rpc-listen-all=true
rpc-listen-port=6800
rpc-secret=mysecret
continue=true
max-concurrent-downloads=5
max-connection-per-server=16
split=16
min-split-size=10M
seed-ratio=2.0
enable-dht=true
dht-listen-port=6881
listen-port=6881-6999
dir=D:/Downloads
max-overall-download-limit=0
max-overall-upload-limit=5M
```

### 7. RPC via curl (JSON-RPC)

```bash
# Add a magnet link via RPC
curl -X POST http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.addUri",
    "params": ["token:mysecret", ["magnet:?xt=urn:btih:..."]]
  }'

# Tell status of a download
curl -s http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.tellStatus",
    "params": ["token:mysecret", "gid"]
  }'

# List active downloads
curl -s http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.tellActive",
    "params": ["token:mysecret"]
  }'

# Pause all
curl -X POST http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.pauseAll",
    "params": ["token:mysecret"]
  }'

# Force pause all
curl -X POST http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.forcePauseAll",
    "params": ["token:mysecret"]
  }'

# Unpause all
curl -X POST http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.unpauseAll",
    "params": ["token:mysecret"]
  }'

# Get global stats
curl -s http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.getGlobalStat",
    "params": ["token:mysecret"]
  }'

# Remove download
curl -X POST http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.remove",
    "params": ["token:mysecret", "gid"]
  }'

# Change global option (speed limit)
curl -X POST http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.changeGlobalOption",
    "params": ["token:mysecret", {"max-overall-download-limit": "5M"}]
  }'

# Change per-download option
curl -X POST http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.changeOption",
    "params": ["token:mysecret", "gid", {"max-upload-limit": "100K"}]
  }'

# Save session (writes downloads to session file)
curl -X POST http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.saveSession",
    "params": ["token:mysecret"]
  }'

# Shutdown
curl -X POST http://localhost:6800/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "aria2.shutdown",
    "params": ["token:mysecret"]
  }'
```

### 8. aria2c RPC Methods Reference

| Method | Description |
|--------|-------------|
| `aria2.addUri` | Add download by URI(s) |
| `aria2.addTorrent` | Add download by torrent file |
| `aria2.addMetalink` | Add download by metalink file |
| `aria2.remove` | Remove download (graceful) |
| `aria2.forceRemove` | Remove download (immediate) |
| `aria2.pause` | Pause download |
| `aria2.pauseAll` | Pause all downloads |
| `aria2.forcePause` | Pause immediately |
| `aria2.forcePauseAll` | Pause all immediately |
| `aria2.unpause` | Resume download |
| `aria2.unpauseAll` | Resume all downloads |
| `aria2.tellStatus` | Get download status |
| `aria2.tellActive` | List active downloads |
| `aria2.tellWaiting` | List queued downloads |
| `aria2.tellStopped` | List completed/removed downloads |
| `aria2.getFiles` | List files in download |
| `aria2.getPeers` | List connected peers |
| `aria2.getServers` | List connected servers |
| `aria2.getUris` | List URIs for download |
| `aria2.changePosition` | Change queue position |
| `aria2.changeUri` | Add/remove URIs from download |
| `aria2.getOption` | Get per-download options |
| `aria2.changeOption` | Change per-download options |
| `aria2.getGlobalOption` | Get global options |
| `aria2.changeGlobalOption` | Change global options |
| `aria2.getGlobalStat` | Get global statistics |
| `aria2.purgeDownloadResult` | Clear completed results |
| `aria2.removeDownloadResult` | Remove specific result |
| `aria2.getVersion` | Get version info |
| `aria2.getSessionInfo` | Get session ID |
| `aria2.shutdown` | Graceful shutdown |
| `aria2.forceShutdown` | Immediate shutdown |
| `aria2.saveSession` | Save session to file |

---

# Decision Guide: Which Tool to Use?

| You want to... | Use |
|---|---|
| Download one torrent and forget it | **aria2c** |
| Manage 50+ torrents with categories/tags | **qBittorrent** |
| Automate RSS feeds / series tracking | **qBittorrent** |
| Download via HTTP/FTP with multi-connection | **aria2c** |
| Integrated search across trackers | **qBittorrent** |
| Minimal setup, no daemon | **aria2c** |
| Full REST API for custom tooling | **qBittorrent** |
| Add a list of 20 magnets from a file | **aria2c** (`-i magnets.txt`) |
| Set per-torrent ratio limits | **qBittorrent** (better UX) |
| Low memory footprint | **aria2c** (4-9 MiB RAM) |
| Need categories, tags, file management | **qBittorrent** |
| One binary, works everywhere | **aria2c** |
| Need Web UI out of the box | **qBittorrent** |

---

# Quick Reference: Common Tasks

| Task | qBittorrent (Python) | aria2c (CLI) |
|------|---------------------|--------------|
| Add magnet | `qbt.torrents_add(urls="magnet:...")` | `aria2c "magnet:..."` |
| Add .torrent file | `qbt.torrents_add(torrent_files=["f.torrent"])` | `aria2c file.torrent` |
| List all torrents | `qbt.torrents_info()` | `curl ... tellActive` (RPC) |
| Pause all | `qbt.torrents_pause("all")` | `Ctrl+C` then `aria2c -c` |
| Resume all | `qbt.torrents_resume("all")` | `aria2c -c` |
| Delete with files | `qbt.torrents_delete(delete_files=True, ...)` | N/A (stop + manual) |
| Set speed limit | `qbt.torrents_set_download_limit(...)` | `--max-overall-download-limit=5M` |
| Add tracker | `qbt.torrents_add_trackers(...)` | `--bt-tracker="url"` |
| Set category | `qbt.torrents_set_category(...)` | N/A |
| Get progress | `t.progress` (0.0-1.0) | Console readout / RPC |
| Run in background | `bg run "qbittorrent-nox..."` | `bg run "aria2c --enable-rpc..."` |

---

# Notes & Tips

- **Firewall:** Both tools need port access. aria2c uses `6881-6999` for DHT/peers by default.
  qBittorrent also uses a listen port for incoming connections. Open these in your firewall.
- **DHT is your friend:** When trackers are unreliable, DHT keeps swarms alive.
  - qBittorrent: enabled by default in preferences
  - aria2c: `--enable-dht --dht-listen-port=6881`
- **Session persistence:** 
  - qBittorrent saves state automatically (resume data)
  - aria2c: use `--save-session=/path/session.txt` and `--input-file=/path/session.txt` on restart
- **Security:** If you expose the Web UI or RPC to the internet, use a strong password
  and consider HTTPS + reverse proxy (nginx/caddy). Never use defaults on a public port.
- **Logging:** 
  - qBittorrent: `qbt.log.main()` (Python) or `/api/v2/log/main`
  - aria2c: `--log=/path/aria2.log`
- **The `Referer` header in qBittorrent** is mandatory — every API call needs it.
  Missing it silently drops requests. This catches everyone at least once.
- **qBittorrent v5.x API changes** are minimal but notable: cookie management
  APIs were added (`app/cookies`, `app/setCookies`), the `cookie` field in
  `/torrents/add` was removed, and `reannounce` was added to torrent info.
  The Python client `qbittorrent-api` **v2026.5.1** fully supports v5.2.0.
  See the [v5 API docs](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-5.0))
  for the full reference.
- **API Key Authentication** (≥v5.2.0) is a new alternative to cookie-based auth —
  generate an API key in the WebUI and use it directly:
  ```bash
  curl --header 'X-API-Key: your_key_here' http://localhost:8080/api/v2/torrents/info
  ```
  See the [wiki page](https://github.com/qbittorrent/qBittorrent/wiki/API-Key-Authentication-(%E2%89%A5v5.2.0))
  for setup instructions.

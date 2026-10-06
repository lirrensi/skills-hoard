#!/usr/bin/env node
// unpack.js — remote-handoff RECEIVER (node tier, zero installs). Fetches, decrypts, extracts.
// Usage: node unpack.js -k KEY_B64 <url|pack.asc|-> [--dir DEST] [--enc auto|hpk2|openssl]
// Needs system `tar` (Linux/macOS/Windows 10+ all ship one). HPK2 handled natively; openssl packs shell out.
"use strict";
const fs = require("fs"),
  os = require("os"),
  path = require("path"),
  https = require("https"),
  http = require("http"),
  crypto = require("crypto"),
  { spawnSync } = require("child_process"),
  h = require("./handoff.js");

const argv = process.argv.slice(2),
  fl = {},
  files = [];
for (let i = 0; i < argv.length; i++)
  if (["-k", "--key", "--dir", "--enc"].includes(argv[i]))
    fl[argv[i]] = argv[++i];
  else files.push(argv[i]);
const die = (m) => {
  process.stderr.write("unpack: " + m + "\n");
  process.exit(1);
};
const key = fl["-k"] || fl["--key"];
const src = files[0];
if (!key || !src)
  die("usage: unpack.js -k KEY_B64 <url|pack.asc|-> [--dir DEST]");

function fetch(u, depth = 0) {
  if (depth > 5) return Promise.reject(new Error("too many redirects"));
  return new Promise((res, rej) => {
    if (!/^https?:/.test(u)) return res(fs.readFileSync(u));
    (u.startsWith("https") ? https : http)
      .get(u, { headers: { "User-Agent": "remote-handoff/1.0" } }, (r) => {
        if ([301, 302, 303, 307, 308].includes(r.statusCode))
          return fetch(r.headers.location, depth + 1).then(res, rej);
        if (r.statusCode !== 200) return rej(new Error("HTTP " + r.statusCode));
        const c = [];
        r.on("data", (d) => c.push(d));
        r.on("end", () => res(Buffer.concat(c)));
      })
      .on("error", rej);
  });
}

const dest =
  fl["--dir"] ||
  "handoff-" + new Date().toISOString().replace(/[-:T]/g, "").slice(0, 15);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "remote-handoff-in-"));
process.on("exit", () => {
  try {
    fs.rmSync(tmp, { recursive: true, force: true });
  } catch {}
});
const tarPath = path.join(tmp, "pack.tar.gz");

(async () => {
  const raw =
    src === "-"
      ? fs.readFileSync(0)
      : await fetch(src).catch((e) => die("fetch failed: " + e.message));
  let ok = false,
    errs = [];
  const tryHpk2 = () => {
    const blob = raw.toString("utf8").trimStart().startsWith("-")
      ? h.dearmor(raw.toString("utf8"))
      : raw;
    fs.writeFileSync(tarPath, h.dec(blob, Buffer.from(key, "base64")));
  };
  const tryOpenssl = () => {
    const encPath = path.join(tmp, "pack.asc");
    fs.writeFileSync(encPath, raw);
    const r = spawnSync(
      "openssl",
      [
        "enc",
        "-d",
        "-aes-256-cbc",
        "-pbkdf2",
        "-pass",
        "pass:" + key,
        "-in",
        encPath,
        "-out",
        tarPath,
      ],
      { encoding: "utf8" }
    );
    if (r.status !== 0)
      throw new Error((r.stderr || "openssl failed").slice(0, 140));
  };
  const order =
    fl["--enc"] === "openssl"
      ? [tryOpenssl]
      : fl["--enc"] === "hpk2"
      ? [tryHpk2]
      : [tryHpk2, tryOpenssl];
  for (const fn of order) {
    try {
      fn();
      ok = true;
      break;
    } catch (e) {
      errs.push(e.message);
    }
  }
  if (!ok)
    die(
      "decrypt failed — wrong password, tampered pack, or unknown format (" +
        errs.join(" | ") +
        ")"
    );

  fs.mkdirSync(dest, { recursive: true });
  // list members first (and refuse unsafe paths), then extract
  const list = spawnSync("tar", ["tzf", tarPath], { encoding: "utf8" });
  if (list.status !== 0)
    die("archive listing failed: " + (list.stderr || "").slice(0, 140));
  const names = (list.stdout || "").trim().split("\n").filter(Boolean);
  const unsafe = names.filter((n) => n.startsWith("/") || n.includes(".."));
  if (unsafe.length)
    die("refusing unsafe archive members: " + unsafe.slice(0, 5).join(", "));
  const x = spawnSync("tar", ["xzf", tarPath, "-C", dest], {
    encoding: "utf8",
  });
  if (x.status !== 0) die("extract failed: " + (x.stderr || "").slice(0, 140));
  console.log("unpacked " + names.length + " entries into " + dest + "/");
  names.forEach((n) => {
    try {
      console.log(
        "   " +
          String(fs.statSync(path.join(dest, n)).size).padStart(9) +
          "  " +
          n
      );
    } catch {
      console.log("          " + n);
    }
  });
  fs.rmSync(tmp, { recursive: true, force: true }); // no leftover plaintext archive in temp
  const readme = path.join(dest, "_HANDOFF.md");
  if (fs.existsSync(readme))
    console.log(
      "\n--- _HANDOFF.md ---\n" + fs.readFileSync(readme, "utf8").trim()
    );
})();

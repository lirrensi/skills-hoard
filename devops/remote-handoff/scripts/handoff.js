#!/usr/bin/env node
// handoff.js — remote-handoff core (node tier, ZERO installs). Importable: require("./handoff.js")
// Container v2: "HPK2" (4) | flags (1, bit0=zlib) | nonce (12) | AES-256-GCM ct | tag (16, trailing)
// CLI: node handoff.js enc [-k KEY_B64] [-o OUT] [IN]   (no -k -> prints KEY:<b64> on stderr)
//      node handoff.js dec -k KEY_B64 [IN]
"use strict";
const crypto = require("crypto"),
  zlib = require("zlib"),
  fs = require("fs");
const MAGIC = Buffer.from("HPK2"),
  HDR = 17;
const BEGIN = "-----BEGIN HANDOFF PACK-----",
  END = "-----END HANDOFF PACK-----";

function enc(pt, key) {
  const n = crypto.randomBytes(12);
  const c = crypto.createCipheriv("aes-256-gcm", key, n);
  return Buffer.concat([
    MAGIC,
    Buffer.from([1]),
    n,
    c.update(zlib.deflateSync(pt, { level: 9 })),
    c.final(),
    c.getAuthTag(),
  ]);
}

function dec(blob, key) {
  if (blob.length < HDR + 16 || !blob.subarray(0, 4).equals(MAGIC))
    throw new Error("not a handoff pack (bad magic or truncated)");
  const flags = blob[4],
    n = blob.subarray(5, 17);
  const ct = blob.subarray(17, blob.length - 16),
    tag = blob.subarray(blob.length - 16);
  const d = crypto.createDecipheriv("aes-256-gcm", key, n);
  d.setAuthTag(tag);
  const pt = Buffer.concat([d.update(ct), d.final()]); // throws on any tamper/wrong key
  return flags & 1 ? zlib.inflateSync(pt) : pt;
}

const armor = (b) =>
  BEGIN +
  "\n" +
  b
    .toString("base64")
    .replace(/(.{64})/g, "$1\n")
    .replace(/\n$/, "") +
  "\n" +
  END +
  "\n";

function dearmor(text) {
  const s =
    text.includes(BEGIN) && text.includes(END)
      ? text.split(BEGIN)[1].split(END)[0]
      : text;
  return Buffer.from(s.replace(/\s/g, ""), "base64");
}

module.exports = { enc, dec, armor, dearmor };

if (require.main === module) {
  const argv = process.argv.slice(2),
    cmd = argv[0] || "",
    fl = {},
    files = [];
  for (let i = 1; i < argv.length; i++)
    if (["-k", "-o"].includes(argv[i]) && i + 1 < argv.length)
      fl[argv[i]] = argv[++i];
    else files.push(argv[i]);
  const die = (m) => {
    process.stderr.write("handoff: " + m + "\n");
    process.exit(1);
  };
  if (!["enc", "dec"].includes(cmd))
    die("usage: handoff.js enc|dec [-k KEY_B64] [-o OUT] [IN]");
  const src = files[0] ? fs.readFileSync(files[0]) : fs.readFileSync(0);
  if (cmd === "enc") {
    const key = fl["-k"]
      ? Buffer.from(fl["-k"], "base64")
      : crypto.randomBytes(32);
    if (key.length !== 32) die("key must be base64 of 32 raw bytes");
    if (!fl["-k"]) process.stderr.write("KEY:" + key.toString("base64") + "\n");
    const out = armor(enc(src, key));
    fl["-o"] ? fs.writeFileSync(fl["-o"], out) : process.stdout.write(out);
  } else {
    if (!fl["-k"]) die("dec needs -k KEY_B64");
    try {
      process.stdout.write(
        dec(
          dearmor(
            src.toString("utf8").trimStart().startsWith("-")
              ? src.toString("utf8")
              : src.toString("utf8")
          ),
          Buffer.from(fl["-k"], "base64")
        )
      );
    } catch (e) {
      die(e.message);
    }
  }
}

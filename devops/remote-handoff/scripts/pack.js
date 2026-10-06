#!/usr/bin/env node
// pack.js — remote-handoff SENDER (node tier, zero installs): collect -> tar -> ENCRYPT -> upload -> message.
// Usage: node pack.js -t "TITLE" [-c "context"] [-n notes.md] [--no-upload] [--host URL] PATH...
// Rules: plaintext archive is deleted before upload; nothing unencrypted ever leaves the box.
// Archive needs system `tar`; crypto is node-native (HPK2 = aes-256-gcm + zlib).
"use strict";
const fs = require("fs"),
  os = require("os"),
  path = require("path"),
  crypto = require("crypto"),
  { spawnSync } = require("child_process"),
  h = require("./handoff.js");

const HOSTS = ["https://x0.at", "https://temp.sh/upload", "https://envs.sh"];
const argv = process.argv.slice(2),
  fl = {},
  paths = [];
for (let i = 0; i < argv.length; i++)
  if (
    ["-t", "--title", "-c", "--context", "-n", "--notes", "--host"].includes(
      argv[i]
    )
  ) {
    if (argv[i] === "-n" || argv[i] === "--notes")
      (fl.notes = fl.notes || []).push(argv[++i]);
    else fl[argv[i]] = argv[++i];
  } else if (["--no-upload", "--keep-plain"].includes(argv[i]))
    fl[argv[i]] = true;
  else paths.push(argv[i]);
const die = (m) => {
  process.stderr.write("pack: " + m + "\n");
  process.exit(1);
};
const title = fl["-t"] || fl["--title"],
  context = fl["-c"] || fl["--context"] || "";
if (!title || !paths.length)
  die('usage: node pack.js -t "TITLE" [-c "context"] [-n notes.md] PATH...');

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "remote-handoff-"));
process.on("exit", () => {
  // scrub plaintext on ANY exit path, crashes included
  if (fl["--keep-plain"]) return;
  try {
    fs.unlinkSync(path.join(tmp, "pack.tar.gz"));
  } catch {}
});
const tarPath = path.join(tmp, "pack.tar.gz"),
  ascPath = path.join(tmp, "pack.asc");
const label =
  "HPK2 (aes-256-gcm + zlib, base64 armor)  [default: python unpack.py / node unpack.js]";
fs.writeFileSync(
  path.join(tmp, "_HANDOFF.md"),
  "# HANDOFF — " +
    title +
    "\n\nwhere: " +
    (context || "(no context given)") +
    "\ncreated: " +
    new Date().toISOString() +
    "\nenc: " +
    label +
    "\n\nThis archive was shipped encrypted; if you are reading it, decryption already worked.\n"
);

const EXCL = [
  "--exclude=__pycache__",
  "--exclude=*.pyc",
  "--exclude=*.pyo",
  "--exclude=.git",
  "--exclude=node_modules",
  "--exclude=.venv",
  "--exclude=venv",
  "--exclude=.mypy_cache",
  "--exclude=.tox",
  "--exclude=.DS_Store",
];
const args = ["czf", tarPath, ...EXCL, "-C", tmp, "_HANDOFF.md"];
(fl.notes || []).forEach((n) =>
  args.push("-C", path.dirname(path.resolve(n)), path.basename(n))
);
paths.forEach((p) => {
  if (!fs.existsSync(p)) die("path not found: " + p);
  args.push(
    "-C",
    path.dirname(path.resolve(p)),
    path.basename(path.resolve(p))
  );
});
let r = spawnSync("tar", args, { encoding: "utf8" });
if (r.status !== 0)
  die("tar failed (system tar required): " + (r.stderr || "").slice(0, 160));

const key = crypto.randomBytes(32);
fs.writeFileSync(ascPath, h.armor(h.enc(fs.readFileSync(tarPath), key)));
const keyB64 = key.toString("base64");
const manifest = spawnSync("tar", ["tzvf", tarPath], {
  encoding: "utf8",
}).stdout.trim();
if (!fl["--keep-plain"]) fs.unlinkSync(tarPath); // plaintext never lingers, never uploads

let url = null;
if (!fl["--no-upload"]) {
  for (const host of [fl["--host"] || null, ...HOSTS].filter(Boolean)) {
    const up = spawnSync(
      "curl",
      ["-s", "-A", "remote-handoff/1.0", "-F", "file=@" + ascPath, host],
      { encoding: "utf8" }
    );
    const out = (up.stdout || "").trim();
    if (/^https?:/.test(out)) {
      url = out;
      break;
    }
    process.stderr.write(
      "pack: host " + host + " refused: " + out.slice(0, 100) + "\n"
    );
  }
}
console.log("======= HANDOFF MESSAGE (copy/paste to the other side) =======");
console.log("HANDOFF — " + title);
console.log("doing: " + (context || "(no context given)"));
console.log(
  "link: " + (url || "<not uploaded — upload " + ascPath + " yourself>")
);
console.log("password: " + keyB64);
console.log("enc: " + label);
console.log(
  "size: " +
    manifest.split("\n").length +
    " entries, " +
    fs.statSync(ascPath).size +
    " bytes encrypted"
);
console.log("unpack (any runtime):");
console.log(
  "   curl -sL <link> -o pack.asc && python3 unpack.py -k '" +
    keyB64 +
    "' pack.asc"
);
console.log(
  "   curl -sL <link> -o pack.asc && node unpack.js -k '" +
    keyB64 +
    "' pack.asc"
);
console.log("============= END =============");
console.error("\nmanifest:\n" + manifest);
console.error("artifacts: " + ascPath + "  (temp: " + tmp + ")");

import json
import os
import re

LOG_PATH = r"C:\Users\Navies\.gemini\antigravity\brain\0a793fa1-5b63-418b-8b0d-a6cbbd34e844\.system_generated\steps\101\output.txt"

ORDER = [
    ("clip5", "act0_hook", "WhatsApp Video 2026-11-26 at 17.10.17.mp4"),
    ("clip4", "act1_2005", "WhatsApp Video 2026-11-26 at 17.10.16.mp4"),
    ("clip3", "act2_numbers", "WhatsApp Video 2026-11-26 at 17.10.14.mp4"),
    ("clip2", "act3_today", "WhatsApp Video 2026-11-26 at 17.10.12.mp4"),
    ("clip1", "act4_outro", "WhatsApp Video 2026-11-26 at 17.10.10.mp4"),
]

with open(LOG_PATH, encoding="utf-8") as f:
    log = f.read()

sections = re.split(r"=== Transcribing (clip\d) ===", log)
by_clip = {}
for i in range(1, len(sections), 2):
    cid = sections[i]
    body = sections[i + 1]
    words = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                obj = json.loads(line)
                if obj.get("type") == "words":
                    words.extend(obj.get("words", []))
            except Exception:
                pass
    by_clip[cid] = words

os.makedirs("assets/subtitles", exist_ok=True)

for cid, name, raw_file in ORDER:
    ws = by_clip[cid]
    out_path = f"assets/subtitles/{name}_raw.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"clip": cid, "act": name, "raw_file": raw_file, "words": ws}, f, indent=2)

    s0 = ws[0]["start"] if ws else 0.0
    e0 = ws[-1]["end"] if ws else 0.0
    print(f"\n=== {name} ({cid} / {raw_file}): {len(ws)} words | {s0:.2f}s -> {e0:.2f}s ===")
    chunk = []
    for w in ws:
        chunk.append(w)
        if w["text"].endswith((".", "?", "!")) or len(chunk) >= 14:
            cs = chunk[0]["start"]
            ce = chunk[-1]["end"]
            txt = " ".join(x["text"] for x in chunk)
            print(f"  [{cs:6.2f} - {ce:6.2f}] {txt}")
            chunk = []
    if chunk:
        cs = chunk[0]["start"]
        ce = chunk[-1]["end"]
        txt = " ".join(x["text"] for x in chunk)
        print(f"  [{cs:6.2f} - {ce:6.2f}] {txt}")

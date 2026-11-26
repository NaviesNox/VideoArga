import html
import json
import re

data = json.load(open("assets/subtitles/captions_all.json", encoding="utf-8"))
groups = data["groups"]
total_dur = data["total_duration"]

EMPH_RE = re.compile(r"(rp|trillion|billion|million|\d|2005|2026|pertamina|tipikor|blbi|kpu|dprd|courts?|verdicts?)", re.I)

group_divs = []
compact_timings = []

for i, g in enumerate(groups):
    gid = f"cg-{i}"
    word_spans = []
    w_meta = []
    for wi, w in enumerate(g["words"]):
        wid = f"cw-{i}-{wi}"
        txt = html.escape(w["text"])
        is_key = 1 if EMPH_RE.search(w["text"]) else 0
        cls = "cap-w cap-key" if is_key else "cap-w"
        word_spans.append(f'<span id="{wid}" class="{cls}">{txt}</span>')
        w_meta.append([w["start"], is_key])

    group_divs.append(f'      <div id="{gid}" class="cap-group">{" ".join(word_spans)}</div>')
    compact_timings.append([g["start"], g["end"], w_meta])

timings_json = json.dumps(compact_timings, separators=(",", ":"))

html_out = f"""<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      overflow: visible;
      font-family: "Oswald", sans-serif;
    }}

    .cap-stage {{
      position: absolute;
      left: 150px;
      top: 1340px;
      width: 740px;
      height: 120px;
      overflow: visible;
    }}

    .cap-group {{
      position: absolute;
      left: 0;
      top: 0;
      width: 740px;
      text-align: center;
      background: rgba(14, 15, 18, 0.92);
      border-left: 8px solid #B91C1C;
      padding: 12px 20px;
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.55);
      line-height: 1.18;
      opacity: 0;
      visibility: hidden;
    }}

    .cap-w {{
      display: inline-block;
      margin: 0 6px;
      font-size: 38px;
      font-weight: 700;
      letter-spacing: 0.01em;
      color: #C9C5BC;
      text-transform: uppercase;
    }}

    .cap-key {{
      color: #F5B841;
    }}
  </style>

  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    <div class="cap-stage" data-layout-allow-caption-zone>
{chr(10).join(group_divs)}
    </div>
  </div>

  <script>
    const tl = gsap.timeline({{ paused: true }});
    const CAP_DATA = {timings_json};
    for (let i = 0; i < CAP_DATA.length; i++) {{
      const [gs, ge, words] = CAP_DATA[i];
      const gid = "#cg-" + i;
      const fadeOut = Math.max(gs + 0.05, Number((ge - 0.1).toFixed(3)));
      gsap.set(gid, {{ opacity: 0, visibility: "hidden" }});
      tl.set(gid, {{ visibility: "visible" }}, gs);
      tl.fromTo(gid, {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.11, ease: "power3.out" }}, gs);
      for (let wi = 0; wi < words.length; wi++) {{
        const [ws, isKey] = words[wi];
        const wid = "#cw-" + i + "-" + wi;
        tl.set(wid, {{ color: "#C9C5BC" }}, gs);
        tl.set(wid, {{ color: isKey ? "#F5B841" : "#FFFFFF" }}, ws);
      }}
      tl.to(gid, {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, fadeOut);
      tl.set(gid, {{ opacity: 0, visibility: "hidden" }}, ge);
    }}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""

with open("compositions/captions.html", "w", encoding="utf-8") as f:
    f.write(html_out)

print(f"Wrote compact compositions/captions.html ({len(html_out.splitlines())} lines, {len(groups)} groups across {total_dur}s)")

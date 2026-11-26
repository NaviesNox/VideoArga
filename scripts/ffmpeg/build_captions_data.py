import json
import os
import re

# Clean ASR transcription errors against the verbatim script (docs/script.md)
# while preserving exact Parakeet word-level timestamps!

ACTS = ["act0_hook", "act1_2005", "act2_numbers", "act3_today", "act4_outro"]

# Exact phrase/word replacements (case-insensitive word sequence matches)
PHRASE_FIXES = [
    (["rubia"], ["rupiah"]),
    (["rubia,"], ["rupiah,"]),
    (["rubia."], ["rupiah."]),
    (["rupee."], ["rupiah."]),
    (["rupee,"], ["rupiah,"]),
    (["rupee"], ["rupiah"]),
    (["rupees."], ["rupiah."]),
    (["rupees,"], ["rupiah,"]),
    (["rupees"], ["rupiah"]),
    (["two", "point", "zero", "two"], ["2.02"]),
    (["vanishes"], ["vanished"]),
    (["ministers", "of", "religious"], ["Minister", "of", "Religious"]),
    (["stationary"], ["stationery"]),
    (["The", "method", "have"], ["The", "methods", "have"]),
    (["never", "stop", "the", "theft."], ["never", "stopped", "the", "theft."]),
    (["vertex"], ["verdicts"]),
    (["verticals"], ["verdicts"]),
    (["wiped", "out", "2", "times"], ["wipe", "out", "20", "times"]),
    (["informed", "AP,"], ["involved", "A.P.,"]),
    (["Nangaraja", "Tokusara,"], ["Nanggroe", "Aceh", "Darussalam,"]),
    (["MI2", "helicopters"], ["MI-2", "helicopter"]),
    (["scheming"], ["skimming"]),
    (["freaking", "out"], ["breaking", "out"]),
    (["Bajang", "City,"], ["Padang", "City,"]),
    (["department", "members", "scored"], ["DPRD", "members", "got"]),
    (["West", "Matra", "Province,"], ["West", "Sumatra", "Province,"]),
    (["department", "members"], ["DPRD", "members"]),
    (["Sumaran", "to", "Point", "Solo", "Tomanato", "and", "Tongala,"], ["Semarang,", "Cirebon,", "Solo,", "Manado,", "and", "Donggala,"]),
    (["Next", "to", "take", "some"], ["Next", "to", "today's", "numbers,"]),
    (["Almost", "a", "little", "small"], ["almost", "looks", "small."]),
    (["white", "gap"], ["wide", "gap"]),
    (["Ape", "and", "Apple", "took", "the", "least"], ["APBN", "and", "APBD,", "topped", "the", "list"]),
    (["206.27"], ["206.37"]),
    (["which", "in", "seven", "cases", "trained"], ["where", "just", "seven", "cases", "drained"]),
    (["Paz", "misused"], ["P.S.", "misused"]),
    (["Plpi", "type", "balance"], ["BLBI", "debit", "balance"]),
    (["Pangmandiri", "issued", "a", "1.89", "trillion", "in", "pet", "loans", "to", "Pete", "Kani", "Katas."], ["Bank", "Mandiri", "issued", "Rp", "1.89T", "in", "bad", "loans", "to", "PT", "Kiani", "Kertas."]),
    (["Fixed", "letters", "of", "credit", "trained"], ["Fictitious", "letters", "of", "credit", "drained"]),
    (["Bangbei", "and", "Iqway", "and", "Baru,"], ["Bank", "BNI", "Kebayoran", "Baru,"]),
    (["Pang", "Takang", "Valley."], ["Bank", "Dagang", "Bali."]),
    (["Outside", "Penging,"], ["Outside", "banking,"]),
    (["Uma", "endowment"], ["Ummah", "Endowment"]),
    (["got", "tracked", "in,"], ["got", "dragged", "in,"]),
    (["50.53"], ["15.53"]),
    (["ERCA", "of", "her"], ["R.K.", "over"]),
    (["and", "as", "of", "a", "Paul", "Worker"], ["N.S.", "over", "poll", "worker"]),
    (["D", "offer", "election", "in"], ["D.D.", "over", "election", "ink,"]),
    (["MWK"], ["M.W.K.,"]),
    (["hit", "stands", "for", "hundreds"], ["hits", "tens", "or", "hundreds"]),
    (["informed", "Partamina"], ["firm", "Pertamina"]),
    (["RS,"], ["R.S.,"]),
    (["rake", "by", "sensing"], ["rig", "licensing"]),
    (["special", "codes"], ["special", "courts"]),
    (["actors", "attacked,"], ["actors", "adapted,"]),
    (["local", "polls", "in", "public", "offers"], ["loopholes", "in", "public", "oversight"]),
    (["final", "penalties"], ["penalties"]),
    (["budget", "of", "skimming"], ["budget", "skimming"]),
    (["went", "on"], ["went", "wrong"]),
]


def apply_fixes(words):
    out = [dict(w) for w in words]
    for pat, rep in PHRASE_FIXES:
        plen = len(pat)
        i = 0
        while i <= len(out) - plen:
            window = [out[i + k]["text"] for k in range(plen)]
            if [x.lower() for x in window] == [x.lower() for x in pat]:
                t_start = out[i]["start"]
                t_end = out[i + plen - 1]["end"]
                dur = max(0.08, t_end - t_start)
                rlen = len(rep)
                new_items = []
                for idx, tok in enumerate(rep):
                    ws = round(t_start + dur * (idx / rlen), 3)
                    we = round(t_start + dur * ((idx + 1) / rlen), 3)
                    new_items.append({"text": tok, "start": ws, "end": we})
                out[i : i + plen] = new_items
                i += rlen
            else:
                i += 1
    # Catch any remaining punctuation/case variants of rubia/rubiah/rupia/rupee(s)
    for item in out:
        item["text"] = re.sub(r"\b(?:rubiah?|rupia|rupees?)\b", "rupiah", item["text"], flags=re.I)
    return out


def build_groups(words, act_offset, act_dur):
    """Build 3-4 word Reels caption groups (max ~24 chars), breaking on punctuation or pauses >= 150ms."""
    groups = []
    cur = []
    for idx, w in enumerate(words):
        if w["start"] >= act_dur - 0.05:
            break
        cur.append(w)
        chars = sum(len(x["text"]) for x in cur) + len(cur) - 1
        next_gap = (words[idx + 1]["start"] - w["end"]) if idx + 1 < len(words) else 1.0
        ends_punct = w["text"].endswith((".", "?", "!", ","))
        if len(cur) >= 4 or chars >= 22 or ends_punct or next_gap >= 0.28:
            gs = max(0.15, cur[0]["start"])
            ge = min(act_dur - 0.08, cur[-1]["end"] + 0.08)
            if ge > gs + 0.12:
                groups.append({
                    "start": round(act_offset + gs, 3),
                    "end": round(act_offset + ge, 3),
                    "words": [
                        {
                            "text": x["text"],
                            "start": round(act_offset + max(gs, x["start"]), 3),
                            "end": round(act_offset + min(ge, x["end"]), 3),
                        }
                        for x in cur
                    ],
                })
            cur = []
    if cur:
        gs = max(0.15, cur[0]["start"])
        ge = min(act_dur - 0.08, cur[-1]["end"] + 0.08)
        if ge > gs + 0.12:
            groups.append({
                "start": round(act_offset + gs, 3),
                "end": round(act_offset + ge, 3),
                "words": [
                    {
                        "text": x["text"],
                        "start": round(act_offset + max(gs, x["start"]), 3),
                        "end": round(act_offset + min(ge, x["end"]), 3),
                    }
                    for x in cur
                ],
            })
    # Ensure zero overlap between adjacent groups
    for i in range(len(groups) - 1):
        if groups[i]["end"] > groups[i + 1]["start"] - 0.04:
            groups[i]["end"] = round(max(groups[i]["start"] + 0.12, groups[i + 1]["start"] - 0.04), 3)
    return groups


def fmt_srt(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    manifest = json.load(open("assets/video/manifest.json", encoding="utf-8"))
    all_groups = []
    for act_info in manifest["acts"]:
        name = act_info["act"]
        raw = json.load(open(f"assets/subtitles/{name}_raw.json", encoding="utf-8"))
        cleaned = apply_fixes(raw["words"])
        with open(f"assets/subtitles/{name}_clean.json", "w", encoding="utf-8") as f:
            json.dump({"act": name, "words": cleaned}, f, indent=2)
        groups = build_groups(cleaned, act_info["start"], act_info["duration"])
        all_groups.extend(groups)

    with open("assets/subtitles/captions_all.json", "w", encoding="utf-8") as f:
        json.dump({"total_duration": manifest["total_duration"], "groups": all_groups}, f, indent=2)

    # Also write SRT sidecar
    with open("assets/subtitles/full_video.srt", "w", encoding="utf-8") as f:
        for i, g in enumerate(all_groups, 1):
            txt = " ".join(w["text"] for w in g["words"])
            f.write(f"{i}\n{fmt_srt(g['start'])} --> {fmt_srt(g['end'])}\n{txt}\n\n")

    print(f"Built {len(all_groups)} caption groups + full_video.srt across {manifest['total_duration']:.2f}s")


if __name__ == "__main__":
    main()

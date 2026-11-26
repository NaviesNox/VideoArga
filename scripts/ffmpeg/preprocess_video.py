import os
import subprocess
import json

CLIPS = [
    ("act0_hook",    "raw/video/WhatsApp Video 2026-11-26 at 17.10.17.mp4"),
    ("act1_2005",    "raw/video/WhatsApp Video 2026-11-26 at 17.10.16.mp4"),
    ("act2_numbers", "raw/video/WhatsApp Video 2026-11-26 at 17.10.14.mp4"),
    ("act3_today",   "raw/video/WhatsApp Video 2026-11-26 at 17.10.12.mp4"),
    ("act4_outro",   "raw/video/WhatsApp Video 2026-11-26 at 17.10.10.mp4"),
]

os.makedirs("assets/video", exist_ok=True)
os.makedirs("assets/audio/voice", exist_ok=True)

manifest = []
cursor = 0.0

for name, src in CLIPS:
    v_out = f"assets/video/{name}.mp4"
    a_out = f"assets/audio/voice/{name}.wav"

    # 1. Video: upscale 480x864 -> 1080x1920, constant 30fps, -g 30 (1s GOP for smooth HyperFrames seek),
    #    subtle denoise + crisp unsharp + investigative contrast/desat polish, muted (-an)
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
        "crop=1080:1920,setsar=1:1,"
        "hqdn3d=1.0:1.0:3:3,"
        "unsharp=5:5:0.45:5:5:0.0,"
        "eq=contrast=1.06:brightness=-0.01:saturation=0.90"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", src,
            "-an",
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "medium",
            "-g", "30",
            "-keyint_min", "30",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            v_out,
        ],
        check=True,
    )

    # 2. Voice audio: highpass 85Hz, light denoise, gentle vocal compression, broadcast -16 LUFS / -1.5 dBTP
    af = (
        "highpass=f=85,"
        "afftdn=nf=-25,"
        "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=120,"
        "loudnorm=I=-16:TP=-1.5:LRA=11"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", src,
            "-vn",
            "-af", af,
            "-ar", "48000",
            "-ac", "2",
            "-c:a", "pcm_s16le",
            a_out,
        ],
        check=True,
    )

    # Probe exact output duration (video and audio)
    vdur = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                v_out,
            ]
        ).decode().strip()
    )
    adur = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                a_out,
            ]
        ).decode().strip()
    )
    dur = round(min(vdur, adur), 3)
    manifest.append(
        {
            "act": name,
            "source": src,
            "video": v_out,
            "audio": a_out,
            "start": round(cursor, 3),
            "duration": dur,
            "end": round(cursor + dur, 3),
        }
    )
    cursor += dur
    print(f"OK {name}: start={manifest[-1]['start']:.3f}s dur={dur:.3f}s end={manifest[-1]['end']:.3f}s")

with open("assets/video/manifest.json", "w", encoding="utf-8") as f:
    json.dump({"total_duration": round(cursor, 3), "fps": 30, "width": 1080, "height": 1920, "acts": manifest}, f, indent=2)

print(f"\nTOTAL DURATION: {cursor:.3f}s ({cursor/60:.2f} min)")

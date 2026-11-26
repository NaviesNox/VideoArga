# VideoArga — FFmpeg + HyperFrames Production Pipeline

## 1. Raw Footage Mapping (`raw/video/`)
| Act | Story Beat | Raw Source File | Preprocessed Video (`assets/video/`) | Normalized Voice (`assets/audio/voice/`) | Timeline Window |
|---|---|---|---|---|---|
| Act 0 | Hook (Rp 8.84T → Rp 193T) | `WhatsApp Video 2026-11-26 at 17.10.17.mp4` | `act0_hook.mp4` | `act0_hook.wav` | `0.000s – 34.667s` |
| Act 1 | 2005 Tipikor & DPRD | `WhatsApp Video 2026-11-26 at 17.10.16.mp4` | `act1_2005.mp4` | `act1_2005.wav` | `34.667s – 102.800s` |
| Act 2 | 40 Cases Charts & Bank Looting | `WhatsApp Video 2026-11-26 at 17.10.14.mp4` | `act2_numbers.mp4` | `act2_numbers.wav` | `102.800s – 216.848s` |
| Act 3 | 2005 vs 2026 Playbook & Pertamina | `WhatsApp Video 2026-11-26 at 17.10.12.mp4` | `act3_today.mp4` | `act3_today.wav` | `216.848s – 300.667s` |
| Act 4 | Outro Timeline & Comment CTA | `WhatsApp Video 2026-11-26 at 17.10.10.mp4` | `act4_outro.mp4` | `act4_outro.wav` | `300.667s – 345.168s` |

## 2. FFmpeg Preprocessing (`scripts/ffmpeg/preprocess_video.py`)
- Upscaled from `480×864` VFR to crisp `1080×1920` constant `30 fps`, `-g 30` (1-second GOP for smooth HyperFrames seeking), `yuv420p`, `+faststart`, subtle denoise (`hqdn3d`) + sharpen (`unsharp`) + investigative contrast balance (`eq`).
- Voice tracks extracted to 48 kHz stereo PCM WAV with `highpass=85Hz`, `afftdn`, gentle vocal compression, and broadcast loudness normalization to `-16 LUFS / -1.5 dBTP`.

## 3. Synced Captions (`scripts/ffmpeg/build_captions_data.py` & `generate_captions_comp.py`)
- Word-level timestamps extracted via HyperFrames Parakeet (`parakeet-tdt-0.6b-v3`).
- Corrected against `docs/script.md` into 196 Reels-safe caption groups (`compositions/captions.html`) plus `assets/subtitles/full_video.srt`.

## 4. Adding Optional Background Music (BGM)
Currently the soundtrack uses your normalized voiceover + real bundled HyperFrames SFX (`assets/audio/sfx/`, peak-normalized to `-3 dBTP`).
To add a music bed:
1. Place any `.mp3`/`.wav` track in `assets/audio/music/bgm.mp3` (or sign in to HeyGen with `npx hyperframes auth login` for the free catalog).
2. Add one `<audio id="bgm" class="clip" src="assets/audio/music/bgm.mp3" data-start="0" data-duration="345.168" data-volume="0.14" data-fade-in="1.5" data-fade-out="2.5" data-track-index="5"></audio>` inside `index.html`.

## 5. FFmpeg Final Post-Processing (`scripts/ffmpeg/postprocess_reels.ps1`)
After rendering from HyperFrames (`npx hyperframes render --quality delivery -o renders/final/corruption_2005_vs_today_raw.mp4`), run:
```powershell
.\scripts\ffmpeg\postprocess_reels.ps1
```
This outputs a two-pass `-16 LUFS` mastered, Reels-ready H.264/AAC MP4 (`renders/final/corruption_2005_vs_today_reels.mp4`) and extracts a crisp cover thumbnail (`renders/thumbnails/cover_hook.jpg`).

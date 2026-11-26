# Review: "2005 vs. Today: How Indonesian Corruption Mutated"

## Creative Calls
- **Built:** Storyline A (**The Evidence Desk**) — charcoal archival mat (`#17181B`), tactile manila/newsprint dossiers (`#DDD6C7`), judicial crimson (`#B91C1C` / `#C81E1E`) rationed strictly to stamps, loss spikes, and 2026 escalation, with `Oswald 700` headlines and `IBM Plex Mono` tabular figures.
- **Not built:** Storyline B (*The Scale Machine* — bright brutalist Swiss ledger wall) and Storyline C (*The Ledger Abyss* — continuous vertical elevation shaft). All three remain saved in `STORYLINES.md`.
- **Footage mapping discovery:** Parakeet ASR transcription revealed the 5 raw WhatsApp recordings in `raw/video/` were stored in reverse story order (`17.10.17` = Hook → `17.10.10` = Outro). All 5 were re-ordered accurately, upscaled cleanly to `1080×1920 @ 30fps, -g 30` with FFmpeg, and voice-normalized to `-16 LUFS`.

## Visual Review & Fixes Made
After inspecting `review-beats.jpg`, `review-phone.jpg`, `review-seam-01..04.jpg`, and 9 targeted hero frames:
1. **P0 fixed — Chart 2 source / caption collision (`t=141s`):** Compacted `.a2-chart-card` bar spacing and shortened source line so Chart 2 ends >70 px clear above captions.
2. **P0 fixed — Act 3 scale stamp / caption overlap (`t=254.5s`):** Reduced `.a3-chart-stage` height (`540px → 440px`) and tightened stamp copy so it clears the caption zone.
3. **P0 fixed — Chest banner touching host's chin (`t=34.5s, 323s`):** Compacted chest banners (`top: 998px`), shifted captions to `top: 1124px` (still strictly inside Reels safe `y ≤ 1248`), and panned host punch-ins upward (`y: -40`) so the speaker's face and chin stay 100% clear.
4. **P1 fixed — Split-screen sidebars (`t=68.7s, 335s`):** Replaced `scale: 0.78` with edge-to-edge `scale: 1, y: -230` across all 4 split-view scenes so there are zero sidebars.
5. **P1 fixed — `A.P.` dossier stamp overlap (`t=51s`) & horizontal Reels balance:** Cleared the upper-right stamp zone on the `A.P.` dossier and centered all plates/captions visually (`left: 150px; width: 740–760px`).

## What Was Measured vs. Looked At
- **Measured (`hyperframes check --safe-zone reels --samples 15`):** `ok=true` — **0 errors, 0 warnings** across `lint`, `runtime`, `layout`, `motion`, `contrast` (42/42 WCAG AA pass), `craft` (598 samples, 0 `line_unread`, 0 `dead_stretch`, 0 `text_below_floor`, 0 `first_frame_empty`), and `audio`.
- **Measured (FFmpeg `ebur128`):** Normalized voice tracks measure `-16.6` to `-15.7 LUFS` (true peak `-2.0` to `-1.5 dBFS`); all bundled SFX peak-normalized to `-3.0 dBTP`.
- **Looked at:** `review-beats.jpg`, `review-phone.jpg` (360px phone legibility), `review-seam-01..04.jpg`, 9 hero frames, and 6 post-polish verification frames.
- **Not heard (measured only):** All audio levels, SFX peak timings, and sync offsets were verified by signal measurement (`ebur128`, Parakeet timestamps, `hyperframes audio`), not listened to by ear.

## Weakest Shot & Future Improvements
- **Weakest shot:** Opening talking-head seconds of Act 1/2/3 (`34.7s`, `102.8s`, `216.8s`) rely on a single camera angle from the source footage before the Evidence Desk cutaways enter. With more time, adding subtle B-roll archival texture or a 2-second visual pre-roll card on chapter transitions would add even more visual momentum.
- **Optional BGM:** Delivered with host voiceover + real bundled SFX only (no HeyGen sign-in or local music model was active, per `sound.md` §3). Drop any investigative track into `assets/audio/music/bgm.mp3` and add one `<audio>` line in `index.html` (`data-volume="0.14"`) if a music bed is desired.

## Warnings Kept on Purpose
- None — all lint, layout, contrast, craft, and audio checks pass with 0 errors and 0 warnings.

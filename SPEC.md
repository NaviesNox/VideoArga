# SPEC: 2005 vs. Today — How Indonesian Corruption Mutated

```text
GOAL:    The viewer feels forensic shock at how Indonesian corruption mutated over 21 years from dispersed regional budget skimming in the billions into systemic Rp 193.7 trillion capture of state enterprises and courts, and comments with their take.
OUTPUT:  HyperFrames + FFmpeg, 1080 x 1920 (9:16 Reels), 30 fps
TIME:    5 real recorded acts concatenated from assets/video/manifest.json (~345 s total, ~10,350 frames at 30 fps); voiceover is the master clock.
LOOK:    Medium: Investigative Print & Court Archive Desk ("The Evidence Desk").
         Ground: Charcoal archive desk mat #17181B (solid, 0 gradients) + tactile manila/newsprint dossier sheets #DDD6C7 with 4% static SVG paper grain.
         Ink: Deep archival ink #111214 on paper sheets; crisp bone #F2EFE9 on charcoal desk; muted slate #8C8A84 for source annotations and secondary ticks.
         Accent: Judicial crimson #C81E1E (rationed strictly to stamps, loss spikes, 2026 escalation bars, and active caption emphasis words). Secondary 2005 ledger ochre #C48B28 used only to distinguish 2005 bars against 2026 crimson bars.
         Display face: Oswald 700, uppercase, 64-112 px, tracking -0.02em.
         Data/tabular face: IBM Plex Mono 600/700, 32-96 px, font-variant-numeric: tabular-nums.
         Body/editorial face: Inter 500/700, 28-44 px (never below 28 px).
         Light & depth: Directional top-left cast shadows on paper sheets (0 18px 36px rgba(0,0,0,0.55)), 2px crisp ink borders (#111214) on dossiers, subtle 18% perimeter desk vignette on dark evidence plates, zero neon glow.
OBJECTS:
         1. Mechanical Rupiah Odometer (Hook): Recessed steel ledger window (#0E0F12) with vertical rolling digit drums, crisp 1px metallic divider rules, locking red judicial stamp "2005 · 40 CASES".
         2. 2005 Newspaper Clippings & Tipikor Dossier Card (Act 1): Printed broadsheet masthead mast ("ARCHIVAL RECORD · 2005"), multi-column newsprint sheet with red highlighter underline, manila case folder card for "A.P." with angled crimson rubber stamp "FIRST TIPIKOR VERDICT", stacked DPRD regional case slips (Padang, West Sumatra, Semarang, Cirebon, Solo, Manado, Donggala).
         3. Dual Vertical Evidence Charts (Act 2): Axis-first ruled archival graph paper plate. Chart 1 (Case Count, 40 cases: APBN/APBD 15 = 37.5% highlighted) physically morphs/flips into Chart 2 (State Losses, Rp 8.84T: Banking & Finance Rp 7.13T = 80.7% dominating while APBN/APBD collapses to Rp 206.37B = 2.3%), followed by bank dossier rows (P.S. BLBI Rp 2.02T, Mandiri Rp 1.89T, BNI Rp 1.7T, Bank Dagang Bali Rp 1.3T), S.A. Hajj/Ummah Rp 719B card, and 4-case KPU Rp 15.53B slip.
         4. 2005 vs. 2026 Playbook Ledger (Act 3): Vertical investigative comparison board (strictly inside Reels safe width 120-888 px) contrasting muted 2005 ochre/manila column ("2005 PLAYBOOK") against aggressive 2026 crimson/charcoal column ("2026 PLAYBOOK"), plus the Rp 8.84T vs Rp 193.7T Pertamina proportional scale shock bar.
         5. 2005-2026 Runaway Timeline (Outro): Ruled vertical year axis (2005 -> 2026) where the red loss curve climbs cleanly off the upper chart frame, transitioning back to the host for the final comment question.
         6. Host Footage Framing: Preprocessed 1080x1920@30fps (-g 30) talking-head video. Speaker's face sits at y=280..960 px. Never cover the face with cards or captions. Alternate rhythmically every 10-18s between: (a) Full-frame host with subtle punch-in & chest-level evidence badge (y=980..1210), (b) Top-split host (y=0..820) + evidence sheet below (y=820..1920, key text <= y=1248), and (c) Full-frame Evidence Desk cutaways (charts, dossiers, split playbooks) with continuous host voiceover.
MOTION:  Enter (cards/dossiers): expo.out / power4.out (14-20 frames / 0.45-0.65s).
         Stamp impact: back.out(1.2) scale 1.8 -> 1.0 in 6 frames (0.2s) synced 1 frame before impact-bass-1.wav peak.
         Data count-up: power2.out over 1.2-1.6s with tabular-nums, then dead still.
         Exits: power3.in (8-12 frames / 0.25-0.4s), 40-50% shorter than entrances.
         Re-framing host wrapper: power2.inOut over 0.55s in natural breath gaps.
         Titles and landed cards remain dead still while read.
SHOTS:
         Act 0 — Hook (act0_hook.mp4, ~34.7s):
           0.0-8.6s: Frame 0 opens directly on the Mechanical Odometer rolling past Rp 8,838,731,700,646 over charcoal desk (never black!), locks at 3.0s on "8.84 trillion" with heavy thud + crimson "2005 · 40 CASES" stamp; host punches in at 8.6s.
           11.8-16.6s: Second counter rips open beneath climbing past Rp 193,000,000,000,000 ("20× that amount") with riser + impact-bass-2.
           16.6-34.7s: Host full-frame with punch-in at 25.6s + lower-chest archive tag "40 VERDICTS · 2005 vs 2026" as bridge into Act 1.
         Act 1 — 2005 Headlines (act1_2005.mp4, ~68.2s):
           0.0-9.3s: Host introduces 2005 Anti-Corruption Court (Tipikor) + crisp chapter header strip.
           9.3-27.7s: Evidence Desk cutaway — 2005 newsprint clipping + A.P. dossier card (Governor of NAD, MI-2 Helicopter mark-up Rp 13.6B), crimson stamp "FIRST TIPIKOR VERDICT" slams on "convicted", sentence strip "APRIL 2005 · 10 YEARS PRISON" lands at 22.2s.
           27.7-53.2s: Split-view (Host top / DPRD case slips bottom-safe) — Padang City (27 DPRD, 4 yrs, Rp 10.4B) at 34.7s, West Sumatra Province (43 DPRD, Rp 6.4B) at 44.9s.
           53.2-68.2s: Regional city cascade tags (Semarang, Cirebon, Solo, Manado, Donggala) at 53.2s, pulling back to Host punch-in at 61.7s ("almost looks small").
         Act 2 — Inside the 2005 Numbers (act2_numbers.mp4, ~114.1s):
           0.0-13.4s: Host introduces 40-case plot; Evidence Desk graph paper rolls up at 6.5s.
           13.4-35.8s: Chart 1 (Case Count) draws in: APBN/APBD = 15 cases (37.5%) highlighted in ochre at 18.5s; then at 23.5s flips/compresses to Chart 2 (State Losses): APBN/APBD drops to Rp 206.37B (2.3%)!
           35.8-47.5s: Banking & Finance bar surges in crimson: 7 cases = Rp 7.13T (80.7% of total losses) with impact SFX.
           47.5-74.6s: Four bank case ledger rows stamp in one-by-one synced to voice: P.S. BLBI Rp 2.02T (47.6s), Bank Mandiri / PT Kiani Kertas Rp 1.89T (55.9s), Bank BNI Kebayoran Baru L/C Rp 1.70T (63.2s), Bank Dagang Bali Rp 1.30T (69.8s).
           74.6-86.2s: Host split-view + S.A. (Former Minister of Religious Affairs) Hajj & Ummah Endowment Funds Rp 719B dossier card.
           86.2-114.1s: 2004 Election (KPU) dossier sheet — 4 cases totaling Rp 15.53B: R.K. ballot paper (96.1s), N.S. poll worker insurance (99.5s), D.D. election ink (103.0s), M.W.K. Rp 300M auditor bribe (105.8s).
         Act 3 — 2005 vs. Today (act3_today.mp4, ~83.8s):
           0.0-16.1s: Host frames shift beyond inflation; 2005 combined total bar Rp 8.84T establishes baseline at 10.0s.
           16.1-45.1s: Proportional scale shock — single SOE case (Pertamina fuel import & blending, R.S.) surges to Rp 193.7T/year at 34.7s with riser + heavy impact, visually crushing 2005's 40-case bar to 4.5% height.
           45.1-67.3s: Split vertical comparison ledger: "2005 PLAYBOOK" (left: mark-ups, direct local budget skimming) vs "2026 PLAYBOOK" (right: supply chains, import quotas, state monopoly licensing).
           67.3-83.8s: Host punch-in + crimson judicial alert card: "COURTS CAPTURED · Tens of Billions to Fix Export Verdicts".
         Act 4 — Outro (act4_outro.mp4, ~44.5s):
           0.0-21.5s: 2005 -> 2026 vertical loss timeline climbs smoothly past Rp 8.84T and shoots vertically off-frame toward Rp 193.7T as voice summarizes the 21-year mutation.
           21.5-30.2s: Host returns full-frame ("loopholes stayed open, penalties failed to scare anyone off") with crisp typographic accent bar.
           30.2-44.5s: Closing question overlay inside Reels safe zone ("WHAT WENT WRONG WITH INDONESIA'S FIGHT AGAINST CORRUPTION?" + "Drop your thoughts in the comments") holding cleanly through the end.
BANNED:  Black empty frame 0; neon glow / bloom / lens flares / floating particles; purple/blue or mesh gradients; glassmorphism cards; generic cream-serif-pill aesthetic; breathing/floating idle loops on titles; corner HUD brackets; docked logos; covering the speaker's face; text under 28 px; text outside Reels safe zone (y 288-1248, x 120-888 / 780 below y=840); synthesized audio tones.
QA:      Run `npx hyperframes check --safe-zone reels --json` (0 errors), `npx hyperframes snapshot --review`, inspect beat sheets + cut seams + 360px phone readability across all 5 acts, verify no speaker face occlusion, verify audio sync and loudness.
```

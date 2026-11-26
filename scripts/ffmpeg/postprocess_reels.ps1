param(
  [string]$InputMp4 = "renders\final\corruption_2005_vs_today_raw.mp4",
  [string]$OutputMp4 = "renders\final\corruption_2005_vs_today_reels.mp4",
  [string]$ThumbnailJpg = "renders\thumbnails\cover_hook.jpg"
)

if (-not (Test-Path $InputMp4)) {
  Write-Error "Input MP4 not found: $InputMp4. Render with HyperFrames first."
  exit 1
}

New-Item -ItemType Directory -Force -Path (Split-Path $OutputMp4), (Split-Path $ThumbnailJpg) | Out-Null

# 1. Measure loudness (Pass 1)
Write-Host "Measuring loudness on $InputMp4..."
$pass1 = ffmpeg -i $InputMp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | Out-String
if ($pass1 -match '(?s)\{[^{}]*"input_i"[^{}]*\}') {
  $m = $matches[0] | ConvertFrom-Json
  $af = "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=$($m.input_i):measured_TP=$($m.input_tp):measured_LRA=$($m.input_lra):measured_thresh=$($m.input_thresh):offset=$($m.target_offset):linear=true"
} else {
  $af = "loudnorm=I=-16:TP=-1.5:LRA=11"
}

# 2. Reels-ready master: lossless H.264 stream copy + faststart + two-pass -16 LUFS AAC 192k audio
Write-Host "Mastering Reels-ready MP4 -> $OutputMp4..."
ffmpeg -y -i $InputMp4 `
  -c:v copy -movflags +faststart `
  -af $af -c:a aac -b:a 192k -ar 48000 `
  $OutputMp4

# 3. Extract crisp cover thumbnail at 3.4s (locked Rp 8,838,731,700,646 odometer + Rp 8.84 TRILLION)
ffmpeg -y -v error -ss 3.4 -i $OutputMp4 -frames:v 1 -q:v 2 $ThumbnailJpg

# 4. Verify output with ffprobe + ebur128
Write-Host "`n=== VERIFY STREAMS ==="
ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate,sample_rate -of compact=p=0 $OutputMp4
Write-Host "`n=== VERIFY LOUDNESS ==="
ffmpeg -i $OutputMp4 -af "ebur128=peak=true" -f null - 2>&1 | Select-String -Pattern "I:|LRA:|Peak:" | Select-Object -Last 6

---
name: reel-breakdown
description: Watch a reel frame by frame and read its words, then break down the hook (first 3 seconds), structure, pacing in cuts per 10 seconds, on-screen text, payoff and CTA, with what to steal and what not to. For your own reels it gets the video through the Otto MCP (or from the user) and pairs the breakdown with real skip rate and watch time. Use when someone says "break down this reel", "analyze this video", "why does this reel work", "study this creator's reel", "map out how this video is built", or "watch my reel and tell me what happens".
license: MIT
---

# Reel breakdown

Turns a reel into a timeline you can learn from: what is on screen and what is said at each moment, where the cuts fall, and how the first three seconds earn the rest. For your own reels it lines that timeline up with Instagram's numbers, so "the hook felt slow" becomes "skip rate 41% against your usual 30%, and the first cut lands at 2.5 s".

Read-only. It works on a temporary copy of the video only to look at it, and deletes it afterwards. It never reposts anything.

## 0. Setup

Follow the settings and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short: read `brand/settings.md` (or your memory of the user's Otto settings) first for workspace, accounts and output mode; ask only what's missing, as one multiple-choice question, and save the answers.

Then:
- If the workspace has more than one Instagram account (`meta_page_list`), ask which one.
- Ask which reel: your own (caption, date or link) or someone else's. **Someone else's reel comes only from the user**: a file they supply, or a link plus the file or screenshots they took. This skill never downloads other people's videos.
- **Pick the path for this environment:**

| Environment | Frames | Words |
|---|---|---|
| Claude Code / Cowork (a local machine) | local `ffmpeg` (`ffmpeg -version`); own reels download from `mediaUrl` | local Whisper (`whisper --help` or `python -c "import whisper"`), else the script or on-screen captions |
| claude.ai chat | the user uploads the video. Run `ffmpeg -version` in the code-execution sandbox: if it works, extract frames there with the commands below | the user pastes the caption and script; or read on-screen text from the frames |
| No ffmpeg anywhere | ask for 5-8 screenshots at 0, 0.5, 1, 2, 3 s and then every few seconds | the caption and script, pasted |

Neither ffmpeg nor Whisper is bundled with this skill, and it never installs them for the user.

## 1. Get the video and the numbers

**Your own reel (Otto)**
1. `meta_ig_list_media` (rowLimit 60). Find the reel. Its `mediaUrl` is a downloadable MP4 (use it on a local machine). It can be `null` even for a reel that plays, and in claude.ai chat the sandbox may not reach it; in both cases ask the user to save the video from the app and upload it.
2. `meta_ig_media_insights([id], metrics: views, reach, likes, comments, shares, saved, ig_reels_avg_watch_time, reels_skip_rate)`. Watch time is **milliseconds**; skip rate is already a **percent**. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
3. Baseline ("your usual"): use the one shared definition (see `otto-rules.md`): the median of your reels at least 3 days old from the **previous 28 days**. Take it from the brand card, settings or last weekly review if they state it; otherwise compute it from this pull and say how many days it covers. Never from just the last week or two. If the reel belongs to a series or period that runs well above or below that usual, show that comparison too, as a second line.

**Someone else's reel**: the user supplies the file (or screenshots) and, if they want, the link. No numbers except what's visible on the post; write those down with the date seen.

## 2. Extract (when ffmpeg is available; in a new empty temp folder, e.g. `reel-tmp/`)

```bash
curl -sL -o reel-tmp/reel.mp4 "<mediaUrl>"          # own reel only
ffprobe -v error -show_entries format=duration -of csv=p=0 reel-tmp/reel.mp4
# hook frames (for the page: 240 px)
for t in 0 0.5 1 2 3; do
  ffmpeg -v error -ss $t -i reel-tmp/reel.mp4 -frames:v 1 -vf scale=240:-2 -q:v 6 -y reel-tmp/h_$t.jpg; done
# a frame every 2.5 s for the whole reel (to look at)
for t in $(seq 0 2.5 <length>); do
  ffmpeg -v error -ss $t -i reel-tmp/reel.mp4 -frames:v 1 -vf scale=360:-2 -y reel-tmp/f_$t.jpg; done
# one contact sheet for a quick look (a frame every 2 s)
ffmpeg -v error -i reel-tmp/reel.mp4 -vf "fps=1/2,scale=180:-2,tile=6x3" -frames:v 1 -y reel-tmp/sheet.jpg
# cut times (scene changes); count them for pacing
ffmpeg -i reel-tmp/reel.mp4 -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*"
# one frame from the middle of each shot (for the page: 200 px); a shot runs from one cut to the next, the last one to the end
for m in <shot midpoints>; do
  ffmpeg -v error -ss $m -i reel-tmp/reel.mp4 -frames:v 1 -vf scale=200:-2 -q:v 6 -y reel-tmp/s_$m.jpg; done
# words with timestamps
ffmpeg -v error -i reel-tmp/reel.mp4 -vn -ac 1 -ar 16000 -y reel-tmp/audio.wav
whisper reel-tmp/audio.wav --model small --output_format srt --output_dir reel-tmp
```

Fill in `<length>` from ffprobe and the shot midpoints from the cut times. Scene threshold 0.3 catches hard cuts; for animated or slow-zoom footage, check the frames by eye and lower to 0.2 if cuts are missed. Small Whisper models mishear names and numbers: correct them against the caption or the on-screen text and say you did.

Look at every frame image (or every screenshot on the no-ffmpeg path; pacing is then an estimate from what changes between screenshots, and you say so). Read the on-screen text from the frames, not from memory.

## 3. Do

Build the timeline first, then judge.

**Hook, frame by frame (0-3 s).** For 0 s, 0.5 s, 1 s, 2 s, 3 s: what's in frame, the on-screen text, the spoken words, and movement. Then answer:
- Does frame 0 show something that makes sense with the sound off?
- Is there a question, tension or surprise by 1 s?
- Do the spoken line and the on-screen text say the same thing or two things?
- When does the first cut land?

**Structure.** Split the reel into beats from the cuts and the transcript: setup → tension → turn → payoff → CTA (rename to fit). Time each beat.

**Pacing.** Cuts per 10 s = cuts ÷ length × 10. Note where pacing changes and the longest shot.

**Payoff and CTA.** When does the promise from the hook get paid? Is there a CTA (comment, follow, save, link), and is it spoken, on screen, or only in the caption?

**Own reel: line it up with the numbers.**

| Signal vs your baseline | Look at |
|---|---|
| Skip rate higher | frames 0-1 s and the first spoken line |
| Avg watch low but skip fine | the beat where the avg watch time lands on the timeline |
| Shares low | was there a moment worth sending? name it or say "none" |
| Strong on all | which hook/structure choices to repeat |

Avg watch in seconds ÷ length × 100 = watch % (cap it at 100: replays can push average watch past the length). Put the avg-watch second on the timeline: that's roughly where the typical viewer was gone, an estimate, not a measured drop.

## 4. Output

**Visual (default):** fill `reel-breakdown.html` in this folder (format in `reel-breakdown-data.md`): the shots with a frame from each and its on-screen text, the sections (setup, tension, turn, payoff...), a `leave` marker at the average watch time and a `payoff` marker, the hook frames at 0, 0.5, 1, 2 and 3 s with pass/fail checks, structure, CTA, the key finding and one change. For your own reels add the KPIs against your usual. Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/breakdown-<slug>.html` (Claude Code / Cowork), or a canvas (ChatGPT). Write the verdict last, from the numbers on the page. **Chat** (settings `output: chat`, or the user asks): use the format below instead.

```markdown
# Reel breakdown: <reel link> (<length> s, <date>)
Numbers (own reel): views <n>, skip <x>% (baseline <y>%), avg watch <s> s = <p>% (baseline <q>%), shares/1k reach <n> (baseline <m>). Other's reel: visible numbers as of <date>.

## Hook, 0-3 s
| t | On screen | Text | Said | Note |
| 0 s | | | | |
| 0.5 s | | | | |
| 1 s | | | | |
| 2 s | | | | |
| 3 s | | | | |
Hook verdict: <one sentence>

## Timeline
| Beat | From-to | What happens | Said (short) |

Pacing: <n> cuts in <len> s = <x> per 10 s. First cut at <t> s. Longest shot <t> s at <time>.
Payoff at <t> s. CTA: <type, where, when>. Avg viewer leaves around <t> s (own reel).

## Steal
- <technique, not words>
## Don't steal
- <what's specific to their voice, brand, footage or audience; anything that would read as a copy>
## One change for the next reel
<single variable>; hand to `hook-writer` or `reel-script`.
```

Then delete the temp folder (`rm -rf reel-tmp`) and say so.

## Never

- Repost, re-upload or reuse someone else's footage, audio, script or on-screen text.
- Claim why a reel worked from one reel. Say "this suggests".
- Keep video copies after the breakdown, or download from accounts the user doesn't own. Other people's videos come only as files or screenshots the user supplies.
- Invent numbers for someone else's reel.

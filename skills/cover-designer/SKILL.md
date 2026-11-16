---
name: cover-designer
description: Design covers for Instagram Reels and YouTube Shorts in code, over a clean frame of your real footage, matched to your brand colours and fonts and checked for the 4:5, 3:4 and 1:1 crops, using your own reels pulled through the Otto MCP. Use when someone says "make a cover for this reel", "design my reel cover", "Shorts cover", "what should my cover say", "grid cover", or "my covers look messy on my profile".
license: MIT
---

# Cover designer

Makes the cover image for an Instagram Reel or a YouTube Short: a frame from your actual video with a few words on it, designed in code and rendered to PNG. A reel cover works mostly on your profile grid, where people decide what to open next, so it has to read when Instagram crops it.

Covers for Reels and Shorts only. Long-form YouTube thumbnails (16:9) are out of scope for this skill.

Never AI-generates an image. The picture is always a frame of the user's own footage, or a photo they supply.

## 1. Setup

Follow the settings, scope and capability rules ("How every skill talks to the user" in this folder's `otto-rules.md`). In short:
- Read `brand/settings.md` (or memory) for workspace, Instagram account and output mode; ask only what's missing, in one multiple-choice message, and save it.
- Output is visual by default (artifact / HTML file / canvas) unless settings say chat.
- Before offering to publish, check which tools this session has (rule 5). No publish tool: hand over the PNG and the steps.

Skill-specific:
- Read `brand/voice.md`, `brand/offer.md`, `brand/facts.md`. Brand colours and fonts: from Brand look in `brand/settings.md` (or the brand card); if missing, offer to read them from the user's site and confirm, or ask (hex codes and font names; "not sure" is fine, use a clean sans-serif and high contrast).
- Ask for the reel's topic and hook (weak hook? `hook-writer` first) and whether they have **reference covers** they like (their own or examples). Use references for layout and type style, never copy text or design outright.

## 2. Get the video and a clean frame

**Source of the video**
- The user's file (upload or a path in the folder), or
- For their own published reels: `meta_ig_list_media` (rowLimit 60 or less) returns `mediaUrl`, a downloadable MP4. It can be null for some reels; then ask for the file. In claude.ai, frames from that link may not export from an artifact (the video sits on Instagram's servers and the link expires): ask for an upload of the video or a screenshot of the frame.

**Pick candidate frames**
- Usually in the first 3 seconds, where the hook sits. Also check the payoff moment.
- Pull 6-10 frames (ffmpeg where available, or a `<video>` element seeked to timestamps in a browser) and show them as a contact sheet.
- Good frame: subject large and sharp, face visible or the product clear, not mid-blink or motion-blurred.

**Critical: the frame must be clean.** Use a frame of the actual footage with no burned-in captions, title text or on-screen graphics. Text baked into the frame will clash with the cover text and can't be removed cleanly.
- Video made in code or in a project folder: first look in the project's output folder for a caption-free render or a saved cover frame (e.g. `out/cover-frame.png`, `out/clean.mp4`); many pipelines keep one. Otherwise re-render that exact frame from the project (HyperFrames / Remotion / HTML / three.js) with the caption and title layers turned off.
- Otherwise: pick a frame where no text is on screen.
- No clean frame exists: ask the user for a clean frame or the raw footage. Don't paint over burned-in text.

## 3. Design the cover in code

Build it as HTML/CSS (SVG where useful) over the frame:
- **Canvas 1080 x 1920 (9:16).**
- **Safe area**: all important text and the subject's face inside the centre **1080 x 1350** (the 4:5 feed crop; also safe for the 3:4 profile grid). Also check the **1:1** centre crop (1080 x 1080), which some grid and share views use.
- **Text**: 2-5 words, the promise of the reel, not the hook word for word. Large enough to read on a grid tile about 3 cm wide: check at 120 px wide.
- **Readability**: a scrim, gradient or solid band behind text when the frame is busy. Contrast ratio 4.5:1 or better.
- **Brand**: colours and fonts from `brand/` (web fonts loaded in the HTML). Same text position and type style across covers so the grid looks like a set; vary the frame.
- **Claims**: only what `brand/facts.md` allows.
- Make **3 text options** on the same frame (or 2 frames x 2 texts), ranked.

Check against the grid: if `meta_ig_list_media` shows recent reels and the user shares a profile screenshot, note whether the new cover fits the last 9 (type, position, colour) and say so.

## 4. Render to PNG

| Environment | How |
|---|---|
| Claude Code / Cowork | Headless browser (Playwright or similar): screenshot the 1080x1920 element to PNG. Also export 4:5 and 1:1 preview crops |
| claude.ai / Claude desktop without a folder | An artifact showing each option at full size plus the crop previews, with a download button per PNG (canvas `toDataURL` or html-to-image in the page) |
| ChatGPT | Canvas with the HTML; the user screenshots or downloads |

Show all options side by side with the 4:5 and 1:1 crops outlined.

## 5. Where to upload

- **Instagram Reel**: set the cover when posting, in the Instagram app (Edit cover > Add from camera roll); the app may also let you change it later. If this Otto connection includes publishing (`meta_ig_publish_reel` in the tool list), the PNG can be uploaded to the Otto media library and passed as `coverMediaId` (9:16 like the video; Otto converts PNG to JPEG) when the reel is published, or `thumbOffsetMs` can pick a video frame instead, after the user approves the exact post. Otherwise use the app. Instagram doesn't let the cover change through the API after posting.
- **YouTube Shorts**: the user sets it in YouTube Studio or the YouTube app (where the option is available for Shorts, choose a custom thumbnail or the closest frame). This skill doesn't upload to YouTube.

## 6. Output

```
COVER: <reel topic> | frame at <s>s (clean: yes) | brand: <colours, font>
Options (best first):
1. "<text>"  -> cover-1.png  (4:5 safe: yes, 1:1 safe: yes, readable at 120 px: yes)
2. "<text>"  -> cover-2.png
3. "<text>"  -> cover-3.png
Grid fit: <matches your last 9 on type and position / breaks pattern because ...>
Upload: Instagram app at posting (or coverMediaId via Otto if available) | YouTube Studio for the Short
```

## Never
- Generate or AI-edit an image, or promise a generated photo. Frames and photos come from the user.
- Use a frame with burned-in captions or titles, or paint over them.
- Publish or schedule the reel; that's a separate approved step.
- Put a claim on the cover that `brand/facts.md` doesn't allow.

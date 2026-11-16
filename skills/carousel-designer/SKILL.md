---
name: carousel-designer
description: Builds a 7-10 slide Instagram carousel from a single idea, designed to be saved and shared, modelled on the structure of your own best carousels (ranked by saves and shares per 1,000 reach from Otto), with slides designed in code from named style presets in your brand colours and rendered to PNG. Use when someone says "make this a carousel", "make slides out of this", "swipe post about X", "design my carousel", or "redo my best carousel on a new topic".
---

# Carousel builder

Produces one carousel: slide-by-slide copy, the finished slides as 1080x1350 PNGs built in code, and the caption hand-off. The structure comes from what your own audience already saves, not from a generic template. Publishing or scheduling waits for an explicit yes and depends on what this Otto connection can do.

Slides are made in HTML/CSS/SVG only. This skill can't create photos: if you want "a dog in the background" or a product shot, supply the photo. Without one, slides are type, shapes and simple SVG graphics.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or memory) for workspace, Instagram account, timezone and output mode; ask only what's missing in one multiple-choice message, then save it.
- Output is visual by default (artifact / HTML file / canvas) unless settings say chat.
- Before offering to publish or schedule, check which tools this session has (rule 5).

Skill-specific:
- `otto_list_connections` to confirm Instagram (`meta_ig`). If not connected, `otto_connect_link` for `meta_ig` and continue with the default structure in step 3.
- Read `brand/voice.md`, `brand/offer.md`, `brand/facts.md`, `brand/winners.md`. Without `brand/`, ask: who it's for, the one action at the end, two words for how you talk. Suggest `brand-brain` once.
- Brand colours (hex) and fonts: from `brand/` or ask. Ask if they have photos to use, and any carousels they like as a style reference.
- Ask for the idea in one sentence. No idea yet: take one from `content-pillars` or `hook-patterns`.

## 1. Pull

1. `meta_ig_list_media` (rowLimit 60). Keep `mediaType: CAROUSEL_ALBUM` posts at least 3 days old. The list gives caption, permalink and timestamp only: no slides, no counts.
2. `meta_ig_media_insights` in batches of 25 with `reach, views, likes, comments, shares, saved, total_interactions`. Don't request reel metrics (`ig_reels_avg_watch_time`, `reels_skip_rate`) for carousels. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
3. Slide content is not in the API. For the top 3 carousels, ask the user for screenshots of every slide (or open the permalink and describe them). Never guess what a slide said.
4. Search wording for the cover line: `gsc_search_analytics` (last 90 days, dimensions `["query"]`, rowLimit 250). Use non-branded queries that match the idea.

**Fallbacks**
- Fewer than 3 carousels (common: many accounts post only reels): say so. Rank `IMAGE` posts and reels by saves per 1,000 reach instead to learn which *topics* get saved, and use the default structure in step 3.
- `ok: false` on any call: say which pull failed, continue with what you have, never fill the gap with invented numbers.

## 2. Rank your carousels

For each carousel: saves per 1,000 reach, shares per 1,000 reach, comments per 1,000 reach. Baseline = the median across your carousels.

| Result | Meaning | Use it as |
|---|---|---|
| Saves/1k ≥ 2x median | People kept it as a reference | Primary structure model |
| Shares/1k ≥ 2x median | People sent it to someone | Model for the cover and the "send this to" slide |
| Reach high, saves and shares at or below median | Cover worked, inside didn't | Borrow the cover style only |
| Everything below median | Not a model | Skip |

Fewer than 5 carousels: call the ranking "a hint, not a pattern".

From the top 1-2 models write the **slide-job sequence** with no topic words, e.g. `cover claim → why it matters → step 1 → step 2 → step 3 → common mistake → checklist → ask`.

## 3. Choose the shape

If you have a model, keep its sequence. If not, pick by the idea:

| The idea is... | Shape | Slides |
|---|---|---|
| A process | Cover → problem → 4-6 steps → checklist → ask | 8-10 |
| A list of mistakes | Cover → mistake/fix pairs, one per slide → summary → ask | 7-9 |
| A myth | Cover (the myth) → why people believe it → what's true → proof → what to do → ask | 7 |
| A before/after | Cover (the result) → before → 3-4 changes → after → how to copy it → ask | 8 |
| A comparison | Cover → criteria → option A → option B → when to pick each → ask | 7-8 |

## 4. Write the slides

Rules for every slide:
- **One idea per slide.** A headline (max ~8 words) plus at most 2 short supporting lines, ~30 words total. If it needs more, split it.
- **Cover (slide 1)**: a specific claim, number or question for the exact reader. Use the searched wording from GSC where it fits. Test: would the reader know in 2 seconds who it's for and what they'll get?
- **Slide 2** pays off the cover straight away. No "let's dive in".
- **The save slide** (second to last): a checklist, summary or template someone would screenshot.
- **Last slide**: one ask, matched to the goal (save / send / comment a word / follow / visit link). Only promise what exists (see `comment-to-lead` for keyword DMs).
- Claims only from `brand/facts.md` or the user. Numbers only from the pull or the user.
- Every word is new. If modelling a competitor's carousel the user pasted, copy the slide jobs, never the wording or design.

Then hand the caption to `caption-writer` (goal + keywords).

## 5. Design the slides in code

Use `slide-template.html` in this folder: one HTML file that renders N slides from a JSON block. Fill the JSON (brand colours, fonts, slides); don't redesign the layout. The small Otto mark sits in the template preview only, never on the exported slides.

**Style presets** (pick one as the base, mix where the slide job calls for it):

| Preset | Look | Best for |
|---|---|---|
| `clean` | White or light background, dark type, lots of space | Explanations, steps, the ask |
| `bold` | Full accent-colour background, huge type | Cover, a strong statement |
| `stat` | One giant number with a short line under it | A figure from `brand/facts.md` or the pull |
| `checklist` | Ticked list, 3-6 lines | The save slide |
| `beforeafter` | Split slide, before on top, after below | Results, mistakes and fixes |

Adapt each preset to the brand colours and fonts. Same template on every slide, slide number on each, swipe cue on slide 1, text large enough to read on a phone without zooming (headline 64 px or more at 1080 wide). Photos only when the user supplied them (`photo` field: a scrim keeps text readable).

**Render to PNG**: in Claude Code / Cowork, open the file with `?export=1` in a headless browser and screenshot each `#slide-N` at 1080x1350. In claude.ai, show the filled template as an artifact with a download step per slide. In ChatGPT, a canvas with the HTML. Name files `slide-01.png` ...

## 6. Publish or schedule (approval, capability check)

Only when the user asks. Show the final slides in order, the caption, and the date and time with time zone; wait for a yes. Then pick the path from what's in the tool list:
- **Scheduling** (`channel_submit_plan` available, if your Otto connection includes scheduling): upload the PNGs to the Otto media library (`media_create_upload` → upload → `media_complete`), then `channel_submit_plan` with `provider: "meta_ig"`, one step `op: "ig_publish_carousel"` with `mediaIds` (2-10, in slide order) and `caption`, plus `publishAt` (ISO with offset) and `timeZone` (IANA). With an `approveUrl`, say it will publish at that time **after they approve in Otto**. Say "scheduled" only when the result has `scheduled: true`.
- **Publish tools only** (`meta_ig_publish_carousel`, which takes public image URLs, 2-10): publish now on approval, or queue with `post-queue`.
- **Neither**: hand over the PNGs, the caption and the steps to post in the Instagram app.

## Output

Default is visual: the filled template with all slides, plus this summary. Chat only if settings or the user say so.

```
## Carousel: <working title>
Model: <your carousel, date, saves/1k vs median> | or "default <shape> (no carousel history)"
Goal: <save / send / comment / follow / link>   Search phrase used: <query or "none">

| # | Job | Preset | Headline | Supporting lines |
|---|-----|--------|----------|------------------|
| 1 | Cover | ... | ... | ... |
| ... |
| N | Ask | ... | ... | ... |

Preset: <base preset> | Brand: <colours, fonts> | Photos: <user-supplied / none>
Files: slides.html, slide-01.png ... slide-NN.png
Caption: hand to caption-writer (goal, keywords above)
Next check: saves and shares per 1,000 reach at day 3 and day 7 vs your carousel median
```

## Never

- Generate images with AI, or promise a photo the user didn't supply.
- Publish or submit a plan without showing the exact post and getting a yes.
- Say a post is scheduled without `scheduled: true` in the result.
- Invent what a past carousel's slides said, or any metric.
- Reuse another account's slide text or design.

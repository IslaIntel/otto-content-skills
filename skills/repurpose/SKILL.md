---
name: repurpose
description: Takes one proven piece (your top YouTube video, a breakout reel, or a blog post that ranks, chosen from your Otto data) and turns it into reels, a carousel, a LinkedIn post, a Facebook post and a blog outline, each fitted to its platform, plus the order to release them. Use when someone says "repurpose this", "turn this video into posts", "get more out of this blog", "cross-post this", "one video into a week of content", or "what should I do with my best video".
license: MIT
---

# Repurpose

Gets more from something that already worked. The source is picked from your own numbers, then broken into parts, and each part is rebuilt for the platform it goes to. A straight copy-paste across platforms is not repurposing. Writes drafts only; posting goes through `posting-plan` (Otto scheduling if your connection has it, else `post-queue` or by hand).

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or the assistant's memory) for workspace, accounts, default platforms and output mode. Ask only what's missing, in one bundled multiple-choice question, and save the answers.
- Make outputs only for the platforms the user named, else the defaults; ask once if there are none ("All connected" as an option). Don't write for a platform the business doesn't use unless asked.
- Output is visual by default (artifact / HTML file / canvas) unless settings or the user say chat.

Also read `brand/voice.md`, `brand/offer.md`, `brand/facts.md` if they exist. If the user already named a source, skip to step 2.

## 1. Pick the source (from data)

Pull candidates from the last 90 days and pick one:

| Source | Pull | Counts as a winner when |
|---|---|---|
| YouTube video | `youtube_top_videos` (startDate, endDate, rowLimit 25); `youtube_channel_analytics` with dimensions `["video"]`, metrics `["views","averageViewPercentage","subscribersGained","shares"]`, **sort `-views`** | Views ≥ 2x the channel median, or average view % (capped at 100: looping Shorts go over) at least 10 points above the channel median |
| Instagram reel | `meta_ig_list_media` (rowLimit 60) → `meta_ig_media_insights` (batches of 25: `views, reach, shares, saved, comments, ig_reels_avg_watch_time, reels_skip_rate`) | Shares or saves per 1,000 reach ≥ 2x your reel median |
| Blog post | `wordpress_list_posts` (if WordPress is connected), plus `gsc_search_analytics` dimensions `["page"]` and `ga4_landing_pages` | Top pages by clicks / sessions; queries it ranks for show the angle people want |
| Facebook / LinkedIn post | `meta_page_posts` + `meta_page_post_insights`; `linkedin_page_posts` | Facebook: clearly above that Page's median. LinkedIn posts carry no per-post numbers: ask the user |

Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).

Prefer a source that won on **shares, saves, watch % or search clicks** over raw views: those show the idea itself landed. Fewer than 5 posts on a platform = no median; say so and let the user pick.

**Getting the content**
- YouTube: Otto returns numbers and titles, not transcripts, and `voc_fetch_url` on a YouTube page returns nothing useful. Ask the user to paste the transcript (YouTube Studio > Subtitles) or a summary.
- Reel: caption comes from `meta_ig_list_media`; `mediaUrl` is a downloadable MP4 the user can watch. Ask for the spoken script if it isn't in the caption.
- Blog: `voc_fetch_url(url)` returns the page text (maxChars up to 8000). If WordPress isn't connected (or the call returns `ok: false`), find the post URL via the GSC `page` report and fetch it that way.
- Any failed call: say so, ask the user to paste the content. Never reconstruct a source from its title.

## 2. Break it into parts

List every usable part, one line each, with where it appears (timestamp, paragraph):
- **Claims** (a point of view someone could disagree with)
- **Steps** (a how-to sequence)
- **Story** (a moment with a before and after)
- **Numbers** (only ones in the source or `brand/facts.md`)
- **Mistakes / myths**
- **Quotable lines** (said well enough to stand alone)
- **Questions** the source answers (check against GSC queries; a match means search demand)

## 3. Rebuild per platform

| Output | Built from | Fit rules | Hand off to |
|---|---|---|---|
| 2-3 reels / Shorts | One claim, mistake or story each | New first line per reel; one idea; vertical; on-screen text carries the point with sound off | `hook-writer`, `reel-script`, `cover-designer` |
| Carousel | Steps, mistakes or a checklist | 7-10 slides, one idea each, a save slide | `carousel-designer` |
| LinkedIn post | The claim + the story behind it | First 2 lines stand alone; short paragraphs; no hashtag pile; end on a question only if the author will reply to answers | `linkedin-post` |
| Facebook post | The story or the most useful tip | Conversational; a native photo or clip beats a bare link; local angle if relevant | `caption-writer` |
| Blog outline | The whole source | H1 = the main search query; H2s = the questions from GSC; embed the original video | none: write the outline here |

Each output gets its own opening line. Facts and claims stay identical everywhere; only the shape changes. Remove the source platform's watermark before re-uploading video.

## 4. Release order

Default order, adjusted to the data:
1. **Day 0**: the strongest short piece on the platform where the source won.
2. **Day 1-2**: the carousel (or the LinkedIn post for a B2B audience).
3. **Day 3**: check the first piece against its platform median. Below median after 72 hours: rewrite the hook of the next pieces, don't just keep pushing the same angle.
4. **Day 3-7**: remaining reels and Facebook.
5. **Blog**: first if GSC shows queries for the topic with no page answering them; otherwise last, linking all pieces.

Links to the website get UTM tags (`utm-builder`) so `ga4_run_report` with `sessionCampaignName` and `sessionManualAdContent` (utm_content) can show which piece sent visits. Put the dates into `posting-plan`.

## Output

Default is visual (artifact / HTML file / canvas) unless settings or the user say chat. Content:

```
## Repurpose: <source title>
Why this source: <metric> = <value> vs median <value> (<platform>, <window>)

### Parts
| # | Type | Part | Where in source |

### Pieces
| # | Platform | Format | Built from part | Opening line | Goal |
Then each draft in full (or the hand-off skill named).

### Release order
| Day | Platform | Piece | Check |
```

## Never

- Paste the same text on every platform.
- Add numbers, quotes or claims that aren't in the source or `brand/facts.md`.
- Publish or schedule from this skill.

---
name: caption-writer
description: Writes the caption, an optional call to action matched to the post's goal, alt text and 3-5 hashtags, learning from which of your own past captions performed (views, reach, search clicks) and using keywords from your real search data in Otto, in your own caption template if you have one. Use when someone says "write a caption", "what do I write under this", "hashtags for this", "keyword research for my reel", "what should my CTA be", or "post copy".
---

# Caption writer

Writes the words around a post so the right people find it and do one thing. Keywords come from what people actually type into Google about this business, because captions, on-screen text and alt text are searchable inside Instagram and YouTube, and posts from both can show up in Google results. It also checks your own history: do your best captions share traits your worst ones don't? Writes copy only; posting is someone else's job (`carousel-builder`, `content-calendar`, `post-queue`).

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or memory) first: workspace, accounts, output mode, `caption_template`, `cta`. Ask only what's missing, in one multiple-choice message, then save it.
- Output is visual by default (artifact / HTML file / canvas) unless settings say chat.

Skill-specific:
- `otto_list_connections`: note whether `gsc` and `gbp` are connected.
- Read `brand/voice.md`, `brand/offer.md`, `brand/facts.md`. Without them, ask for two sample captions the user liked and the one action they want people to take.
- Ask: what the post is (or the script / slides), the platform, and the **goal**: save, share, comment, follow, DM, or click. One goal.
- **CTA setting** (`cta: on | off | ask`): if it isn't set, ask once ("End captions with a call to action? Always / Never / Ask me each time") and save it. `off` means no ask line at all.

## 1. Pull

1. **Search Console**: `gsc_search_analytics`, last 90 days, dimensions `["query"]`, rowLimit 500. If the topic has a clear word, add `dimensionFilterGroups` with `contains` on `query`. Optionally a second call with `["query","page"]` to see which page each query lands on.
2. **Google Business Profile** (local businesses): `gbp_search_keywords` (rowLimit 100) for the searches that showed the profile, with monthly impressions. If it returns `ok: false` / not connected, say so, offer `otto_connect_link` for `gbp`, and continue without it.
3. **Your own captions**: `meta_ig_list_media` (rowLimit 60) for captions, then `meta_ig_media_insights` (batches of 25: `views, reach, likes, comments, shares, saved`; reel-only metrics only for `VIDEO` ids). Facebook: `meta_page_posts` + `meta_page_post_insights` (`post_media_view`). Search: `gsc_search_analytics` with dimensions `["page"]` (rowLimit 500) for clicks on post or blog URLs a caption points to (see `search-and-social`).
4. **YouTube titles** (if connected): `youtube_top_videos` for the last 90 days. Titles that earned views show the wording your audience clicks.
5. **Other accounts' captions** (optional): if `meta_ig_business_discovery` is in the tool list, pull recent captions from accounts the user names, for comparison only. Without it, use captions the user pastes. Never copy their wording.

If neither GSC nor GBP is connected or has data, say "no search data; keywords below are from your comments and captions, not search volume". Pull wording from `comment-mining` or the user. Never invent search volumes.

## 2. Learn from your own captions

Rank your posts (3+ days old, reach at least half the median) by views or reach, and by search clicks where a page is linked. Compare the top 10 with the bottom 10 on:

| Trait | Measure |
|---|---|
| Length | characters |
| First line | question / number / statement / name of the problem; contains a search phrase? |
| Keywords | non-branded search phrases present |
| CTA | none / save / share / comment / DM / link |
| Hashtags | count |

Report plainly whether traits track performance: `Top 10: median 140 chars, 7 open with a number; bottom 10: 420 chars, 2 with a number.` If the groups look the same, say "your caption traits don't track performance here; the video or topic matters more". Under 5 posts per side: "too few to tell". Time confounds traits: if a style only ran in one period, say so (see `otto-rules.md`). Use what tracks; ignore the rest.

## 3. Pick the keywords

1. Split queries into **branded** (the business name, its misspellings, product names) and **non-branded**. Branded queries tell you people already know you; they don't help strangers find you. Use non-branded for discovery.
2. Keep non-branded queries that match this post's topic. Rank by impressions; note position (a query where you sit at position 5-15 is one where more content can help).
3. Choose:
   - **Primary phrase**: the one a stranger would type to find this post. Goes in the first line, the on-screen text, and is said out loud in a video.
   - **2-3 supporting words**: synonyms or the local area, used naturally in the body and alt text.
4. Queries with impressions but the wrong audience (another industry, another meaning of the word, position 50+) don't count: drop them. Fewer than ~10 relevant impressions for the topic in 90 days = "too little search data on this topic"; fall back to the words customers use in comments.

## 4. Choose the CTA (if on)

Skip this step when `cta: off`. With `cta: ask`, ask once for this post.

| Goal | Reason line (why they should) | Ask |
|---|---|---|
| Save | When they'll need it again | "Save this for your next <situation>" |
| Share | Who it's for | "Send this to the <person> who <problem>" |
| Comment | A question with a short, easy answer | A specific either/or or "which one are you?" |
| Follow | What comes next | "Part 2 on <day>" / name the series |
| DM / keyword | What they get, exactly | "Comment <WORD> and I'll send <thing>" (only if it's wired; see `comment-to-lead`) |
| Click | What's on the other side | "Link in bio: <what they'll find>" (track it with `utm-builder`) |

One ask per post. If the user wants two, keep the one that matches the goal and say why the other was dropped. If step 2 shows one CTA style (or no CTA) clearly beat the others on your account (5+ posts each), prefer it.

## 5. Write

**Caption template**: if settings have `caption_template`, follow it exactly (structure, line breaks, sign-off, hashtag rule) and fill it with this post's content. Don't add parts it doesn't have. If there's no template and the user likes a caption you wrote (or one of their own), offer once to save it as their template in `brand/settings.md`. Never force a house style on them.

Without a template:

- **First line** (Instagram shows ~125 characters before "more"; LinkedIn ~200; Facebook a few lines): carries the primary phrase and a reason to keep reading. Not a repeat of the cover.
- **Body**: 2-5 short lines of the actual value or story. Plain words from `brand/voice.md`.
- **CTA** (when on): the reason line, then the ask.
- **Alt text** (images and carousel slides): what's in the image plus the primary phrase where it describes it honestly. 1-2 sentences.
- **YouTube / Shorts**: a title under ~60 characters starting with the primary phrase; the description's first 2 lines say what the video answers.
- **Hashtags: 3-5, in the caption.** Each earns its place:

| Slot | What | Example (a dog groomer in Leeds) |
|---|---|---|
| Topic | The subject in the words people search | #doggrooming |
| Specific | The narrower problem this post solves | #doublecoatgrooming |
| Place | Only for local businesses | #leedsdogs |
| Series / brand | Only if you use it every time | #groomroomtips |

Otto has no hashtag volume data. Tell the user to type each tag into Instagram search before posting and drop any tag that is off-topic, flooded with spam, or empty.

## Output

Default is visual (artifact / HTML file / canvas) with a copy button for the caption; chat if settings or the user say so.

```
## Caption: <post>
Goal: <goal>   Platform: <platform>   CTA: <on/off/ask>   Template: <yours / none>
What your captions show: <one line from step 2, or "traits don't track performance" / "too few to tell">
Primary phrase: "<phrase>" (GSC: <impressions> impr., pos <x> | GBP: <impressions>/mo | "from comments, no search data")

**Caption**
<first line>
<body>
<reason line> <ask>
<hashtags>

**Alt text**: <...>
**Say / show in the video**: "<line with the primary phrase>"
**Hashtag reasons**: #a (topic) ... #d (series)
**Dropped**: <second CTA or keyword and why>
```

## Never

- Invent search volumes, hashtag sizes or past results.
- Stuff keywords: if the phrase reads awkwardly, use it once.
- Promise a DM, freebie or link that doesn't exist yet.
- Post or schedule anything from this skill.
- Override the user's caption template or CTA setting, or copy another account's caption.

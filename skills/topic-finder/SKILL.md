---
name: topic-finder
description: Research what to make next by combining four kinds of evidence through the Otto MCP (what people search for in Google, what gets watched on YouTube (yours through Otto; other channels from what you paste), what people complain about online, and your own breakout posts) into a ranked topic list where every topic shows its proof. Use when someone says "research my niche", "what topics would do well for me", "find topics that will work", "what's working in my industry", "give me content ideas with data", or "what are people searching for".
license: MIT
---

# Topic finder

Ideas are cheap; ideas with evidence are rare. This skill stacks independent signals for each topic (searched, watched, complained about, already worked for you) and ranks topics by how many signals agree. It hands the winners to `viral-reel-planner` and `hook-writer`.

Read-only.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, timezone, output mode. Ask only what's missing, as one multiple-choice question, and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". A platform in scope with nothing in the window gets one line, never an empty table.

Then:
- If the workspace has more than one Instagram or Facebook account (`meta_page_list`), ask which one.
- Read `brand/offer.md`, `brand/audience.md`, `brand/winners.md`, `brand/personas.md` if present.
- Ask: the niche in a few words, the place you serve (if local), and up to 5 YouTube channels or creators the user watches or competes with (links). Window: last 90 days.

## 1. Pull

**A. Searched (Google)**
- `gsc_search_analytics`, dimension `query`, rowLimit 500, last 90 days. Then the previous 90 days for comparison.
- Keep: questions (how, why, what, can, best, vs, cost, near me), queries with impressions ≥ 50 and position worse than 8 (people search, you're barely there), and queries whose impressions grew 50%+ period over period.
- `gbp_search_keywords` if Google Business Profile is connected.

**B. Watched (YouTube)**
- Your channel: `youtube_top_videos` (90 days) and `youtube_channel_analytics(dimensions ["video"], metrics ["views","averageViewPercentage","subscribersGained","shares"], sort "-views", rowLimit 200)` (200 is the API maximum for this dimension). Subscribers gained per video is the best "this topic builds an audience" signal you have.
- `youtube_traffic_sources` to see if YouTube search drives views (if yes, video titles are search topics too).
- Other channels: Otto's YouTube tools read only your own channel. Use a YouTube public-stats tool if one is in this session; otherwise ask the user to paste titles and view counts of each channel's last 20-30 videos (or screenshots).

**C. Complained about (customer language)**
- `voc_search_reddit(query)` with 3-5 problem phrases (not brand names). Often returns `http_403`: say Reddit is unavailable and continue.
- `voc_fetch_url` on 1-3 public forum threads, review pages or Q&A pages the user names.
- Your own comments: run `comment-insights`, or reuse its clusters from `brand/audience.md`.

**D. Worked for you (your breakouts)**
- `meta_ig_list_media` (rowLimit about 1.2 x posts per day x 90; if the result is saved to a file, read it with code) + `meta_ig_media_insights` (batches of 25): `views, reach, shares, saved, comments` for every post; add `ig_reels_avg_watch_time` and `reels_skip_rate` for `mediaType: VIDEO` ids only (one image in the batch fails the whole call).
- `meta_page_posts` + `meta_page_post_insights`. LinkedIn posts carry no per-post numbers through Otto, so they can't count as breakouts.
- Breakout = 2x your usual reach (median of posts at least 3 days old from the previous 28 days), or 2x your median shares/saves per 1,000 reach. Use `brand/winners.md` if it's current.

If a whole source is missing, the topic score just has fewer possible signals; say which.

## 2. Do

**Step 1. Normalize to topics.** Turn every query, video title, complaint and breakout into a short topic in the customer's words ("knee pain after running", "website not showing on Google"). Merge near-duplicates.

**Step 2. Score each topic.** One point per independent signal:

| Signal | Point if |
|---|---|
| Searched | a query group with ≥ 50 impressions in 90 days, or rising 50%+ |
| Search gap | you rank worse than position 8 for it (opportunity) |
| Watched (yours) | one of your videos on it beat your median views or subscribers gained |
| Watched (others) | a supplied channel's video on it got 2x that channel's median views |
| Complained | 3+ independent complaints/questions (Reddit, forums, your comments) |
| Breakout | one of your posts on it was a breakout |
| Sellable | it leads to something in `brand/offer.md` |

Rank by score, then by search volume. Score 1 topics go to "untested ideas". A topic backed by only one post or one person stays a hypothesis.

**Step 3. Pick an angle per top topic.** For each of the top 10, write the angle the evidence suggests: the question to answer, the mistake to name, the myth to correct, the comparison to make. Note the format that fits (reel, carousel, long video, or a blog post for search-led topics). Give each ranked topic a call: **Take** (score 3+, fits what you sell and how you talk), **Adapt** (score 3+, but the usual angle or format isn't you: say what to change), **Skip** (score 1-2 with nothing sellable, or it doesn't serve your buyers). Score 2 with something sellable: **Adapt** or the watch list; say which.

**Step 4. Don't copy.** For topics found on other channels, note the technique (format, structure, length) and write a different take.

## 3. Output

**Visual (default):** fill `dashboard.html` in this folder (format in `dashboard-data.md`). `blocks`: a `stats` block (topics scored, sources used), a wide `table` of ranked topics (topic, score, the signals that fired, and a `pill` column Take / Adapt / Skip), then `cards` for the top 5 with their evidence, and a `list` of sources that were unavailable. Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/topic-finder-<YYYY-MM-DD>.html` (Claude Code / Cowork), or a canvas (ChatGPT). Write the verdict last, from the numbers on the page. **Chat** (settings `output: chat`, or the user asks): use the format below instead.


```markdown
# Topic finder: <niche> (<date range>)
Sources: GSC <n queries> · YouTube own <n videos> / others <n videos from n channels> · complaints <n> (Reddit: ok / unavailable) · your posts <n>.

## Ranked topics
| # | Topic (their words) | Score | Searched | Watched | Complained | Your breakout | Sellable | Angle | Format |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | 5/7 | "<query>" 640 impr, pos 11 | your video: 2.3x median, +18 subs | 6 comments | reel 3x median reach | yes | <angle> | reel |

## Top 3, ready to hand off
1. <topic>: evidence in one line. First line idea: "<in their words>". Next: `viral-reel-planner` → `hook-writer`.

## Search topics better as a page than a post
<queries where a website page would win; hand to `search-and-social`>

## Untested ideas (one signal)
<list>
```

## Never

- Invent search volumes, view counts or complaints. Every cell in the table comes from a pull or a paste.
- Present another creator's video as something to re-upload or script word for word.
- Install tools or scrape accounts for the user.

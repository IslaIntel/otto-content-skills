---
name: competitor-watch
description: Break down 3-5 rival accounts to find the pattern behind their best posts, what they say in their ads, and the gaps you can own, then compare it all with your own numbers pulled through the Otto MCP. Use when someone says "break down this competitor", "why is this account growing", "what are my competitors posting", "what ads are they running", "how do I compare to them", or "what are they doing that I'm not".
license: MIT
---

# Competitor watch

Finds the mechanism behind a rival's best work and the openings they leave, then sets it next to **your** baseline so you know which of their moves would actually be new for you. The goal is a lane to own and three things to make, never a copy of their posts.

Read-only. This skill never posts, comments, follows or messages anyone.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, timezone, output mode. Ask only what's missing, as one multiple-choice question, and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". A platform in scope with nothing in the window gets one line, never an empty table.

Then:
- If the workspace has more than one Instagram or Facebook account (`meta_page_list`), ask which one.
- Ask for **3 to 5 rivals**: name, website, and their Instagram handle and other profile links you care about. Ask which country they sell in (for ad research). If the user names more than 5, ask them to pick the 5 that steal real customers.
- Read `brand/offer.md`, `brand/audience.md` and `brand/winners.md` if they exist.

## 1. Pull

**Their public material, in this order**

Check the tool list first and use the first source that works for each rival; say which one each card came from.

1. **Tools in this session**
   - `meta_ig_business_discovery`, if present: per rival handle, followers and recent posts with captions, like and comment counts and timestamps. Works for business and creator accounts only (a personal account returns nothing: say so). Views may not be included; then rank their posts on likes + comments.
   - A YouTube public-stats tool for other channels, if one is present (Otto's YouTube tools read only your own channel).
   - Ad library, if enabled: `ad_library_find_advertisers(query: <rival name or category>, country)` to find each rival's advertiser Page, then `ad_library_list_ads(pageId, country, limit 30)` for copy, CTA, format, start dates and platforms. If it returns `ok: false` (e.g. `ad_library_disabled`), say ad research is off right now, give the returned `libraryUrl` if any, and ask for pasted ad text or screenshots of 5-10 active ads. Ad longevity and volume are **not** performance: an ad running 90 days is a hint it pays, never proof.
   - `voc_fetch_url` on each rival's homepage, pricing page and one service or product page (`maxChars` 6000; pass `query` such as "pricing", "reviews", "guarantee" on long pages). A JavaScript-only page can come back nearly empty: say so and ask for a screenshot.
2. **What the user supplies**: links, screenshots of each rival's **last 12-20 posts with the visible numbers**, or videos they downloaded themselves. Break down supplied videos with `reel-breakdown`. If they share fewer than 8 posts per rival, say the read is thin.
3. **Last resort, clearly labelled**: the user browses the rivals themselves, in their own browser, ideally logged in with a separate account, and you analyse what they paste or screenshot. Say plainly: logging in to Instagram with automation can get an account restricted, so this skill never logs in for them and never drives a login.

**Your own numbers (for the comparison)**

- `meta_ig_list_media` (rowLimit 60) + `meta_ig_media_insights` (batches of 25): `views, reach, likes, comments, shares, saved, ig_reels_avg_watch_time, reels_skip_rate`. Watch time is in **ms**; skip rate is already a percent. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
- Platforms in scope only: `meta_page_posts` + `meta_page_post_insights` (`post_media_view`, `post_reactions_by_type_total`), `linkedin_page_posts`, `youtube_top_videos`.
- `gsc_search_analytics` (last 28 days, dimension `query`, rowLimit 200): what people already find you for.

Never invent a rival post, ad, number or quote. Anything you couldn't see is "not seen", not "doesn't exist".

## 2. Do

**Per rival, find their winners against their own median.** Use the visible metric (views for reels, likes+comments otherwise). Winner = 2x their median or more. Fewer than 8 posts supplied: "too few to tell", describe instead of rank.

For each rival, fill one card:

| Field | What to write |
|---|---|
| Who they talk to | the audience their copy names or clearly implies (quote it) |
| Promise | the outcome they sell, in their words, with source URL |
| Proof style | reviews, numbers, before/after, founder story, none |
| Winning trait | what their winners share that the rest lack (topic, hook shape, format, length, face on camera) |
| Hook template | their opening reduced to a fill-in pattern, e.g. "The [thing] every [audience] gets wrong" |
| Cadence | posts per week, share of each format, how they follow up a hit (repeat, series, nothing) |
| Ads | angles, offers and CTAs that repeat across their live ads; oldest still running |
| Asked, not answered | questions in their comments they never made a post about (from screenshots) |

**Then compare with you.** Build a side-by-side on the things you can both measure:

| | Rival A | Rival B | ... | You (median, last 4 weeks) |
|---|---|---|---|---|
| Posts per week | | | | |
| Main format | | | | |
| Winner topic(s) | | | | your top 3 from `brand/winners.md` or the pull |
| Promise | | | | from your site |

Their visible views and your API reach are **different numbers**; never put them in one column as if comparable. Compare patterns, not totals.

**Find the gaps you can own.** A gap counts only if it passes all three:

1. Rivals leave it alone (or do it badly) across the material you saw.
2. Your audience asks for it: it appears in your comments (`comment-insights`), your GSC queries, or their unanswered comments.
3. You can back it: a service you offer, proof you have (`social-proof-finder`), or a result you can show.

A gap that fails test 3 goes in "not yet" with what proof it would need.

## 3. Output

Default is visual: an artifact (claude.ai / Claude desktop), an HTML file opened in the browser (Claude Code / Cowork), or a canvas (ChatGPT), built in code with the sections below. If settings say `output: chat` or the user asks for chat, give the same content as markdown in chat.

```markdown
# Competitor watch: <business> vs <rivals> (<date>)
Sources per rival: business discovery / supplied by you / you browsed; <n> pages read, <n> ads seen (or "ad research off: pasted by user").

## What each rival does
<one card per rival, from the table above, every claim with a source link or "from your screenshot">

## Side by side
<comparison table>

## Patterns worth borrowing (technique only)
1. <pattern>: seen at <rival>, <n> of their <n> winners. You do this: yes / no / sometimes (evidence).

## Gaps you can own
| Gap | Rivals | Your demand evidence | Your proof | Confidence |

## Three posts to make this week
1. <idea in your voice>: fills gap <x>; first line: "<hook>"; format; hand to `viral-reel-planner` or `hook-writer`.

## Not seen / not known
<what you couldn't check and how the user can fill it>
```

## Never

- Copy a rival's caption, script, visuals or ad wording. Reduce to a pattern, then write it new.
- State a rival's results, revenue or ad performance as fact. "Their ad has run since <date>" is an observation; "their ad works" is a guess.
- Call something absent because you didn't see it.
- Comment on, follow or message a rival, or publish anything.
- Scrape profiles, log in to anyone's account, or automate a browser session on a social platform.

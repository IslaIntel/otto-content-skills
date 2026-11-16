---
name: search-and-social
description: Connect what people search with what you post. Uses Search Console queries and pages, Google Business Profile search keywords, YouTube search terms and GA4 social traffic through Otto to find topics people search that your social content hasn't covered, the exact words to put in captions, titles and alt text, and which platforms and pages actually send visitors to your site. Use when asked "what are people searching for", "which keywords should my captions use", "does social send anyone to my site", "make my posts findable on Google", or "turn my search data into content".
license: MIT
---

# Search and social

People type their problems into Google and YouTube in plain words. Those words are the best brief a business has: they show what to post about and how to phrase it. Social posts are searchable too (Instagram search reads captions, and alt text may help too; public Instagram reels and YouTube videos can appear in Google results). This skill does three jobs: finds **gaps** (searched, not posted), hands over **keywords** for captions, titles and alt text, and shows which posts and platforms **drive site visits**. Read-only.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, timezone, output mode. Ask only what's missing, as one multiple-choice question, and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". A platform in scope with nothing in the window gets one line, never an empty table.

Then:
- `otto_list_connections`: this skill needs at least GSC or GA4. If neither is connected, `otto_connect_link` with source `search_console` and `google_analytics`, and stop.
- Read `brand/offer.md` and `brand/audience.md`. Ask for the service area if the business is local.
- Window: last 90 days for search (enough volume for small sites), ending 3 days ago (GSC lags).

## 1. Pull

**What people search (Google)**
- `gsc_search_analytics` dimensions `["query"]`, rowLimit 500. Keep `clicks, impressions, ctr, position`.
- `gsc_search_analytics` dimensions `["query","page"]`, rowLimit 500: which page Google shows for each query.
- `gsc_search_analytics` dimensions `["page"]`: which pages earn search traffic.
- Question and comparison queries: dimensions `["query"]` with `dimensionFilterGroups` `[{filters:[{dimension:"query", operator:"includingRegex", expression:"(^| )(how|what|why|when|can|does|is|should|best|vs|cost|price)( |$)"}]}]`.
- Optional: `type: "video"` or `"image"` to see searches where the site appears in video or image results.

**What people search (local)**
- `gbp_search_keywords`: monthly searches that showed the business profile. Often not connected (`ok: false`, "not connected"): say so and offer `otto_connect_link` with source `business_profile`.

**What people search (YouTube)** (only if YouTube is in scope; Google search data is always in scope, since it's about the business, not a platform)
- `youtube_traffic_sources`: how many views come from `YT_SEARCH` vs Shorts feed, suggested, external.
- `youtube_channel_analytics` dimensions `["insightTrafficSourceDetail"]`, metrics `["views"]`, filters `insightTrafficSourceType==YT_SEARCH`, sort `-views`, rowLimit 25 (the API maximum for this dimension): the terms. This list is noisy (a word in a title matched an unrelated search). Keep only terms related to the business.

**What you've posted** (platforms in scope only)
- `meta_ig_list_media` (rowLimit about 1.2 x posts per day x 90) captions; `meta_page_posts`; `linkedin_page_posts`; `youtube_top_videos` titles for 90 days.

**What social sends to the site (GA4)**
- `ga4_run_report` dimensions `["sessionSource","landingPage"]`, metrics `["sessions","engagedSessions","keyEvents"]`, `dimensionFilter` `{filter:{fieldName:"sessionDefaultChannelGroup", stringFilter:{matchType:"EXACT", value:"Organic Social"}}}`.
- Same report with `sessionCampaignName` added, to see UTM-tagged posts.
- `ga4_run_report` dimensions `["sessionDefaultChannelGroup"]`, metrics `["sessions"]`: the Organic Social and Organic Search totals for the KPIs.

`ok: false` on any call: say which source is missing and continue.

## 2. Build the search topic list

1. Drop brand-name queries (the business's own name and misspellings) into a separate "people looking for you" bucket.
2. Cluster the rest into topics: queries that mean the same thing ("how much does X cost", "X price") are one topic. Keep the 2-3 most common phrasings word for word.
3. Per topic: total impressions, clicks, best position, the page Google shows.
4. Add GBP keywords and YouTube search terms to matching topics, or as new topics.

## 3. Find the gaps

Match each topic to your posts (caption, title, or on-screen topic if you know it).

| Search demand | Posted on social? | Site page ranks (pos ≤ 10)? | Read |
|---|---|---|---|
| high | no | yes | **Post gap**: people search it, you have the answer on your site, nobody on social hears it. Easiest win. |
| high | no | no | **Full gap**: content for both. Hand to `topic-finder`. |
| high | yes | no | Social covers it; your site doesn't. Flag for the website. |
| high | yes | yes | Covered. Check your captions use the searcher's words. |
| low | yes, a lot | n/a | You talk about it more than people search it. Fine for loyalty; don't expect discovery. |

"High" = top third of topics by impressions for this site. Small sites: rank, don't use absolute cut-offs.

Questions with high impressions and low CTR at position 1-5 are a sign the answer isn't obvious from the result, or that Google already answers it on the results page (a snippet), so few people click. A short video or carousel answering exactly that question is a strong post.

## 4. Keywords for posts

For each of the top 10 topics, give:
- **Caption first line**: the searcher's phrasing, natural, in the first 125 characters (the part shown before "more").
- **Alt text** (Instagram and Facebook images): describe what's in the image and include the phrase once.
- **YouTube title**: lead with the phrase, then the promise; description first two lines restate it.
- **On-screen text / spoken line**: say the phrase out loud in the first 5 seconds; YouTube reads captions and transcripts, and other platforms may too.
- **Local**: add the town or neighbourhood people actually search with ("near me" searches show the place names they use in GBP keywords and GSC).

No keyword lists stuffed at the end of captions; one phrase per post, used the way a person would say it.

## 5. What drives site visits

From the GA4 pull:
- Sessions and key events by social source. Merge `facebook.com`, `m.facebook.com`, `l.facebook.com`, `meta` as Facebook; `instagram.com`, `l.instagram.com`, `ig` as Instagram (Instagram tags some outbound links itself with source `ig`).
- Landing pages from social, ranked by engaged sessions. These are the pages your posts should link to.
- Untagged social traffic can't be traced to a post. Tagged traffic (`sessionCampaignName`) can: list which posts or campaigns sent visitors. If nothing is tagged, recommend `utm-builder`.

## 6. Output

**Visual (default):** fill `dashboard.html` in this folder (format in `dashboard-data.md`). `kpis` (platform `all`): Google clicks, clicks on brand queries (the step 2 bucket), sessions from Organic Social and from Organic Search. `blocks`: a wide `table` of what people search (query, impressions, clicks, position, and a `pill` column "Posted about?" with covered / missing), `cards` for the posts to make (tag Take or Adapt, meta = the query and its numbers), `bars` of site visits by source, and a `list` of words for captions and titles. Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/search-and-social-<YYYY-MM-DD>.html` (Claude Code / Cowork), or a canvas (ChatGPT). Write the verdict last, from the numbers on the page. **Chat** (settings `output: chat`, or the user asks): use the format below instead.


```
## Search and social: <business>, <window>
Sources used: <only the ones that returned data; one line for any in scope that didn't>

### Top search topics
| Topic | How people phrase it | Impressions | Clicks | Best page (pos) | On social? | Read |
### Gaps to post (top 5)
| Topic | Phrase to use | Format | Link to (page) | Why (numbers) |
### Keywords per post
| Topic | Caption first line | Alt text | YouTube title |
### Social → site
| Platform | Sessions | Engaged | Key events | Top landing page |
Tagged posts/campaigns: ... | Untagged share: <x>%
### People looking for you by name
<brand queries, impressions, trend>
```

Hand gaps to `topic-finder` or `carousel-designer`, phrasing to `caption-writer`, linking to `utm-builder`.

## Never

- Never invent search volume. GSC impressions are only searches where your site appeared, not total demand; say so.
- Never stuff keywords; one natural phrase per post.
- Read-only: never edit pages, posts or profiles from this skill.

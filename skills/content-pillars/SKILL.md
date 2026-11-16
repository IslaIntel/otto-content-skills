---
name: content-pillars
description: Builds 3-5 content pillars from evidence in your Otto data (Search Console queries, Business Profile searches, comments, your best posts per platform) and your offer, each with its share of output, the formats that work for it, and 10 seed ideas. Use when someone says "what topics should I stick to", "my feed feels random", "build my content pillars", "content themes", "what topics should I own", or before planning a content calendar.
---

# Content pillars

Decides the 3-5 themes the account posts about, using what people search for, what they ask in comments, what already performs and what the business sells. A pillar is a recurring subject you have a clear stance on, and it should lead viewers toward what the business sells, not a topic bucket. Read-only; saves the result to `brand/pillars.md` for `content-calendar` and other skills.

## 0. Setup

- If more than one Otto workspace is connected, ask which business, then keep it. If the workspace has more than one Instagram or Facebook account (`meta_page_list`), ask which one.
- `otto_list_connections` to see what's connected.
- Read `brand/offer.md`, `brand/audience.md`, `brand/winners.md` if they exist. Without `brand/offer.md`, ask: what you sell, who buys it, and what a viewer should do next.
- If `brand/pillars.md` exists, this run is an update: compare against it.

## 1. Pull the evidence (last 90 days unless told otherwise)

| Signal | Pull |
|---|---|
| What strangers search | `gsc_search_analytics` dimensions `["query"]`, rowLimit 500 |
| What locals search | `gbp_search_keywords` (rowLimit 200), local businesses only |
| What performs | `meta_ig_list_media` (rowLimit 60) → `meta_ig_media_insights` (batches of 25: `reach, views, shares, saved, comments, likes`); `meta_page_posts` → `meta_page_post_insights`; `linkedin_page_posts`; `youtube_top_videos` |
| What people ask | `meta_ig_list_comments` on the top 10 posts; `meta_page_list_comments`; `linkedin_page_list_comments`; `gbp_list_reviews` for local businesses |
| What sells | `brand/offer.md`, or `ga4_landing_pages` to see which offer pages get visits |

Fallbacks: any source not connected or returning `ok: false` is listed as "missing" in the output, and the pillars rest on what's left. With fewer than two evidence types, say the pillars are a draft and suggest running `comment-mining` or connecting GSC (`otto_connect_link`). Never invent queries, comments or numbers.

## 2. Cluster

1. Drop **branded** queries (business or product names, misspellings). They show awareness, not topics.
2. Tag every non-branded query, top post, recurring comment question and review theme with a short topic label.
3. Merge labels into 6-10 candidate themes.

## 3. Score each candidate (0-2 each)

| | 0 | 1 | 2 |
|---|---|---|---|
| **Demand** (search + questions) | No queries or questions | Some | Many queries or a question asked again and again |
| **Proof** (your posts) | Below your median or never tried | Mixed / fewer than 5 posts | Above median on shares or saves per 1,000 reach, 5+ posts |
| **Business fit** | Doesn't lead to the offer | Indirectly | A viewer who likes this is a likely buyer |
| **Right to talk** | Anyone could say it | Some experience | Your own results, process or stories |

Keep the top 3-5 by total. A theme with Business fit 0 is out, whatever else it scores. A theme with high Demand but Proof 0 is kept as a **test pillar** at a small share.

## 4. Define each pillar

- **Name** (2-4 words) and **point of view** (one sentence the business believes about it).
- **Job**: attract strangers / build trust / convert. Aim for at least one of each across the set.
- **Share of output**: proven pillars get more; test pillars 10-15%. Shares add to 100%.
- **Formats** that worked for this theme on your account (reel, carousel, talking head, demo, story). "Untested" if no data.
- **Evidence**: the queries, posts and comments behind it, with numbers.
- **10 seed ideas**, each traced to a source: a GSC query, a comment, a remix of a winning post, or a question from a review.

Then write **out of scope**: 3-5 things the account will stop posting about, with the evidence (below median, no business fit).

## Output

Save to `brand/pillars.md` (create `brand/` if missing) and show it:

```
# Content pillars (<date>, evidence window <dates>)
Position: after ten posts, people should say "<one sentence>".
Evidence used: GSC ✓/missing | GBP ✓/missing | IG ✓/missing | FB | LinkedIn | YouTube | comments | reviews

| Pillar | POV | Job | Share | Formats | Score D/P/F/R |
|---|---|---|---|---|---|

## <Pillar 1>
Evidence: "<query>" (<impr> impressions), <post> (<saves>/1k reach vs median <x>), comment: "<paraphrase>"
Seed ideas:
1. <idea>  (source: GSC "<query>")
...
10.

## Out of scope
- <theme>: <why, with evidence>
```

Hand off: `content-calendar` turns the pillars into dated posts and recurring series; `hook-writer` and `carousel-builder` turn seed ideas into posts.

## Never

- Keep more than 5 pillars. If everything fits, the pillars aren't choosing anything.
- Use invented search data or comments as evidence.
- Quote a commenter by name or handle in `brand/pillars.md`; paraphrase.

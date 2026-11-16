---
name: comment-insights
description: Pull the comments from the sources you choose (Instagram, Facebook, LinkedIn, Google reviews, Reddit; only connected ones) through the Otto MCP, cluster them into questions, objections and requests in your audience's own words, and turn the clusters into content ideas and FAQ answers. Use when someone says "what are people asking in my comments", "dig through my comments", "what do people want from me", "what objections do people have", "turn comments into content", or "build an FAQ from my comments".
---

# Comment mining

Your audience writes your content plan in the comments. This skill reads them at scale, counts what repeats, and keeps their exact words so hooks and captions sound like the customer, not the brand. Every idea it returns traces back to real comments.

Read-only on every platform. It never replies, hides or deletes. For replying to buyers, use `comment-to-lead`.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, output mode, `comment_sources`. Ask only what's missing and save the answers. If the workspace has more than one Instagram or Facebook account (`meta_page_list`), ask which one.
- **Sources (first run, or when `comment_sources` isn't set)**: check `otto_list_connections`, then ask one multiple-choice question listing only the sources this connection can read: Instagram (`meta_ig`), Facebook (`meta_pages`), LinkedIn (`linkedin_pages`), Google reviews (`gbp`), Reddit (only if `voc_search_reddit` is in the tool list), plus "All connected" first. Save the answer as `comment_sources`. If the user names sources in the request, use those for this run.
- A source with nothing in the window gets one line ("No Facebook comments in this window"), never an empty table or a zero row. Out-of-scope sources aren't mentioned.

Read `brand/audience.md` and `brand/offer.md` if present. Window: the last 90 days of posts, or the last 50 posts per platform, whichever is more. Ask whether to include DMs or sales-call notes the user can paste (Otto can't read DMs).

## 1. Pull (only the sources in `comment_sources`)

**Instagram**
1. `meta_ig_list_media` (rowLimit 60). Keep posts with `commentsCount` > 0; sort by `commentsCount` descending so the busiest threads come first.
2. `meta_ig_list_comments(mediaId, rowLimit 100)` for each. Fields: `text, username, timestamp, likeCount, hidden`.
3. `text` can come back `null` (Meta withholds some comment text). Count those as "unreadable" and report how many; ask for a screenshot if a busy thread is mostly unreadable.

**Facebook Page**: `meta_page_posts` (rowLimit 50), then `meta_page_list_comments(postId)` for posts with engagement. Includes replies.

**LinkedIn Page**: `linkedin_page_posts`, then `linkedin_page_list_comments(postId)`. This can fail with `linkedin_api_403` (the connection lacks comment permission). Then say so and ask the user to paste comments from their top 5 LinkedIn posts.

**Google reviews**: `gbp_list_reviews` (rowLimit 200). If the user wants reviews but `gbp` isn't connected, mention `otto_connect_link` for `gbp` once. Reviews are the best source of objections that got resolved.

**Reddit (optional)**: `voc_search_reddit(query)` with 2-3 phrases a customer would use about the problem (not your brand name). Often returns `http_403`; then say Reddit is unavailable and continue. Keep Reddit apart: it's the wider market, not your audience.

**Never** include comments the user hid, your own replies, spam, or emoji-only comments in the counts. Keep usernames out of the output.

## 2. Do

**Step 1. Tag every comment** with one primary type:

| Type | Looks like |
|---|---|
| Question | "how long does it take?", "do you do X?" |
| Objection | price, time, trust, "I tried that", "is it safe" |
| Request | "do one on...", "part 2", "can you show..." |
| Buying signal | price asks, "link?", "where are you", "DM me" (hand to `comment-to-lead`) |
| Praise / story | outcomes, "this happened to me" (hand to `social-proof-finder`) |
| Misread | they understood the post wrong |
| Noise | tags of friends with no text, emojis, spam |

**Too few to cluster?** Under 10 meaningful comments (after dropping noise) across all sources: say so, list them as-is, and switch the main source to Search Console question queries (`gsc_search_analytics`, dimension `query`, `includingRegex` on `^(how|what|why|can|does|is|where|when|which|who) `) and, if connected, Google reviews. Re-run once there are more comments.

**Step 2. Cluster** questions, objections and requests by the underlying need, not by wording. Name each cluster in the customer's words, not yours.

**Step 3. Score** each cluster:

| Label | Rule |
|---|---|
| Recurring | 3+ comments from different people across 2+ posts |
| Emerging | 2 comments, or 3+ on a single post |
| One-off | 1 comment; keep in the appendix only |

A cluster that also shows up in Search Console queries (`gsc_search_analytics`, dimension `query`, filter `contains` a key word) or Google reviews gets marked **confirmed**. That's demand beyond the comment section.

**Step 4. Keep their words.** For each recurring cluster, copy 2-3 short verbatim phrases (exact spelling, no clean-up). Those are hook and caption material.

**Step 5. Turn clusters into work:**
- Recurring question → a post that answers it (first line uses their phrase) + an FAQ entry.
- Objection → a post that names it out loud and shows proof.
- Request → a post or series, promised in a reply only if the user wants to.
- Misread → a short "what I meant" post or a caption fix on the original.

Rank by: confirmed > recurring > emerging, then by count.

## 3. Output

**Visual (default):** fill `dashboard.html` in this folder (format in `dashboard-data.md`). `kpis`: comments read per source in scope, meaningful comments, clusters found. `blocks`: `bars` of clusters by count (note = recurring / emerging), `cards` for the top clusters (tag Recurring, Emerging or Confirmed; evidence = 2-3 verbatim phrases), and a `list` of FAQ drafts or post ideas. Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/comment-insights-<YYYY-MM-DD>.html` (Claude Code / Cowork), or a canvas (ChatGPT). Write the verdict last, from the numbers on the page. **Chat** (settings `output: chat`, or the user asks): use the format below instead.


```markdown
# Comment mining: <business> (<date range>)
Read: <n> comments on <n> posts, by source (only sources in scope that returned something; one line for a source with nothing). Unreadable: <n>. Noise removed: <n>.

## What they ask, object to and want
| Cluster (their words) | Type | Count | People | Posts | Status | Their exact phrases |

## Content ideas, ranked
1. "<hook in their words>" — answers <cluster> (<n> comments). Format: <reel/carousel/post>. Next: `hook-writer` / `carousel-designer`.

## FAQ draft
**<question in their words>**
<answer from brand/offer.md or facts; "[needs answer from you]" if unknown>

## Buying signals to answer
<count and post links; run `comment-to-lead`>

## Proof spotted
<count; run `social-proof-finder`>
```

**Update `brand/audience.md`**: show the user a short diff (new questions, objections and phrases, each with its count and date range) and append it only after they say yes. Keep it dated so old clusters can age out.

## Never

- Invent or "tidy" a quote. Their spelling stays.
- Count one person's five comments as five people.
- Reply to, hide or delete a comment, or promise content to a commenter without the user's yes.
- Put usernames or personal details in shared output.

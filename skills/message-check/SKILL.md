---
name: message-check
description: Check whether your website, bio and recent posts all say one clear thing, by reading your site and captions and comparing them with what people actually search to find you (Search Console via Otto), then return one positioning line, its proof, and what to stop saying. Use when someone says "audit our positioning", "what do we stand for", "we blend in with our competitors", "is our message clear", "rewrite our bio", or "what should our tagline be".
license: MIT
---

# Message check

Compares three things that should match and usually don't: **what you say** (site, bio, captions), **what people find you for** (search queries), and **what you can prove** (reviews, results). The output is one sentence you can defend, the proof behind it, and a list of phrases to drop. It does not invent a new identity; when proof is missing it stops at a diagnosis.

Read-only. Proposed copy is shown, never published.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, timezone, output mode. Ask only what's missing, as one multiple-choice question, and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". A platform in scope with nothing in the window gets one line, never an empty table.

Then:
- If the workspace has more than one Instagram or Facebook account (`meta_page_list`), ask which one.
- Read `brand/offer.md`, `brand/audience.md`, `brand/facts.md` if present.
- Ask: the website URL, the action a stranger should take (book, call, buy, DM), and the 1-3 rivals a customer would compare you with. Ask for the current Instagram/LinkedIn bio text if you can't see it (Otto doesn't return bios).

## 1. Pull

**What you say**
- `voc_fetch_url` on the homepage, the main service/product page and the about page (`maxChars` 6000; use `query` to jump to "about", "why", "reviews" on long pages). JavaScript-only pages may return little: ask for a screenshot.
- Platforms in scope only: `meta_ig_list_media` (rowLimit 30) captions; `meta_page_posts` (rowLimit 20) messages; `linkedin_page_posts` (rowLimit 20) commentary.

**What people find you for**
- `gsc_search_analytics`, last 90 days, dimension `query`, rowLimit 500. Then again with dimension `page` to see which pages earn the clicks.
- `gbp_search_keywords` if Google Business Profile is connected (the searches that showed your listing).
- If GSC isn't connected: `otto_connect_link` for `gsc`, and continue without the "found for" column. Say the audit is weaker without it.

**What you can prove**
- `gbp_list_reviews` (often not connected; then skip), testimonials found on your site in the fetch above, and `brand/facts.md`. Or run `social-proof-finder` first.

**Rivals (light)**: `voc_fetch_url` on each rival's homepage only. For a deep look, use `competitor-watch`.

## 2. Do

**Step 1. Map the message.** For each source, write what it claims, in its own words (quote):

| Source | Audience named | Outcome promised | How (mechanism / category) | Proof shown | Next action asked |
|---|---|---|---|---|---|
| Homepage | | | | | |
| Bio | | | | | |
| Last 30 captions (most common) | | | | | |
| Rival A homepage | | | | | |

Count how many different audiences and promises appear across your own rows. More than two of either = the message is split.

**Step 2. Read the search truth.** Sort GSC queries by clicks and group them:

| Group | Meaning |
|---|---|
| Brand queries (your name) | people who already know you; ignore for positioning |
| Service + place ("physio near me", "pilates austin") | the job people hire you for |
| Problem queries ("knee pain when running") | the problem you are trusted on |
| Queries you rank for but don't want | a mismatch to fix on the page, not in the bio |

Then compare: the promise on your homepage vs the group that brings the most non-brand clicks. If they differ, that's the first finding. Fewer than 50 non-brand clicks in 90 days: "too little search data to tell", lean on reviews instead.

**Step 3. Find the one thing.** Pick the claim that passes all four:
1. Your audience uses words for it (in search queries or reviews).
2. You can prove it (a review, a number in `brand/facts.md`, a visible result).
3. At least one rival doesn't say it, or says it without proof.
4. It leads naturally to the next action you want.

Write it as: **For [who], [business] [does what outcome], because [proof].** Brackets you can't fill from evidence stay as `[needs proof: ...]`.

**Step 4. Stress-test.** Could a rival paste it unchanged? Does a stranger understand every word? Is the proof real? Would the next action make sense right after reading it? Any "no" → revise or downgrade to a hypothesis.

**Step 5. What to stop saying.** List phrases from your own copy that are: empty ("quality service", "passionate"), shared word-for-word with rivals, aimed at an audience search and reviews show you don't get, or claims you can't prove.

## 3. Output

Default is visual: an artifact (claude.ai / Claude desktop), an HTML file opened in the browser (Claude Code / Cowork), or a canvas (ChatGPT), built in code with the sections below. If settings say `output: chat` or the user asks for chat, give the same content as markdown in chat.

```markdown
# Message check: <business> (<date>)

## The line
For <who>, <business> <outcome>, because <proof>.
Confidence: high / medium / hypothesis. Why: <one sentence>.

## Evidence
- Search: <top non-brand query groups with clicks, last 90 days>
- Proof: <review or fact, source>
- Gap vs rivals: <what they say instead, with URL>

## Where you say something else
| Place | Says now | Change to |
(homepage headline, bio, pinned post, link button, top 3 recent captions)

## Stop saying
| Phrase | Where | Why |

## Missing proof
<claims you want to make but can't yet, and how to get the proof>
```

Hand the line to `profile-check` (bio and link), `brand-brain` (save to `brand/offer.md` after the user agrees), and `content-pillars`.

## Never

- Invent proof, outcomes or customer quotes to fill the sentence.
- Change the website, bio or any post. Show the copy; the user applies it by hand.
- Treat one quiet rival as an empty market.

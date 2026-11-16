---
name: social-proof-finder
description: Find the proof you already have (Google reviews, positive comments on Instagram and Facebook, testimonials on your own site, DMs and emails you share) through the Otto MCP, match each piece to the claim it supports, check permission, and save a reusable proof bank. Use when someone says "find testimonials", "what proof do we have", "find good reviews to post", "social proof for this campaign", "which review backs this claim", or "build a testimonial bank".
license: MIT
---

# Social proof finder

Most small businesses have more proof than they use: a glowing review from last spring, a comment that says "this fixed my back", a thank-you email. This skill finds it, ties each piece to one specific claim, and tracks whether you're allowed to use it. The result is `brand/proof.md`, a bank other skills draw from.

Read-only on every platform. It never asks a customer for permission by itself; it drafts the ask for you to send.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, timezone, output mode. Ask only what's missing, as one multiple-choice question, and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". Window: the last 12 months. A platform in scope with nothing in the window gets one line, never an empty table.

Then:
- If the workspace has more than one Instagram or Facebook account (`meta_page_list`), ask which one.
- Read `brand/facts.md`, `brand/offer.md` and any existing `brand/proof.md` (don't duplicate entries).
- Ask what the proof is for, if anything specific (a campaign, a service page, an objection like "too expensive"). Ask the user to paste any DMs, emails or texts they want considered (Otto can't read DMs).

## 1. Pull

1. **Google reviews**: `gbp_list_reviews` (rowLimit 500). Fields include rating, text, reviewer name, date and any owner reply. Often not connected, or it returns an error even when connected (it needs an extra Google API); then say so, offer `otto_connect_link` with source `business_profile` if it isn't connected, and ask for a screenshot of the best reviews.
2. **Your website**: `voc_fetch_url` on the homepage and any testimonials / reviews / case-study page, with `query: "testimonial"` or `"review"` to center the excerpt. These are usually already approved for public use; note the URL as the source.
3. **Comments**: `meta_ig_list_media` (rowLimit about 1.2 x posts per day x 365, max 500, to cover the 12 months; if 500 doesn't reach that far, say how far back it goes; if the result is saved to a file, read it with code) → `meta_ig_list_comments` on posts with `commentsCount` > 0; `meta_page_posts` → `meta_page_list_comments`. IG comment `text` can be `null`; skip those. `linkedin_page_posts` → `linkedin_page_list_comments` (it may return `linkedin_api_403`; then ask for pasted comments instead).
4. **What the user pastes**: DMs, emails, survey answers, case results.

Never invent, merge or "improve" a quote. If something is paraphrased by the user, mark it "paraphrase, not quotable".

## 2. Do

**Step 1. Keep only real proof.** A piece qualifies if it says something specific happened: an outcome, a before/after, a time or money figure, a fear that turned out wrong, a comparison with what they tried before. Generic praise ("great service!") goes to a separate "warm but vague" list; it's fine for star counts, weak as proof.

**Step 2. Match to one claim.** For each piece, write the narrowest claim it supports, with its conditions: "one client's knee pain eased within 3 sessions" not "we fix knees fast". Note which objection it answers (price, time, trust, "will it work for me") and which persona it fits (see `brand/personas.md` if present).

**Step 3. Rate strength.**

| Strength | Rule |
|---|---|
| A | specific outcome + identifiable source + recent (under 12 months) |
| B | specific but older, or anonymous |
| C | vague praise or an outcome with no detail |

**Step 4. Permission check.** Every piece gets a status before any public use:

| Source | Default status | What's needed |
|---|---|---|
| Testimonial already on your site | Approved (confirm it's still OK if over 2 years old) | nothing |
| Google review | Public, but quoting it in an ad or post with the name needs a yes | ask the reviewer if you know them; otherwise quote it without the name, as "Google review" |
| Public comment | Public, not consented for reuse | ask the commenter before quoting with their handle; anonymous quote only if they can't be identified |
| DM, email, text | **Private** | written permission required, always |
| Health, legal, money outcomes | Sensitive | permission + check `brand/facts.md` and local advertising rules; add "results vary" |
| Before/after photos, faces, minors | Sensitive | written consent per image; never for minors without a guardian |

For each "needs permission" item, draft a short, polite ask the user can send themselves (one message, says exactly where it would appear, easy to say no). Don't send it.

## 3. Output

Default is visual: an artifact (claude.ai / Claude desktop), an HTML file opened in the browser (Claude Code / Cowork), or a canvas (ChatGPT), built in code with the sections below. If settings say `output: chat` or the user asks for chat, give the same content as markdown in chat.

Show the bank, then in a working folder save it to `brand/proof.md` after the user says yes (append; keep earlier entries). Without a folder, give the markdown for the user to keep.

```markdown
# Proof bank: <business> (updated <date>)

| # | Exact words | Source (platform, date, link) | Who (as allowed) | Claim it supports | Answers objection | Strength | Permission | Use where |
|---|---|---|---|---|---|---|---|---|
| 1 | "<verbatim>" | Google review, 2026-03-14 | Maria G. | <narrow claim> | price | A | needs ask | ad, service page |

## Strongest 5 to use now
<numbers from the table, only items with permission = approved>

## Waiting on permission
<items + the drafted ask for each>

## Gaps
<claims you make in `brand/facts.md` or on your site that no proof supports yet, and how to collect it (e.g. ask the next 5 clients one question after the session)>

## Warm but vague
<count; fine for "4.9 stars from 120 reviews" style lines>
```

Hand approved proof to `caption-writer`, `carousel-designer`, `campaign-plan` and `message-check`.

## Never

- Write, composite or edit a testimonial, or present a paraphrase as a quote.
- Use a DM, email, face or name publicly without written permission.
- Stretch one result into a promise ("guaranteed", "everyone").
- Reply to a reviewer or commenter, or publish anything. Drafts only.

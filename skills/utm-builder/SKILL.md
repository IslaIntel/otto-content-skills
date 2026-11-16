---
name: utm-builder
description: Build tracked links for your posts and campaigns with one lowercase naming scheme, one link per platform and post, a running log file, and a check in GA4 through Otto (sessionSource / sessionCampaignName) that the tags actually arrive. Use when asked to "make UTM links", "tag my links", "track which post sent traffic", "set up tracking for this campaign", or "are my UTMs working".
---

# UTM builder

Without tags, GA4 sees "facebook.com sent some visits" and nothing more. With tags it sees which campaign and which post. This skill sets a naming scheme once, builds the links, logs them, and later checks in GA4 that they arrived as written. It only creates text (links and a log file); it never posts or edits anything.

## 0. Setup

Follow the settings and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short: read `brand/settings.md` (or your memory of the user's Otto settings) first for workspace, accounts and output mode; ask only what's missing, as one multiple-choice question, and save the answers.

Then:
- `otto_list_connections` to confirm GA4 is connected (needed for step 4; without it, build links and skip verification).
- Read `brand/offer.md` for the approved destination URLs. Read `social-data/utm-log.csv` if it exists and reuse its values; never invent a second name for something already logged.
- Ask: the campaign (what and when), destination page(s), and the posts or placements that will carry links.
- Check existing names first: `ga4_run_report` dimensions `["sessionSource","sessionMedium","sessionCampaignName"]`, metric `sessions`, last 90 days. Keep whatever convention is already in use if it's consistent.

## 1. The naming scheme

All values **lowercase**, words joined with hyphens, no spaces, no accents. GA4 treats `Instagram` and `instagram` as two sources.

| Parameter | Allowed values | Example |
|---|---|---|
| `utm_source` | the platform: `instagram`, `facebook`, `linkedin`, `youtube`, `tiktok`, `x`, `newsletter`, `gbp`, or a partner's short name | `instagram` |
| `utm_medium` | `social` (organic post), `paid-social` (ads), `email`, `creator` (partner posts), `bio` (link in profile), `qr` | `social` |
| `utm_campaign` | `<topic>-<yyyy-mm>` | `spring-cleanup-2026-03` |
| `utm_content` | which post or placement: `<format>-<short-slug>-<mmdd>` | `reel-before-after-0314` |
| `utm_term` | only for paid search keywords; leave out otherwise | |

Rules:
- Medium separates organic, paid, creator and email so they never blend in reports. Meta ads that already set their own URL parameters keep them; log what they use.
- Use the same campaign value on every platform for one campaign; vary source and content.
- **Nothing personal in any value**: no customer names, emails, phone numbers, staff names, or private IDs. Use a neutral label.

## 2. Build the links

For each post or placement: `<destination>?utm_source=…&utm_medium=…&utm_campaign=…&utm_content=…`. If the destination already has `?`, join with `&`. Encode nothing that doesn't need it (the scheme above avoids special characters).

Where links can go:
- Instagram: link in bio (medium `bio`), Stories link sticker, DMs. Caption links aren't clickable.
- Facebook, LinkedIn: in the post. YouTube: description and pinned comment. GBP posts: the button URL.
- If a link shortener is used, the full tagged URL goes into the shortener; log both.

## 3. Log

Append one row per link to `social-data/utm-log.csv` (create it with this header if missing):

`created,campaign,source,medium,content,destination,full_url,placement,post_permalink,status`

`status` starts as `built`. Fill `post_permalink` once the post is live.

## 4. Verify in GA4 (24-48 hours after the first link goes live)

1. `ga4_run_report` dimensions `["sessionSource","sessionMedium","sessionCampaignName"]`, metrics `["sessions","engagedSessions","keyEvents"]`, from the campaign start, `dimensionFilter` on `sessionCampaignName` `CONTAINS` the campaign value.
2. Add `sessionManualAdContent` as a dimension to see `utm_content` per post.
3. Compare with the log:

| GA4 shows | Means | Fix |
|---|---|---|
| Rows match the log | working | mark `status` = `verified` |
| Campaign missing, posts are live and clicked | tag dropped (redirect, shortener, app browser) | open the link, check the final URL still has the tags |
| Same campaign in two spellings / cases | someone typed it by hand | correct future links; add both together in reports |
| Source shows as `(not set)` or `(direct)` | link copied without tags | rebuild from the log |
| Sessions but 0 engaged | wrong or slow landing page | check the destination |

Also look at untagged social rows (`facebook.com`, `m.facebook.com`, `ig`, `l.instagram.com`) in the same window: that's the share of social traffic still invisible at post level.

## 5. Output

Default is visual: an artifact (claude.ai / Claude desktop), an HTML file opened in the browser (Claude Code / Cowork), or a canvas (ChatGPT), with each link in a copyable field. Also print the full links as plain text in chat so they can be copied without opening anything. If settings say `output: chat` or the user asks for chat, give the markdown below in chat only.

```
## UTM links: <campaign>
Scheme: source=<platform> · medium=<type> · campaign=<value> · content=<format-slug-mmdd>

| Placement | Platform | Full link | Logged |

### Verification (<date>)
| Campaign | Source / medium | Content | Sessions | Engaged | Key events | Status |
Untagged social sessions in window: <n> (<x>% of social)
Fixes: ...
```

Hand results to `campaign-retro` after the campaign ends.

## Never

- Never put personal or private data in a UTM value.
- Never tag internal links between pages of the same site (it resets the visitor's real source).
- Never post, edit a post, or change a profile link from this skill; the person places the links.
- Never treat a tagged visit as proof the post caused a sale.

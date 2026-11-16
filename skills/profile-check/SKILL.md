---
name: profile-check
description: Check the social profiles your content sends people to (Instagram first, then TikTok, YouTube, Facebook, LinkedIn, X; TikTok and X from screenshots) and propose the smallest changes so a visitor arriving from one post understands who you are, what you offer, and the one thing to do next. Use when asked "check my profile", "fix my bio", "which posts should I pin", or when reels get views but few follows, DMs or site visits.
license: MIT
---

# Profile check

A post earns the visit; the profile decides what happens next. This skill reads the profile the way a stranger arriving from one reel sees it, and proposes changes. It changes nothing: the owner makes every edit by hand.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or the assistant's memory) for workspace, accounts, default platforms and output mode. Ask only what's missing, in one bundled multiple-choice question, and save the answers.
- Check only the profiles the user named, else the default platforms; ask once if there are none ("All connected" as an option).
- Output is visual by default (artifact / HTML file / canvas) unless settings or the user say chat.

## 1. See it as a visitor does

Ask for phone screenshots of each profile, or the public URL. Record only what is actually there: name field, handle, category, bio, link, pinned posts, highlights, the first nine grid covers.

From the Otto MCP (read-only), if connected:
- Instagram: `meta_ig_account_insights` (time_series `reach`, `follower_count`) for the last 28 days (`follower_count`, daily new follows, only exists at 100+ followers), `meta_ig_list_media` (rowLimit 30) for recent posts, and `meta_ig_media_insights` on them (`reach, shares, comments`) to find the best performer. Otto doesn't show which posts are pinned: take that from the screenshots or URL.
- If GA4 is connected: `ga4_run_report` with dimension `sessionSource`, metric `sessions`, filtered to `sessionDefaultChannelGroup` = Organic Social, shows how many site visits come from each social platform.

If `brand/offer.md` doesn't say, ask for the business's one-line offer and the one action they want visitors to take (book, buy, DM a keyword, visit the site).

## 2. The ten-second test

Can someone who just watched one post tell, in ten seconds:

1. Who this account is for?
2. What the business does, in a customer's words?
3. Why it's worth following (what more of this they'll get)?
4. What to do next, and only that?

Write down each "no", each competing call to action, each word a customer wouldn't use, and anything the profile promises that the link's page doesn't.

## 3. Propose the smallest changes

In order of what fixes the most:

- **Name field** (Instagram search reads it): what a customer would search for, beside the name. Three options, for example "Ana | Wedding florist in Austin".
- **Bio**, three lines: who it's for and what you do; why follow; the one action.
- **Link**: one destination. Suggest UTM tags (`?utm_source=instagram&utm_medium=social&utm_campaign=profile`) so the weekly review can see the visits in GA4. Never put anything about a person in a tag.
- **Pinned three, in order**: the clearest "what we do" post, the best proof (a result, a before/after, a review, only if real), and the best performer by shares or comments per 1,000 reach.
- **Grid**: do the last nine covers look like one account? Flag any cover unreadable at grid size.

Never invent follower counts, customer logos, testimonials or results.

## 4. One change at a time

Pick the one change to make first and what to watch afterwards (follows per 1,000 reach, link clicks or site visits, DMs). Wait two weeks before the next change so you can tell what it did.

## Output

Visual by default (artifact / HTML file / canvas), chat if settings or the user say so. A table per profile: element | what it says now | the problem (or "fine") | proposed text. Then the one change to make first, and what number to watch.

---
name: audience-personas
description: Build evidence-led audience personas from your real data through the Otto MCP (comments, Google reviews, YouTube age/gender and country, GA4 location and device, Search Console queries), where every claim cites its source and nothing is made up. Use when someone says "who is my audience", "build personas", "who actually follows me", "who am I talking to", "what does my customer look like", or "who should I make content for".
---

# Audience personas

A persona is only useful if you can point at the data behind every line. This skill groups people by **the job they want done** and the words they use, then attaches the numbers that are measurable (age bands, countries, devices, searches). Anything the data doesn't show is written as unknown. No stock photos, no invented names, no made-up hobbies or incomes.

Read-only.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, timezone, output mode. Ask only what's missing, as one multiple-choice question, and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". A platform in scope with nothing in the window gets one line, never an empty table.

Then:
- If the workspace has more than one Instagram or Facebook account (`meta_page_list`), ask which one.
- Read `brand/audience.md` (especially anything `comment-mining` wrote) and `brand/offer.md`.
- Ask the user two things the data can't tell: who buys today (from their side: bookings, invoices, intake forms) and whether the person who **buys** differs from the person who **watches** (a parent booking for a teen, an office manager booking for a team).
- Window: last 90 days.

## 1. Pull

| Source | Tool | What it can claim | Watch out |
|---|---|---|---|
| Comments | run `comment-mining` first, or `meta_ig_list_comments` / `meta_page_list_comments` | jobs, objections, exact words | LinkedIn comments may 403; IG `text` can be null |
| Reviews | `gbp_list_reviews` | why buyers chose you, outcomes | often not connected: skip, offer `otto_connect_link` |
| YouTube viewers | `youtube_demographics(startDate, endDate)` | age band × gender as % of viewers | signed-in viewers only; channel viewers, not buyers |
| YouTube countries | `youtube_geo_countries` | views, minutes, avg view duration per country | |
| Site visitors | `ga4_geo` (rowLimit 100) | sessions and engaged sessions by country / region / city | data-centre cities (high sessions, near-zero engaged sessions) are bots: drop them |
| Devices | `ga4_tech` | mobile vs desktop, browser | |
| Searches | `gsc_search_analytics`, dimension `query`, rowLimit 500 | the problems and places people type | brand queries tell you little |
| Local searches | `gbp_search_keywords` | what found the listing | needs GBP |
| Instagram followers | not available through Otto | | ask for a screenshot of Instagram's audience tab if it matters |

If a tool returns `ok: false`, list it under "not available" and continue. Fewer than 3 sources working: say the personas are a draft.

## 2. Do

**Step 1. Clean the numbers.** In GA4, rank locations by **engaged sessions**, not sessions. In YouTube, note the share of viewers under 18; if it's large and you don't sell to teens, say the channel's reach is drifting from the buyer.

**Step 2. Find the jobs.** From comments, reviews and search queries, list the distinct jobs people want done ("fix my knee before the race", "get the website updated without calling anyone"). Merge jobs that lead to the same purchase. Usually 2-4 survive. Fewer than 30 comments + reviews in total: "too little language to split; one persona with open questions".

**Step 3. Attach evidence to each job.** For each, gather: the trigger (what made them look now), their words (verbatim), objections, the place they found you (search, Instagram, referral), and where it's measurable, their age band, country/city and device.

Only attach a demographic to a persona if a source links them (e.g. the persona's search queries are local and GA4 shows that city in the top 3). Otherwise write the channel-wide figure once in "audience numbers" and leave the persona's own line as "unknown".

**Step 4. Label confidence.**

| Level | Rule |
|---|---|
| Strong | 3+ independent sources agree (e.g. comments + reviews + search) |
| Medium | 2 sources |
| Hypothesis | 1 source, or only the user's word |

## 3. Output

Default is visual: an artifact (claude.ai / Claude desktop), an HTML file opened in the browser (Claude Code / Cowork), or a canvas (ChatGPT), built in code with the sections below. If settings say `output: chat` or the user asks for chat, give the same content as markdown in chat.

In a working folder, save the markdown to `brand/personas.md` after the user approves, and offer to add a short summary to `brand/audience.md`. Without a folder, give the markdown for the user to keep.

```markdown
# Audience personas: <business> (<date range>)
Sources used: <list with counts>. Not available: <list>.

## Audience numbers (whole account, not per persona)
- YouTube viewers: <top age bands and %> (signed-in viewers, <dates>)
- Top countries (YouTube views): <...>; top cities (GA4 engaged sessions): <...>
- Device: <mobile %> (GA4)

## Persona 1: <label from the job, e.g. "the race-week runner">  — confidence: strong / medium / hypothesis
- Job: <one line> [source]
- Trigger: <what makes them look now> [source]
- In their words: "<verbatim>" [comment, <date>] · "<verbatim>" [review]
- Objections: <...> [source]
- Finds you via: <search query group / platform> [GSC / GA4]
- Age / place / device: <only if linked by a source; else "unknown">
- Content that serves them: <2-3 angles>; hooks to test with `hook-writer`
- Open questions: <what would confirm or kill this persona>

## Who you're reaching but not selling to
<e.g. a large under-18 YouTube share, a country you don't serve>
```

## Never

- Give a persona a name, face, salary, family or hobby the data doesn't show.
- Present YouTube or GA4 demographics as "your customers". They're viewers and visitors.
- Turn one loud commenter into a segment.
- Put a real commenter's name or handle in the personas file.

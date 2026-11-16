---
name: linkedin-post
description: Write a founder or expert LinkedIn post from something the author actually did, saw or decided, shaped by what has worked on your own LinkedIn (pulled through the Otto MCP), with an optional post image built in code, and publish or schedule it on your personal profile or Company Page only after you approve the exact text. Use when asked to "write a LinkedIn post", "make this a LinkedIn post", "give me a LinkedIn idea from this week", "founder post about this", or "plan a LinkedIn series".
license: MIT
---

# LinkedIn post

Turns one real piece of work (a decision, a mistake, a number, a customer conversation) into a post a buyer or peer would stop for. The author must be able to defend every sentence. Generic advice, invented stories and motivational posts are out of scope.

## 0. Setup

Follow the settings, scope and capability rules ("How every skill talks to the user" in this folder's `otto-rules.md`). In short:
- Read `brand/settings.md` (or memory) for workspace, LinkedIn account (personal profile, Company Page or both), timezone and output mode; ask only what's missing in one multiple-choice message, then save it.
- Output is visual by default (artifact / HTML file / canvas) unless settings say chat.
- Before offering to publish or schedule, check which tools this session has (rule 5) and offer only what's there.

Skill-specific:
- `otto_list_connections`: is `linkedin_profile` (personal profile) and/or `linkedin_pages` (Company Page) connected? Ask which one this post is for if both are. If the one they want isn't connected, say so: LinkedIn has no `otto_connect_link` source, so the user connects it in Otto's settings.
- Read `brand/voice.md`, `brand/audience.md`, `brand/offer.md`, `brand/facts.md`. If `brand/` is missing, ask: who reads your LinkedIn (role, company size), what you sell, two words you'd never use. Suggest `brand-brain` once.
- Ask for the raw material: **what happened, what you decided, what you'd tell someone in the same spot.** A voice note transcript or bullet notes is enough. If they have nothing firsthand, stop and offer `topic-finder` instead.
- Optional inspiration: posts from peers or other companies the user pastes or links. Use them for structure and opening style only; never copy wording. Otto can't read other people's LinkedIn posts.

## 1. Pull: learn from your own LinkedIn

**Company Page** (if connected)
- `linkedin_page_posts` (organizationId, rowLimit 50): id, `commentary` (the post text), `createdAt` (epoch ms). No per-post metrics.
- `linkedin_page_insights` (startDate, endDate, last 90 days): `kpis` (followers total, views, uniqueViews, likes, comments, shares, clicks) plus `daily` rows with impressionCount, uniqueImpressionsCount, likeCount, commentCount, shareCount, clickCount.
- Since posts carry no numbers, attribute each daily row to the most recent post published 0-3 days before it. Sum impressions and engagements per post over those days. With two posts in the same 3-day window, mark both "shared window, can't separate". Label these numbers approximate: page impressions also include older posts.

**Personal profile** (if connected)
- `linkedin_profile_list`: profiles and sign-in `status`. If `expiring_soon` or `expired`, tell the user to reconnect LinkedIn (personal profile) in Otto Settings before any publish.
- `linkedin_profile_otto_posts`: only posts Otto published, with text and `publishedAt`. LinkedIn does not let Otto read other profile posts or any profile analytics. For profile performance, ask for a screenshot or the CSV export from LinkedIn's own post analytics (impressions, reactions, comments, reposts per post).

**Fallback**: if a call returns `ok: false`, say which one and the error text, and continue with what you have. If the page is new or quiet (most daily rows near zero), say the baseline is too thin and write from `brand/` and the author's notes alone. Never invent a past "best post".

## 2. Find what works for this author

From the posts with numbers (page attribution or the user's export):
- Baseline = **median** impressions and median engagements per 1,000 impressions.
- Tag each post: type (story / lesson / announcement / how-to / opinion / promo), language, opening line style (number, confession, contrarian, plain news), length (short under 600 characters, long), has a question at the end or not.
- Winners = 2x the median on either number. Note what they share. Groups under 5 posts are "too few to tell".
- Check `brand/winners.md` for LinkedIn entries too.

One clear finding is enough ("Your three best page posts were firsthand stories with a number in line one; your promos sat at a third of the median"). If nothing stands out, say so.

## 3. Write the post

1. **Pick one point.** The single thing a reader in the author's audience should think or do differently. If the notes hold three points, that's three posts; offer a series.
2. **Right to say it.** Mark each claim as firsthand (author did or saw it) or secondhand. Secondhand claims get a source or get cut. Numbers must come from the author or `brand/facts.md`.
3. **Opening (first 2 lines, before "see more").** Concrete, specific to the reader, no throat-clearing. Options to draft: the number, the moment, the decision, the thing most people get wrong. Write three; recommend one using the step 2 finding.
4. **Body.** Situation → what was decided and why → what happened (or "too early to know") → the takeaway the reader can use. Short paragraphs, one idea each. Include one limit or trade-off; it makes the rest believable.
5. **Ending.** End on a question only when the author plans to reply to answers. Otherwise a plain next step from `brand/offer.md` (or none). One link at most; mention that some authors put it in the first comment.
6. **Run `sound-human`** on the draft. Keep it under 3,000 characters (the API limit), ideally 900-1,500. Hashtags: 0-3, only if the author already uses them.
7. **Image (optional).** A photo from the work (the user's own file) beats anything else. If they want a graphic instead (a stat, a short list, a quote from the post), build it in HTML/CSS/SVG at 1200x1200 or 1080x1350 in their brand colours and render it to PNG (headless browser in Claude Code / Cowork; artifact with a download in claude.ai). Never AI-generate an image.

## 4. Output

Default is visual (artifact / HTML file / canvas) showing the post as it will look, plus the image if any; chat if settings or the user say so.

```
POINT: <one sentence>
FROM YOUR DATA: <the one finding from step 2, or "baseline too thin">

OPENING OPTIONS
A) ...   B) ...   C) ...   Recommended: <letter>, because <reason from data>

POST (<characters> chars)
<full text>

CLAIMS CHECK
| Claim | Firsthand / source | OK to publish? |

IMAGE (optional): <photo supplied / graphic built in code: post-image.png>
FIRST COMMENT (optional): <link or added context>
REPLY PLAN: <2-3 replies the author could add from real context in the first hour>
NEXT IN SERIES (optional): <2 more points from the same notes>
```

## 5. Publish or schedule (only after a yes)

Show the exact final text, the image and the target (personal profile or Company Page). Ask once: "Post this as it is?" Then pick the path from the tools in this session:

| Target | Now | Later |
|---|---|---|
| Personal profile | `linkedin_profile_create_post` (commentary, plus imageMediaIds with imageAltTexts, or videoMediaId, or articleUrl, not a mix; profileId when several). Goes live immediately | `channel_submit_plan` with provider `linkedin_profile`, op `linkedin_profile_create_post`, `publishAt` + `timeZone`, if your Otto connection includes scheduling |
| Company Page | `linkedin_page_create_post` if it's in the tool list. Text or a link only: it takes no image, so add the image by hand in LinkedIn | `channel_submit_plan` with provider `linkedin_pages`, op `linkedin_create_post`, `publishAt` + `timeZone`, if your connection includes scheduling |
| No matching tool | Hand over the text, the image and the steps to post on LinkedIn | same |

Images for a personal-profile post go into the Otto media library first (`media_create_upload` → upload → `media_complete`) to get a mediaId. A plan returns an `approveUrl`: say "will publish at <time> after you approve in Otto", and claim it's scheduled only if the result says `scheduled: true`.

Afterwards, log the post in `brand/winners.md` once it has 7 days of numbers, if it beat the median.

## Never

- Invent a story, customer, result, job title or number. Ask instead.
- Publish, schedule or reply without an explicit yes on the exact text in this conversation.
- Claim to have read personal-profile analytics; Otto can't.
- Turn the post into a pitch the lesson doesn't support.

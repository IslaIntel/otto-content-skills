---
name: story-sequence
description: Lay out a run of 6-9 Instagram Stories, choosing where each poll, question box, quiz and link sticker goes to earn tap-through and DMs, built from your audience's own words and your recent reels pulled through the Otto MCP. Use when someone says "what should my stories be today", "story sequence for this launch", "how do I get DMs from stories", "push my new reel in stories", or "what should I post on stories today".
license: MIT
---

# Story sequence

Stories reach the people who already follow you. That makes them the place to turn a viewer into a conversation: a reply, a poll vote, a DM, a booking. This skill plans one arc with one goal, frame by frame, with the exact sticker wording and where each sticker goes.

Read-only. Otto can't post Stories, so the owner posts the frames in the Instagram app. Text-only or graphic frames can be built in code (HTML/CSS, 1080x1920) and rendered to PNG if the owner wants them; photos and video come from the owner's camera roll.

## 1. Setup
Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short: read `brand/settings.md` (or memory) for workspace, Instagram account and output mode; ask only what's missing in one multiple-choice message and save it. Output is visual by default (artifact / HTML file / canvas) unless settings say chat.

- Read `brand/` (voice, audience, offer, facts). Missing: ask what you sell, who buys it, and what a viewer should do next. Suggest `brand-brain`.
- Ask for the goal of this sequence. Pick one:

| Goal | Proof it worked | Main sticker |
|---|---|---|
| Send people to a new reel | the reel's views a few days later vs your usual (Otto gives lifetime numbers, not a 24-hour count) | none until the last frame; then share the reel itself |
| Start DMs | DMs and story replies | question box, then "reply with <word>" |
| Clicks to a page | link sticker taps | link sticker on the last frame only |
| Learn something | poll / quiz votes | poll early, result reveal later |
| Bookings or sales | bookings (ask) | link sticker or "DM <word>" |

Two goals? Ask which one matters today.

## 2. Pull
- `meta_ig_list_media` (rowLimit 20) for the latest reel, its caption and permalink, if the goal is to push it.
- `meta_ig_account_insights` (`metricType: time_series`, metrics `reach`, last 28 days) and `profile.followersCount` for scale: a story usually reaches a fraction of followers, so set expectations from that total.
- `meta_ig_list_comments` (rowLimit 50) on your 5 most-commented recent posts for questions people ask. Skip comments where `text` is null. These become poll and question-box wording.
- Story analytics (taps forward, exits, replies, sticker taps) are **not** available through Otto. Ask for screenshots of the last sequence's insights from the app if the owner wants this one compared.

Not connected or `ok: false`: say so and plan from `brand/` and the owner's answers.

## 3. Build the arc

Default shape (6 to 9 frames, one idea per frame):

1. **Open**: a moment, not a greeting. Something in motion or mid-story, with 1 line of text. No "hey guys".
2. **Tension**: the problem or question, in the customer's words from `brand/audience.md`.
3. **Interaction**: a poll or quiz with two real options. Early enough that most viewers still see it (frames 2 to 4).
4. **Build**: 1 to 3 frames of proof or story (a behind-the-scenes clip, a result from `brand/facts.md`, a customer quote with permission).
5. **Turn**: show the poll result or answer the top question. People come back to see this.
6. **Ask**: one action, matching the goal. Link sticker or "reply <word>" goes here, after the value, never on frame 1.
7. (Optional) **Thank-you**: the next thing to watch for, for those who stayed.

Rules:
- Text per frame: 15 words or fewer, readable in 3 seconds. Keep it out of the top 14% and bottom 20%.
- Video frames: about 15 seconds each (Instagram allows up to 60s, but short frames keep people tapping forward). Photos stay 5 seconds; don't put a paragraph on a photo.
- One ask in the whole sequence.
- Post the frames in one go, unless the arc is built around a poll result, then post the "turn" frame 4 to 8 hours later.
- Reply to every DM the stickers produce within the day. `comment-to-lead` covers DM scripts.

## 4. Output

Default is visual (artifact / HTML file / canvas); chat if settings or the user say so.

```
STORY SEQUENCE: <goal> | <n> frames | post <time>
Your followers: <n>. Story reach isn't available through Otto; compare with your last sequence's screenshot.

| # | Shot (what to film) | Text on frame | Sticker (exact wording) | Why it's here |
|---|---|---|---|---|
| 1 | ... | "..." | none | open |
| 3 | ... | "..." | Poll: "<question>" <A> / <B> | interaction |
| 6 | ... | "..." | Link: "<label>" -> <URL> | the ask |

Words taken from your audience: "<quote>" (comment, <date>)
Measure tomorrow: <the one number for this goal>. Screenshot story insights and paste them here next time to compare sequences.
```

## Never
- Invent a poll result, a testimonial or a "spots left" number.
- Put the link sticker before the value.
- Ask for two things in one sequence.

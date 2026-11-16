---
name: comment-to-lead
description: Read the comments on your recent Instagram, Facebook and LinkedIn posts through the Otto MCP, sort them (keyword requests, questions, support, spam), draft public replies, send approved replies through Otto when your connection has reply tools, and write a ManyChat-ready DM flow (keyword triggers, first DM, follow-ups) for an official DM tool, since Otto doesn't send DMs. Use when asked "check my comments", "reply to the comments", "who commented the keyword", "draft the DMs", "set up a comment-to-DM flow", or every day a "comment X and I'll send it" post is live.
license: MIT
---

# Comment to lead

If a post says "Comment PRICE and I'll DM you the list", that promise only counts if it gets kept. This skill is the back half of the post.

Nothing runs unattended. Reading comments is free; every reply or hide waits for the owner's yes in this conversation, for that batch.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or the assistant's memory) for workspace, accounts, comment sources and output mode. Ask only what's missing, in one bundled multiple-choice question, and save the answers.
- Read comments only on the platforms the user named, else the defaults in settings.
- **Capability check**: if this session has reply tools (`meta_ig_reply_comment`, `meta_page_reply_comment`, `linkedin_page_reply_comment`), approved replies are sent through Otto (official API). If not, this skill drafts only and the owner pastes the replies.
- Output is visual by default (artifact / HTML file / canvas) unless settings or the user say chat.

Skill questions: the comment keyword (if any), what the keyword gets them (a link, a guide, a booking page), and the facts you may use to answer questions (offer, price if public, hours, link). Answer only from those facts (`brand/offer.md`, `brand/facts.md`).

## 1. Read the comments (read-only)

For each post from the last 7 days:
- Instagram: `meta_ig_list_media`, then `meta_ig_list_comments` per post.
- Facebook: `meta_page_posts`, then `meta_page_list_comments`.
- LinkedIn: `linkedin_page_posts`, then `linkedin_page_list_comments`. This can return `ok: false` with `linkedin_api_403` (the connection lacks comment permission): say so, and ask the owner to reconnect LinkedIn Pages in Otto or paste the comments.
- TikTok, X, YouTube and personal LinkedIn profile comments aren't listed through Otto: say so and ask the owner to check those apps.

Skip comments the account already replied to. Read the oldest unanswered first: a question that waited two days goes to the top.

## 2. Sort every comment

| Bucket | What it is | What happens |
|---|---|---|
| Keyword | The keyword or a near miss ("guide pls", "GIUDE") | Public reply + DM draft |
| Question | A real question about the business or the post | Answer from the facts only; if they don't cover it, it goes to the owner |
| Customer / support | "My order...", billing, a complaint | Public: "Sending you a message." The owner handles it privately |
| Hostile, spam, competitor | Insults, scams, someone selling | No reply. Hide (`meta_ig_set_comment_hidden` / `meta_page_set_comment_hidden`) only if the owner says so |
| Other | Praise, emoji, tagged friends | A short thanks, or nothing |

A comment that fits no bucket goes to the owner. Never guess.

## 3. Draft the public reply

- Short, warm, plain, in the business's voice. No hype, no promised results.
- **No link in a public reply.** Links only travel by private message.
- Before it's sent, say "Sending it to your messages now", never "sent".
- Vary the wording; twenty identical replies read as a bot.

## 4. Draft the DM flow (comment to booked call)

Otto doesn't send DMs. The owner sends them from the inbox, or loads them into a DM tool (step 6). On Instagram a business gets one private reply per comment; the person must write back before you can message again. So message one has to earn a reply.

| Step | Goal | Draft |
|---|---|---|
| 1. Deliver | Keep the promise | The thing, plus one easy question whose answer qualifies them ("Is this for a salon or a clinic?"). No pitch, no price unless asked. |
| 2. Understand | Learn their situation | Reflect their answer, ask one more: what they've tried, or what's in the way. |
| 3. Offer the next step | Only if they fit and showed a need | One sentence linking their problem to the offer, then the booking link or "want me to send times?" |
| 4. Confirm | Booked | Date, what to bring, what happens on the call. |

Branches drafted after step 1: **interested** → step 2; **not now** → thank them, offer to check back in a month only if they say yes; **wrong fit** → point them to something useful, no pitch; **no reply** → on Instagram, nothing (the one private reply is used); where the platform allows a follow-up, one after 2-3 days that adds something (a tip, an example), then stop.

Rules: match how they wrote (one word in, two lines out). Under 950 characters. Never more than one question per message. Optional UTM on links: `?utm_source=<instagram|facebook|linkedin>&utm_medium=social&utm_campaign=<post or campaign>`; booking-page visits then show in GA4 (`ga4_run_report`, dimension `sessionCampaignName`). Nothing about the person in a tag.

### Objection replies (public or DM, from the facts only)

| They say | Reply shape |
|---|---|
| "How much?" | Public: "Depends on <what it depends on>; sending you the details." DM: the price if public in `brand/offer.md`, else the range or the call. |
| "Does this work for <their case>?" | Yes/no from the facts, plus one example. Unsure → owner. |
| "I tried something like this before" | Ask what didn't work. Don't argue. |
| "No time / later" | Acknowledge; offer the smallest next step. |
| "Is this legit?" | Public proof only (reviews, `social-proof-finder`); never invent a client. |

A reply that needs a claim not in the facts goes to the owner.

## 5. Show, then send

One table (visual by default): comment (first 60 characters) | platform | bucket | public reply | DM draft. Ask once: "Send these replies?"

- **Reply tools available**: send only the approved rows, exactly as approved: Instagram `meta_ig_reply_comment`, Facebook `meta_page_reply_comment`, LinkedIn `linkedin_page_reply_comment`. If a call fails, report it; don't retry in a loop.
- **No reply tools**: hand over the approved replies as a list to paste, one per comment, with a link to each post.

DM drafts always go to the owner (or into step 6). End with: comments read, keyword requests, questions sent to the owner, replies sent (or handed over).

## 6. ManyChat-ready DM flow

For a keyword post, write the flow so the owner can paste it into ManyChat or a similar official, Meta-approved DM tool. Never browser automation, never an unofficial tool. If Otto ever adds comment-to-DM automation, use that instead.

```
TRIGGER: comments on <post or "all posts"> containing: <KEYWORD>, <near misses: guide, giude, GUIDE pls>
PUBLIC AUTO-REPLY (3-5 variants, rotated): "<Sending it to your messages now>"
DM 1 (the one private reply, < 950 chars): <delivers the thing + one qualifying question>
  Buttons (optional): <"Salon" / "Clinic"> or none
IF THEY REPLY -> DM 2: <reflect + one question>   (inside the 24 h window their reply opens)
IF THEY FIT -> DM 3: <next step + booking link with UTM>
IF NO REPLY: nothing automatic. The owner may send one follow-up by hand only if the platform allows it.
STOP WORDS: stop, unsubscribe -> end the flow
```

**Setup checklist** for the owner: connect the Instagram professional account to the DM tool with its official Meta login; create the keyword trigger on the chosen post(s); paste the public replies and DM 1; add the reply branches; test with a second account; turn it off when the offer ends. Because the flow sends without a per-message yes, the owner approves the whole flow text here first.

## 7. Daily routine (15 minutes, human-run)

- **Morning**: run steps 1-5 on posts from the last 7 days. Reply to new-post comments within the first hours; early replies keep the thread going.
- **Afternoon**: a second pass on the newest post only. Send pending DMs; check who answered message one and send step 2.
- **Weekly**: count keyword comments, DMs answered, calls booked (owner's numbers) and booking visits from GA4. Repeated questions go to `comment-insights` and `topic-finder` as next post ideas. Log the totals in `social-data/leads.csv` (`week,post,keyword_comments,dm_replies,calls_booked`).

## Never

- Reply, hide or delete without the yes. Never set up an automatic responder yourself, and never use browser automation; automated DMs only through an official DM tool the owner sets up from the approved flow.
- Put a link in a public reply, or claim something was sent before it was.
- Answer a customer or billing issue in public.
- Message anyone who didn't comment or write first.

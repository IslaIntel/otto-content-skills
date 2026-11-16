---
name: sound-human
description: Edit a script, caption or post so it sounds like the business owner wrote it, by comparing it with brand/voice.md and the owner's real captions pulled through the Otto MCP, removing machine-sounding habits and running a read-aloud test, while keeping every fact and claim exactly as it was. Use when someone says "this sounds like AI", "make it sound like me", "humanize this", "too salesy", "too polished", or "clean up this caption".
license: MIT
---

# Sound human

Generated copy is easy to spot: every sentence the same length, three adjectives in a row, a cheerful wrap-up nobody asked for. Followers scroll past it, and on a small business account it costs trust. This skill edits text until it sounds like the owner on a normal day, and keeps every fact and promise exactly as it was.

Edits text only. Never posts or schedules.

## 1. Setup
Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short: read `brand/settings.md` (or memory) for workspace, accounts and output mode; ask only what's missing in one multiple-choice message and save it. Output is visual by default (artifact / HTML file / canvas) unless settings say chat.

- Read `brand/voice.md` (sound, words used, words never used, sample captions) and `brand/facts.md`.
- No `brand/`? Pull samples instead (step 2) and ask: "Three words for how you sound, and one word you'd never say?"
- Input: the text, and where it goes (spoken in a reel, caption, LinkedIn, story, email). Spoken text gets the stricter read-aloud test.

## 2. Pull the owner's real voice
- `meta_ig_list_media` (rowLimit 30): the captions. Keep the ones the owner wrote themselves (ask if unsure); drop ones made by a tool or an agency.
- `linkedin_profile_otto_posts` or `linkedin_page_posts` for LinkedIn text if that's the destination.
- From 10+ real captions, note the fingerprint: average sentence length, capital letters or not, emoji per post, how they start (straight in? a question?), how they end, the words they repeat, how they write numbers.

Under 10 real samples: say the fingerprint is thin. Not connected or `ok: false`: use `brand/voice.md` and the owner's answers only.

## 3. Our list of machine habits to look for

| Habit | What it looks like | Fix |
|---|---|---|
| Throat-clearing opener | starts by announcing what it's about to say | start at the point |
| Even rhythm | every sentence 12 to 18 words | mix: some 3 words, some longer |
| Stacked adjectives | three descriptive words in a row | keep the one that's true and specific |
| Grand verbs | "elevate", "transform", "empower", "unleash" | the plain verb for what actually happens |
| Vague praise | "high-quality", "seamless", "top-notch" | a fact: the material, the time, the number |
| The neat bow | a last line that restates the post as a lesson | stop when the point is made, or end on the action |
| Fake contrast | sets up a claim nobody made just to knock it down | say the claim directly |
| Hedge pile | "can help", "may potentially", "in many cases" | commit, or cut the claim |
| Rule of three | lists that always have exactly three items | use the real number of items |
| Formal links | "additionally", "furthermore", "moreover" | "and", "also", or a new sentence |
| Emoji confetti | an emoji on every line | match the owner's real habit (often zero or one) |
| Hashtag soup | 15+ generic tags | the owner's usual count, specific to place and topic |
| Brand-speak | "we are passionate about", "our mission is" | what you did, for whom, this week |
| Over-explaining a joke | the punchline followed by why it's funny | delete the explanation |

Add any word from "words we never use" in `brand/voice.md` to the search.

## 4. Edit, in this order
1. **Lock the meaning**: list every fact, number, price, promise and call to action in the original. These must survive unchanged. If one is not allowed by `brand/facts.md`, flag it rather than rewriting it.
2. **Strip the habits** from the table.
3. **Match the fingerprint**: sentence length, capitals, emoji, opening and closing style, the owner's repeated words. Swap generic words for words from their captions or their customers' words in `brand/audience.md`.
4. **Read-aloud test**: read it at speaking speed. Any spot where you'd take a breath mid-phrase, trip on a word, or sound like a radio ad gets rewritten. For spoken reel lines, every sentence must be sayable in one breath (about 15 words or fewer).
5. **Meaning check**: compare with the locked list from step 1. Same facts, same promise, same call to action. Nothing added.
6. **Length**: the edit should usually be shorter. Never longer by more than 10%.

## 5. Output

Default is visual (artifact / HTML file / canvas); chat if settings or the user say so.

```
VOICE: <3 words> | fingerprint from <n> of your captions: <avg sentence length>, <caps>, <emoji>/post
Destination: <reel spoken / caption / LinkedIn / story>

BEFORE
<original>

AFTER
<edited text>

Changed: <habit> x<n>, <habit> x<n> ...
Kept exactly: <facts, numbers, CTA>
Flags: <any claim not in brand/facts.md, or "none">
Read-aloud: passes / lines rewritten: <which>
```

If the owner rejects a word or phrasing, offer to note it in `brand/voice.md` via `brand-brain` wrap-up.

## Never
- Change a fact, a price, a promise or a call to action.
- Add claims, stories or details that weren't in the original.
- Make text sound like a specific real person other than the owner.

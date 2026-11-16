---
name: hook-writer
description: Write 10 short-video hooks (spoken line, first frame and on-screen text for each) across different patterns, ranked against the hooks that actually worked on your account, pulled through the Otto MCP or read from brand/winners.md. Use when someone says "write me a hook", "how should this reel start", "first 3 seconds", "opening line for this video", "scroll stopper", or "my hook is weak".
license: MIT
---

# Hook writer

A hook is three things that land together in the first 1 to 2 seconds: what's on screen, what's said, and what's written. This skill writes 10 across at least 7 patterns, then ranks them by how close they come to what already stopped the scroll on your account.

Read-only. It writes text; it doesn't post anything.

## 1. Setup
Follow the settings, scope and capability rules ("How every skill talks to the user" in this folder's `otto-rules.md`). In short: read `brand/settings.md` (or memory) for workspace, Instagram account and output mode; ask only what's missing in one multiple-choice message and save it. Output is visual by default (artifact / HTML file / canvas) unless settings say chat.

- Read `brand/voice.md`, `brand/audience.md` and `brand/winners.md`. Missing? Ask what the reel is about, who it's for, and the one reaction you want (stop, share, save, comment). Suggest `brand-brain`.
- Ask for the topic and the payoff (what the viewer gets by the end). If you don't know the payoff, the hook can't be honest; ask.
- If the reel already exists, ask what the first frame shows. A hook has to match footage you have or can film.

## 2. Pull your winning hooks
Use `brand/winners.md` if it's under 2 weeks old. Otherwise:
- `meta_ig_list_media` (rowLimit 60), then `meta_ig_media_insights` (batches of 25): `reach, shares, saved, comments, ig_reels_avg_watch_time, reels_skip_rate`. Reels at least 3 days old from the previous 28 days (your usual). Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
- Take the first line of each caption as a stand-in for the on-screen hook, and ask the owner to correct it where the reel said something else.
- Best 5 and worst 5 by skip rate (lower is better), with shares and saves per 1,000 reach alongside.
- If `hook-patterns` has run, use its pattern table instead.

`reels_skip_rate` is already a percent. Not connected or `ok: false`: say so and rank on principles only.

**Second source: other accounts' hooks (comparison only).** If `meta_ig_business_discovery` is in the tool list, pull recent reels from accounts the user names and take the first caption line of their most-liked reels. Otherwise use examples the user supplies (links or files), analysed with `reel-breakdown` for the first frame, first line and on-screen text. Note the patterns; never copy the words. Your own winners stay primary.

## 3. Write 10 hooks, at least 7 patterns

| Pattern | Shape |
|---|---|
| Caught mid-problem | the viewer's situation, already going wrong on screen |
| The odd number | a specific, surprising figure from `brand/facts.md` |
| For the person who | "for anyone who <specific situation>" (built for shares) |
| Wrong way first | someone doing the common mistake, then the stop |
| The result, then how | the finished outcome in frame 1, method withheld |
| A question they'd answer yes to | names the pain in their words from `brand/audience.md` |
| Overheard | a line a customer actually says, quoted |
| Before / after split | both halves visible at once |
| The countdown | "3 things", with the list visible and number 3 promised as the best |
| Plain contrarian | a true opinion most of the industry wouldn't say |

For each hook:
- **Spoken**: 12 words or fewer, in the owner's voice, subject first.
- **First frame**: what's moving at 0.0s and what fills most of the screen.
- **On-screen text**: 3 to 7 words. It must work alone with the sound off; don't repeat the spoken line word for word.

## 4. Score and rank

Score each hook 0 to 2 on six checks (12 max):
1. Something moves or changes at 0.0s.
2. The viewer can tell it's about them within a second.
3. Text works on mute and is readable on a phone held at arm's length.
4. It opens a question the reel truly answers.
5. Uses the customer's words, not marketing words.
6. **Matches your data**: resembles your low-skip hooks (pattern, first-frame type, opening word form) and avoids what your high-skip hooks share. With fewer than 5 reels on a side, score this 1 for all and say "too few to tell". A pattern seen only in other accounts' examples can earn 1 here, never 2.

Rank by total; break ties on check 6. For the top 3, give a one-line reason that cites your numbers where they exist:
`Similar to your "for anyone who..." reels: median skip 24% vs your 33% (n = 6).`

## 5. Output

Default is visual (artifact / HTML file / canvas); chat if settings or the user say so.

```
HOOKS for: <topic> | goal: <reaction> | payoff: <what they get>
Your hook baseline: median skip <x>% across <n> reels (<dates>)
Seen elsewhere: <patterns from other accounts' examples, n, source, or "none supplied">

| # | Pattern | Spoken | First frame | On-screen text | Score |
|---|---|---|---|---|---|
| 1 | ... | "..." | ... | "..." | 11/12 |
...

Test first:
1. #<n> because <reason with your numbers>
2. #<n> because ...
3. #<n> because ...

Test plan: post the top pick; if skip rate is worse than <baseline>% after 3 days, hand #1 vs #2 to `hook-test` (change only the first 2-3 seconds; reposting the same reel can count as a duplicate).
```

Hand off to `reel-script` with the chosen hook, or to `hook-test` to compare two hooks on the same footage.

## Never
- Write a hook that promises something the reel doesn't show.
- Use a number that isn't in the pull, `brand/facts.md`, or the owner's message.
- Lift another creator's hook word for word.

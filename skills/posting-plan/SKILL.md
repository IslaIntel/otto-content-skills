---
name: posting-plan
description: Builds a 2-4 week posting plan from your content pillars, your own winning posts and your best posting times, checks what's already scheduled in Otto, includes recurring series, and after you approve hands posts to Otto scheduling (if your connection has it), to `post-queue`, or to you to post by hand. Use when someone says "plan my content", "make a content calendar", "what should I post next week", "plan the next month", "I need a posting schedule", or "start a weekly series".
license: MIT
---

# Content calendar

Turns pillars and past results into dated posts the user can actually make. Most slots go to ideas that are close to what already worked; a few test something new. It fits around what is already scheduled and never plans more than the user has been able to ship. Planning is read-only; scheduling waits for an explicit yes on each post.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or the assistant's memory) for workspace, accounts, default platforms and timezone. Ask only what's missing, in one bundled multiple-choice question, and save the answers.
- Plan only for the platforms the user named, else the defaults; with no default, ask once ("All connected" as an option). A platform with no posts gets one line, not an empty table.
- Before offering to schedule, check which tools this session has (step 5).

Also read `brand/pillars.md` (from `content-pillars`; if missing, run it first or ask for 3-5 themes and mark the plan "pillars unverified"), `brand/winners.md` and `brand/offer.md`.

Skill questions: length (2, 3 or 4 weeks), hours per week available to create, dates that matter (launch, holiday, event).

## 1. Pull

1. **Already scheduled**: `otto_schedule_list` with `status: "upcoming"`, `from`/`to` covering the plan, `timeZone`. Leave `showCalendar` unset (on an external connection it opens a new Otto chat). Rows give channel, title, time and status; treat each as a fixed slot.
2. **Recent cadence**: `otto_schedule_list` with `status: "past"` for the last 4 weeks, and `meta_ig_list_media` (rowLimit 60) timestamps. Count posts per week per platform.
3. **Winners**: `meta_ig_media_insights` on the last 90 days (batches of 25: `reach, views, shares, saved, comments`, plus `ig_reels_avg_watch_time, reels_skip_rate` for reels); `youtube_top_videos`; `meta_page_posts` + `meta_page_post_insights`; `linkedin_page_posts` + `linkedin_page_insights`. Winner = 2x your median on reach, or on shares or saves per 1,000 reach. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
4. **Timing**: use `best-time-to-post` output if it exists. If not, group your own posts by weekday and hour block and compare median reach; with fewer than 5 posts per block, say "too few to tell" and keep your usual times.

Any failed pull: name it, plan with what's left, never fill numbers in.

## 2. Set the volume

- Planned posts per week ≤ **1.25x your average of the last 4 weeks**, per platform. More than that needs the user to say so, with their hours.
- Repurposed pieces (`repurpose`) count, since they still take time.

## 3. Fill the slots

Split each week:

| Slot type | Share | What it is |
|---|---|---|
| Remix | ~60% | A winner's idea with a new hook or angle, or a winner's format on a new topic |
| Pillar fill | ~30% | Seed ideas from `brand/pillars.md`, in proportion to each pillar's share |
| Test | 1 per week | One new thing, changing one variable (format, hook style, length or time). Name the number that decides it |

Rules: no pillar twice in a row on the same platform; spread formats by what has worked per pillar; the business ask (offer, booking, link) on roughly 1 in 4 posts, not every post; dates the user named get a matching post before them.

## 4. Series (recurring formats)

Add 1 series (2 if the user ships 5+ posts a week). A series earns its slot when:
- It's built on a format or topic that has already won at least once.
- It has a name people can say, the same opening each time, and the same day and time.
- You can list 8 episodes now. If you can't, it isn't ready.
- There's a reason to come back (each episode stands alone, and the next one is promised in the caption).

Run it for at least 6 episodes before judging. Compare each episode with your median, not with episode 1.

## 5. Optional: get approved posts out

Only for posts whose media is final, and only after the user says yes to that exact post (media, caption, platform, time). Pick the path by what this connection can do:

1. **Otto scheduling** (only if your Otto connection includes `channel_submit_plan`): media must be in the Otto library (`media_list`). `channel_submit_plan` with the right `provider` (`meta_ig`, `meta_pages`, `linkedin_profile`, `gbp`), one step (`ig_publish_reel`, `ig_publish_carousel`, `ig_publish_image`, `page_publish_video`, `page_create_post`, `linkedin_profile_create_post`, `gbp_create_local_post`), `publishAt` as ISO with offset, `timeZone` as IANA. Each extra post needs `additional: true`, or it replaces the plan still waiting for approval. It publishes **after the user approves in Otto** (`approveUrl`); call it scheduled only if the result says `scheduled: true`, then confirm with `otto_schedule_list` (upcoming).
2. **Publish tools but no scheduling**: hand the approved posts to `post-queue`, which queues them and sets up scheduled tasks to publish on time.
3. **Neither**: the calendar is the deliverable. The user posts each item by hand from it; give the file, caption and time per post.

YouTube is read-only in Otto: always by hand.

## Output

Default is visual (artifact / HTML file / canvas) unless settings or the user say chat. Content:

```
## Content calendar: <start> to <end> (<time zone>)
Volume: <n>/week on <platforms> (last 4 weeks averaged <n>)
Already scheduled: <count> (kept as fixed slots)

| Date | Time | Platform | Pillar | Format | Slot | Idea / working hook | Built from | Goal |
|---|---|---|---|---|---|---|---|---|

### Series: <name>
Day/time: <...>  Opening: <...>  Built on: <winning post, metric vs median>
Episodes 1-8: ...

### This period's tests
| Test | Variable changed | Decides on | Needs |

### Batch plan
Make together: <which posts share a shoot or a setup>
```

## Never

- Plan over the volume cap without the user agreeing.
- Schedule or queue a post without an explicit yes to that post, or call it scheduled without `scheduled: true`.
- Promise Otto scheduling before checking the connection has it.
- Double-book a slot already in `otto_schedule_list`.
- Cancel or move existing scheduled posts unless asked (`otto_schedule_cancel` / `otto_schedule_move` need a yes too).

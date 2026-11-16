---
name: weekly-social-review
description: Weekly social media performance review across the platforms you choose (Instagram, Facebook, LinkedIn, YouTube), measured against your own baseline, ending in a short keep/change/test/stop plan for next week. Use when asked for "the weekly review", "weekly report", "how did my posts do this week", "how did my reels do", or "what's working on social".
license: MIT
---

# Weekly social review

Turns a week of numbers into at most three decisions, shown as an interactive dashboard: weekly totals at the top, every post in a list, and a click on any reel opens its full diagnosis.

## 0. Setup

Before anything else (full rules: "How every skill talks to the user" in `otto-rules.md` (in this skill's folder)):
- **Settings**: read `brand/settings.md` (or what the assistant remembers). Don't ask what it already answers. Save new answers there (or to memory when there's no folder).
- **Account**: if the Otto connection has more than one business or more than one Instagram / Facebook account (`meta_page_list`), ask which, once.
- **Scope**: platforms the user named are the scope ("my Instagram" = Instagram only). Nothing named: use "Default platforms" from settings; with none saved, ask once with the connected platforms (`otto_list_connections`) as options plus "All connected", and save the answer. A platform in scope with no posts gets one line; out-of-scope platforms aren't mentioned. A platform in scope that isn't connected: say so every run, in one line with its `otto_connect_link`, in the chat summary and in the dashboard `notes`.
- **Output**: visual by default (the dashboard below); chat if settings say `output: chat` or the user asks.
- Read-only on every platform: never call a publish, schedule, delete, reply or hide tool. Organic posts only; ads only if asked.
- **Accounts**: put each in-scope platform's handle and profile URL in `meta.accounts` (from `meta_page_list`, `linkedin_page_list`, `youtube_list_channels`; Instagram: `https://www.instagram.com/<username>/`), so the names in the header link to the profiles.
- Window: the last 7 days **including today**, unless told otherwise, so the newest posts always show. Posts under 3 days old get an **early read** (status `young`, "Early read") and a final call next week; totals (views on the week's posts) include every post in the window; medians, KPI comparisons and calls use only posts old enough to judge. YouTube Analytics runs about 2 days behind: for the newest Shorts use the lifetime public counts from `youtube_list_recent_videos` and say so.
- If a `social-data/` folder exists, read the earlier weeks from it. If not, create it (see step 6).

## 1. Pull

**Instagram**
- `meta_ig_list_media`: every post since the last review, plus the previous 4 weeks for the baseline. Set rowLimit to about 1.2 x posts per day x days; if the result is saved to a file, read it with code.
- `meta_ig_media_insights`, batches of 25: `views, reach, likes, comments, shares, saved, total_interactions, ig_reels_avg_watch_time, reels_skip_rate`. Don't request `crossposted_views` or `facebook_views`: one reel that wasn't crossposted to Facebook fails the whole batch. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
- `meta_ig_account_insights`, `metricType: time_series`, metrics `reach` and `follower_count`, with `endDate` = the day after the window ends (the end date is exclusive). `follower_count` is **daily new follows**, and Meta returns it only once the account has 100+ followers. The total audience is `profile.followersCount`; record it every run and compute growth as the difference from last week.

**Facebook Page**: `meta_page_list` (it also maps each Page to its Instagram account), `meta_page_posts`, then `meta_page_post_insights` (batches of 25; `post_media_view` is Facebook's "views"), and `meta_page_insights` for the page trend. Page-level views can be lower than the sum of post views, so rank posts with post-level numbers.

**LinkedIn Page**: `linkedin_page_posts` and `linkedin_page_insights`. `kpis.followers` is the current total, not the week's gain.

**YouTube**: `youtube_top_videos` and `youtube_channel_analytics` (dimensions `["video"]`, metrics `views, averageViewPercentage, subscribersGained, shares`, sort `-views`, rowLimit 200) for the window; `youtube_traffic_sources` if views moved a lot.

**Search and site (if GA4 / Search Console are connected)**: social and search feed each other. Instagram reels, YouTube videos and Facebook posts can show up in Google results, and people who see a post often Google the business afterwards.
- `ga4_run_report`, dimensions `["date","sessionDefaultChannelGroup"]`, metrics `sessions, engagedSessions`, the window and the 4 weeks before it, then add the days up into your window and the previous ones (ISO weeks only line up when the window runs Monday-Sunday): sessions from Organic Social, and whether Organic Search moved in weeks with a breakout post. (`ga4_traffic_sources` only gives one total for the range.)
- `ga4_run_report`, dimension `landingPage`, filtered to `sessionDefaultChannelGroup` = `Organic Social`: the pages social visitors land on, and whether they stay.
- `gsc_search_analytics`, dimension `query`, this week vs the previous 4 weeks. Search Console runs 2-3 days behind: end its window 3 days ago, or mark the last days "not yet available", so they don't read as a drop. Look for brand-name searches (a lift after a strong week of posts is a real signal), and new questions people are typing that a post could answer. Hand those to `search-and-social`.
Visits and searches show what happened, not why. Say "coincides with", not "caused by".

## 2. Compute

For every post: reach (or views), engagement per 1,000 reach (likes, comments, shares, saves separately), and for reels: skip rate, average watch seconds (`ig_reels_avg_watch_time` is in **ms**), watch % (avg watch / length; `reels_skip_rate` is already a percent).

**Totals first.** Per platform, add up views for the posts in the window and for the same number of days before it: these are the headline numbers (`hero` KPI, `vsLabel: "last week"`), because people want to see the big number. The per-post median goes underneath (`sub`).

Baseline for judging single posts = **median of the previous 4 weeks**, per platform. Each platform counts a "view" differently: report each in its own column, never one summed total.

Group posts by format (reel, carousel, image, video, text), topic, series and hook style when you can tell them apart. A group with fewer than 5 posts is labelled "too few to tell". If a group only ran in one stretch of time (a new series, a new cadence), compare it with the median of that stretch, not the whole baseline.

## 3. Diagnose

Run the `reel-diagnosis` skill on the best 3 and worst 3 reels, and on any group that moved more than 25% from its baseline.

Then decide, one variable at a time:
- **Winner**: 2x the median on reach, or on shares/comments per 1,000 reach with reach at least half the median. If a median is 0 (common on small accounts), drop that signal and say so. Remix it: same idea, new hook, new look.
- **Keep**: above the median.
- **Below usual**: below the median, but not yet three weeks running (post status `stalled` with label "Below usual"; group call `below`).
- **Retire**: a format or topic below the median three weeks running.
- **Tiny numbers**: when a platform's median is under 50 views (e.g. a quiet Facebook Page), a post also needs **100+ views** to be called a winner; 2x of 5 views is noise.

## 4. Show it: the dashboard

Run `reel-diagnosis` logic on **every** reel in the window (not just the best and worst), so each post carries its own `diagnosis` (steps, verdict, evidence, one change). Then:

- **Visual (default)**: fill `dashboard.html` in this folder, following `dashboard-data.md`. Platforms in `meta.platforms` = the scope only. Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/<YYYY>-W<ISO week of the window's last day>.html` (Claude Code / Cowork), or a canvas (ChatGPT).
- **Chat**: the `report-template.md` file next to this SKILL.md, as markdown. Also saved as `social-data/reports/<...>.md` when there's a folder.

Rules for either:
- Keep what was measured apart from what you think caused it.
- Max **3 changes** for next week, each with its evidence and a "done when" check.
- If you suggest a test, it changes one thing and holds everything else (topic, length, caption, time, platform). Name the deciding number and how many posts or views before it means anything.
- Include the posts that did badly and the ones with missing data.
- "Not enough signal yet" beats a story.

## 5. Save the numbers

**No folder (claude.ai, ChatGPT):** give `posts.csv` and `account.csv` as downloads and say: "Attach these next week so the review has a full baseline." If the user attaches last week's CSVs, read them first and add the new rows.

With a folder, so next week has a baseline, upsert one row per post into `social-data/posts.csv`:

`platform,post_id,permalink,posted_at,format,age_days,reach,views,likes,comments,shares,saves,skip_rate,avg_watch_s,watch_pct,length_s`

and one row per day per platform into `social-data/account.csv`: `date,platform,followers_total,new_follows,reach`.

End your reply with three lines: the week in one sentence, the best post, and the one change to make first.

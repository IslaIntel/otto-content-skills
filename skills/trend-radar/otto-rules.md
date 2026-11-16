# Otto skill rules

Shared rules for every Otto Content Skill. The SKILL.md next to this file says what the skill does; this file says how every skill talks to the user, what to check before calling tools, and the verified facts about the Otto MCP tools. Read it before the first Otto tool call.

## How every skill talks to the user

These rules apply to every skill. Skills reference this section instead of repeating it.

### 0. Workspace and accounts first, before any data

Do these before calling any other Otto tool:
1. **Workspace.** If `otto_list_workspaces` is available, call it. One workspace: use it. Several: ask which (multiple choice). Pass its **id** to every later call. Never assume the workspace is named after the business; if a call returns `workspace_forbidden`, the error lists the user's real workspaces: use those.
2. **Connections.** `otto_list_connections`, then the account lists (`meta_page_list`, `linkedin_page_list`, `youtube_list_channels`).
3. **More than one account on a platform** (e.g. three Instagram accounts): **ask which one**, with the account names as options. Don't choose by matching a name, even when one looks obvious. Exception: settings or a brand card that name the account count as the answer.
4. **Website.** If the skill needs the business's site, ask for it or confirm the one you found ("Is example-florist.com your site?"). Don't guess.
5. Settings and interview questions come **before** pulling data or writing files. Ask them in one bundled multiple-choice message.

Only `otto_list_workspaces`, `otto_list_connections` and the account-list tools may run before these answers.

**Finding the tools.** Some clients load tools on demand (claude.ai shows them only after a tool search). If a tool named in a skill isn't available, search for its exact name (e.g. `otto_list_workspaces`); if that doesn't load it, search a short description ("list workspaces"). Only after both fail, treat the tool as unavailable. Tool lists can differ between chats on the same account. If `otto_list_workspaces` is unavailable, use the workspace named in settings or the brand card; with none, call tools without a workspace (the connection's default) and say which business the data turned out to be.

### 1. Settings: ask once, remember

Preferences live in `brand/settings.md` (template: `skills/brand-brain/settings-template.md`): business and accounts (which Otto workspace, which Instagram / Facebook / LinkedIn / YouTube account), platforms to include by default, timezone, output mode, caption template, CTA on or off, comment sources.

- **Read it first.** If it exists, don't ask what it already answers.
- **Missing pieces**: ask only what this skill needs, in one go, then save the answers.
- **Where to save, by environment:**
  - A working folder (Claude Code, Claude Cowork, Claude desktop with a folder): write `brand/settings.md`.
  - No folder (claude.ai chat, ChatGPT): ask the assistant's own memory to keep it ("remember my Otto settings: ..."), and if the user works in a Claude Project, give them the settings block to paste into the Project's instructions or knowledge once. Never ask the same question twice in one conversation.
  - **Memory off** (the assistant can't save memories): say so once, in one line: "To skip these questions next time, turn on memory (Settings → Capabilities), or keep the brand card in a Claude Project." Then carry on.
  - **Settings pasted or attached by the user** (a `settings.md`, a brand card, a Project file): read them first and treat them as answered.
- The user can change any setting by saying so ("from now on, no CTA"). Update the file or memory.

### 2. Scope: only what the user wants

- **Named platforms are the scope.** "Weekly review for Instagram and Facebook" means only those two, even if YouTube is connected.
- **Nothing named**: use the default platforms from settings. With no default yet, ask once which connected platforms to include, with "All connected" as an option, and save the answer.
- **In scope but not connected** (the user asked for it, or it's in their default platforms): say so **every run**, in one line with the `otto_connect_link` link, in the chat summary and in the dashboard `notes` ("YouTube isn't connected yet: connect it and this review will include it."). Each chat starts fresh, so "I mentioned it before" doesn't count.
- **Not in scope and not connected**: mention it at most once, during setup (brand-brain), never in reports.
- **Nothing to show**: a platform in scope with no posts in the window gets one line ("No Facebook posts this week"), never an empty table or a row of zeros. A platform out of scope isn't mentioned at all.

### 3. Asking questions

Bundle questions and keep them short. Use the client's multiple-choice question tool when there is one (Claude Code and claude.ai can show clickable options with an "Other" answer): 2-4 options, the recommended one first. Otherwise ask in one short message with numbered options the user can answer with a number.

### 4. Output: visual by default

- **Default**: anything that reports, compares or plans is shown visually. In claude.ai / Claude desktop: an artifact. In Claude Code / Cowork: an HTML file saved next to the data and opened in the browser. In ChatGPT: a canvas.
- Skills that ship a template **fill the template**; they don't redesign it. Keep the Otto mark in the header and footer. The shared dashboard (`templates/dashboard.src.html`, built into each skill by `templates/build.py`) serves every report skill: post reviews use `kpis`/`daily`/`posts`, other reports use `blocks` (stats, table, bars, heatmap, cards, list). Format: `templates/dashboard-data.md`. To add a report skill: give it an example in `templates/samples.py` and run the build. `reel-breakdown` has its own layout (`templates/reel-breakdown.src.html`, frame timeline) built from the dashboard's base styles, so branding changes in the dashboard reach it too.
- Write the verdict last, from the numbers on the page; every claim in it must match a number shown.
- **Chat mode**: if the user says "just tell me in chat" (or settings say `output: chat`), answer in chat and remember it. If they later say "show me this visually", make the visual for that answer; switch the default back only if they say so.

### 5. Check what this Otto connection can do

Otto plans differ in which tools they include. Before a skill offers to publish, schedule, reply, upload or touch ads, it checks which of those tools are available in this session (look at the tool list, or `otto_list_connections`) and picks a path:

| Available | Path |
|---|---|
| `channel_submit_plan` with `publishAt` | Schedule through Otto (approval in Otto) |
| Publish tools only (`meta_ig_publish_reel`, ...) | Publish now on approval, or queue with `post-queue` |
| Reply tools (`meta_ig_reply_comment`, ...) | Send approved replies |
| Ads write tools (`meta_create_campaign`, ...) | Build paused, on approval |
| None of the above | Hand over the finished thing and step-by-step instructions to do it by hand |

Don't talk about plans or tiers. Say what will happen ("I'll give you the file and the steps to post it").

A tool being listed doesn't guarantee the plan allows it: some Otto plans list every write tool even when the plan doesn't include it. If a write call comes back refused (not allowed, upgrade required, permission error), don't retry: say it plainly in one line and switch to the next path down the table (publish now → `post-queue`/manual, schedule → manual, reply → drafts only).

### 6. Visuals are made in code, never by AI image generation

Covers, carousels, slides, charts and dashboards are built by Claude in code: HTML/CSS, SVG, Canvas, three.js for 3D or motion, then rendered to PNG/MP4 where the environment can (a headless browser in Claude Code / Cowork; in claude.ai the artifact is the deliverable, plus a screenshot or download step). Photos and video frames come from the user's own files or their own posts. Never call `media_generate` or any image-generation tool, and never promise a generated photo.

### 7. Otto mark

Every shipped template has a small, non-blocking Otto mark (header logo text "Otto" and a footer "Made with Otto Content Skills" that links to ottowebmaster.com). Keep it when filling a template; don't add it to the user's own published posts.

## Brand brain (shared memory)

Skills read, and the `brand-brain` skill writes, a `brand/` folder in the working directory:

- `brand/settings.md`: workspace, accounts, default platforms, timezone, output mode and other preferences (rule 1 above).
- `brand/voice.md`: how the business talks, words it uses and avoids, sample captions.
- `brand/audience.md`: who they serve, their problems in the customer's words.
- `brand/offer.md`: what they sell, prices if public, the one action they want people to take, links.
- `brand/facts.md`: claims the business may make (and may not).
- `brand/winners.md`: their best posts with numbers and why they worked (updated by analytics skills).
- `brand/pillars.md`: 3-5 content pillars with share of output and seed ideas (written by `content-pillars`).
- `brand/personas.md`: evidence-led audience personas (written by `audience-map`).
- `brand/proof.md`: approved testimonials, reviews and results with permission status (written by `social-proof-finder`).

If `brand/` is missing, a creation skill asks the 3-4 questions it needs and suggests running `brand-brain` once.

Analytics history lives in `social-data/` (`posts.csv`, `account.csv`, `reports/`), with the columns defined in `skills/weekly-social-review/SKILL.md`.

## Rules learned from live test runs

- **Check connections every run**, even when settings or a brand card answer everything: `otto_list_connections` is cheap and is the only way to notice a platform in scope that isn't connected (mention it every run, in one line, with `otto_connect_link`).
- **Tiny numbers.** When a platform's usual is under 50 views or reach (a quiet Facebook Page), a post also needs **100+** to be called a winner or "taking off"; 2x of 4 views is noise. Say the platform is too quiet to judge single posts.
- **One "usual" for every skill.** "Your usual" always means the median reach (or views) of posts at least 3 days old from the **previous 28 days**, per platform. Daily, weekly and per-reel skills must agree; if a skill can't reach 28 days back, it says how many days its usual covers. A short window (the last 1-2 weeks) makes a slow stretch look normal and every post look like a winner.
- **One workspace can hold several brands.** A workspace may have more than one Instagram/Facebook pair (`meta_page_list`). Ask which account, then keep it.
- **Reel-only metrics on reels only.** `ig_reels_avg_watch_time` and `reels_skip_rate` fail the whole `meta_ig_media_insights` batch if any id in it is an IMAGE or CAROUSEL_ALBUM. Split by `mediaType` first.
- **Big results get saved to a file.** `meta_ig_list_media` returns ~2,000 characters per row (signed media URLs): 25 rows fits in a normal tool result, 40+ usually doesn't. `gsc_search_analytics` overflows at a few hundred rows (more with two dimensions). When a result is too big, the client saves it to a file: read that file with code (parse the JSON, keep the fields you need) instead of asking again with a smaller limit and losing data. `meta_ig_list_media` has no paging cursor yet, so request the rows the window needs (about 1.2 x posts per day x days). `youtube_channel_analytics` with dimension `insightTrafficSourceDetail`: rowLimit 25 (API maximum).
- **New accounts look like everything is rising.** If a comparison window has under 25% of the recent window's volume, report "too new to compare" instead of growth.
- **Too few comments to cluster.** Under ~10 meaningful comments, fall back to Search Console question queries.
- GA4 Organic Social sources include `meta` (Facebook) and `ig` (Instagram) as well as the domains.
- `profile.mediaCount` can be higher than what `meta_ig_list_media` returns (some items, e.g. Stories or removed posts, aren't listed). Count posts from the list, not the profile.
- **Windows that don't match calendar weeks.** GA4 `isoYearIsoWeek` buckets are Monday-Sunday. For any other window, pull with dimension `date` and add up the days yourself.
- **GA4 times are in the property's timezone** (`metadata.timeZone` in the result). Convert to the user's timezone before comparing with post times.
- **Windows that end in the future.** When part of a window (e.g. a 7-day tail) hasn't happened yet, report the days available, mark the rest "not yet available" and say when to re-run.
- **End dates are exclusive on account insights.** For a window ending on day D, pass `endDate` = D + 1.
- **A median of zero kills the signal.** Small accounts often have a median of 0 shares or comments per post. Then "2x the median" is meaningless: drop that signal and say so.
- **Reach floor.** Don't call a post a winner on a ratio alone when its reach is under half the account median (1 share on 200 reach is noise).
- **Time confounds traits.** If a trait (format, series, caption style) only ran during one period, compare it against that period's medians, not the whole window: a cadence or algorithm change can look like a trait effect.
- **Unknown reel length.** Without lengths, compare average watch seconds only between reels of similar length, and don't call a pacing failure.
- **YouTube `averageViewPercentage` can exceed 100%** on Shorts that loop. Cap it at 100 when ranking and say why.
- **GA4 weekly splits.** `ga4_traffic_sources` returns one total for the range. For week-by-week, use `ga4_run_report` with dimensions `["isoYearIsoWeek","sessionDefaultChannelGroup"]`. To see where social visitors land, `ga4_run_report` with `landingPage` filtered to `sessionDefaultChannelGroup == Organic Social` (`ga4_landing_pages` can't filter).

## Otto MCP: verified facts (tested against a live account, Nov 2026)

**Discovery**: `otto_list_connections` (providers: `meta_ig`, `meta_pages`, `linkedin_pages`, `linkedin_profile`, `youtube`, `ga4`, `gsc`, `gbp`, `meta` (ads), `google_ads`, `shopify`, `wordpress`, ...; each with selected ids). `meta_page_list` maps each Facebook Page to its `instagramBusinessAccountId`. `linkedin_page_list`, `youtube_list_channels`.

**Instagram**
- `meta_ig_list_media(igAccountId, rowLimit)`: id, caption, mediaType (VIDEO / IMAGE / CAROUSEL_ALBUM), mediaUrl (a downloadable MP4 for your own reels; it can be null for reels that still play), permalink, timestamp, commentsCount. No views.
- `meta_ig_media_insights(igAccountId, mediaIds[≤25], metrics[≤15])`: works: `views, reach, likes, comments, shares, saved, total_interactions, ig_reels_avg_watch_time, reels_skip_rate`. `ig_reels_avg_watch_time` is **milliseconds**. `reels_skip_rate` is already a **percent**. Never request `crossposted_views` / `facebook_views` (one non-crossposted reel fails the whole batch). No per-reel follows or profile visits.
- `meta_ig_account_insights(igAccountId, startDate, endDate, metricType: "time_series", metrics: ["reach","follower_count"])`: daily reach; `follower_count` = daily NEW follows and only exists at 100+ followers. `profile.followersCount` = total, returned on every call. Daily `endTime` labels mark the start of the Pacific day. **Facebook is the opposite**: `meta_page_insights` daily `end_time` marks the end of the day, so the value labelled Nov 8 is Nov 7's. Today's value on either platform is incomplete: label it "so far" or leave it out.
- `meta_ig_list_comments(igAccountId, mediaId, rowLimit)`. Some comments come back with `text: null`; skip them. List only posts with `commentsCount > 0`.
- Reel length is not a returned field. Fallback: the `mediaUrl` query string carries an `efg` value (URL-safe base64 JSON) with `duration_s`; decode it **with code**, never by reading the base64 by eye (`json.loads(base64.urlsafe_b64decode(efg + '=' * (-len(efg) % 4)))['duration_s']`), and say the length was read from the video link. No `mediaUrl` (it can be null): ask the user, or use average watch seconds instead of watch %.
- Stories: Otto can't post them or read Story insights. Story skills work from the user's screenshots.
- Writes (approval only): `meta_ig_reply_comment`, `meta_ig_set_comment_hidden`, `meta_ig_publish_image`, `meta_ig_publish_carousel` (public image URLs, 2-10), `meta_ig_publish_reel` (Otto media library `mediaId`, optional cover; cover can only be set at publish).

**Facebook Pages**: `meta_page_posts(pageId)` (id, message, createdTime, permalinkUrl), `meta_page_post_insights(pageId, postIds[≤25])` returns by default `post_media_view` (times on screen), `post_clicks`, `post_reactions_by_type_total`; use `post_media_view` as Facebook "views". `meta_page_insights(pageId, startDate, endDate)` returns daily `page_follows`, `page_media_view`, `page_post_engagements` and a weekly `kpis` object (followers, followerGain, views, likes, shares, posts, engagements). Page-level views can come out lower than the sum of post views (reel views may not be counted at page level), so rank posts with post-level numbers and treat page `kpis` as a rough trend only. `meta_page_list_comments`, `meta_page_reply_comment`.

**LinkedIn**: `linkedin_page_posts(organizationId)`, `linkedin_page_insights(organizationId, startDate, endDate)` → `kpis` (followers total, views, uniqueViews, likes, comments, shares, clicks) + daily rows. `linkedin_page_posts` carries no per-post numbers. `linkedin_page_list_comments` can return `linkedin_api_403` when the connection lacks comment permission: ask the user to reconnect LinkedIn Pages in Otto or paste the comments. `linkedin_page_reply_comment`. Personal profile: `linkedin_profile_list`, `linkedin_profile_otto_posts` (only posts Otto published, without analytics), `linkedin_profile_create_post` (approval only).

**YouTube**: `youtube_top_videos(startDate, endDate)` (views, minutes watched, averageViewDuration, likes, title, url). `youtube_channel_analytics(startDate, endDate, dimensions, metrics, sort)` is a free-form Analytics API report, e.g. dimensions `["video"]`, metrics `["views","averageViewPercentage","subscribersGained","shares"]`: **per-video subscribers gained**, which Instagram can't give. Also `youtube_traffic_sources`, `youtube_demographics`, `youtube_geo_countries`, `youtube_daily_overview`, `youtube_list_recent_videos`.

**Website / search**: `ga4_traffic_sources` (sessions by channel group incl. Organic Social), `ga4_landing_pages`, `ga4_run_report` (custom, e.g. filter `sessionSource` / `utm_campaign`), `ga4_geo`. `gsc_search_analytics(startDate, endDate, dimensions:["query"|"page"], dimensionFilterGroups)`: the questions people type into Google. Great for content ideas and caption keywords.

**Google Business Profile**: `gbp_list_reviews`, `gbp_search_keywords` (the searches that found the business), `gbp_daily_metrics`.

**Research (may be unavailable)**: `voc_search_reddit(query)` and `voc_fetch_url(url)` for customer language; `ad_library_find_advertisers` / `ad_library_list_ads` / `ad_library_search(country, query)` for competitor ads. These can return `ok: false` (e.g. `http_403`, `ad_library_disabled`). Then: say research is unavailable right now, offer the `libraryUrl` if returned, and ask the user to paste examples. Never invent competitor posts or quotes.

**Media library**: `media_create_upload` → upload → `media_complete` puts a user's own file into the Otto library and returns a mediaId (publishing tools take mediaIds). `media_list`, `media_get`. Image generation tools are **not** part of the public setup: never use them (rule 6).

**Scheduling (only on connections that include it; see rule 5)**: `otto_schedule_list` shows what's scheduled/published. To schedule a post for later: `channel_submit_plan(provider, steps:[{id, op, args}], summary, publishAt, timeZone)`; ops include `ig_publish_reel`, `ig_publish_carousel`, `ig_publish_image`, `page_publish_video`, `page_create_post`, `linkedin_profile_create_post`, `gbp_create_local_post`. It returns an `approveUrl`: the post goes out only after the user approves in Otto. Never claim something is scheduled unless the result says `scheduled: true`.

**Not available through Otto**: TikTok and X analytics/comments. Skills say so and ask for a screenshot or export when those matter.

## Writing style

- Plain, specific, second person to the user ("your reels"). Short sentences. No hype words (unlock, supercharge, game-changer), no "it's not X, it's Y" constructions, few dashes.
- Every number in an output must come from the pull or from the user. Say "not enough data to tell" rather than inventing a pattern. Groups under 5 posts are "too few to tell".
- One reel never proves a cause. Keep what was measured apart from what you think caused it.
- Analytics skills are read-only. Anything that posts, replies, hides, deletes, builds paid ads or schedules shows the exact content first and waits for an explicit yes in the conversation.
- Hand off to sibling skills by name (`reel-diagnosis`, `hook-writer`, ...) where the next step lives.
- Never mention other companies' products as requirements. No private ids, handles or names of real accounts in examples; use invented examples ("a florist in Austin").
- Write it originally. Don't copy wording from other skill packs; implement the job in our own words and method.

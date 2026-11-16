# Filling dashboard.html

`dashboard.html` (next to this file) is the finished design. To show results visually:

1. Copy `dashboard.html`. Don't edit the HTML: the browser tab title comes from `meta.title`, and the layout already handles phones. Replace **only** the JSON inside `<script id="otto-data" type="application/json">`. Don't change the HTML, CSS, script or the Otto mark.
2. Leave out anything you don't have. Every section hides itself when its key is missing or empty, so never fill gaps with zeros.
3. Where to show it:
   - **claude.ai / Claude desktop**: create an HTML artifact with the filled file.
   - **Claude Code / Cowork**: save it as `social-data/reports/<name>.html` and open it in the browser.
   - **ChatGPT**: a canvas with the filled HTML, or the HTML file to download.
   - **Chat mode** (the user asked for chat): don't use the dashboard; give the same content as short tables.

## The JSON

```json
{
  "meta": {
    "title": "Weekly social review",          // or "Daily pulse", "Content audit"
    "accounts": [                               // one per platform in scope; the url makes the name a link to the profile
      {"platform": "instagram", "handle": "@bloomandstem", "url": "https://www.instagram.com/bloomandstem/"},
      {"platform": "facebook", "handle": "@bloomandstem", "url": "https://www.facebook.com/bloomandstem"}],   // same handle everywhere: shown once
    "platforms": ["instagram", "facebook"],    // ONLY platforms in scope. One platform = no tabs.
    "start": "Mar 03", "end": "Mar 09, 2026",
    "baselineLabel": "your previous 4 weeks",
    "generated": "Mar 10, 2026", "timezone": "America/Chicago",
    "verdict": "One or two sentences: what happened and why it matters.",
    "footnote": "",
    "focusPost": "…"               // optional: open this post's diagnosis on load (reel-diagnosis uses this)
  },
  "kpis": [   // 4-6 per platform. platform: "instagram" | "facebook" | "linkedin" | "youtube" | "all"
    {"platform": "instagram", "label": "Views on this week's reels", "value": 21400, "baseline": 15800, "hero": true,
     "sub": "Median 1,180 reach per reel (usual 855)", "vsLabel": "last week"},   // vsLabel: what the baseline is ("vs last week"); default "usual"   // hero: the big number on the platform's card. Use a TOTAL for the period (vs the previous period); put the per-post median in sub
    {"platform": "instagram", "label": "Median reach", "value": 1180, "baseline": 855},
    {"platform": "instagram", "label": "Median skip rate", "value": 28, "baseline": 33, "unit": "%", "lowerIsBetter": true},
    {"platform": "instagram", "label": "Reels posted", "value": 6, "note": "5 old enough to judge"},
    {"platform": "instagram", "label": "Ad spend", "value": 300, "prefix": "$"}   // prefix for currency
  ],
  "daily": [ {"platform": "instagram", "date": "2026-03-03", "value": 2100} ],   // daily reach/views
  "dailyLabel": "Daily reach", "dailyNote": "",
  "dailyLabels": {"instagram": "Daily reach", "facebook": "Daily Page views", "youtube": "Daily channel views"},   // per platform; overrides dailyLabel
  "posts": [ {
    "platform": "instagram", "id": "…", "permalink": "https://…", "posted_at": "2026-03-06T11:00",   // in the USER's timezone (convert from UTC)
    "usual": 855,                  // this platform's usual reach/views: draws the reach bar and its "usual" tick
    "first_line": "first caption line or title", "age_days": 4,
    "reach": 4120, "views": 5600, "likes": 80, "comments": 6, "shares": 25, "saves": 76,
    "skip_rate": 22, "avg_watch_s": 14.2, "length_s": 21, "watch_pct": 68,
    "shares_per_1k": 6.1, "saves_per_1k": 18.4,
    "status": "winner",            // winner | keep | stalled | young
    "status_label": "Winner",      // "Early read" for young
    "diagnosis": {                 // from reel-diagnosis, computed during the run
      "steps": ["pass","pass","pass","skip","pass"],   // Hook, Pacing, Shares, Follows, Distribution: pass | fail | skip. After the first fail, the rest are skip. Distribution = was reach normal on the account's other posts that week
      "verdict": "Did its job",
      "evidence": ["Skip rate 22% vs your usual 33%"],
      "change": "The one thing to try next",
      "note": "optional"
    }
  } ],
  "groups": [ {"platform": "instagram", "name": "How-to reels", "n": 9, "median_reach": 1950, "multiple": 2.3, "median_skip": 25, "call": "winner"} ],   // call: winner | keep | below | retire | too few
  "search": { "rows": [ {"signal": "Sessions from Organic Social", "value": 63, "baseline": 40, "note": ""} ], "note": "" },
  "plan": { "title": "Next week", "keep": [], "change": [], "test": [], "stop": [], "next": [], "nextTitle": "Next five posts" },
  "decisions": [ {"observation": "", "confidence": "low|medium|high", "action": "", "confirm": ""} ],
  "notes": [ "One per line" ],
  "notesTitle": "Missing data and open questions"   // e.g. "Flags and today" in daily-pulse
}
```

`status_label` sets the wording on both the pills and the filter buttons (e.g. "Taking off" instead of "Winner").

Posts are always listed newest first. Instagram rows use `reach`; Facebook, YouTube and LinkedIn rows use `views`. With more than one platform in `meta.platforms` the page opens on an overview card per platform (its `hero` KPI, daily chart and 3 more KPIs), with a tab per platform.

**Write the verdict last.** It's the sentence people read first, so it comes from the numbers already on the page: every claim in it (best, worst, up, down, how much) must match a number shown in a KPI, chart or table. Re-read it against them before showing the dashboard.

Rules: the `//` comments above are explanations only; the JSON you put in the file must not contain them. Numbers are numbers (not strings). Percentages are plain numbers (28 means 28%). `avg_watch_s` in seconds (Instagram returns milliseconds: divide by 1,000). Columns that are empty or zero for every post hide themselves. Keep the file under ~1 MB (no embedded media).

## Report blocks

Skills that aren't a post-by-post review (best time, search, hooks, trends, comments, research, campaign results, tests) use `blocks`: an ordered list of sections. Use `posts` too when the report is about specific posts. Blocks with `"top": true` appear above the posts; the rest below. Half-width blocks sit two per row; `"wide": true` (and every heatmap, cards and stats block) takes the full row. Add `"platform"` to a block to show it only on that platform's tab.

```json
"blocks": [
  {"type": "stats", "title": "Campaign at a glance", "items": [
     {"label": "Site visits", "value": 640, "baseline": 410}, {"label": "Bookings", "value": 23, "note": "from GA4 key events"}]},

  {"type": "table", "title": "What people search to find you", "hint": "Search Console, last 28 days", "wide": true,
   "columns": [
     {"key": "q", "label": "Query"}, {"key": "impr", "label": "Impressions", "num": true},
     {"key": "pos", "label": "Position", "num": true, "fmt": "pos"},
     {"key": "covered", "label": "Posted about?", "pill": true}],
   "rows": [{"q": "wedding flowers austin", "impr": 880, "pos": 9.4, "covered": "missing"}],
   "note": "optional line under the table"},

  {"type": "bars", "title": "Patterns by median reach", "items": [
     {"label": "POV", "note": "16 hooks · skip 30%", "value": 1698},
     {"label": "Confession", "note": "2 hooks", "value": 1115, "dim": true}],
   "note": "Faded bars: fewer than 5, too few to tell."},

  {"type": "heatmap", "title": "Median reach by day and time", "rows": ["Mon","Tue"], "cols": ["Morning","Midday"],
   "values": [[175, 268], [1095, null]], "valueLabel": "reach", "showValues": true},

  {"type": "cards", "title": "Trends to act on", "items": [
     {"title": "Holiday hours checks", "tag": "Take", "meta": "Search +140% · 3 comment questions", "body": "Why it fits you.",
      "evidence": ["one fact per line"], "platform": "instagram"}]},

  {"type": "list", "title": "Words to put in captions", "items": ["wedding florist austin", "same-day flowers"]}
]
```

Column formats (`fmt`): `pct` (28 → 28%), `x` (1.4 → 1.4x), `s` (seconds), `pos` (one decimal). `"pill": true` shows the cell as a status pill. These words get colours automatically: take / proven / winner / confirmed / arrived (green), adapt / test / emerging / young (amber), skip / retire / failed / missing / stalled (red), keep / recurring (grey), too few / one-off (muted). Set `"<key>Status"` on a row (or `tagStatus` on a card) to pick the colour yourself: `winner`, `keep`, `stalled`, `young`, `few`. `"link": "url"` on a column makes the cell a link to `row.url`. In a heatmap, `null` means no data (outlined cell).

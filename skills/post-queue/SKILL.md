---
name: post-queue
description: Posts content you already made and approved at set times, for Otto connections that can publish but can't schedule. Builds a queue file, gets your approval on every item once, and sets up your assistant's scheduled tasks to publish each approved item through Otto when it's due. Use when someone says "post this at 9am tomorrow", "queue these reels", "schedule these posts" (and Otto scheduling isn't available), "post one a day for a week", or "set up a posting queue".
---

# Post queue

Some Otto connections can publish now but can't schedule for later. This skill fills that gap: approved posts wait in a queue file, and a scheduled task in your assistant publishes each one when it's due, through Otto's own publish tools. Posting happens while nobody is watching, so approval is explicit, per item, and nothing outside the approved queue ever goes out.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or the assistant's memory) for workspace, accounts and timezone. Ask only what's missing, in one bundled multiple-choice question, and save the answers.
- Only queue for platforms the user named, or the defaults in settings.
- **Capability check first.** If this session has `channel_submit_plan` (scheduling with `publishAt`), stop here: schedule through Otto instead (`content-calendar` step 5 shows how). This skill is only for connections with publish tools (`meta_ig_publish_reel`, `meta_page_publish_video`, ...) and no scheduling. With neither, give the user the files, captions and times to post by hand.
- Output is visual by default (artifact / HTML file / canvas) unless settings or the user say chat.

Skill questions: posting times (e.g. 9:00, 12:00, 16:00), the daily cap (default 3 posts a day per account), and where the user's assistant runs (see step 3).

## 1. Build the queue

Write `social-data/queue/queue.json` (or `queue.md` if the user prefers to read it). One entry per post:

```json
{
  "id": "q-2026-11-20-01",
  "platform": "instagram_reel",
  "account": "<from settings>",
  "files": { "video": "social-data/queue/media/reel-01.mp4", "cover": "social-data/queue/media/reel-01-cover.jpg" },
  "mediaId": null, "coverMediaId": null,
  "caption": "<exact approved caption>",
  "publishAt": "2026-11-20T09:00:00", "timeZone": "America/Chicago",
  "status": "pending", "approvedAt": null,
  "result": null, "error": null
}
```

- Status flows `pending` → `approved` → `posted` or `failed`. Only `approved` items are ever published.
- Captions are final text, not notes. Check length (Instagram caption max 2,200 characters).
- Files are the user's own (from `cover-designer`, their editor, their camera). Check each path exists before showing the queue.
- Platform tools: Instagram reel `meta_ig_publish_reel` (mediaId, caption, optional coverMediaId; the cover can only be set at publish). Facebook reel `meta_page_publish_video`. Instagram image and carousel tools take public image URLs, not library ids; if the library can't give a public URL, those items stay manual (unverified, test first).

## 2. One approval, item by item

Show the whole queue as it will post: for each item the platform and account, the time with timezone, the full caption, and the video/cover/images (preview in the visual). Then ask once, with options: "Approve all", "Approve some (list ids)", "Change something". Mark only the approved ids `approved` with `approvedAt`. Any later edit to an item sets it back to `pending` and needs a new yes.

## 3. Set up the scheduled tasks

Create one recurring task per posting time (e.g. daily at 9:00, 12:00, 16:00), or one task per item for a short queue. Where tasks can run:

| Environment | Works? |
|---|---|
| Claude desktop / Cowork scheduled tasks | Best fit: reads local files. The app and computer must be on at post time |
| Claude Code scheduled cloud agents | Only if the files are reachable from the cloud (local files aren't). Prefer desktop |
| ChatGPT tasks | No local files: only for items whose media is already in the Otto library (mediaId filled) |

Say "unverified, test on a test account first" for any environment you haven't seen a successful run in. Before relying on it, run one task by hand against a test item.

**The task prompt** (paste as is, with the queue path filled in):

> Read `<path>/social-data/queue/queue.json`. Take the single earliest item with status `approved` whose `publishAt` is now or up to 30 minutes past, in its timeZone. If none, stop. Check today's posted count for that account is under the cap of <n>; if not, stop. If the item has no `mediaId`, upload its file to the Otto library: `media_create_upload` (filename, mimeType, byteSize, purposes ["publish"]), PUT the bytes to the returned URL, then `media_complete`; do the same for the cover. Save the ids in the item. Publish with the item's platform tool (for an Instagram reel: `meta_ig_publish_reel` with mediaId, the caption exactly as stored, coverMediaId if present, confirm true). On success set status `posted` and store the permalink in `result`. Append one line to `social-data/queue/log.md`: time, id, platform, result or error. If the file is missing, the caption or files differ from the approved item, or any call fails: do not retry, set status `failed` with the error, log it, and stop. Never publish an item that isn't `approved`.

## 4. After it runs

Each day (or on request), read `log.md` and the queue, and report: posted with links, failed with the reason, still waiting. A failed item goes back to the user; fixing it means a new approval. Hand posted items to `comment-to-lead` and, from day 3, `reel-diagnosis`.

## Output

The queue as a visual: one card per item (preview, platform, time, caption, status), plus the list of scheduled tasks created and the test result. In chat mode, a table: id | platform | time | caption (first 60 characters) | status.

## Never

- Publish an item that wasn't approved in this conversation, or one changed since approval.
- Retry a failed post in a loop, or post over the daily cap.
- Use browser automation or any route other than Otto's publish tools.
- Say something is posted without a permalink from the tool result.
- Use this when the connection already has `channel_submit_plan`.

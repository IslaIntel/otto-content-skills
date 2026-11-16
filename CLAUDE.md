# otto-content-skills

Public repo of free Claude skills that use the Otto MCP (ottowebmaster.com) for social media analytics, research, content creation and distribution. Every file here is read by strangers, so:

- **No private data.** No account ids (Instagram, Page, channel, property ids), handles, staff names, internal file paths or reports, and no connector-specific tool prefixes (`mcp__...`). Refer to Otto tools by bare name (`meta_ig_list_media`). Examples use invented businesses.
- **Generic.** Skills work for any small business connected to Otto, not just ours.
- **Safe by default.** Analytics and research skills are read-only. Anything that posts, replies, hides, deletes, generates paid media or schedules shows the exact content first and waits for the user's yes in the conversation.
- **Original work only.** Don't copy wording from other skill packs; don't bundle third-party skills without keeping their license and attribution.
- **Follow `docs/AUTHORING.md`** for section order, the verified Otto MCP tool facts, the rules learned from live test runs, the shared `brand/` and `social-data/` folders, and style. Update its tool facts when the MCP changes.
- **Test against a live Otto workspace before shipping a skill**, read-only: run it the way a new user would and fix what breaks.
- Layout: `skills/<name>/SKILL.md` (+ optional supporting files). Add each new skill to the README table. Bump `version` in `.claude-plugin/plugin.json` when skills change.

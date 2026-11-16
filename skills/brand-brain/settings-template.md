# brand/settings.md template

Copy this into `brand/settings.md` (or, with no folder, into the assistant's memory or a Claude Project's instructions). Fill only what the user told you; leave a line blank rather than guessing. Every skill reads it first and asks only for what's missing.

```markdown
# Settings
Last updated: YYYY-MM-DD

## Business
Workspace: <Otto workspace name> (id: <workspace id>)
Business: <one line: what it is and where>

## Accounts (one per platform; leave blank if not used)
Instagram: <account name as shown in Otto>
Facebook Page: <page name>
LinkedIn: <personal profile / Company Page name / both>
YouTube: <channel name>
Google Business Profile: <location name>
Website (Search Console / GA4): <domain>

## Defaults
Default platforms: <e.g. Instagram, Facebook / All connected>
Timezone: <IANA name, e.g. Europe/London>
Output: <visual | chat>          # visual = artifact / HTML file / canvas
Caption template: <none, or the template below>
CTA: <on | off | ask>             # ask = ask each time
Comment sources: <e.g. Instagram, Facebook, LinkedIn Company Page>

## Brand look (used by cover-designer, carousel-designer, story-sequence)
Colours: <2-4 hex codes: main, accent, text, background>
Fonts: <heading font, body font (Google Fonts names if possible)>
Logo: <file name or link, if the user shared one>
Reference posts: <1-3 links or file names of covers/carousels they like>

## Caption template (optional, followed exactly by caption-writer)
<first line pattern>
<body pattern>
<sign-off / CTA pattern>
<hashtag rule>

## Notes
- YYYY-MM-DD: <a change the user asked for, e.g. "from now on, no CTA">
```

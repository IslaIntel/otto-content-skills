"""Example data for the report skills' shipped dashboard.html (invented business: Bloom & Stem, a florist).
Used by build.py. Real runs replace the whole JSON block with live Otto data."""

M = dict(accounts=[dict(platform="instagram", handle="@bloomandstem")], generated="Mar 10, 2026", timezone="America/Chicago", footnote="Example data")

SAMPLES = {
 "best-time-to-post": dict(
  meta=dict(M, title="Best time to post", platforms=["instagram"], start="Feb 08", end="Mar 09, 2026", baselineLabel="your median reach",
            verdict="Your evening posts do best (median reach 1,410) and your midday posts do worst (520). Most cells hold only 1-3 posts, so hold the new schedule for 4 weeks."),
  kpis=[dict(platform="instagram", label="Posts analysed", value=38), dict(platform="instagram", label="Timezone", value="Chicago"),
        dict(platform="instagram", label="Best slot", value="Evening", note="18:00-22:00 · median 1,410"), dict(platform="instagram", label="Weakest slot", value="Midday", note="12:00-15:00 · median 520")],
  blocks=[dict(type="heatmap", title="Median reach by day and time", rows=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], cols=["Morning 9-12","Midday 12-15","Afternoon 15-18","Evening 18-22"],
               values=[[640,410,None,1220],[880,520,900,1350],[None,480,760,1410],[720,None,1010,1690],[950,610,1120,1580],[1300,None,None,1100],[None,None,820,940]], valueLabel="reach", showValues=True),
          dict(type="bars", title="By time slot", items=[dict(label="Evening (18:00-22:00)", note="12 posts", value=1410), dict(label="Afternoon (15:00-18:00)", note="8 posts", value=940),
               dict(label="Morning (9:00-12:00)", note="10 posts", value=880), dict(label="Midday (12:00-15:00)", note="8 posts", value=520)]),
          dict(type="list", title="Schedule to hold for 4 weeks", items=["Main slots: evening and afternoon.", "Move the midday post to the morning.", "One test slot a week: Saturday morning."])]),

 "search-and-social": dict(
  meta=dict(M, title="Search and social", platforms=["instagram"], start="Feb 08", end="Mar 07, 2026", baselineLabel="the 28 days before",
            verdict="'wedding flowers austin' showed you in Google 880 times in 28 days, and you've never posted about weddings. Same-day delivery impressions are up 40%."),
  kpis=[dict(platform="instagram", label="Google clicks", value=412, baseline=350), dict(platform="instagram", label="Brand searches", value=1240, baseline=1100),
        dict(platform="instagram", label="Sessions from social", value=310, baseline=240)],
  blocks=[dict(type="table", title="What people search to find you", hint="Search Console, last 28 days", wide=True, top=True,
               columns=[dict(key="q", label="Query"), dict(key="impr", label="Impressions", num=True), dict(key="clicks", label="Clicks", num=True), dict(key="pos", label="Position", num=True, fmt="pos"), dict(key="covered", label="Posted about?", pill=True)],
               rows=[dict(q="wedding flowers austin", impr=880, clicks=21, pos=9.4, covered="missing"), dict(q="same day flower delivery austin", impr=640, clicks=48, pos=4.1, covered="covered", coveredStatus="keep"),
                     dict(q="sympathy flowers", impr=410, clicks=9, pos=12.2, covered="missing"), dict(q="bloom and stem", impr=1240, clicks=260, pos=1.1, covered="covered", coveredStatus="keep")]),
          dict(type="cards", title="Posts to make from these searches", items=[
               dict(title="What a $400 wedding bouquet actually includes", tag="Take", meta="'wedding flowers austin' · 880 impressions, position 9.4", body="Put 'Austin wedding flowers' in the first caption line and the cover title."),
               dict(title="How late you can order same-day", tag="Take", meta="'same day flower delivery' · +40%", body="Answer the cut-off time in the first 2 seconds."),
               dict(title="Choosing sympathy flowers", tag="Adapt", meta="'sympathy flowers' · 410 impressions", body="Gentle tone, no hard sell; link to the order page in the bio.")]),
          dict(type="bars", title="Where site visits came from", items=[dict(label="Organic Search", value=1820), dict(label="Direct", value=990), dict(label="Organic Social", value=310, platform="instagram"), dict(label="Referral", value=120)]),
          dict(type="list", title="Words to put in captions", items=["Austin wedding flowers", "same-day flower delivery", "sympathy flowers Austin"])]),

 "hook-patterns": dict(
  meta=dict(M, title="Hook patterns", platforms=["instagram"], start="Feb 08", end="Mar 07, 2026", baselineLabel="your medians",
            verdict="Number-first hooks are your strongest pattern (median reach 1,920 across 7 hooks). Questions are the weakest (610, skip 41%)."),
  kpis=[dict(platform="instagram", label="Hooks analysed", value=34), dict(platform="instagram", label="Median skip rate", value=33, unit="%"), dict(platform="instagram", label="Proven", value=8)],
  blocks=[dict(type="bars", title="Patterns by median reach", top=True, items=[dict(label="number-result", note="7 hooks · skip 27%", value=1920), dict(label="this-vs-that", note="9 hooks · skip 30%", value=1380),
               dict(label="mistake-warning", note="3 hooks", value=1250, dim=True), dict(label="direct-question", note="8 hooks · skip 41%", value=610)], note="Faded bars: fewer than 5 hooks, too few to tell."),
          dict(type="table", title="Your proven hooks", columns=[dict(key="h", label="Hook"), dict(key="p", label="Pattern"), dict(key="reach", label="Reach", num=True), dict(key="skip", label="Skip", num=True, fmt="pct")],
               rows=[dict(h="3 flowers that last two weeks in a vase", p="number-result", reach=4120, skip=22), dict(h="Before: grocery roses. After: 10 minutes with us.", p="this-vs-that", reach=2010, skip=26)]),
          dict(type="cards", title="Remixes: same skeleton, new words", items=[
               dict(title="4 flowers that survive a heatwave", tag="Proven", tagStatus="winner", meta="From: '3 flowers that last two weeks in a vase'", body="Keeps: a number, a benefit, a hidden loser."),
               dict(title="2 vase tricks florists don't tell you", tag="Test", meta="Same skeleton", body="Confirm both tricks are real before posting.")])]),

 "trend-radar": dict(
  meta=dict(M, title="Trend radar", platforms=["instagram"], start="Feb 08", end="Mar 07, 2026", baselineLabel="the 28 days before",
            verdict="Two trends are worth acting on this month: dried-flower arrangements (search, comments and peers agree) and 'flowers for no reason' gifting (your own breakout, plus comments asking for it)."),
  blocks=[dict(type="stats", title="This run", top=True, items=[dict(label="Signals checked", value=5), dict(label="Trends to take", value=2), dict(label="To skip", value=1)]),
          dict(type="cards", title="Trends", top=True, items=[
               dict(title="Dried-flower arrangements", tag="Take", meta="Search +140% · 4 comment questions · 2 peers posted it", body="Fits: you already sell dried bundles. A how-long-do-they-last reel answers the top question.", evidence=["'dried flowers austin' 90 → 216 impressions", "4 comments asking 'do you do dried?'"]),
               dict(title="Flowers for no reason", tag="Take", meta="Your own breakout · 2.4x median reach · 3 comments asking for 'just because' bouquets", body="Make it a weekly series with a different 'reason' each week."),
               dict(title="Dancing florist trend audio", tag="Skip", meta="1 peer post · no search or comment signal", body="Doesn't match your voice or what people ask you.")]),
          dict(type="table", title="Rising searches", columns=[dict(key="q", label="Query"), dict(key="a", label="Previous", num=True), dict(key="b", label="This window", num=True), dict(key="c", label="Change", num=True, fmt="pct")],
               rows=[dict(q="dried flowers austin", a=90, b=216, c=140), dict(q="flower subscription", a=120, b=180, c=50)]),
          dict(type="list", title="Watch next month", items=["Mother's Day: your Search Console impressions for it rose from mid-April last year.", "'Flower subscription' if it keeps climbing."])]),

 "comment-insights": dict(
  meta=dict(M, title="Comment insights", platforms=["instagram", "facebook"], accounts=[dict(platform="instagram", handle="@bloomandstem"), dict(platform="facebook", handle="@bloomandstem")], start="Feb 08", end="Mar 07, 2026", baselineLabel="last month",
            verdict="Price and delivery cut-off time are the questions people keep asking. Neither is answered in a post or your bio."),
  kpis=[dict(platform="instagram", label="Comments read", value=214), dict(platform="instagram", label="Meaningful", value=96), dict(platform="facebook", label="Comments read", value=38)],
  blocks=[dict(type="bars", title="What people ask about", top=True, items=[dict(label="Price", note="recurring · 22 comments", value=22), dict(label="Delivery cut-off", note="recurring · 17", value=17),
               dict(label="Dried flowers", note="emerging · 6", value=6), dict(label="Allergies", note="one-off · 2", value=2, dim=True)]),
          dict(type="cards", title="Top clusters", items=[
               dict(title="How much is a bouquet?", tag="Confirmed", meta="22 comments · also searched on Google", evidence=["'how much for one like this??'", "'price pls'", "'is this $$$'"]),
               dict(title="Can I still order for today?", tag="Recurring", meta="17 comments", evidence=["'too late for today?'", "'what time do you stop delivering'"])]),
          dict(type="list", title="Post ideas from these", items=["Our bouquets at three prices, side by side.", "The same-day cut-off, answered in 3 seconds."])]),

 "topic-finder": dict(
  meta=dict(M, title="Topic finder", platforms=["instagram"], start="Dec 08", end="Mar 07, 2026", baselineLabel="your past 90 days",
            verdict="Wedding flowers score highest: searched often, never covered by you, and your best-selling service."),
  blocks=[dict(type="stats", title="This run", top=True, items=[dict(label="Topics scored", value=14), dict(label="Sources used", value=5, note="Reddit unavailable")]),
          dict(type="table", title="Ranked topics", wide=True, top=True, columns=[dict(key="t", label="Topic"), dict(key="s", label="Score", num=True), dict(key="sig", label="Signals"), dict(key="v", label="Call", pill=True)],
               rows=[dict(t="Wedding flowers", s=5, sig="searched, search gap, complained, watched (others), sellable", v="Take"), dict(t="Same-day delivery", s=3, sig="searched, complained, sellable", v="Take"),
                     dict(t="Flower care tips", s=3, sig="breakout, watched (others), complained", v="Adapt"), dict(t="Shop playlist", s=1, sig="watched (others)", v="Skip")]),
          dict(type="list", title="Sources not available this run", items=["Reddit search returned an error; ran without it."])]),

 "campaign-retro": dict(
  meta=dict(M, title="Campaign retro: Valentine's Day", platforms=["instagram"], start="Feb 01", end="Feb 21, 2026", baselineLabel="the 21 days before",
            verdict="The campaign doubled site visits and brought 41 orders through the tracked links. Reach fell back to normal within 5 days."),
  kpis=[dict(platform="instagram", label="Reach", value=48200, baseline=21900), dict(platform="instagram", label="Site visits from social", value=1320, baseline=610),
        dict(platform="instagram", label="Orders (GA4 key events)", value=41, baseline=12), dict(platform="instagram", label="Ad spend", value=300, prefix="$", note="3 orders from the ad")],
  daily=[dict(platform="instagram", date=f"2026-02-{d:02d}", value=v) for d, v in zip(range(1, 22), [900,1100,1300,2400,2100,2600,3100,2900,3300,3800,4200,5100,6300,4800,1900,1500,1300,1200,1100,1000,950])],
  dailyLabel="Daily reach",
  blocks=[dict(type="table", title="Where the visits came from", columns=[dict(key="s", label="Source / medium (campaign valentines)"), dict(key="v", label="Sessions", num=True), dict(key="k", label="Orders", num=True)],
               rows=[dict(s="instagram / social", v=860, k=29), dict(s="instagram / bio", v=310, k=9), dict(s="facebook / paid-social", v=150, k=3)]),
          dict(type="list", title="Tracking fixes", items=["2 Story link stickers used the link without tags: 120 visits landed as Direct."])],
  plan=dict(title="Next campaign", keep=["Countdown reels in the last 5 days."], change=["Start ads a week earlier."], stop=["Untagged links in Stories and the bio."])),

 "hook-test": dict(
  meta=dict(M, title="Hook test: number vs question", platforms=["instagram"], start="Mar 02", end="Mar 09, 2026", baselineLabel="the pre-registered rule",
            verdict="Version A (number first) won on the deciding metric: skip rate 24% vs 37%, with both reels past the minimum reach."),
  kpis=[dict(platform="instagram", label="A skip rate", value=24, unit="%"), dict(platform="instagram", label="B skip rate", value=37, unit="%"),
        dict(platform="instagram", label="Minimum reach", value=800, note="both passed"), dict(platform="instagram", label="Read at", value=72, unit=" h")],
  blocks=[dict(type="table", title="Both versions", columns=[dict(key="m", label="Metric"), dict(key="a", label="A: number", num=True), dict(key="b", label="B: question", num=True)],
               rows=[dict(m="Reach", a=1840, b=1210), dict(m="Skip rate %", a=24, b=37), dict(m="Avg watch (s)", a=13.1, b=9.4)]),
          dict(type="cards", title="Result", items=[dict(title="Number-first wins", tag="Winner", tagStatus="winner", body="Use number-first openers for the next 2 weeks, then retest against a before/after hook.")])]),
}


# ---- reel-breakdown example (invented florist; frames are simple illustrations, not real footage)
def _frame(bg1, bg2, shape="vase", label=""):
    import base64
    shapes = {
        "vase": '<rect x="70" y="170" width="60" height="90" rx="14" fill="#f4efe8"/><circle cx="85" cy="150" r="22" fill="#e86a8e"/><circle cx="115" cy="140" r="20" fill="#f2a541"/><circle cx="100" cy="120" r="18" fill="#c94f7c"/>',
        "hands": '<ellipse cx="100" cy="200" rx="70" ry="34" fill="#e9b48f"/><circle cx="80" cy="150" r="20" fill="#e86a8e"/><circle cx="118" cy="146" r="18" fill="#9bd27a"/>',
        "face": '<circle cx="100" cy="150" r="52" fill="#e9b48f"/><circle cx="82" cy="140" r="6" fill="#222"/><circle cx="118" cy="140" r="6" fill="#222"/><path d="M80 172 q20 14 40 0" stroke="#222" stroke-width="5" fill="none" stroke-linecap="round"/>',
        "card": '<rect x="35" y="120" width="130" height="90" rx="12" fill="#fff"/><rect x="50" y="138" width="80" height="10" rx="5" fill="#1877f2"/><rect x="50" y="158" width="100" height="8" rx="4" fill="#ccc"/><rect x="50" y="174" width="70" height="8" rx="4" fill="#ccc"/>',
    }
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 356"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient></defs>'
           f'<rect width="200" height="356" fill="url(#g)"/>{shapes[shape]}</svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

_shots = [(0, 1.8, "#6b8f71", "#2f4a35", "face", "3 flowers that last two weeks"), (1.8, 4.6, "#f3d9c4", "#c98a6a", "vase", "Number 1: lisianthus"),
          (4.6, 7.9, "#e8e1f5", "#9a86c9", "vase", "Number 2: chrysanthemums"), (7.9, 11.5, "#fbe3e8", "#d98aa0", "vase", "Number 3: alstroemeria"),
          (11.5, 14.2, "#3b3b3b", "#1d1d1d", "hands", "And the one that dies in 2 days"), (14.2, 16.8, "#f6efe2", "#d6b98d", "card", "Order by 2 p.m. for same day"),
          (16.8, 19.0, "#6b8f71", "#2f4a35", "face", "Save this for your next bouquet")]
REEL_SAMPLE = dict(
    meta=dict(title="3 flowers that last two weeks in a vase", series="Flower care, part 4", length_s=19.0, posted="Mar 06, 2026",
              accounts=[dict(platform="instagram", handle="@bloomandstem")], baselineLabel="your usual (last 28 days)",
              generated="Mar 10, 2026", footnote="Example data",
              verdict="Your best reel this month: 4.8x your usual reach. The average viewer stays until 14.1 s, just past the reveal of the flower that dies."),
    kpis=[dict(label="Reach", value=4120, baseline=855), dict(label="Skip rate", value=22, baseline=33, unit="%", lowerIsBetter=True),
          dict(label="Avg watch", value=14.1, unit=" s", note="74% of 19 s"), dict(label="Saves", value=76, baseline=9)],
    timeline=dict(length_s=19.0, shots=[dict(start=a, end=b, frame=_frame(c1, c2, sh), text=tx) for a, b, c1, c2, sh, tx in _shots],
                  sections=[dict(label="Hook", start=0, end=1.8), dict(label="List", start=1.8, end=11.5), dict(label="Twist", start=11.5, end=14.2),
                            dict(label="Offer", start=14.2, end=16.8), dict(label="Ask", start=16.8, end=19.0)],
                  markers=[dict(t=14.1, label="Avg viewer leaves · 14.1 s", kind="leave"), dict(t=11.5, label="Twist · 11.5 s", kind="payoff")],
                  note="The average viewer stays until 14.1 s, past the twist; the offer and the ask come after that point."),
    hook=dict(frames=[dict(t=t, frame=_frame("#6b8f71", "#2f4a35", "face"), note=n) for t, n in
                      [(0, "Face to camera, the promise on screen"), (0.5, "Leans in"), (1, "Hand holds up the first stem"), (2, "Cut to the vase"), (3, "'Number 1' title")]],
              checks=[dict(status="pass", label="Readable with the sound off", note="Promise written on screen from frame 0"),
                      dict(status="pass", label="Something moves in the first second"), dict(status="pass", label="A number in the promise", note="'3 flowers', 'two weeks'")]),
    structure=[dict(beat="Hook", start=0, end=1.8, what="The promise: 3 flowers that last two weeks"), dict(beat="List", start=1.8, end=11.5, what="One flower per shot, with how long it lasts"),
               dict(beat="Twist", start=11.5, end=14.2, what="The one that dies in two days"), dict(beat="Offer", start=14.2, end=16.8, what="Same-day order cut-off"),
               dict(beat="Ask", start=16.8, end=19.0, what="Save this for your next bouquet")],
    cta=dict(present=True, text="'Save this for your next bouquet' at 16.8 s.", note="It lands after the average leave point; try it on screen during the list."),
    finding="The twist (the flower that dies) holds people; the offer and the save ask come after the average viewer has left.",
    change="Move 'save this' onto the screen during the list (around 8 s) and keep the rest the same.",
    borrow=["A number in the promise", "One item per shot", "A twist before the ask"], leave=["Putting the ask after the average leave point"],
    notes=["Example data for an invented business."])

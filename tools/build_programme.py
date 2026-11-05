#!/usr/bin/env python3
"""Clean the raw programme scrape (public pages) into programme.json.
Usage: build_programme.py raw.json programme.json"""
import json, re, sys
raw = json.load(open(sys.argv[1], encoding="utf-8"))
ROOM_AREA = {"Portal Stage": "portal", "Relic Stage": "relic", "Cage Stage": "cage", "Intraprenör": "intra"}
HINTS = [("Keller", "keller", "Alte Münze Keller"), ("Galerie", "galerie", "Alte Münze Galerie")]
def mins(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)
out, n = [], 0
for x in raw:
    ts = x["times"]
    i = next((k for k in range(len(ts) - 3) if ts[k] in ("Thu", "Fri") and re.fullmatch(r"\d+:\d\d", ts[k + 1]) and ts[k + 2] == "-"), None)
    if i is None:
        print("no time:", x["title"]); continue
    s, e = mins(ts[i + 1]), mins(ts[i + 3])
    if e <= s:
        e = 1439
    n += 1
    room = (x.get("room") or [""])[0]
    area = ROOM_AREA.get(room, "")
    if not room:
        for key, a, label in HINTS:
            if key in x["title"]:
                area, room = a, label
    # who/comp come twice (card + popup): keep the first half, keep order
    who = list(dict.fromkeys(x.get("who") or []))
    comp = list(dict.fromkeys(x.get("comp") or []))
    out.append(dict(id="p%02d" % n, day=x["day"], s=s, e=e, title=x["title"], who=", ".join(who),
                    comp=", ".join(c for c in comp if c), room=room, area=area,
                    cat=x.get("cat") or "", track=(x.get("track") or [""])[0],
                    desc=x.get("desc") or ""))
out.sort(key=lambda o: (o["day"] != "thu", o["s"], o["room"]))
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "items; empty room:", [o["title"][:40] for o in out if not o["room"]])

#!/usr/bin/env python3
"""src/app.html + programme.json -> index.html (the clean app, no personal data)
   and dist/artifact.html (same code, without the document wrapper).
   Optional: build.py --pack pack.json --shim shim.js out.html  makes a local test page."""
import json, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = open(root + "/src/app.html", encoding="utf-8").read()
prog = json.dumps(json.load(open(root + "/programme.json", encoding="utf-8")), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
app = app.replace("/*PROGRAMME*/", prog)
HEAD = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'
PWA = ('<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#111017">'
       '<meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">'
       '<meta name="apple-mobile-web-app-status-bar-style" content="black"><meta name="apple-mobile-web-app-title" content="Games Ground">'
       '<link rel="apple-touch-icon" href="icons/icon-180.png"><link rel="icon" href="icons/icon-192.png">')
SW = ('<script>if("serviceWorker"in navigator&&(location.protocol==="https:"||location.hostname==="localhost"))'
      'addEventListener("load",function(){navigator.serviceWorker.register("sw.js");'
      'if(navigator.storage&&navigator.storage.persist)navigator.storage.persist()})</script>')
def page(pre="", pwa=False):
    head = HEAD.replace("</head>", PWA + "</head>") if pwa else HEAD
    return head + pre + app + (SW if pwa else "") + "</body></html>"
if "--pack" in sys.argv:
    a = sys.argv
    pack = open(a[a.index("--pack") + 1], encoding="utf-8").read().replace("</", "<\\/")
    pre = "<script>window.GG_PACK=" + pack + "</script>"
    if "--shim" in a:
        pre += "<script>" + open(a[a.index("--shim") + 1], encoding="utf-8").read() + "</script>"
    open(a[-1], "w", encoding="utf-8").write(page(pre))
    print("test page", a[-1], len(page(pre)))
else:
    open(root + "/index.html", "w", encoding="utf-8").write(page(pwa=True))
    os.makedirs(root + "/dist", exist_ok=True)
    open(root + "/dist/artifact.html", "w", encoding="utf-8").write(app)
    print("index.html", len(page()))

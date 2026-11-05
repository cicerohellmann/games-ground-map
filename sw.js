/* Keeps the app working with no signal. Your notes and pasted questions live in this
   phone's browser storage, not here. New code arrives the next time you open it online. */
const CACHE = "gg-v1";
const CORE = ["./", "manifest.webmanifest", "icons/icon-180.png", "icons/icon-192.png", "icons/icon-512.png"];
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())
));
const keep = (req, res) => { if (res && (res.ok || res.type === "opaque")) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); } return res; };
self.addEventListener("fetch", e => {
  const r = e.request;
  if (r.method !== "GET") return;
  if (r.mode === "navigate") {
    const net = fetch(r).then(res => keep(new Request("./"), res));
    const late = new Promise(ok => setTimeout(ok, 2500)).then(() => caches.match("./"));
    e.respondWith(Promise.race([net.catch(() => caches.match("./")), late.then(c => c || net)]));
    return;
  }
  e.respondWith(caches.match(r).then(c => c || fetch(r).then(res => keep(r, res))));
});

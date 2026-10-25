/* Rent to Home service worker. Scope is /mortgagetool/ only, so it
   cannot interfere with the rest of fwiwletter.com. Everything is
   network-first with a cache fallback: when you are online the
   installed app always loads the latest published page and rates,
   and when you are offline it falls back to the cached copy. This
   matters because a cache-first shell would otherwise keep serving
   an old page after a site update. */
const CACHE = "rent-to-home-v2";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "rates.json"];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (url.pathname.indexOf("/mortgagetool/") === -1) return;
  if (e.request.method !== "GET") return;
  e.respondWith(fetch(e.request).then((res) => {
    const copy = res.clone();
    caches.open(CACHE).then((c) => c.put(e.request, copy));
    return res;
  }).catch(() => caches.match(e.request)));
});

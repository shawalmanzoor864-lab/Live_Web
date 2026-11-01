// Saves the try-on engine on the visitor's device so every later visit opens instantly.
const C='aurelle-v1';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(clients.claim()));
self.addEventListener('fetch',e=>{
 const u=new URL(e.request.url);if(e.request.method!=='GET')return;
 const ok=(u.origin===location.origin&&/\/(vendor|models)\//.test(u.pathname))||u.hostname==='cdn.jsdelivr.net'||u.hostname==='storage.googleapis.com';
 if(!ok)return;
 e.respondWith(caches.open(C).then(async c=>{const m=await c.match(e.request);if(m)return m;
  const r=await fetch(e.request);if(r.ok)c.put(e.request,r.clone());return r}))});

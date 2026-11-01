"""Run ONCE on your PC (needs internet) before deploying to Vercel:   python download_vendor.py
Downloads the face-tracking engine + 3D library into ./vendor so your site no longer depends on
other websites (CDNs). Then deploy the whole folder (index.html, sw.js, vercel.json, vendor, models, ...)."""
import json, os, urllib.request
VER = "0.10.14"; J = "https://cdn.jsdelivr.net/npm/"; PKG = f"@mediapipe/tasks-vision@{VER}"
files = []
def get(url, p):
    dest = os.path.join("vendor", p); os.makedirs(os.path.dirname(dest), exist_ok=True)
    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=180).read()
    open(dest, "wb").write(data); files.append({"p": p.replace("\\", "/"), "s": len(data)}); print("ok", p, len(data))
try:
    lst = json.load(urllib.request.urlopen(f"https://data.jsdelivr.com/v1/package/npm/{PKG}/flat"))["files"]
    names = [f["name"] for f in lst if f["name"].startswith("/wasm/") or f["name"] == "/vision_bundle.mjs"]
except Exception:
    names = ["/vision_bundle.mjs"] + [f"/wasm/vision_wasm{n}internal.{e}" for n in ("_", "_nosimd_") for e in ("js", "wasm")]
for n in names: get(J + PKG + n, "mp" + n)
get("https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task", "face_landmarker.task")
get(J + "three@0.147.0/build/three.min.js", "three.min.js")
get(J + "three@0.147.0/examples/js/loaders/GLTFLoader.js", "GLTFLoader.js")
json.dump({"files": files}, open("vendor/manifest.json", "w"))
get("https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task", "hand_landmarker.task")  # only downloaded by visitors who try a watch
print("Done. Now deploy the whole folder.")
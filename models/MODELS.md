# Portable panel part meshes

Four GLB meshes for the three.js viewer (`models/<slot>.glb`, rescaled by
bounding box; +Y is up in every file). Meshes are geometry-only (no
materials/textures — Modly ran with `enable_texture:false` per the
gpu-cluster skill, since the 1060's texture pipeline is not built).

All four were generated end-to-end on the home GPU box (GTX 1060 6GB) via
ComfyUI (SD1.5, txt2img source images) -> Modly (Hunyuan3D 2 Mini,
image->mesh) -> gltf-transform (simplify + center) on this Mac. No vendor
product photos were used — see caveat below.

## Caveat: source images are AI-generated stand-ins, not vendor photos

Step B first tried fetching real vendor product photos (WIKA, Swagelok,
FAV). WebFetch could not extract a direct hotlinkable image URL from any of
the vendor pages (WIKA returned HTTP 403 to WebFetch; Swagelok's and FAV's
product galleries are JS-rendered with no plain `<img src>`/`og:image` in
the fetched markup). Per the task's fallback instruction, all four source
images were instead generated locally with ComfyUI (SD1.5,
`v1-5-pruned-emaonly-fp16.safetensors`, 768x768, 25 steps, euler/normal).

SD1.5 repeatedly rendered these mechanical/symmetric objects as **pairs or
clusters** rather than single items (a known weak point for this
checkpoint). Where that happened, the single cleanest object was cropped
out of the composition and padded to a square with a flat background before
being sent to Modly. This means the valve, coupling, and digital-gauge
meshes are **stylized generic stand-ins** for their reference products, not
accurate replicas — see per-row caveats below. The gauge mesh is closest to
the reference product (round dial, chrome bezel) but its dial markings are
hallucinated, illegible glyphs, not real WIKA 232.50 graphics.

## Modly setup notes (relevant to reproducing this)

Modly was unreachable on the LAN at the start of this run (TCP connect to
`192.168.1.16:8765` succeeded but the server sent an empty reply). Root
cause found via SSH: the `ModlyServe` scheduled task's FastAPI backend
failed to bind `127.0.0.1:8765` (`OSError: [Errno 13] ... forbidden by its
access permissions`) — a known Windows quirk where a `netsh portproxy`
rule with the **same** listen and connect port on `127.0.0.1` reserves
that port for the kernel-level redirector, so the app can never bind it
locally. Fix applied (no reboot): `schtasks /end /tn ModlyServe` to stop
the wedged instance, delete the portproxy rule, `schtasks /run /tn
ModlyServe` (this re-attached to the already-active interactive logon
session, so CUDA still worked), confirm `curl 127.0.0.1:8765/health` is
`ok` from the box, then re-add the portproxy rule
(`listenaddress=0.0.0.0 listenport=8765 connectaddress=127.0.0.1
connectport=8765`) for LAN access. Health and `/model/all` were both
`ok` afterward and stayed reachable for the rest of the run.

Generation used `POST /generate/from-image` directly (not the `agent.py`
CLI, which could not be fetched — GitHub raw download was blocked by this
session's tool policy) with `model_id=hunyuan3d-mini/generate` and
`enable_texture=false`, polling `GET /generate/status/{job_id}`. Each job
reported progress up to 80% quickly, then held at 80% ("Generating 3D
shape…") for the bulk of the run — this is the marching-cubes/mesh
extraction stage at `octree_resolution=380` and is apparently CPU-bound,
independent of the GPU being "warm". The very first job (gauge, right
after the Modly restart) took ~9.3 minutes total; the other three, with
the model already loaded, still took 7.5-9.5 minutes each — noticeably
longer than the skill doc's "~4 minutes" estimate. No run hit the
known 12%/`NoneType` texture-poisoning failure mode (texturing was off
throughout, and `/model/unload-all` was never needed).

## Per-slot results

| Slot | Source image | Modly job | Gen time | Tris before -> after | Verts before -> after | File size | Orientation | Caveat |
|---|---|---|---|---|---|---|---|---|
| gauge.glb | ComfyUI, SD1.5, seed 777, prompt "a single analog pressure gauge, round white dial with black numbers and a red needle, chrome bezel, isolated on plain white background, product photography, one object only" (neg: two/multiple/duplicate/...). Cropped to isolate the larger of two gauges SD produced, padded to square. | `d384cfcf-a4d5-465d-b205-a52e78a7a0d1` | ~9.3 min (cold start, first job after Modly restart) | 561,492 -> 56,148 | 280,746 -> 28,074 | 674.7 KB | +Y up; source photo is an elevated/top-down angle onto the gauge lying dial-up, matching "dial faces +Y" | Dial numerals/branding are AI-hallucinated illegible glyphs, not real WIKA 232.50 graphics. No case/material texture (geometry only). |
| valve.glb | ComfyUI, SD1.5, seed 555, prompt "product photo of a single stainless steel industrial needle valve, standing upright, round black knurled handle on top, front view, isolated on plain white background, studio lighting, centered, one object only, photorealistic". Used as generated (already single-object, square). | `0ccf1a5f-e091-4df6-a540-81848cb70fef` | ~8.1 min | 650,500 -> 58,544 | 325,244 -> 29,266 | 703.3 KB | +Y up; standing upright, rounded handle knob at top faces +Y | **Not an accurate SS-1RS4 replica.** SD1.5 rendered a "thermos-like" cylindrical body with a domed cap/hex-nut/handle assembly rather than a real needle-valve body+bonnet+wheel-handle. Two follow-up attempts asking more literally for "needle valve" / "handwheel" produced cluttered multi-part plumbing scenes or a flat door-knob shape, both worse; this was the best single-object result of 3 tries. Geometry-only stand-in for "cylindrical body, round handle on top". |
| coupling.glb | ComfyUI, SD1.5, seed 646, prompt "a simple stainless steel cylinder with a wider sliding sleeve collar near one end, smooth metal rod, single object, standing upright, front view, plain white background, product photography, minimalist, clean, industrial". SD produced 3 cylinders of different heights; the middle one was cropped out and padded to square. | `7f735d96-4147-4d2e-ac0e-49fdc0107900` | ~9.2 min | 1,004,716 -> 55,258 | 502,357 -> 27,631 | 664.0 KB | +Y up; cylinder axis vertical, standing | **Generic cylinder, not a QRC-style coupling.** The "sliding sleeve" reads only as a subtle lip/cap at the top of the cylinder, not a distinct collar — 2 attempts to get an FDQRCO2-style socket produced an unrelated bent/faceted abstract shape instead, so this plain-cylinder crop was used as the cleanest single-object result. |
| digital.glb | ComfyUI, SD1.5, seed 212, prompt "a single digital pressure gauge, small rectangular LCD screen on top of a cylindrical stainless steel body, one object, standing upright, front view, plain white background, product photography, minimalist, clean, industrial instrument". SD produced 3 objects; the cleanest (analog-dial-looking, not actually digital) cylindrical instrument was cropped out and padded to square. | `060dd1da-68d4-4f8b-9cb9-6d66d8544668` | ~7.5 min | 743,792 -> 55,784 | 371,885 -> 27,886 | 670.2 KB | +Y up; standing upright, face/screen toward +Y | **Face reads as an analog dial, not a digital LCD** — SD1.5 kept substituting a round analog gauge face for "digital display" language across 2 attempts (a 3rd attempt asking explicitly for LCD digits produced two unrelated black plastic multimeters with a logo watermark, discarded). Also carries a small extraneous black strap/hose detail inherited from the source crop. Geometry-only stand-in for "cylindrical body, screen/face on top". |

## Reproducing / regenerating better meshes later

If closer-to-reference geometry is wanted later, the two highest-leverage
changes are: (1) fetch real vendor photos through a tool that can execute
the vendor sites' JS-rendered galleries (e.g. a headless-browser fetch)
instead of WebFetch's markdown-only pass, and (2) for ComfyUI, try an
SDXL or a mechanical-parts LoRA checkpoint, or explicitly force
single-object composition with an image-to-image pass at low denoise over
a hand-placed reference silhouette, since plain SD1.5 txt2img on these
prompts consistently produced multi-object clusters that had to be cropped
down.

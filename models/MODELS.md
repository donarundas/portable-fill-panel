# 3D model files

| File | What | Made by |
|---|---|---|
| `build_panel.py` | Parametric Blender build of the whole panel from the BSD-PFS-003 numbers (case, hinged lid, plate with holes, gauges, valves, couplings, digital gauge, labels, bands, whips, lights, cameras). Run phase by phase: `exec(open(path).read()); run('case')` … | Blender 5.1 via the MCP bridge, 2026-09-04 |
| `portable-fill-panel.blend` | Saved scene with editable text and curves, before conversion for export | same |
| `panel.glb` | Export for the web viewer (`portable-3d.html`). Metres, +Y up. Named nodes: `LidHinge` (rotate X to open), `Labels`, `FillWhip`, `Case`, `Panel` | same |
| `../renders/{iso,top,front,operator}.png` | Eevee renders, 1800 × 1125 | same |
| `gauge.glb` `valve.glb` `coupling.glb` `digital.glb` | Superseded 2026-09-04: Hunyuan3D meshes from the GPU box, generated from AI-drawn stand-in images because vendor photo downloads were blocked. Generic shapes; no longer used by the viewer | Modly on the GTX 1060 |

Lesson recorded in the build: a solid "rim lip" slab across the case opening hid every part shorter than 36 mm — build rims as rings.

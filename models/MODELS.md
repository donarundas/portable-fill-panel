# 3D model files

| File | What | Made by |
|---|---|---|
| `build_panel.py` | Parametric Blender build of the whole panel from the BSD-PFS-003 numbers. Pass 1–3: case, hinged lid, plate with holes, gauges, valves, couplings, digital gauge, engraved labels, bands, fill whip, lights, cameras. Pass 4: ¼ in tube runs under the plate to the P&ID (`build_piping`), painted flow mimic with arrows and 5 mm tags (`build_mimic`), three cascade sets with 47 L cylinders, pigtails, check valves, tee chains, bleeds and whips (`build_cascade`), brushed/textured materials + HDRI (`realism`). Pass 5: enamel cylinder paints, whips draped to the floor and over the front rim (`whip_path`), top camera offset so its roll is defined, cascade view rendered 0.5 stop darker. Run phase by phase: `exec(open(path).read()); M = materials(); run('case')` … `run('piping')`, `run('mimic')`, `run('cascade')`, `run('realism')`, `run('under')`, `run('cascade_render')`, `run('save')`, then `run('convert')` and `run('export')` last (conversion destroys the editable text, so never save after it). | Blender 5.1 via the MCP bridge, 2026-09-04 |
| `portable-fill-panel.blend` | Saved scene with editable text and curves (54 text objects), saved before conversion for export | same |
| `panel.glb` | Export for the web viewer (`portable-3d.html`). Metres, +Y up, ~9.1 MB. Toggle nodes: `LidHinge` (rotate X to open), `Plate`, `Piping`, `Mimic`, `Labels`, `Cascade`, `FillWhip`. Hover anchors: `<TAG>_grp` for every P&ID tag, `CV-0x`, `PSV-01_grp`, `VB01`, `HDR_manifold`, `PM-0x_bleed_grp` | same |
| `../renders/{iso,top,front,operator,under,cascade}.png` | Eevee renders, 1800 × 1125. `under` = plate, mimic and labels hidden so the tube runs show; `cascade` = the three cylinder sets beside the case | same |
| `gauge.glb` `valve.glb` `coupling.glb` `digital.glb` | Superseded 2026-09-04: Hunyuan3D meshes from the GPU box, generated from AI-drawn stand-in images because vendor photo downloads were blocked. Generic shapes; no longer used by the viewer | Modly on the GTX 1060 |

Lessons recorded in the build (see also ../../MISTAKES.md):
- A solid "rim lip" slab across the case opening hid every part shorter than 36 mm — build rims as rings.
- A TRACK_TO camera placed dead above its target has an undefined roll; the top view came out rotated ~60° until the camera was offset 120 mm towards the front.
- Cylinder paints at metallic 0.3 under the studio HDRI all read as white; enamel is metallic ≈0. When colours look wrong, render once with flat diagnostic colours (red/green/blue per material) before touching lighting — it separates "wrong material" from "exposure" in one 5 s render.

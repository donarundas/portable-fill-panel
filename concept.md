# Portable Fill Station — Concept and decision record

**Drawings:** BSD-PFS-001 REV A — fill panel P&ID ([portable-pid.html](portable-pid.html)) ·
BSD-PFS-002 — cascade pigtail manifolds ([portable-cascade-pid.html](portable-cascade-pid.html)) ·
BSD-PFS-003 — general arrangement & plate drilling ([portable-ga.html](portable-ga.html)) ·
3D arrangement pass 1, on hold ([portable-3d.html](portable-3d.html)) · superseded sketch SK-A ([portable-pid-sketch.html](portable-pid-sketch.html)) ·
live BOQ ([boq.html](boq.html), shared store at https://claude.ai/code/artifact/84d72dae-c9cd-4820-afc1-2cd6e2a3a71b).
**Companion to:** the fixed-plant [station P&ID](../station-pid.html) (BSD-PID-001) — same symbols, colours and O₂-clean rules.
**Status 2026-09-04:** concept → sketch → REV A → 002 → 003 GA issued; decisions locked (§7); Indian sourcing done (`sourcing/`); 3D parked at the user's request in favour of the 2D GA.

## 1. What it is

A partial-pressure decant and blending panel in a Pelican 1550. Three keyed, self-venting high-pressure
(HP) quick couplings bring in an oxygen cascade, a helium cascade and an air cylinder; a common manifold
feeds either the fill line directly or an external booster in its own case. Fully mechanical: no power
except the digital master gauge.

**Who it is for:** a CCR / technical-diving expedition or dive boat filling small O₂ and diluent cylinders
(3 L, AL40, twinsets) from a handful of supply cylinders where no fixed plant exists. **Its one job:** put a
measured partial pressure of each gas into a cylinder, safely, from supplies that are slowly running down.

**Form-factor references:** Kirby Morgan KMACS-5 and Amron 8225 portable air panels (HP inlets on hoses,
valves and gauges on a plate in the case) and Pelican-cased O₂/He analysers.

## 2. Basis of design (locked)

| Item | Value |
|---|---|
| Gases | O₂, He, air; product = any mix of the three |
| Supply pressures | O₂ 150 bar (Indian 46.7 L jumbo, 147 bar at 15 °C) · He 150 or 200 bar (specify at order) · air 232 bar (300 possible, not the Indian norm) |
| Supply connections | Indian cylinders per IS 3224:2002, **gas-specific**: O₂ outlet No. 3 G 5/8 RH female → bullnose nut + nipple · He outlet No. 20 G 3/4 RH male → female nut · air outlet No. 19 G 7/8 RH. Pigtails per BSD-PFS-002 [CONFIRM on the supplier's cylinders] |
| Inlet legs, manifold, booster loop | see supply pressure ≤300 bar; source-limited, no relief needed; rated 414 bar |
| Fill zone | **200 bar fill · PSV-01 set 220 bar**, downstream of NV-04 and CV-04 |
| Booster | **USUN XBD30-OL** in its own Pelican: 30:1, drive ≤8 bar, inlet ≥30 bar, max out ≈240 bar, O₂-cleaned. Drive from a scuba first stage set ≈7 bar so stall stays below 220 bar [CONFIRM curve] |
| Component rating | ≥ 414 bar (6000 psi), except needle valves at 344 bar (Swagelok SS-1RS4 class) — accepted 2026-09-04 against a 300 bar maximum supply |
| Cleanliness | whole panel O₂-service. Standard Swagelok or FAV parts, oxygen-cleaned in-house: degrease, FKM/PTFE seals (aftermarket Viton where an O-ring exists), Krytox/Christo-Lube only, UV inspection to ASTM G93 / CGA G-4.1. No factory SC-11 variants (decided 2026-09-04) |
| Valves in the gas path | needle valves only (slow opening). No ball valves (ASTM G88 adiabatic-compression case) |
| Tubing | ¼ in × 0.065 in wall 316 SS |
| Gauges | dry, O₂-cleaned; glycerine fill prohibited. Master gauge digital |
| Case | Pelican 1550: interior 47.3 × 36.0 × 19.6 cm, body depth 14.9 cm, lid 4.4 cm, 4.8 kg. Panel only — booster and analyser travel in their own cases |
| Environment | tropical, salt air; lid open during operation; PSV vents outside the case |

## 3. Arrangement (five groups)

1. **Inlet legs ×3** — keyed quick coupling with integrated vent → supply gauge → needle valve (isolate + meter)
   → check valve → common manifold. The check valve stops a high-pressure supply pushing gas back into a
   lower-pressure one.
2. **Common manifold** — short header, no instruments; at supply pressure in booster mode, cylinder pressure in direct mode.
3. **Selector** — NV-04 DIRECT to the fill line; NV-05 to the booster-suction coupling. Boosted gas returns through
   QC-05 and CV-04 into the fill line. Both shut = panel isolated.
4. **Fill line** — digital master gauge PI-04, relief PSV-01 (220 bar) discharging through vent bulkhead VB-01, product coupling QC-06.
5. **Venting** — bleed V-01 on the fill line just before QC-06 empties the whole panel through VB-01, inlet legs included (their gas flows forward through the open needle valve and check valve into the manifold); each cascade chain has a bleed after its last tee; the fill whip bleeds at its DIN adaptor. The couplings need no vent of their own.

## 4. Cascade pigtail manifolds (BSD-PFS-002)

Reference: Allegro 9891-17 style HP pigtail cascade kit, redrawn for Indian IS 3224 cylinder outlets, which
differ by gas (O₂ G 5/8 bullnose, He G 3/4 male outlet, air G 7/8) and so guard against cross-connection at
the cylinder as well as at the keyed plug. PM-01 (O₂, 3 cylinders) and PM-02 (He, 2 cylinders): per cylinder
the IS 3224 nut and nipple for that gas, a 0.6 m
O₂-clean HP pigtail and a check valve into a chain of ¼ in tees linked by 0.4 m hoses (no manifold bar —
catalogue parts, lighter, the Allegro form); one bleed at the chain end; one outlet whip with the keyed plug
for the panel. PM-03 (air) is a single pigtail with the air key. Details on the sheet.

## 5. Lean choice vs. alternative (as decided)

| Question | Decided | Alternative considered |
|---|---|---|
| Cascade inlets | 1 keyed inlet per gas; cascade on an external pigtail manifold | 2 inlets per gas on the panel |
| Booster switching | two needle valves + one check valve | three-way ball valve (fast opening, rejected) |
| Bleeds | one fill-line bleed V-01 (vents the inlet legs through the open needle valves) + one bleed per cascade chain after the last tee | per-leg bleed valves (SK-A) and vent-on-disconnect couplings (both dropped) |
| Quick couplings | FAV FDQRCO2 double-check poppet, ¼ in NPT F, 6000 psi, 316 SS, standard part with seals swapped in-house; ports labelled and colour-banded, not keyed | keyed, self-venting import couplings (WEH, Stäubli ROX) — unnecessary once the bleeds exist |
| Cross-feed protection | check valve per inlet and per pigtail | procedure only |
| Cascade collector | chain of ¼ in tees + short hoses | machined manifold bar (first draft, dropped at review) |
| Master gauge | digital | 100 mm analogue class 1.0 |
| Booster drive | scuba cylinder through a first stage | small LP compressor |

## 6. Removed from scope (2026-09-04)

Inline analyser module and diver gas panel. The analysis port drawn on SK-A is deleted. Analysis is done
at the cylinder valve with a hand-held analyser that travels in its own case.

## 7. Decisions locked 2026-09-04

1. Fill 200 bar, PSV-01 220 bar. 2. One keyed inlet per gas. 3. Integrated coupling vents; fill-line bleed V-01 before QC-06; fill-whip bleed at
the DIN adaptor. 4. USUN XBD30-OL booster. 5. Pelican 1550 for the panel only. 6. Digital master gauge.
7. Cascade pigtails with IS 3224 gas-specific cylinder ends (BSD-PFS-002). 8. Needle valves at 344 bar accepted.
9. Standard Swagelok or FAV parts, cleaned in-house; no factory oxygen variants.
10. Selector stays two needle valves (NV-04 DIRECT, NV-05 TO BOOSTER); a 3-way ball valve was assessed and declined — it
would move the adiabatic-compression safeguard from hardware into an equalise-before-switching procedure.
11. Quick couplings: FAV FDQRCO2, not keyed — labels and colour bands instead; no vent-on-disconnect, because V-01 and
the chain bleeds vent every segment before a coupling is parted. Cascade chain bleed moved to just before the outlet whip;
the single air pigtail gets its own bleed. WEH quote kept as a comparison only.

## 8. Confirm before purchase [CONFIRM]

- FAV FDQRCO2 couplings: gas service and leak-tightness at 300 bar with helium, seal materials, poppet spring
  material, locking mechanism (FAV's page does not state it), cycle life, mating/parting rules. Fallback: DIN 477
  handwheels on the panel.
- In-house oxygen-cleaning procedure written down before the first oxygen fill (degrease, seal swap, Krytox, UV
  inspection). Trim material at the throttling points.
- PSV-01 spring range at 220 bar and capacity against the XBD30-OL flow; XBD30-OL stall curve for the R-01 set point.
- Pelican 1550 depth against the gauge and valve stack (mock-up; see the 3D pass).
- Cylinder outlets on the supplier's actual cylinders (IS 3224 No. 3 / 20 / 19 assumed; legacy and imported
  valves exist); whip hose O₂ rating at 300 bar.

## 9. Sourcing (2026-09-04) — see [sourcing/SOURCING.md](sourcing/SOURCING.md)

- Valves, fittings, tube: Swagelok Bangalore / Bombay with factory `-SC11` O₂ cleaning; Parker India second.
  FAV (Mumbai) can machine the metal half (10 000 psi panel-mount needle valve, 6000 psi check valves, manifolds)
  but publishes no oxygen cleaning anywhere.
- Gauges: WIKA 232.50 NS 63 dry with the oxygen option; digital WIKA CPG1500 (oxygen option) or Keller LEO5.
  Divesoft makes no pressure gauge — the earlier reference to one is withdrawn.
- Booster: no USUN dealer in India; Maximator India (Navi Mumbai) makes an oxygen-rated rebreather booster.
- Hoses: Hydroflex Pipe (Ahmedabad) 400 bar DN6 assemblies; O₂ cleaning is an RFQ question. Bullnose and
  IS 3224 nut/nipple sets are ordinary catalogue stock.
- Quick couplings: FAV FDQRCO2 decided 2026-09-04; addendum sent under RFQ PFS-2609-03. WEH quote kept for comparison.

## References

- USUN XBD30-OL: https://www.diverightinscuba.com/xbd30-ol-booster-pump.html · XB30-OL spec: https://www.diverightinscuba.com/usun-xb30-ol-booster-pump.html
- Pelican 1550: https://www.pelican.com/us/en/product/cases/1550
- Allegro 9891-17 cascade kit: https://www.industrialsafetyproducts.com/allegro-9891-17-airline-cascade-kits-hp-flexible-pigtail/
- WEH TW17/TW117: https://www.weh.com/media/downloads/brief-overview/gas-brief-overview-en.pdf · Stäubli RBL: https://www.staubli.com/content/dam/fcs/brochures/products/rbl/rbl-all-fluids-stainless-steel-couplings-staubli-en.pdf
- Swagelok N-series: https://www.swagelok.com/downloads/webcatalogs/en/ms-01-168.pdf · CH check valves: https://www.swagelok.com/downloads/webcatalogs/EN/MS-01-176.PDF · R3A/R4 relief: https://www.swagelok.com/downloads/webcatalogs/en/MS-01-141.PDF
- KMACS-5 manual: https://www.kirbymorgan.com/sites/default/files/2021-06/KMACS-5-Manual.pdf · Amron 8225-HP: http://www.amronintl.com/media/PDF/products/8225-HP_MANUAL_12-12.pdf

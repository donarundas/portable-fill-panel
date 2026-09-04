# Sourcing synthesis — portable fill station (India), 2026-09-04

Three research passes (files in this folder): [fav.md](fav.md) — FAV, Mumbai · [indian-hp-components.md](indian-hp-components.md) —
other Indian makers, distributors, cylinder outlets · [gauges-case-booster-cylinders-india.md](gauges-case-booster-cylinders-india.md) —
gauges, case, booster, cylinder facts. Everything below is read from those reports; part numbers were read off
supplier pages by the researchers, and anything they could not verify is marked "inferred" there.

## Findings that changed the design

1. **Cylinder outlets are gas-specific in India** (IS 3224:2002, cross-checked with AIGA 098/17 and a live Indian
   valve maker): O₂ = outlet No. 3, G 5/8 RH female → male bullnose nut + nipple · He/Ar/N₂ = outlet No. 20,
   G 3/4 RH **male** → female nut · air = outlet No. 19, G 7/8 RH. BS 341 puts helium on the oxygen No. 3 outlet;
   India does not. BSD-PFS-002 was corrected the same day (note 6, Detail A, parts table).
2. **Indian O₂ arrives at ~147 bar** (46.7 L jumbo, 7 m³ at 150 kgf/cm² @ 15 °C). He is sold at 150 or 200 bar.
   Breathing air is 232 bar; no Indian dive centre advertising 300 bar fills was found (a negative search, not proof).
3. **No valve offers regulating stem + panel mount + 6000 psi.** Swagelok SS-1RS4 has the first two at 344 bar.
   **Decided 2026-09-04: 344 bar accepted** against the 300 bar maximum supply; standard (non-SC-11) parts from
   Swagelok or FAV, oxygen-cleaned in-house with aftermarket FKM seals and Krytox.
4. **Stäubli RBL is not an oxygen coupling** above 725 psi; Stäubli routes O₂ to the ROX family. WEH TW17 is a
   350 bar test connector. Quick couplings are import-only; WEH has no Indian entity, Stäubli does (Tec-Systems India).
5. **Divesoft makes no digital pressure gauge** — removed from the schedule. WIKA CPG500 fails the spec (no 400 bar
   range, 0.25 % FS, NBR). Viable: WIKA CPG1500 with the factory oxygen option, or Keller LEO5 0–400 bar.

## Candidate table

| Tag / item | Import candidate | India candidate | Status |
|---|---|---|---|
| NV-01..05 needle valves | Swagelok SS-1RS4 (344 bar, regulating, panel nut) via Swagelok Bangalore/Bombay | FAV FNV/MF/HP/02 (10 000 psi, panel nut; plain stem) | decided: either, cleaned in-house |
| CV-01..04, pigtail CVs | Swagelok SS-CHS4-1-SC11 (6000 psi, 1 psig crack) | FAV FAVCV/MF/04 (6000 psig, Viton; cleaning to arrange) | ready to RFQ |
| PSV-01 | Swagelok SS-4R3A5 + spring F (206–275 bar); proportional, not a certified safety valve | FAV FRV/MF-4N family (10–400 bar by spring, but carbon-steel spring, 1/2 in shown) | Swagelok preferred |
| VB-01, tube fittings, tube | Swagelok / Parker India | FAV FCF/BU/4I bulkhead, FCF/U/4I unions (ratings not published); no Indian 316 SS instrument tube found | Swagelok/Parker |
| Cascade tees (PM-01/02) | Swagelok SS-400-3-SC11 union tees | FAV tube tees (ratings not published) | Swagelok; the manifold bar was dropped at review, so FAV's build-to-order manifold is no longer needed |
| QC-01..06 quick couplings | WEH TW17/TW117 quote kept for comparison | **FAV FDQRCO2** double-check poppet, ¼ in NPT F, 6000 psi, 316 SS — decided 2026-09-04, not keyed, no vent (bleeds do that) | FAV; confirm gas-tightness, seals, locking |
| Hoses: whips and pigtails | Parker / Swagelok hose assemblies | Hydroflex Pipe, Ahmedabad: DN6 corrugated 316L + braid, 400 bar WP, cylinder-valve ends; oxygen not listed | RFQ O₂ cleaning |
| Cylinder nuts + nipples (IS 3224) | — | ordinary catalogue stock (e.g. Cryo Gas Engineers, Noida) | ready |
| PI-01..03 | WIKA 232.50 NS 63, 0–400 bar, cl. 1.6, centre-back, "oil- and grease-free for oxygen" option, custom "USE NO OIL" dial | WIKA India (Pune) | note ¾ FS steady limit = 300 bar |
| PI-04 | WIKA CPG1500 (oxygen option) · Keller LEO5 0–400 bar (±0.4 bar, no factory O₂ option) | WIKA India / Keller distributor | quotes needed |
| BST-01 | USUN XBD30-OL — no Indian dealer, import | Maximator India Pvt Ltd (Navi Mumbai): rebreather oxygen booster; DLE series O₂-rated to 350 bar | user decided XBD30-OL; local alternative noted |
| Case | Pelican 1550 ≈ ₹42 000 (Amazon.in) | **Case N Foam** (Toolfit, Bengaluru, info@caseandfoam.in) EW/MAX waterproof series, 190+ sizes, RFQ PFS-2609-12 sent; MAX / Unicase ≈ ₹6 700–7 050 | Pelican or Case N Foam — compare quotes |

## FAV quote received 2026-09-04 (PFS-2609-03)

Needle valve ₹2 275 · check valve ₹1 865 · tee ₹683 · union ₹387 · elbow ₹587 · male connector ₹288 · bulkhead ₹755 (MOQ 5) · plug ₹283 · cap ₹335. Ex-works Mumbai, GST 18 % extra, 25 working days, advance. Valves and fittings subtotal ≈ ₹68 700 ex GST. Technical questions unanswered; follow-up sent. FAV can also supply the relief valve, hose assemblies, gauge adaptors and bulkhead adaptors — asked in the follow-up. Not from FAV: gauges, digital gauge, booster, case, IS 3224 cylinder nuts, aluminium plate, probably tube.

## RFQ shortlist

- **Swagelok Bangalore / Bombay:** SS-1RS4 ×8 (5 panel + 1 fill-line bleed + 2 cascade bleeds), SS-CHS4-1 ×10,
  SS-4R3A5 + spring F ×1, SS-400-3 tees ×5, bulkhead union, ¼ in fittings, ¼ in × 0.065 in tube — standard parts;
  the user cleans in-house.
- **FAV, Mumbai:** needle valves FNV/MF/HP/02, check valves FAVCV/MF/04, tees and bulkhead fittings as the local
  alternative; ask for seal and lubricant declaration and stem type (cleaning is done in-house).
- **Hydroflex Pipe, Ahmedabad:** 4 × 1.5 m whips, 6 × 0.6 m pigtails, 3 × 0.4 m link hoses, IS 3224 ends per gas, DIN 232 fill end with
  bleed screw; ask for oxygen service, cleaning, 400 bar certification.
- **WIKA India, Pune:** 3 × 232.50 NS 63 0–400 bar with oxygen option and custom dial; 1 × CPG1500 oxygen option.
- **Stäubli / Tec-Systems India:** ROX couplings — pressure rating, keying, vent-on-disconnect, mating under pressure.
- **Maximator India:** oxygen booster datasheet and price, as the no-import alternative to the XBD30-OL.

## Caveats

No Indian maker publishes an oxygen-cleaning standard; outside Swagelok and Parker, cleaning is an RFQ question and
a certificate must be demanded. Prices for WIKA and Keller were not published anywhere. Import duty for the booster
(HS 8414.80.90) was not checked.

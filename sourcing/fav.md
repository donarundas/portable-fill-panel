# FAV (Fittings and Valves) — sourcing check against the portable panel schedule

Checked 2026-09-04 against `fav.net.in`, and the same firm's sister sites `favfittings.com` and
`instrumentation-fittings.com` (all FAV / brand of Pioneer Enterprise, Mazgaon, Mumbai —
sales@fav.net.in, +91 22 23757188). No one was contacted; everything below is from published pages.

## 1. Verdict

FAV is a credible source for the **metal** half of this panel and a poor source for the **oxygen**
half of it. They are a Mumbai bar-stock instrumentation maker (ISO 9001:2015, PED 2014/68/EU) with
published part-number tables for 1/4 in 316 SS needle valves, check valves, relief valves, double-
ferrule tube fittings and bulkhead unions at 6000 psi and above, plus a genuinely useful build-to-
order high-pressure distribution manifold / air header (up to 18 ports, 1/4 in NPT female, 10 000–
15 000 psi) that maps almost exactly onto our cascade manifold bars. What is missing is everything
that makes a part fit for oxygen: across every product, category and certification page I read, FAV
**never mentions oxygen service, oxygen cleaning, degreasing, ASTM G93 / A380 cleanliness levels, or
O₂-compatible lubricants** — nor do they publish seal materials for some items (QRC), and their
high-pressure relief valve uses a powder-coated ASTM A576 carbon-steel spring. So FAV should be
treated as a *machining and assembly* supplier whose parts would need an O₂-cleaning and
seal-substitution scope agreed in writing, not as an off-the-shelf oxygen-service catalogue. The
gas-specific items — keyed quick-connects with vent-on-disconnect, and 400 bar O₂ hose with 5/8 in
BSP bullnose ends — they do not appear to make at all.

## 2. Match table

| Our tag / item | FAV product line & part no. pattern | Rating | Material & seals | End connections | O₂-service option? | Source | Confidence |
|---|---|---|---|---|---|---|---|
| NV-01..05 needle valve, 1/4 in, panel-mount, 6000 psi | HP needle valve, integral bonnet **with panel mounting nut**: `FNV/MF/HP/02` (1/4 in) | 10 000 psi | 316 SS body; **PTFE seats**; stem thread-rolled | NPT M × F (BSP on request) | Not offered/stated | https://www.fav.net.in/high-pressure-needle-valves-male-x-female-10000-psi/ | checked on page |
| NV alt (non-panel, exact 6000 psi) | `FNV/MF/02` (1/4 in, M×F), `FNV/OD/02` (1/4 in tube OD both ends) | 6000 psi | 316 SS, double bonnet union spindle, PTFE seats | NPT/BSP, or double-ferrule tube | Not offered/stated | https://www.fav.net.in/needle-valves-male-x-female-6000-psi/ , https://www.fav.net.in/needle-valve-compression-tube-double-ferrule-6000-psi/ | checked on page |
| NV regulating / fine-metering stem | **No metering-stem, vee-stem or Cv-graded variant published.** "Flow Control Valve" page is generic marketing with no data | — | — | — | — | https://www.fav.net.in/flow-control-valves/ | checked on page (absent) |
| CV-01..04 check valve, 1/4 in, 6000 psi | `FAVCV/MF/04` (1/4 in NPT M×F); also female, male, and double-ferrule tube versions | 6000 psig | 316 SS body/poppet/spring/guide/stopper; **Viton O-ring** | NPT M/F, BSPT, BSPP, tube OD | Not offered/stated | https://www.fav.net.in/check-valve-male-x-female/ | checked on page |
| CV cracking pressure | Standard **20 psi ±30 %**; "selectable" and "adjustable crack pressures" offered | — | — | — | — | https://www.fav.net.in/check-valves/ | checked on page |
| PSV-01 relief, 1/4 in, set 220 bar | Standard series `FRV/MF-4N` (1/4 NPT M×F, orifice 6 mm, Cv 0.65); tube versions `FRV/MT-4-4I` (imperial), `FRV/M-4-4M` (metric) | Series shown for lower sets (e.g. 1/4 in M×F @150 psi); **HP series to 6000 psi** | 316 SS body/bonnet/disc/guides; **seats + stem seals Viton or Buna-N**; standard spring 316 SS | NPT M×F, tube OD, F×F | Not offered/stated | https://www.fav.net.in/pressure-relief-valve/ | checked on page |
| PSV-01 set-point range | HP relief valve: **"Pressure Range 10 Bar to 400 Bar with Different Spring"**, range-setting screw under a cap — covers our 200–250 bar. Caveat: that variant is illustrated as **1/2 in NPT M×F**, seals Viton, PTFE backup ring, and **spring = ASTM A576 (carbon steel), powder coated** | ≤6000 psi | as above | 1/2 in NPT M×F shown | Not offered/stated | same page | checked on page; 1/4 in @220 bar = inferred |
| VB-01 bulkhead union, 1/4 in | `FCF/BU/4I` — panel hole 29/64 in, max panel thickness 0.40 in | not published for this item | 316 SS (material list: 316/304/Monel/Hastelloy/Inconel/Ti/Super Duplex) | double-ferrule tube × tube, through-panel | Not offered/stated | https://favfittings.com/instrument-fittings/double-ferrule-compression-fittings/bulkhead-union-2/ | checked on page |
| Tube fittings — union | `FCF/U/4I` (1/4 in) | not published | 316 SS, twin/double ferrule + nut | tube × tube | Not offered/stated | https://www.fav.net.in/straight-union-double-ferrule-fittings/ | checked on page |
| Tube fittings — union tee (×8) | `FCF/UT/4I` | not published | as above | tube × tube × tube | Not offered/stated | https://favfittings.com/instrument-fittings/double-ferrule-compression-fittings/tee-union-2/ | checked on page |
| Tube fittings — union elbow | `FCF/UE/4I` (pattern seen as `FCF/UE/12I` for 3/4 in) | not published | as above | tube × tube | Not offered/stated | https://www.scribd.com/document/369106136/FAV-Double-Ferrule-Compression-Tube-Fittings (FAV catalogue) | **inferred** (size code only) |
| Tube fittings — male connector 1/4 in tube × 1/4 NPT | `FCF/MC/4I-4T` (pattern `FCF/MC/<tube>I-<NPT>T`, e.g. published `FCF/MC/1I-1T`) | not published | as above | tube × NPT male (BSPP `FCF/MC/IP/…`, BSPT variants exist) | Not offered/stated | https://favfittings.com/instrument-fittings/double-ferrule-compression-fittings/male-connector-npt-2/ | **inferred** (size code only) |
| 1/4 in × 0.065 in 316 SS seamless tube, ~6 m | **No tubing product found** on any FAV site (they list PTFE tube only) | — | — | — | — | site map + search of all three FAV domains | checked (absent) |
| Manifold blocks, 3-inlet and 2-inlet, 1/4 NPT, 6000 psi | **Distribution manifold / air header**, built to order: "up to 18 ports", 1/4"–1" NPT female, needle or ball valves integral, gauge/check-valve/hose accessories, mounting stand | **10 000–15 000 psi** | 316/304 SS (and exotics) | NPT female (BSP, socket/butt weld, flanged, compression on request) | Not offered/stated | https://www.fav.net.in/distribution-manifold-and-air-header-10000-to15000-psi/ , https://www.fav.net.in/manifold-for-hydro-testing/ | checked on page |
| Manifold alt | **High Pressure Manifold Block**, 2/3/4/5/6-way drilled blocks — photos only, **no rating, material or part numbers published** | not published | not published | not published | Not stated | https://www.fav.net.in/high-pressure-manifold-block/ | checked (data absent) |
| QC-01..06 quick coupling ≥400 bar, keyed, vent on disconnect | **Double-check-valve QRC**: `FDQRCO2` = 1/4 in NPT(F); series `FDQRCO1`…`FDQRCO8` (1/8"–1.5") | **6000 psi / 400 bar** (own design; 10 000 and 15 000 psi QRC also listed) | SS 316 body; **seal material not published** | NPT female both halves | Not offered/stated | https://www.fav.net.in/quick-disconnect-coupling-double-check-type-6000-psi/ , https://www.fav.net.in/quick-release-couplings/ | checked on page |
| QC keying / vent-on-disconnect | **Not offered.** Double-check type shuts both halves and traps line pressure; no gas-specific keying or non-interchangeable profiles anywhere on the site | — | — | — | — | https://www.fav.net.in/quick-release-couplings/ | checked (absent) |
| Hose 1/4 in, 400 bar, 1.5 m + 0.9 m, 5/8 in BSP bullnose | SS braided / corrugated hose assemblies and crimped hydraulic hose (SAE 100R1/R2/R3/R6, 1–6 wire; Parker/Polyhose/Goodyear/Dunlop hose bought in) | **No pressure ratings published**; hose temp −270 to 700 °C for SS corrugated | SS 304/316/321 braid, SS 316 end fittings, TIG welded | NPT M/F, BSP/BSPT M/F (fixed + swivel), JIC, SAE, flange, double-ferrule tube. **No bullnose / IS 3224 / BS 341 No.3 cylinder end listed** | Not offered/stated | https://www.fav.net.in/hose-fittings-stainless-steel-braided-hose-hoses-hose-fittings-high-pressure-hose-assemblies/ , https://www.fav.net.in/stainless-steel-braided-hose/ | checked on page |
| Gauge adaptors | 8 styles listed (M×M, M×F, multiport long/extra-long, elbow, swivel) — **no part numbers, ratings or materials published** | not published | not published | NPT/BSP implied | Not stated | https://www.fav.net.in/pressure-gauge-accessories-and-pressure-gauge-swivel-adapters/ | checked (data absent) |
| Certifications | ISO 9001:2015 (prev. 9001:2008), PED 2014/68/EU; "tested to internationally recognised standards or our own internal procedures"; client-specific testing on request. **No cleanliness, NACE, MTC or oxygen-cleaning certificate mentioned** | — | — | — | — | https://www.fav.net.in/certifications/ | checked on page |

## 3. Gaps FAV cannot fill (from published information)

1. **Oxygen cleaning / oxygen service, on any item.** Zero occurrences of "oxygen", "O₂ clean",
   "degreased", ASTM G93 or A380 across product, certification and about pages on all three FAV
   domains. This is the decisive gap: every wetted part in our schedule needs it.
2. **Keyed / gas-specific quick connects with vent-on-disconnect.** Not made. Their 400 bar QRC is a
   single generic NPT profile — nothing prevents cross-connecting O₂ and He, and disconnect leaves
   trapped pressure. This is a safety-critical item to buy elsewhere (or design out).
3. **Oxygen hose assemblies with Indian cylinder bullnose ends** (5/8 in BSP RH per IS 3224 / BS 341
   No. 3). Their hose ends stop at NPT/BSP/JIC/flange; no bullnose, and no published working
   pressure for the hose itself.
4. **316 SS instrument tubing.** Not a FAV product — source separately (with an O₂-clean spec).
5. **Fine-metering / regulating needle stems.** No metering-stem option, no Cv-vs-turns data, no flow
   curves. Their needle valves are on/off-and-throttle bar-stock valves; fine PP blending control is
   not evidenced.
6. **Published pressure ratings on several items we would rely on** — bulkhead union and tube
   fittings (no rating tables), manifold blocks, gauge adaptors, hoses. Ratings exist only in the
   valve tables.
7. **Elastomer choice.** Viton (FKM) is the default on check and relief valves — good for us — but
   Buna-N is offered interchangeably on relief valves and QRC seals are unpublished. Nitrile in O₂ at
   300 bar is not acceptable; this must be pinned down per line item.

## 4. RFQ questions to put to FAV (sales@fav.net.in)

1. Do you offer **oxygen cleaning** to a stated standard (ASTM G93 level, or EN ISO 15001 / CGA G-4.1)
   with a **cleanliness certificate**, and can parts be **double-bagged and sealed** after cleaning?
   If yes: which product lines, and what is the price and lead-time adder per piece?
2. For O₂ service at 300 bar working: can you supply **all wetted seals in Viton (FKM) or PTFE only**,
   with **no hydrocarbon lubricant, cutting oil or anti-seize** anywhere on the wetted path? Which
   assembly lubricant / thread sealant do you normally use, and can it be replaced with an
   O₂-compatible one (PTFE tape or Fluorolube-type)?
3. `FNV/MF/HP/02` — confirm 1/4 in NPT, 316 SS, PTFE seat, **panel mounting nut dimensions and
   maximum panel thickness**, and confirm the same body is available with **tube-OD (double-ferrule)
   ends**. Is a **regulating / metering stem** available, and can you supply Cv-vs-turns data?
4. `FAVCV/MF/04` — confirm 6000 psi, 316 SS, Viton seal, and quote a **low cracking pressure option
   (target ≤ 3–5 psi)**; state the tolerance and whether it is repeatable after O₂ cleaning.
5. Relief valve for a **220 bar set point in 1/4 in NPT**: is the 10–400 bar spring-range HP body
   available in 1/4 in (part number?), what is the **spring material** in that variant (the page shows
   ASTM A576 powder-coated carbon steel — can it be 316 SS or fully isolated from the gas?), and is
   the relieving characteristic **proportional/modulating or pop-action**? Can you supply a
   **calibration certificate at 220 bar** and state reseat pressure?
6. `FCF/BU/4I` bulkhead union and `FCF/U/4I` / `FCF/UT/4I` / `FCF/UE/4I` / `FCF/MC/4I-4T`: confirm the
   1/4 in part numbers and give the **published working pressure with 1/4 in × 0.065 in wall 316 SS
   tube**, plus ferrule material and **whether the fittings are interchangeable with Swagelok-pattern
   tube fittings**.
7. **Cascade manifold bars**: quote two custom distribution manifolds — one 3-inlet and one 2-inlet,
   all ports 1/4 in NPT female, **no integral valves**, 316 SS bar stock, rated ≥6000 psi, with
   mounting holes for panel fixing; supply a dimensioned drawing before manufacture.
8. `FDQRCO2` 400 bar QRC — what are the **seal materials**, is a **vent/bleed on disconnect** possible,
   and can you supply **non-interchangeable (keyed or differently sized) variants** so that O₂, He and
   air couplings cannot be cross-connected?
9. **Hose assemblies**: can you supply 1/4 in ID assemblies at a **certified 400 bar working pressure
   (4:1 burst)** in 1.5 m and 0.9 m, oxygen-cleaned, with one end **5/8 in BSP RH male bullnose to
   IS 3224 / BS 341 No. 3** and the other 1/4 in NPT male? State hose construction (PTFE-lined vs
   rubber) and give the **hydrostatic test certificate** per assembly.
10. Do you supply **1/4 in × 0.065 in wall 316 SS seamless instrument tubing (ASTM A269/A213)**,
    oxygen-cleaned, in ~6 m lengths — or should we source tube separately?
11. What **documentation** ships with an order: material test certificates (EN 10204 3.1) per heat,
    pressure-test records per valve, and PED conformity where applicable?
12. Confirm **export/domestic lead time and MOQ** for the above, and whether the panel-mount needle
    valves can be supplied with **handle colour-coding or gas labelling** (O₂ / He / air).

---
*Compiled from FAV's own web pages only. Items marked "inferred" in the table are size codes derived
from FAV's published part-number pattern for other sizes — confirm before ordering. "Not offered/
stated" means the option does not appear anywhere on FAV's published pages; it is not proof that FAV
cannot do it to order, which is what question 1 is for.*

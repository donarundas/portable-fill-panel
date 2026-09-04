# Indian sourcing — HP oxygen-service components (excl. FAV)

Research date 2026-09-04. Web/catalogue research only; no supplier was contacted.

## 1. Verdict

**Most of the schedule is buyable in India, but almost none of it is *made* in India to
oxygen-service spec.** The instrumentation core — needle, check and relief valves, ¼ in tube
fittings and ¼ × 0.065 in 316 SS tube — is available through Swagelok's two Indian Authorised
Sales & Service Centres (Bangalore and Bombay/Pune) and through Parker Hannifin India (Navi
Mumbai), both of which sell the parent catalogue including the factory oxygen-clean option
(Swagelok `-SC11`, ASTM G93 Level C). That is an import at the component level with local
invoicing, stock and support, which is the practical answer for a five-off build. Genuinely
Indian-manufactured alternatives exist for the valve bodies (Astec Valves & Fittings, Mumbai —
6000 psi instrumentation valves) but no Indian instrumentation-valve maker was found publishing
an oxygen-cleaning specification, so O₂ service would have to be an RFQ question, not a
catalogue tick-box. Three things are genuinely Indian and off the shelf: **HP hose** (Hydroflex
Pipe, Ahmedabad — DN6 annular-corrugated 316L with 304 double braid, 400 bar working, 1200 bar
burst, assemblies with cylinder-valve ends), **bullnose nut-and-nipple sets** (standard catalogue
item from gas-equipment houses such as Cryo Gas Engineers, Noida), and **cascade manifold bars**
(Unique Pipeline, JK Subsea — SS bar-stock headers, though at 240–300 bar, not 414). **What must
be imported: the six HP quick couplings.** WEH has no Indian entity (`weh.in` is a 301 redirect
to `weh.com`); Stäubli does have an Indian subsidiary (Stäubli Tec-Systems India, Bengaluru) but
its own literature routes oxygen above 725 psi / 50 bar away from RBL to the ROX family, so RBL
is only the answer for the helium and air ports.

**Three findings that change the schedule** (detail in §3 and the table notes):

1. **Helium in India is not a 5/8 in bullnose.** IS 3224 outlet No. 20 (Ar/N₂/He) is **G 3/4 RH
   with a *male* outlet on the cylinder valve**; oxygen (outlet No. 3) is **G 5/8 RH *female***.
   Different size *and* opposite gender. The five cascade pigtails cannot share one end fitting.
2. **No single valve gives regulating stem + panel mount + 6000 psi.** Swagelok's panel-mountable
   regulating-stem series (O/1/18) is rated 5000 psig / 344 bar; the 6000 psig / 413 bar series
   (20/26) has vee or soft-seat stems only and no panel nut. 344 bar still clears 300 bar working
   but misses the ≥414 bar rule — a deliberate decision is needed.
3. **The Swagelok R-series relief valve is proportional and explicitly not an ASME or PED
   certified safety device.** Fine as a system relief, not as a certified safety accessory.

## 2. Supplier table

| Item | Supplier | Product / part pattern | Rating | O₂-service option | End connections | URL | Confidence |
|---|---|---|---|---|---|---|---|
| ¼ in needle valve, regulating stem, panel-mount | Swagelok Bangalore / Bombay (ASSC) | Integral-bonnet, 1 series — `SS-1RS4-SC11`, 0.37 Cv | 5000 psig / 344 bar (316 SS, ≤100 °F) — **not 6000 psi** | Yes, `-SC11` = ASTM G93 Level C | ¼ in Swagelok tube fitting; panel nut is a catalogue component of O/1/18 series | [product](https://products.swagelok.com/en/c/straight-pattern-regulating-stem/p/SS-1RS4-SC11) · [MS-01-164](https://www.swagelok.com/downloads/webcatalogs/en/ms-01-164.pdf) | checked on page |
| ¼ in needle valve at 6000 psi (alternative) | Swagelok ASSC | 20 series, e.g. `SS-20VS4` (vee stem) / `SS-20KF4` (soft-seat) | 6000 psig / 413 bar | `-SC11` available (catalogue-wide option) | ¼ in tube fitting or NPT; **no panel mount, no regulating stem** | [MS-01-164](https://www.swagelok.com/downloads/webcatalogs/en/ms-01-164.pdf) | checked on page |
| ¼ in needle valve (Indian-made) | Astec Valves & Fittings Pvt Ltd, Andheri W, Mumbai | Instrumentation needle / gauge-root valves | up to 6000 psi / 413 bar stated | **Not published** — RFQ item | ⅛–2 in, NPT / BSPT / tube fitting | [astecflow.com](https://www.astecflow.com/) | checked on page (rating); O₂ inferred/unknown |
| ¼ in check valve, low cracking | Swagelok ASSC | Poppet check, CH series — `SS-CHS4-1-SC11` | 6000 psig / 413 bar | Yes, `-SC11` | ¼ in Swagelok tube fitting; 1 psig (0.07 bar) crack | [product](https://products.swagelok.com/en/c/fixed-pressure/p/SS-CHS4-1-SC11) | checked on page |
| ¼ in relief valve, ~220 bar | Swagelok ASSC | R3A series — `SS-4R3A` (tube) / `SS-4R3A5` (M-NPT × F-NPT); spring designator **F** = 3000–4000 psig (206–275 bar) covers 220 bar; add `-SET` for factory-set | 6000 psig inlet / 413 bar; set range 50–6000 psig | Yes, `-SC11` | ¼ in tube fitting or NPT; wetted 316 SS, FKM O-ring, PTFE-coated FKM quad seal | [MS-01-141](https://www.swagelok.com/downloads/webcatalogs/en/ms-01-141.pdf) | checked on page |
| ¼ in tube fittings + ¼ × 0.065 in 316 SS seamless tube | Swagelok ASSC (fittings + tube); Indian mills for tube: Multi Metals India, Roopam Steel, Siddhagiri Metals | Swagelok tube fittings; tube to ASTM A269/A213 TP316/316L seamless | fitting/tube rating per MS-01-107 tubing data | `-SC11` on fittings; tube needs separate degrease spec | ¼ in tube | [Multi Metals](https://www.multimetalsindia.com/stainless-steel-316-tube.html) · [Roopam](https://www.roopamsteel.com/astm-a269-stainless-steel-316-tube.html) | supplier checked; **O₂-clean tube supply inferred** |
| ¼ in valves/fittings, alternative brand | Parker Hannifin India Pvt Ltd, Mahape, Navi Mumbai (Instrumentation Products Div.) | IPD needle, check, relief valves; "oxygen clean options available" | per IPD catalogue | Stated available — confirm spec/standard on RFQ | NPT / BSP / tube | [ipd.parker.com](https://ipd.parker.com/category/valves-1) | supplier checked; O₂ option stated, spec not verified |
| ¼ in valves, further alternatives | Fitok via **A B Process Technologies**, Pune (India distributor); Hy-Lok via Indian dealers; Stäubli/Ham-Let/DK-Lok — no Indian entity confirmed | Fitok needle / check / ball valves | per Fitok catalogue | not verified | NPT / tube | [abprocesstech.com](https://www.abprocesstech.com/fitok/) | distributor checked; product fit inferred |
| 6 × HP quick couplings ≥400 bar, keyed, vent on disconnect | **Import.** WEH GmbH (no India entity — `weh.in` 301-redirects to `weh.com`); Stäubli Tec-Systems India Pvt Ltd, Bengaluru | Stäubli **RBL06** (¼ in) 6527 psi / 450 bar, 316 SS. **For O₂ >725 psi Stäubli directs to ROX 05**, designed against adiabatic-compression autoignition. WEH TW17 is a *test* connector, 350 bar — filling family needed instead | RBL06 450 bar; TW17 350 bar (**below the 400 bar requirement**) | RBL O₂ codes JV/OX, JE/OX only **below 725 psi**; above that → ROX | NPT ¼/⅜, G threads, tube ends | [RBL brochure](https://www.staubli.com/content/dam/fcs/brochures/products/rbl/rbl-all-fluids-stainless-steel-couplings-staubli-us.pdf) · [Stäubli India](https://www.staubli.com/global/en/about-us/our-business-units/staubli-india.html) | checked on page |
| HP hose, ¼ in, 400 bar | **Hydroflex Pipe Pvt Ltd**, Jetalpur, Ahmedabad | Annular-corrugated 316L + 304 double wire braid; DN6 = **400 bar WP @20 °C**, 600 bar test, 1200 bar burst; assemblies made with ¼ in NPT female and cylinder-valve ends | 400 bar | **Oxygen not explicitly listed** — degrease to ASTM G93 must be specified on RFQ | ¼ in NPT female fixed; "suitable for gas cylinder valve" | [hydroflexpipe.com](https://www.hydroflexpipe.com/metal-hoses.html) | checked on page; O₂ clean inferred/unconfirmed |
| HP hose, alternatives | Aeroflex Industries Ltd, Taloja, Navi Mumbai; OxyVac India, Vadodara; Sunlight Gas & Equipment, Navi Mumbai; Polyhose India, Chennai | SS corrugated + braided hose and pigtail assemblies | OxyVac 300 bar; Sunlight 200 bar; Polyhose hybrid 165–400 bar (hydraulic) | not published | OxyVac: pre-assembled cylinder-valve adaptor "to national standard", W21.8 outlets | [Aeroflex](https://www.aeroflexindia.com/product/corrugated-stainless-steel-hose/) · [OxyVac](https://oxyvacindia.com/High-Pressure-Pigtails/high-pressure-pigtails.php) | checked on page; **most rated below 400 bar** |
| Bullnose nipple + nut sets (O₂, and inert) | **Cryo Gas Engineers India, Noida**; also Pushp Enterprise (Jamnagar), Chaman Engg (Kanpur), Al-Can Exports (Thane) | "Oxygen Nut Nipple", "Oxygen Cylinder Nut" — 28 mm brass hex, 5/8 in, for oxygen cylinder valve; CGA 540/580 sets also stocked | brass; manifolds quoted 150–200 kg/cm², HP systems to 400 bar | brass is inherently O₂-compatible; cleaning to be specified | 5/8 in for O₂; ¼ in NPT on the fitting side | [Cryo Gas Engineers](https://www.indiamart.com/cryogasengineersindia/gas-manifold-accessories-division.html) | checked on page — **yes, it is a standard catalogue item** |
| HP manifold bar / cascade block, ¼ NPT, 3-in and 2-in | Unique Pipeline Projects Pvt Ltd; JK Subsea; Excelgas & Equipment, Navi Mumbai | Manifold headers machined from single-piece SS 304/316 bar stock | Unique: **240 bar WP, 300 bar hydro test**; JK Subsea: inlet to 300 bar, SS316, IS 6901:2009 | not published | ¼ in NPT ports available | [Unique Pipeline](https://www.uniquepipeline.com/industrial-manifold.php) · [JK Subsea](https://www.jksubsea.com/product/gas-manifold/) | checked on page; **240–300 bar < 414 bar target** |

## 3. Indian cylinder valve outlet facts (O₂ and He)

India uses **IS 3224:2002** (*Valve fittings for compressed gas cylinders excluding LPG*), the
national standard named for India in AIGA 098/17. It is *equivalent in spirit* to BS 341 but
**not identical in the outlets that matter here.** Read directly from the standard's own gas
table and outlet drawings:

| Gas | IS 3224 outlet No. | Thread | Valve outlet gender | Mating part |
|---|---|---|---|---|
| **Oxygen** | **3** | **G 5/8 RH (BSP 5/8)**, pitch 1.814 mm | **Female (internal)** — minor dia 21.128/20.587 mm | Male **hexagon nut G 5/8A RH** capturing a **connector** (bullnose nipple) — i.e. the classic bullnose union |
| **Helium** (also Ar, N₂, Ne, Kr, Xe) | **20** | **G 3/4 RH (BSP 3/4)**, pitch 1.814 mm | **Male (external)** — drawing reads "Threads G3/4 EXT — RH (BSP 3/4)" | **Female hexagon nut G 3/4 INT RH** over a connector nipple |
| Air | 19 | G 7/8 RH (BSP 7/8) | Male ("G7/8 EXT RH") | Female nut G 7/8 INT RH |
| Hydrogen / flammables | 2 | G 5/8 **LH** | — | — |

Sources: IS 3224:2002 full text — gas table entries *"Oxygen · O₂ · non-ferrous · **G 5/8-RH** ·
1.814 · **3**"* and *"Helium · He · non-ferrous or steel · **G3/4A-RH** · 1.814 · **20**"*, plus
the outlet drawings captioned *"Outlet No. 3 Outlet Connection for Oxygen"* and *"Outlet No. 20
Outlet Connection for Argon, Nitrogen, Helium, Neon, Krypton and Xenon"*
([law.resource.org PDF](https://law.resource.org/pub/in/bis/S08/is.3224.2002.pdf) ·
[archive.org text](https://archive.org/stream/gov.in.is.3224.2002/is.3224.2002_djvu.txt)).
Cross-checked against [AIGA 098/17 §8 table](https://asiaiga.org/uploaded_docs/en_AIGA_098-17_Ref_Guide_for_Industrial_Gas_Cyl_Valve_Outlet_Connections.pdf)
(IS 3224 column: O₂ = 3 / G 5/8 RH; He = 20 / G 3/4A RH) and against a live Indian valve maker's
product page — Aims Oxygen Pvt Ltd's argon/nitrogen/helium valve states outlet **"G ¾ EXT – RH
(BSP ¾)"**, working pressure 200 kgf/cm², to IS 3224:2002
([aopl.net.in](https://aopl.net.in/allied-product/cylinder-valve/argon-nitrogen-helium-valve/)).
Note that under BS 341 (Singapore/Malaysia/Bangladesh/Sri Lanka) helium *does* share the No. 3
5/8 in BSP outlet with oxygen — which is likely where the schedule's assumption came from — but
that is not the Indian arrangement.

**Consequences for the build.** The four O₂/fill whips and the O₂ cascade pigtails take a 5/8 in
BSP RH male bullnose union; the helium pigtails take a **3/4 in BSP RH female nut**. Both nut +
nipple sets are ordinary Indian catalogue items (§2, Cryo Gas Engineers row), so this is a
specification change, not a sourcing problem. Also note AIGA's standing advice that **adaptors
between outlets defeat the purpose of the keying** and should be used only under a reviewed,
permitted control — relevant if anyone proposes a He→O₂ adaptor to simplify the pigtail set.
Cylinder working pressure is worth confirming separately: the Indian valves found here are
150–200 kgf/cm² class, whereas the panel is designed for 300 bar.

## 4. RFQ shortlist

1. **Swagelok Bangalore** (Doddanakkundi Ind. Area, Bengaluru 560048 — covers South/North India)
   **or Swagelok Bombay** (Swagelok House, Baner, Pune 411045 — covers West/East India). Ask for:
   5 × `SS-1RS4-SC11` (flag the 344 vs 414 bar question and ask whether a 6000 psi panel-mountable
   regulating-stem alternative exists); 4 × `SS-CHS4-1-SC11`; 1 × R3A relief `SS-4R3A5` with
   spring **F** factory-set to 220 bar, `-SC11` — and ask explicitly whether `-SET`, spring
   designator and `-SC11` combine in one ordering number; ¼ in tube fittings `-SC11`; ¼ × 0.065 in
   316 SS seamless tube; and whether the ASSC can supply hose assemblies cleaned to SC-11.
2. **Parker Hannifin India Pvt Ltd**, Mahape, Navi Mumbai (Instrumentation Products Division).
   Same schedule as a competing quote; ask which cleaning standard their "oxygen clean" option
   certifies to (ASTM G93 level, or CGA G-4.1) and whether a 6000 psi panel-mount regulating
   needle valve exists in the IPD range.
3. **Astec Valves & Fittings Pvt Ltd**, Andheri West, Mumbai. Indian-made 6000 psi needle, check
   and relief valves. Key questions: 316 SS wetted parts, PTFE/FKM seals, **do they offer O₂
   cleaning and degreasing to ASTM G93 Level C**, panel-mount option, and a relief valve
   adjustable around 220 bar. Best domestic fallback if imported lead times bite.
4. **Hydroflex Pipe Pvt Ltd**, Jetalpur, Ahmedabad (Plot 230-A, NH-8). 4 × 1.5 m whip assemblies
   and 5 × 0.9 m cascade pigtails in DN6 400 bar corrugated 316L/304-braid. Must specify: O₂
   degreasing to ASTM G93, DIN 232 G5/8 fill adaptor (one with bleed screw), **5/8 in BSP RH
   bullnose nut + nipple for the O₂ pigtails and 3/4 in BSP RH female nut for the helium
   pigtails**, and a test certificate per assembly.
5. **Cryo Gas Engineers India**, Noida (Gas Manifold & Accessories Division). Bullnose nut and
   nipple sets — 5/8 in for O₂ and 3/4 in for inert gases per IS 3224 outlets 3 and 20 — plus
   ¼ in NPT adaptors. Ask for brass vs SS 316 and whether they degrease for O₂ service. Also a
   second-source quote for the 3-inlet and 2-inlet cascade manifold bars.
6. **Unique Pipeline Projects** and **JK Subsea** for the manifold bars. State the requirement as
   **300 bar working / ≥414 bar design**, since their published headers are 240–300 bar; ask
   whether they will machine SS 316 bar stock to a higher rating and supply ¼ in NPT ports
   O₂-clean.
7. **Stäubli Tec-Systems India Pvt Ltd**, Yelahanka New Town, Bengaluru 560064. Quick couplings.
   Ask for the **ROX** family for the two oxygen ports (their own literature rules RBL out above
   725 psi for O₂) and **RBL06** for helium/air; confirm 400 bar, per-gas keying, and whether any
   variant vents residual pressure on disconnect — the RBL brochure does not claim it.
8. **WEH GmbH, Illertissen, Germany — direct import.** There is no Indian entity. Ask WEH for the
   *filling* connector family rated ≥400 bar with integrated bleed (TW17 is a 350 bar test
   connector and does not meet the spec), O₂-clean versions, per-gas keying, and their nominated
   agent for India plus HS code and lead time.

**Open items to close before ordering:** (a) confirm the actual outlet fitted to the specific
helium and oxygen cylinders the site will receive, physically, rather than relying on the
standard; (b) decide 344 bar vs 414 bar for the needle valves; (c) get a written oxygen-cleaning
standard from every Indian supplier, since none publishes one; (d) confirm whether a certified
(ASME/PED) relief device is required rather than the proportional R3A.

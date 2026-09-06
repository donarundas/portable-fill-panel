/* Portable fill station — bill of quantities, single source of truth.
 *
 * Loaded as a plain script (no module, so it works from file:// too) by:
 *   boq.html    the working sheet where quotes are entered
 *   index.html  the dashboard, which summarises it
 *
 * Every price carries its provenance, because mixing the two silently would be a lie:
 *   src 'quote'   a vendor's written offer against an RFQ reference — a real number
 *   src 'listing' a catalogue or marketplace price — indicative, not offered to us. Case N Foam
 *                 answered PFS-2609-12 by pointing at their own catalogue rather than quoting, so
 *                 their price is theirs but still carries no validity or terms.
 * A line with no price in `quotes` is simply not priced yet, and is counted as such.
 *
 * The vendor selected on a line is the cheapest one that has a price. A vendor answer
 * entered by hand (or held in the shared store) always wins over that default.
 */
(function (root) {
  'use strict';

  const VENDORS = {
    FAV:   'FAV (Mumbai)',        SWB:  'Swagelok Bangalore', SWM:   'Swagelok Bombay',
    HYD:   'Hydroflex Pipe',      WIKA: 'WIKA India',         YAS:   'Yashtec / KELLER',
    USUN:  'USUN',                MAX:  'Maximator India',    CRYO:  'Cryo Gas Engineers',
    PELI:  'Peli / Pelican',      CNF:  'Case N Foam',        AMZ:   'Amazon.in listing',
    LOCAL: 'Local machine shop',  OWN:  'Own stock',          WEH:   'WEH (comparison)',
  };

  const RFQ = {
    SWB: 'PFS-2609-01', SWM: 'PFS-2609-02', FAV: 'PFS-2609-03', HYD:  'PFS-2609-04',
    WIKA:'PFS-2609-05', YAS: 'PFS-2609-06', WEH: 'PFS-2609-07', USUN: 'PFS-2609-08',
    CRYO:'PFS-2609-09', PELI:'PFS-2609-10', MAX: 'PFS-2609-11', CNF:  'PFS-2609-12',
  };

  const SECTIONS = [
    { id: 'A', title: 'Panel valves',                   dwg: 'BSD-PFS-001 · 002' },
    { id: 'B', title: 'Fittings and tube',              dwg: 'BSD-PFS-001 · 002 · 003' },
    { id: 'C', title: 'Instruments',                    dwg: 'BSD-PFS-001' },
    { id: 'D', title: 'Hoses and cylinder connections', dwg: 'BSD-PFS-002' },
    { id: 'E', title: 'Case and plate',                 dwg: 'BSD-PFS-003' },
    { id: 'F', title: 'Booster and drive',              dwg: 'BSD-PFS-001' },
    { id: 'G', title: 'Cleaning and consumables',       dwg: 'assembly notes' },
  ];

  /* FAV's written offer, thread PFS-2609-03, 2026-09-04: ex-works Mumbai, GST 18 % extra,
     25 working days, advance payment, validity not stated. */
  const FAVQ = (price, note) => ({ price: price, src: 'quote', lead: 25, on: '2026-09-04', note: note || 'FAV quote PFS-2609-03, ex-works Mumbai' });

  const ITEMS = [
    { id: 'nv', s: 'A', item: 'Needle valve ¼ in, panel-mount, 316 SS', tags: 'NV-01..05 · V-01 · V-11 · V-21 · V-31',
      spec: 'FAV FNV/MF/HP/02 10 000 psi (stem type to confirm) or Swagelok SS-1RS4 regulating stem 344 bar',
      qty: 9, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'],
      quotes: { FAV: FAVQ(2275, 'FAV quote PFS-2609-03; confirmed 2026-09-05 as the panel-mount type. Stem type, Cv, seat and packing materials and the panel hole size are still unanswered') } },
    { id: 'cv', s: 'A', item: 'Check valve ¼ in NPT M×F, 6000 psi', tags: 'CV-01..04 · CV-11..13 · CV-21..22 · CV-31',
      spec: 'FAV FAVCV/MF/04 (≈10 psi crack, Viton) or Swagelok SS-CHS4-1 (1 psig)',
      qty: 10, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'],
      quotes: { FAV: FAVQ(1865, 'FAV quote; confirmed 2026-09-05: Viton O-ring, cracking pressure stays at 10 psi — they will try lower but do not commit') } },
    { id: 'psv', s: 'A', item: 'Relief valve ¼ in, set 220 bar', tags: 'PSV-01',
      spec: 'Swagelok SS-4R3A5 + spring F (206–275 bar) or FAV FRV ¼ in; plus one spare spring',
      qty: 1, unit: 'ea', vendors: ['SWB', 'SWM', 'FAV'], quotes: {} },
    { id: 'qcs', s: 'A', item: 'Quick coupling socket ¼ in NPT F, double-check', tags: 'QC-01..06',
      spec: 'FAV FDQRCO2, 316 SS, 6000 psi; seals swapped to FKM in-house',
      qty: 6, unit: 'ea', vendors: ['FAV', 'WEH'], quotes: {} },
    { id: 'qcp', s: 'A', item: 'Quick coupling plug ¼ in NPT F', tags: 'QC-01P..06P + 4 spares',
      spec: 'FAV FDQRCO2 plug half', qty: 10, unit: 'ea', vendors: ['FAV', 'WEH'], quotes: {} },
    { id: 'qcc', s: 'A', item: 'Dust caps for sockets and plugs', tags: '—',
      spec: 'one set covering all halves', qty: 1, unit: 'set', vendors: ['FAV'], quotes: {} },

    { id: 'tee', s: 'B', item: 'Union tee ¼ in OD', tags: 'panel manifold ×8 · cascade chains ×5',
      spec: '316 SS, 6000 psi (FAV FCF/UT/4I or Swagelok SS-400-3)',
      qty: 13, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'], quotes: { FAV: FAVQ(683) } },
    { id: 'union', s: 'B', item: 'Straight union ¼ in OD', tags: '—', spec: '316 SS, 6000 psi',
      qty: 10, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'], quotes: { FAV: FAVQ(387) } },
    { id: 'elbow', s: 'B', item: 'Elbow union ¼ in OD', tags: '—', spec: '316 SS, 6000 psi',
      qty: 10, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'], quotes: { FAV: FAVQ(587) } },
    { id: 'mc', s: 'B', item: 'Male connector ¼ in OD × ¼ in NPT M', tags: 'valve and gauge ports',
      spec: '316 SS, 6000 psi', qty: 20, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'], quotes: { FAV: FAVQ(288) } },
    { id: 'bhu', s: 'B', item: 'Bulkhead union ¼ in OD, tube × tube', tags: 'VB-01 vent through the case wall',
      spec: 'FAV FCF/BU/4I or Swagelok SS-400-61', qty: 1, unit: 'ea', moq: 5, vendors: ['FAV', 'SWB', 'SWM'],
      quotes: { FAV: FAVQ(755, 'FAV quoted tube × ¼ NPT M, minimum order 5; the tube × tube type was asked in the follow-up') } },
    { id: 'bha', s: 'B', item: 'Bulkhead adaptor ¼ in NPT M × F, through-plate', tags: 'under QC-01..06',
      spec: '316 SS, 6000 psi; mounts the FDQRCO2 sockets through the 4 mm plate',
      qty: 6, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'], quotes: {} },
    { id: 'ga', s: 'B', item: 'Gauge adaptor ¼ in NPT M × G¼ F', tags: 'PI-01..04', spec: '316 SS',
      qty: 4, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'], quotes: {} },
    { id: 'pi4a', s: 'B', item: 'Bulkhead adaptor for the digital gauge', tags: 'PI-04',
      spec: 'G¼ gauge through the 4 mm plate', qty: 1, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'], quotes: {} },
    { id: 'plug', s: 'B', item: 'Tube plug ¼ in OD', tags: '—', spec: '316 SS',
      qty: 6, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'], quotes: { FAV: FAVQ(283) } },
    { id: 'cap', s: 'B', item: 'Tube cap ¼ in OD', tags: 'incl. 3 cascade chain end caps', spec: '316 SS',
      qty: 9, unit: 'ea', vendors: ['FAV', 'SWB', 'SWM'], quotes: { FAV: FAVQ(335, 'FAV quote; they priced 6, we need 9') } },
    { id: 'tube', s: 'B', item: 'Tube ¼ in OD × 0.065 in wall, 316/316L seamless', tags: 'panel runs',
      spec: 'ASTM A269, degreased before assembly', qty: 6, unit: 'm', vendors: ['SWB', 'SWM', 'FAV'], quotes: {} },

    { id: 'pi', s: 'C', item: 'Supply gauge 63 mm, 0–400 bar, dry, oxygen version', tags: 'PI-01 · PI-02 · PI-03',
      spec: 'WIKA 232.50 NS 63, centre-back, G¼B, class 1.6, U-clamp bracket, "USE NO OIL" dial',
      qty: 3, unit: 'ea', vendors: ['WIKA'], quotes: {} },
    { id: 'pi4', s: 'C', item: 'Digital master gauge 0–400 bar', tags: 'PI-04',
      spec: 'WIKA CPG1500 (oxygen option) or KELLER LEO5', qty: 1, unit: 'ea', vendors: ['WIKA', 'YAS'], quotes: {} },

    { id: 'whip', s: 'D', item: 'Supply whip 1.5 m, ¼ in NPT M both ends', tags: 'W-01 · W-02 · W-03',
      spec: 'DN6 SS-braid, 400 bar WP, oxygen-clean', qty: 3, unit: 'ea', vendors: ['HYD', 'FAV'], quotes: {} },
    { id: 'fwhip', s: 'D', item: 'Fill whip 1.5 m with DIN 232 handwheel and bleed screw', tags: 'W-04',
      spec: 'DN6 SS-braid, 400 bar WP, oxygen-clean', qty: 1, unit: 'ea', vendors: ['HYD'], quotes: {} },
    { id: 'pig', s: 'D', item: 'Pigtail 0.6 m, ¼ in NPT M × IS 3224 cylinder end',
      tags: 'P-11..13 (No. 3) · P-21..22 (No. 20) · P-31 (No. 19)',
      spec: 'DN6 SS-braid, 400 bar WP, oxygen-clean; cylinder ends per gas', qty: 6, unit: 'ea', vendors: ['HYD'], quotes: {} },
    { id: 'link', s: 'D', item: 'Link hose 0.4 m, ¼ in NPT M both ends', tags: 'cascade chains',
      spec: 'DN6 SS-braid, 400 bar WP, oxygen-clean', qty: 3, unit: 'ea', vendors: ['HYD', 'FAV'], quotes: {} },
    { id: 'nut3', s: 'D', item: 'IS 3224 outlet No. 3 nut + nipple, G5/8 RH bullnose (oxygen)', tags: 'incl. 1 spare',
      spec: 'brass, ¼ in NPT M outlet, oxygen-clean', qty: 4, unit: 'set', vendors: ['CRYO', 'HYD'], quotes: {} },
    { id: 'nut20', s: 'D', item: 'IS 3224 outlet No. 20 nut + nipple, G3/4 RH (helium)', tags: 'incl. 1 spare',
      spec: 'brass, female nut for the male valve outlet', qty: 3, unit: 'set', vendors: ['CRYO', 'HYD'], quotes: {} },
    { id: 'nut19', s: 'D', item: 'IS 3224 outlet No. 19 nut + nipple, G7/8 RH (air)', tags: 'incl. 1 spare',
      spec: 'brass', qty: 2, unit: 'set', vendors: ['CRYO', 'HYD'], quotes: {} },

    { id: 'case', s: 'E', item: 'Hard case, interior ≈ 470 × 360 × 195 mm', tags: 'Pelican 1550 or Case N Foam EW/MAX',
      spec: 'waterproof, one Ø11.5 vent hole in the back wall', qty: 1, unit: 'ea', vendors: ['CNF', 'PELI', 'AMZ'],
      quotes: {
        CNF: { price: 5500, src: 'listing', on: '2026-09-05', note: 'EW4920: interior 490 × 362 × 195, base 149, lid 46 — the drop-in for the Pelican 1550, whose 149 mm base BSD-PFS-003 is dimensioned around, so no change to the standoffs or the section. Case N Foam answered PFS-2609-12 with five models but no quotation, so this is their own catalogue price: GST extra, free shipping, no validity. EW4820-W is ₹3,750 and also fits (480 × 370 × 200) but its 162 mm base drops the plate to 43 below the rim, which changes the GA — worth ₹1,750 only if that redraw is wanted. EW4820 is ₹5,480 with 5 mm width clearance. MAX505 (350 wide) and MAX465H220 (335 wide) do not fit a 350 mm plate at all' },
        AMZ: { price: 42000, src: 'listing', on: '2026-09-04', note: 'Pelican 1550 with foam on Amazon.in, incl. tax — the imported original, eleven times the local case' },
      } },
    { id: 'plate', s: 'E', item: 'Panel plate 460 × 350 × 4 mm aluminium', tags: '—',
      spec: '5052-H32 / 6061-T6, R10, anodised, laser-engraved, paint-filled bands', qty: 1, unit: 'ea', vendors: ['LOCAL'], quotes: {} },
    { id: 'base', s: 'E', item: 'Base plate 440 × 330 × 3 mm aluminium', tags: '—', spec: '4 × M6 bosses',
      qty: 1, unit: 'ea', vendors: ['LOCAL'], quotes: {} },
    { id: 'stand', s: 'E', item: 'Standoff Ø16 × 112 mm aluminium, M6 both ends', tags: '—', spec: '',
      qty: 4, unit: 'ea', vendors: ['LOCAL'], quotes: {} },
    { id: 'fast', s: 'E', item: 'M6 × 12 A4 stainless cap screws with washers', tags: '—', spec: '',
      qty: 8, unit: 'ea', vendors: ['LOCAL'], quotes: {} },
    { id: 'lid', s: 'E', item: 'Lid organiser', tags: '—', spec: 'foam or nylon, pockets for 4 whips and the pigtail sets',
      qty: 1, unit: 'ea', vendors: ['CNF', 'PELI', 'LOCAL'], quotes: {} },

    { id: 'bst', s: 'F', item: 'Oxygen booster', tags: 'BST-01',
      spec: 'USUN XBD30-OL with hoses and seal kit; the air-drive filter/regulator is sourced locally. Maximator India as the no-import alternative',
      qty: 1, unit: 'ea', vendors: ['USUN', 'MAX'],
      quotes: { USUN: { price: 136880, src: 'quote', lead: null, on: '2026-09-04',
        note: 'USUN quote PFS-2609-08: USD 1450 DAP India by FedEx — booster 1250, oxygen-clean hose set 120, spare seal kit 80. Converted at ₹94.4/USD on 2026-09-04. Indian customs duty and IGST are on top: DAP does not clear customs. No drive kit and no case offered; GB40-OL-F quoted at USD 2250 for comparison. Seals are UHMWPE, not the PTFE we asked for. Stall curve still not supplied' } } },
    { id: 'reg', s: 'F', item: 'Drive-gas regulator (scuba first stage) and drive cylinder', tags: 'R-01',
      spec: 'own equipment, intermediate pressure set ≈7 bar', qty: 1, unit: 'ea', vendors: ['OWN'], quotes: {} },

    { id: 'lube', s: 'G', item: 'Oxygen-compatible lubricant', tags: '—',
      spec: 'Krytox GPL 205 or Christo-Lube MCG 111, 57 g', qty: 1, unit: 'tube', vendors: ['LOCAL'], quotes: {} },
    { id: 'oring', s: 'G', item: 'FKM O-ring kits for valves and couplings', tags: '—',
      spec: 'per FAV / Swagelok part lists', qty: 1, unit: 'lot', vendors: ['FAV', 'SWB'], quotes: {} },
    { id: 'clean', s: 'G', item: 'Cleaning consumables', tags: '—',
      spec: 'lint-free wipes, degreaser, UV lamp, bags and caps', qty: 1, unit: 'lot', vendors: ['LOCAL'], quotes: {} },
  ];

  const STATUSES = ['RFQ sent', 'Quoted', 'Ordered', 'Received', 'Not needed'];

  /* Where each RFQ stands, from sourcing/RFQ-LOG.md. A reply is not the same as a quotation:
     Case N Foam sent model links, Yashtec asked for our GST details first. */
  const REPLIES = {
    FAV:  { kind: 'quoted',  on: '2026-09-04', note: 'quoted 9 lines; 11 more are still unpriced, the quick disconnects among them — their offer went out an hour before our coupling addendum arrived. Water testing confirmed acceptable on 2026-09-06 and the revised quote chased' },
    USUN: { kind: 'quoted',  on: '2026-09-04', note: 'quoted USD 1450 DAP India; no stall curve available' },
    CNF:  { kind: 'partial', on: '2026-09-05', note: 'five models offered with no quotation; prices taken from their catalogue' },
    YAS:  { kind: 'partial', on: '2026-09-04', note: 'asked for company and GST details before quoting; supplied the same day' },
  };

  const byId = {};
  ITEMS.forEach((i) => { byId[i.id] = i; });

  /* The quantity actually bought: a minimum order overrides the drawing quantity. */
  function orderQty(it) { return it.moq && it.moq > it.qty ? it.moq : it.qty; }

  /* The cheapest vendor that has a price on this line, or null if nothing is priced.
     Ties go to the first vendor in the item's own preference order. */
  function cheapest(it) {
    let best = null;
    (it.vendors || []).concat(Object.keys(it.quotes || {})).forEach((v) => {
      const q = it.quotes && it.quotes[v];
      if (!q || q.price == null) return;
      if (!best || q.price < best.price) best = { vendor: v, price: q.price, src: q.src, lead: q.lead ?? null, note: q.note || '' };
    });
    return best;
  }

  /* What a line looks like before anyone has touched it. */
  function defaults(it) {
    const best = cheapest(it);
    if (it.vendors[0] === 'OWN') return { vendor: 'OWN', price: null, lead: null, status: 'Not needed', note: '' };
    if (!best) return { vendor: it.vendors[0], price: null, lead: null, status: 'RFQ sent', note: '' };
    return {
      vendor: best.vendor, price: best.price, lead: best.lead,
      status: best.src === 'quote' ? 'Quoted' : 'RFQ sent', note: best.note,
    };
  }

  /* One line, defaults overlaid with whatever has been entered. */
  function line(id, state) {
    const it = byId[id];
    return Object.assign({}, defaults(it), (state && state[id]) || {});
  }

  function lineTotal(it, state) {
    const r = line(it.id, state);
    if (r.status === 'Not needed' || r.price == null) return null;
    return r.price * orderQty(it);
  }

  /* Everything the dashboard shows, computed rather than typed. */
  function summary(state, gstPct) {
    const gst = 1 + (gstPct == null ? 18 : gstPct) / 100;
    let ex = 0, priced = 0, quoted = 0, listed = 0, skipped = 0, awaiting = 0, lead = 0;
    const byVendor = {}, bySection = {};
    ITEMS.forEach((it) => {
      const r = line(it.id, state), lt = lineTotal(it, state);
      if (r.status === 'Not needed') { skipped++; return; }
      if (lt == null) { awaiting++; return; }
      priced++; ex += lt;
      byVendor[r.vendor] = (byVendor[r.vendor] || 0) + lt;
      bySection[it.s] = (bySection[it.s] || 0) + lt;
      const q = it.quotes && it.quotes[r.vendor];
      if (r.status === 'Quoted' || r.status === 'Ordered' || r.status === 'Received' || (q && q.src === 'quote')) quoted++;
      else listed++;
      if (r.lead) lead = Math.max(lead, r.lead);
    });
    const vendorsAsked = new Set();
    ITEMS.forEach((it) => it.vendors.forEach((v) => { if (RFQ[v]) vendorsAsked.add(v); }));
    return {
      lines: ITEMS.length, priced: priced, awaiting: awaiting, skipped: skipped,
      quoted: quoted, listed: listed,
      ex: ex, gstPct: gstPct == null ? 18 : gstPct, inc: ex * gst,
      leadDays: lead, vendorsAsked: vendorsAsked.size,
      byVendor: byVendor, bySection: bySection,
    };
  }

  /* Prices entered in the browser, when the shared store is not reachable. */
  const LS_KEY = 'pfs-boq-v1';
  function localState() {
    try { return JSON.parse(localStorage.getItem(LS_KEY) || '{}'); } catch (e) { return {}; }
  }

  root.PFS_BOQ = {
    VENDORS: VENDORS, RFQ: RFQ, SECTIONS: SECTIONS, ITEMS: ITEMS, STATUSES: STATUSES, byId: byId,
    REPLIES: REPLIES, LS_KEY: LS_KEY, localState: localState,
    orderQty: orderQty, cheapest: cheapest, defaults: defaults, line: line, lineTotal: lineTotal, summary: summary,
  };
})(window);

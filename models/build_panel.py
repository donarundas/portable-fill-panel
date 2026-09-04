"""Portable fill panel (BSD-PFS-003) — parametric Blender build.
Run phase by phase from the MCP bridge:  exec(open(PATH).read()); run('case')  …
Units: Blender metres; all design numbers below are millimetres (MM = 0.001).
Plate datum (GA): x to the right, y towards the operator. Blender: X right, +Y = back (away from operator), Z up.
"""
import bpy, bmesh, math
from mathutils import Vector, Matrix

MM = 0.001
PLATE_W, PLATE_D, PLATE_T = 460, 350, 4
FLOOR_T, WALL_T, BODY_IN_H, LID_IN_H = 10, 26, 149, 44
CASE_IN_X, CASE_IN_Y = 473, 360
CASE_EX_X, CASE_EX_Y = CASE_IN_X + 2*WALL_T, CASE_IN_Y + 2*WALL_T          # 525 × 412
BODY_H = FLOOR_T + BODY_IN_H                                             # 159
LID_H = LID_IN_H + 11                                                    # 55
BASE_T, STANDOFF_H = 3, 112
PLATE_TOP = FLOOR_T + BASE_T + STANDOFF_H + PLATE_T                      # 129
OUT_DIR = '/Users/donarundas/Projects/gas_fill_station/design/portable'

def P(x_ga, y_ga, z_mm):
    """GA plate coordinates (mm) → Blender world (m)."""
    return ((x_ga - PLATE_W/2) * MM, (PLATE_D/2 - y_ga) * MM, z_mm * MM)

# ---------------------------------------------------------------- materials
def mat(name, color, metallic=0.0, roughness=0.5, emission=None, transmission=0.0, alpha=1.0, specular=None):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*color, 1.0)
    b.inputs['Metallic'].default_value = metallic
    b.inputs['Roughness'].default_value = roughness
    if transmission:
        b.inputs['Transmission Weight'].default_value = transmission
        b.inputs['IOR'].default_value = 1.5
    if emission:
        b.inputs['Emission Color'].default_value = (*emission, 1.0)
        b.inputs['Emission Strength'].default_value = 4.0
    if alpha < 1.0:
        b.inputs['Alpha'].default_value = alpha
        try: m.surface_render_method = 'BLENDED'
        except Exception: pass
        try: m.blend_method = 'BLEND'
        except Exception: pass
    return m

def materials():
    return dict(
        case=mat('CasePlastic', (0.035, 0.037, 0.04), 0.0, 0.78),
        rubber=mat('Rubber', (0.02, 0.02, 0.022), 0.0, 0.9),
        foam=mat('Foam', (0.09, 0.095, 0.1), 0.0, 1.0),
        plate=mat('AnodisedAl', (0.60, 0.62, 0.65), 0.85, 0.42),
        steel=mat('Stainless', (0.82, 0.83, 0.84), 1.0, 0.22),
        steel_dull=mat('StainlessDull', (0.6, 0.62, 0.64), 1.0, 0.45),
        brass=mat('Brass', (0.85, 0.62, 0.30), 1.0, 0.35),
        black=mat('BlackPhenolic', (0.03, 0.03, 0.033), 0.0, 0.45),
        o2=mat('O2Green', (0.03, 0.42, 0.14), 0.0, 0.45),
        he=mat('HeBrown', (0.42, 0.22, 0.08), 0.0, 0.45),
        air=mat('AirBlue', (0.05, 0.16, 0.72), 0.0, 0.45),
        mix=mat('MixBlack', (0.06, 0.07, 0.09), 0.0, 0.5),
        white=mat('DialWhite', (0.95, 0.95, 0.94), 0.0, 0.55),
        red=mat('NeedleRed', (0.75, 0.05, 0.05), 0.0, 0.5),
        ink=mat('EngravedInk', (0.06, 0.07, 0.09), 0.0, 0.6),
        glass=mat('Glass', (1, 1, 1), 0.0, 0.03, transmission=1.0, alpha=0.25),
        screen=mat('Screen', (0.02, 0.05, 0.03), 0.1, 0.3),
        lcd=mat('LCDGreen', (0.4, 1.0, 0.55), 0.0, 0.5, emission=(0.45, 1.0, 0.6)),
        hose=mat('Hose', (0.04, 0.045, 0.05), 0.0, 0.85),
        cyl=mat('CylinderSteel', (0.22, 0.24, 0.27), 0.7, 0.4),
        ground=mat('Ground', (0.86, 0.88, 0.9), 0.0, 1.0),
    )

M = None
def link(o, parent=None):
    if o.name not in bpy.context.collection.objects: bpy.context.collection.objects.link(o)
    if parent: o.parent = parent
    return o

def empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.get(name)
    if not e:
        e = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(e)
    e.location = loc
    return e

def apply_scale(o):
    o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.select_set(False)

def box(name, sx, sy, sz, loc, m, parent=None, bevel=0.0, segs=3):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.active_object; o.name = name
    o.scale = (sx * MM, sy * MM, sz * MM); apply_scale(o)
    if bevel:
        md = o.modifiers.new('bevel', 'BEVEL'); md.width = bevel * MM; md.segments = segs; md.limit_method = 'ANGLE'; md.angle_limit = math.radians(40)
    o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def cyl(name, r, h, loc, m, parent=None, axis='Z', verts=64, bevel=0.0):
    rot = {'Z': (0, 0, 0), 'Y': (math.pi/2, 0, 0), 'X': (0, math.pi/2, 0)}[axis]
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r * MM, depth=h * MM, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name; o.data.materials.append(m)
    if bevel:
        md = o.modifiers.new('bevel', 'BEVEL'); md.width = bevel * MM; md.segments = 2; md.limit_method = 'ANGLE'; md.angle_limit = math.radians(40)
    if parent: o.parent = parent
    return o

def hexnut(name, r, h, loc, m, parent=None):
    return cyl(name, r, h, loc, m, parent, verts=6, bevel=0.6)

def boolean_cut(target, cutter):
    md = target.modifiers.new('cut', 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.object = cutter; md.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target; target.select_set(True)
    bpy.ops.object.modifier_apply(modifier=md.name); target.select_set(False)
    bpy.data.objects.remove(cutter, do_unlink=True)

def join(objs, name):
    for o in bpy.context.selected_objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join(); j = bpy.context.active_object; j.name = name; j.select_set(False)
    return j

def text(name, body, size, loc, m, rot=(0, 0, 0), parent=None, align='CENTER', extrude=0.15):
    c = bpy.data.curves.new(name, 'FONT'); c.body = body; c.size = size * MM; c.extrude = extrude * MM
    c.align_x = align; c.align_y = 'CENTER'
    o = bpy.data.objects.new(name, c); bpy.context.collection.objects.link(o)
    o.location = loc; o.rotation_euler = rot; o.data.materials.append(m)
    if parent: o.parent = parent
    return o

# ---------------------------------------------------------------- phases
def clear_scene():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for d in list(coll):
            if d.users == 0: coll.remove(d)
    bpy.context.scene.unit_settings.system = 'METRIC'; bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'

def build_case():
    global M; M = materials()
    root = empty('Case')
    body = box('CaseBody', CASE_EX_X, CASE_EX_Y, BODY_H, (0, 0, BODY_H/2 * MM), M['case'], root, bevel=14, segs=5)
    bpy.context.view_layer.objects.active = body; body.select_set(True); bpy.ops.object.modifier_apply(modifier='bevel'); body.select_set(False)
    cutter = box('cut_in', CASE_IN_X, CASE_IN_Y, BODY_IN_H + 20, (0, 0, (FLOOR_T + (BODY_IN_H + 20)/2) * MM), M['case'])
    boolean_cut(body, cutter)
    # rim lip, latches, handle, feet, ribs
    box('RimLip', CASE_EX_X + 4, CASE_EX_Y + 4, 6, (0, 0, (BODY_H + 3) * MM), M['rubber'], root, bevel=2)
    for x in (-150, 150):
        box(f'Latch{x}', 54, 16, 44, (x * MM, -(CASE_EX_Y/2 + 6) * MM, (BODY_H - 30) * MM), M['case'], root, bevel=3)
    box('Handle', 160, 22, 24, (0, -(CASE_EX_Y/2 + 11) * MM, 80 * MM), M['rubber'], root, bevel=6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f'Foot{sx}{sy}', 60, 60, 8, (sx * (CASE_EX_X/2 - 50) * MM, sy * (CASE_EX_Y/2 - 50) * MM, -4 * MM), M['rubber'], root, bevel=3)
    for i, x in enumerate(range(-200, 201, 50)):
        box(f'Rib{i}', 10, 6, BODY_H - 30, (x * MM, -(CASE_EX_Y/2 + 3) * MM, (BODY_H/2) * MM), M['case'], root, bevel=2)
    # lid on a hinge empty at the back top edge
    hinge = empty('LidHinge', (0, (CASE_EX_Y/2) * MM, BODY_H * MM))
    lid = box('Lid', CASE_EX_X, CASE_EX_Y, LID_H, (0, -(CASE_EX_Y/2) * MM, (LID_H/2) * MM), M['case'], hinge, bevel=14, segs=5)
    bpy.context.view_layer.objects.active = lid; lid.select_set(True); bpy.ops.object.modifier_apply(modifier='bevel'); lid.select_set(False)
    lc = box('cut_lid', CASE_IN_X, CASE_IN_Y, LID_IN_H + 20, (0, -(CASE_EX_Y/2) * MM, (LID_IN_H/2 - 10) * MM), M['case'])
    boolean_cut(lid, lc)
    box('LidFoam', CASE_IN_X - 6, CASE_IN_Y - 6, 18, (0, -(CASE_EX_Y/2) * MM, 9 * MM), M['foam'], hinge)
    text('LidText', 'WHIPS · PIGTAIL SETS', 12, (0, -(CASE_EX_Y/2 + 140) * MM, 18.2 * MM), M['plate'], parent=hinge)
    # coiled supply whips stowed in the lid foam
    for i, (x, m) in enumerate(((-140, 'o2'), (0, 'he'), (140, 'air'))):
        bpy.ops.curve.primitive_bezier_circle_add(radius=70 * MM, location=(x * MM, -(CASE_EX_Y/2) * MM, 22 * MM))
        c = bpy.context.active_object; c.name = f'Coil{i}'; c.data.bevel_depth = 5 * MM; c.data.bevel_resolution = 6
        c.data.materials.append(M['hose']); c.parent = hinge
        cyl(f'CoilBand{i}', 6.5, 18, (x * MM, -(CASE_EX_Y/2 - 70) * MM, 22 * MM), M[m], hinge, axis='X', verts=24)
    hinge.rotation_euler = (math.radians(-105), 0, 0)
    return 'case ok'

def build_plate():
    root = empty('Panel')
    # base plate + standoffs
    box('BasePlate', 440, 330, BASE_T, (0, 0, (FLOOR_T + BASE_T/2) * MM), M['plate'], root, bevel=2)
    for x, y in ((14, 14), (446, 14), (14, 336), (446, 336)):
        cyl(f'Standoff_{x}_{y}', 8, STANDOFF_H, P(x, y, FLOOR_T + BASE_T + STANDOFF_H/2), M['steel_dull'], root, verts=32)
    plate = box('Plate', PLATE_W, PLATE_D, PLATE_T, (0, 0, (PLATE_TOP - PLATE_T/2) * MM), M['plate'], root, bevel=10, segs=6)
    bpy.context.view_layer.objects.active = plate; plate.select_set(True); bpy.ops.object.modifier_apply(modifier='bevel'); plate.select_set(False)
    holes = []
    def h(x, y, d): holes.append(cyl('hole', d/2, 20, P(x, y, PLATE_TOP - PLATE_T/2), M['plate'], verts=48))
    for x in (60, 135, 210): h(x, 75, 67)
    for x in (60, 135, 210, 320, 400): h(x, 185, 14.5)
    h(425, 235, 14.5); h(380, 75, 14.5)
    for x in (60, 135, 210, 285, 360, 435): h(x, 290, 14.5)
    for x, y in ((14, 14), (446, 14), (14, 336), (446, 336)): h(x, y, 6.5)
    cutter = join(holes, 'holes'); boolean_cut(plate, cutter)
    # colour bands (paint-filled engraving) and MIX strip
    lab = empty('Labels')
    for x, m in ((60, 'o2'), (135, 'he'), (210, 'air')):
        box(f'Band_{m}', 12, 260, 0.4, P(x, 175, PLATE_TOP + 0.2), M[m], lab)
    box('Band_mix', 180, 10, 0.4, P(360, 323, PLATE_TOP + 0.2), M['mix'], lab)
    # vent bulkhead VB-01 through the back wall (x = 20 GA, 100 above the floor)
    vb = P(20, 0, 100); vb = (vb[0], (CASE_IN_Y/2) * MM, vb[2])
    cyl('VB01', 6, WALL_T + 40, (vb[0], vb[1] + (WALL_T/2) * MM, vb[2]), M['steel'], root, axis='Y', verts=32)
    box('VB01_deflector', 18, 10, 10, (vb[0], vb[1] + (WALL_T + 22) * MM, vb[2] - 6 * MM), M['steel_dull'], root, bevel=1)
    return 'plate ok'

def knurled_knob(name, r, h, loc, m, parent):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=48, radius1=r * MM, radius2=r * MM, depth=h * MM)
    for v in bm.verts:
        a = math.atan2(v.co.y, v.co.x); sector = int(math.floor((a + math.pi) / (2 * math.pi) * 48 + 0.5))
        if sector % 2: v.co.x *= 0.92; v.co.y *= 0.92
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.location = loc; o.parent = parent
    me.materials.append(m)
    md = o.modifiers.new('bevel', 'BEVEL'); md.width = 1.2 * MM; md.segments = 2; md.limit_method = 'ANGLE'; md.angle_limit = math.radians(40)
    return o

def gauge(tag, gas, x, y, parent):
    g = empty(f'{tag}_grp', P(x, y, PLATE_TOP)); g.parent = parent
    z0 = PLATE_TOP
    cyl(f'{tag}_case', 31.5, 34, (0, 0, (-34/2 + 7) * MM), M['steel_dull'], g).parent = g
    cyl(f'{tag}_bezel', 34.5, 7, (0, 0, 3.5 * MM), M['steel'], g, bevel=1.5)
    cyl(f'{tag}_dial', 29.5, 1.0, (0, 0, 7.2 * MM), M['white'], g)
    cyl(f'{tag}_glass', 31, 1.2, (0, 0, 9.6 * MM), M['glass'], g)
    # ticks: 0–400 bar over 270°, from 225° clockwise to −45°
    bm = bmesh.new()
    for i in range(41):
        ang = math.radians(225 - i * 270 / 40); major = (i % 5 == 0)
        r0, r1 = (19.5 if major else 22.0), 25.0
        w = 0.9 if major else 0.5
        c = math.cos(ang), math.sin(ang)
        p = [Vector(((r0 * c[0] - w * -c[1]) * MM, (r0 * c[1] - w * c[0]) * MM, 0)), Vector(((r0 * c[0] + w * -c[1]) * MM, (r0 * c[1] + w * c[0]) * MM, 0)),
             Vector(((r1 * c[0] + w * -c[1]) * MM, (r1 * c[1] + w * c[0]) * MM, 0)), Vector(((r1 * c[0] - w * -c[1]) * MM, (r1 * c[1] - w * c[0]) * MM, 0))]
        vs = [bm.verts.new(q) for q in p]; bm.faces.new(vs)
    me = bpy.data.meshes.new(f'{tag}_ticks'); bm.to_mesh(me); bm.free()
    t = bpy.data.objects.new(f'{tag}_ticks', me); bpy.context.collection.objects.link(t); t.parent = g; t.location = (0, 0, 7.85 * MM); me.materials.append(M['ink'])
    for i, lbl in enumerate(('0', '100', '200', '300', '400')):
        ang = math.radians(225 - i * 67.5)
        text(f'{tag}_n{i}', lbl, 4.2, (15.5 * math.cos(ang) * MM, 15.5 * math.sin(ang) * MM, 7.8 * MM), M['ink'], parent=g, extrude=0.05)
    text(f'{tag}_bar', 'bar', 3.6, (0, -7 * MM, 7.8 * MM), M['ink'], parent=g, extrude=0.05)
    text(f'{tag}_o2', 'USE NO OIL', 2.4, (0, -12 * MM, 7.8 * MM), M['red'], parent=g, extrude=0.05)
    # needle at zero (225°) + hub
    n = box(f'{tag}_needle', 1.2, 24, 0.6, (0, 0, 0), M['red'], g)
    n.location = (12 * math.cos(math.radians(225)) * MM, 12 * math.sin(math.radians(225)) * MM, 8.5 * MM); n.rotation_euler = (0, 0, math.radians(225 - 90))
    cyl(f'{tag}_hub', 2.2, 1.2, (0, 0, 8.5 * MM), M['ink'], g)
    return g

def needle_valve(tag, knob_mat, x, y, parent):
    g = empty(f'{tag}_grp', P(x, y, PLATE_TOP)); g.parent = parent
    hexnut(f'{tag}_nut', 11, 8, (0, 0, 4 * MM), M['steel'], g)
    cyl(f'{tag}_bonnet', 9, 28, (0, 0, (8 + 14) * MM), M['steel'], g, bevel=1)
    cyl(f'{tag}_stem', 3, 12, (0, 0, (36 + 6) * MM), M['steel_dull'], g, verts=24)
    knurled_knob(f'{tag}_knob', 19, 14, (0, 0, (42 + 7) * MM), M[knob_mat], g)
    cyl(f'{tag}_cap', 12, 1.5, (0, 0, 49.8 * MM), M['steel'], g, bevel=0.5)
    # body and side ports under the plate
    cyl(f'{tag}_body', 11, 60, (0, 0, (-PLATE_T - 30) * MM), M['steel_dull'], g, verts=32)
    cyl(f'{tag}_portL', 6.5, 30, (-17 * MM, 0, (-PLATE_T - 45) * MM), M['steel_dull'], g, axis='X', verts=24)
    cyl(f'{tag}_portR', 6.5, 30, (17 * MM, 0, (-PLATE_T - 45) * MM), M['steel_dull'], g, axis='X', verts=24)
    return g

def coupling(tag, ring_mat, x, y, parent):
    g = empty(f'{tag}_grp', P(x, y, PLATE_TOP)); g.parent = parent
    hexnut(f'{tag}_adaptor', 10, 10, (0, 0, 5 * MM), M['steel'], g)
    cyl(f'{tag}_ring', 16, 4, (0, 0, 12 * MM), M[ring_mat], g, bevel=0.8)
    cyl(f'{tag}_body', 13, 40, (0, 0, (14 + 20) * MM), M['steel'], g, bevel=1.2)
    cyl(f'{tag}_sleeve', 15.5, 16, (0, 0, (28 + 8) * MM), M['steel_dull'], g, bevel=1.2)
    cyl(f'{tag}_mouth', 9, 3, (0, 0, 55 * MM), M['black'], g)
    cyl(f'{tag}_under', 10, 26, (0, 0, (-PLATE_T - 13) * MM), M['steel_dull'], g, verts=32)
    return g

def digital_gauge(tag, x, y, parent):
    g = empty(f'{tag}_grp', P(x, y, PLATE_TOP)); g.parent = parent
    hexnut(f'{tag}_adaptor', 9, 10, (0, 0, 5 * MM), M['steel'], g)
    cyl(f'{tag}_stem', 6, 18, (0, 0, 19 * MM), M['steel'], g, verts=32)
    body = cyl(f'{tag}_body', 36, 30, (0, 0, 64 * MM), M['black'], g, axis='Y', bevel=3)
    cyl(f'{tag}_face', 30, 1.5, (0, -15.5 * MM, 64 * MM), M['screen'], g, axis='Y')
    text(f'{tag}_lcd', '0.0', 13, (0, -16.6 * MM, 68 * MM), M['lcd'], rot=(math.pi/2, 0, 0), parent=g, extrude=0.1)
    text(f'{tag}_lcd2', 'bar', 5, (0, -16.6 * MM, 56 * MM), M['lcd'], rot=(math.pi/2, 0, 0), parent=g, extrude=0.1)
    text(f'{tag}_brand', 'CPG1500', 3.2, (0, -16.6 * MM, 84 * MM), M['plate'], rot=(math.pi/2, 0, 0), parent=g, extrude=0.05)
    return g

def build_components():
    root = bpy.data.objects['Panel']
    for tag, gas, x in (('PI-01', 'o2', 60), ('PI-02', 'he', 135), ('PI-03', 'air', 210)): gauge(tag, gas, x, 75, root)
    digital_gauge('PI-04', 380, 75, root)
    for tag, m, x in (('NV-01', 'o2', 60), ('NV-02', 'he', 135), ('NV-03', 'air', 210), ('NV-04', 'mix', 320), ('NV-05', 'mix', 400)): needle_valve(tag, m, x, 185, root)
    needle_valve('V-01', 'mix', 425, 235, root)
    for tag, m, x in (('QC-01', 'o2', 60), ('QC-02', 'he', 135), ('QC-03', 'air', 210), ('QC-04', 'mix', 285), ('QC-05', 'mix', 360), ('QC-06', 'mix', 435)): coupling(tag, m, x, 290, root)
    return 'components ok'

def build_labels():
    lab = bpy.data.objects['Labels']
    def L(s, x, y, size=4.0, m='ink'): text(f'lbl_{s}', s, size, P(x, y, PLATE_TOP + 0.3), M[m], parent=lab, extrude=0.25)
    L('PORTABLE FILL STATION · MODULE A · O2 SERVICE — NO OIL · 200 bar FILL · PSV 220 bar', 230, 12, 4.6)
    for tag, gas, x in (('PI-01', 'O2', 60), ('PI-02', 'He', 135), ('PI-03', 'AIR', 210)): L(f'{tag} · {gas} SUPPLY', x, 118, 3.6)
    L('PI-04 · MASTER', 380, 118, 3.6)
    for tag, gas, x in (('NV-01', 'O2', 60), ('NV-02', 'He', 135), ('NV-03', 'AIR', 210), ('NV-04', 'DIRECT', 320), ('NV-05', 'TO BOOSTER', 400)): L(f'{tag} · {gas}', x, 212, 3.6)
    L('V-01 · BLEED', 425, 262, 3.4)
    for tag, gas, x in (('QC-01', 'O2 IN', 60), ('QC-02', 'He IN', 135), ('QC-03', 'AIR IN', 210), ('QC-04', 'BOOSTER OUT', 285), ('QC-05', 'BOOSTER IN', 360), ('QC-06', 'PRODUCT', 435)): L(f'{tag} · {gas}', x, 336, 3.4)
    L('MIX · BOOSTER LOOP & PRODUCT', 360, 313, 3.0)
    return 'labels ok'

def build_whips():
    w = empty('FillWhip')
    # fill whip: QC-06 socket → over the front rim → 3 L cylinder valve, standing front-right
    qx, qy, qz = P(435, 290, PLATE_TOP + 56)
    cx, cy = 0.44, -0.44
    pts = [(qx, qy, qz), (qx, qy - 0.03, qz + 0.09), (qx + 0.07, qy - 0.16, 0.20), (cx - 0.04, cy + 0.03, 0.40), (cx, cy, 0.50)]
    cu = bpy.data.curves.new('FillWhipCurve', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 5 * MM; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = Vector(p); bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new('FillWhipHose', cu); bpy.context.collection.objects.link(o); o.data.materials.append(M['hose']); o.parent = w
    # 3 L steel cylinder Ø100 × 480 with shoulder, valve, DIN handwheel
    c = cyl('FillCyl', 50, 430, (cx, cy, 0.215), M['cyl'], w, verts=64)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=50 * MM, location=(cx, cy, 0.43)); s = bpy.context.active_object; s.name = 'FillCylShoulder'; s.data.materials.append(M['cyl']); s.parent = w; s.scale.z = 0.6
    cyl('FillCylNeck', 14, 30, (cx, cy, 0.485), M['brass'], w, verts=32)
    box('FillCylValve', 30, 22, 34, (cx, cy, 0.512), M['brass'], w, bevel=3)
    cyl('DINWheel', 18, 8, (cx + 0.026, cy, 0.512), M['black'], w, axis='X', verts=32, bevel=1.5)
    cyl('DINBleed', 4, 12, (cx, cy - 0.016, 0.52), M['brass'], w, axis='Y', verts=16)
    text('FillCylLabel', '3 L · 232 bar · O2', 9, (cx - 0.052, cy, 0.30), M['plate'], rot=(math.pi/2, 0, -math.pi/2), parent=w, extrude=0.1)
    return 'whips ok'

def lights_cameras():
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, -8 * MM)); g = bpy.context.active_object; g.name = 'Ground'; g.data.materials.append(M['ground'])
    focus = empty('Focus', (0.02, -0.02, PLATE_TOP * MM))
    def light(name, kind, loc, energy, size=1.5):
        ld = bpy.data.lights.new(name, kind); ld.energy = energy
        if kind == 'AREA': ld.size = size; ld.shape = 'RECTANGLE'; ld.size_y = size * 0.7
        o = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(o); o.location = loc
        c = o.constraints.new('TRACK_TO'); c.target = focus; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
        return o
    light('Key', 'AREA', (-0.7, -1.0, 1.4), 900, 2.2); light('Fill', 'AREA', (1.1, -0.5, 0.9), 350, 1.6); light('Rim', 'AREA', (0.3, 1.1, 1.1), 400, 1.4)
    w = bpy.context.scene.world or bpy.data.worlds.new('World'); bpy.context.scene.world = w; w.use_nodes = True
    bg = w.node_tree.nodes.get('Background'); bg.inputs[0].default_value = (0.75, 0.78, 0.82, 1); bg.inputs[1].default_value = 0.5
    def cam(name, loc, lens=40):
        cd = bpy.data.cameras.new(name); cd.lens = lens
        o = bpy.data.objects.new(name, cd); bpy.context.collection.objects.link(o); o.location = loc
        c = o.constraints.new('TRACK_TO'); c.target = focus; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
        return o
    cam('Cam_iso', (-0.78, -0.82, 0.66), 42); cam('Cam_top', (0.0, -0.001, 1.25), 50); cam('Cam_front', (0.0, -1.25, 0.42), 45); cam('Cam_operator', (0.16, -0.72, 0.62), 40)
    sc = bpy.context.scene
    for eng in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE'):
        try: sc.render.engine = eng; break
        except Exception: pass
    try: sc.eevee.taa_render_samples = 64
    except Exception: pass
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1800, 1125, 100
    sc.render.image_settings.file_format = 'PNG'
    return f'lights+cameras ok, engine {sc.render.engine}'

def render(view):
    sc = bpy.context.scene; sc.camera = bpy.data.objects[f'Cam_{view}']
    sc.render.filepath = f'{OUT_DIR}/renders/{view}.png'
    bpy.ops.render.render(write_still=True)
    return sc.render.filepath

def convert_text_and_curves():
    dg = bpy.context.evaluated_depsgraph_get(); n = 0
    for o in [x for x in bpy.data.objects if x.type in ('FONT', 'CURVE')]:
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        new = bpy.data.objects.new(o.name + '_m', me); bpy.context.collection.objects.link(new)
        new.matrix_world = o.matrix_world.copy(); new.parent = o.parent
        if o.parent: new.matrix_parent_inverse = o.matrix_parent_inverse.copy()
        for slot in o.data.materials:
            if slot and slot.name not in [m.name for m in me.materials if m]: me.materials.append(slot)
        bpy.data.objects.remove(o, do_unlink=True); n += 1
    return f'converted {n}'

def export_glb():
    for o in bpy.data.objects: o.select_set(False)
    skip = {'Ground', 'Focus', 'Key', 'Fill', 'Rim'}
    for o in bpy.data.objects:
        if o.name in skip or o.type in ('CAMERA', 'LIGHT'): continue
        o.select_set(True)
    path = f'{OUT_DIR}/models/panel.glb'
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_yup=True, export_cameras=False, export_lights=False, export_texcoords=True, export_normals=True)
    for o in bpy.data.objects: o.select_set(False)
    import os; return f'{path} {os.path.getsize(path)//1024} KB'

def save_blend():
    bpy.ops.wm.save_as_mainfile(filepath=f'{OUT_DIR}/models/portable-fill-panel.blend'); return 'saved'

def run(phase):
    return {'clear': clear_scene, 'case': build_case, 'plate': build_plate, 'components': build_components, 'labels': build_labels,
            'whips': build_whips, 'lights': lights_cameras, 'convert': convert_text_and_curves, 'export': export_glb, 'save': save_blend}[phase]()

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
    # Cam_top is offset 120 mm to the front: a dead-vertical TRACK_TO camera has an undefined roll
    cam('Cam_iso', (-0.78, -0.82, 0.66), 42); cam('Cam_top', (0.0, -0.12, 1.25), 50); cam('Cam_front', (0.0, -1.25, 0.42), 45); cam('Cam_operator', (0.16, -0.72, 0.62), 40)
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
    """Text and bevelled curves → meshes for the glTF export. Parent FIRST, then set the world matrix: assigning .parent
    afterwards keeps the local transform, so a parent that is not at the origin gets added twice (on the bench pass every
    label and tube exported 760 mm above the plate). Each converted object is checked against the original world matrix."""
    dg = bpy.context.evaluated_depsgraph_get(); n = 0; bad = []
    for o in [x for x in bpy.data.objects if x.type in ('FONT', 'CURVE')]:
        orig = o.matrix_world.copy()
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        new = bpy.data.objects.new(o.name + '_m', me); bpy.context.collection.objects.link(new)
        new.parent = o.parent
        if o.parent: new.matrix_parent_inverse = o.matrix_parent_inverse.copy()
        new.matrix_world = orig
        for slot in o.data.materials:
            if slot and slot.name not in [m.name for m in me.materials if m]: me.materials.append(slot)
        bpy.data.objects.remove(o, do_unlink=True); n += 1
        bpy.context.view_layer.update()
        if max(abs(a - b) for ra, rb in zip(new.matrix_world, orig) for a, b in zip(ra, rb)) > 1e-5: bad.append(new.name)
    return f'converted {n}' + (f' — WARNING {len(bad)} objects moved during conversion: {bad[:5]}' if bad else ', all transforms preserved')

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


# =====================================================================================
# PASS 4 — under-plate piping, flow mimic, cascade sets, realism
# =====================================================================================
def D(depth_mm):
    """z (mm, absolute) at a depth below the plate top."""
    return PLATE_TOP - depth_mm

def tube(name, pts, parent, r=3.2, m=None):
    """Polyline tube through GA points (x_ga, y_ga, z_abs_mm)."""
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r * MM; cu.bevel_resolution = 4; cu.use_fill_caps = True
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for p, (x, y, z) in zip(sp.points, pts):
        wx, wy, wz = P(x, y, z); p.co = (wx, wy, wz, 1.0)
    o = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(o); o.parent = parent
    o.data.materials.append(m or M['steel']); return o

def fitting(name, x, y, z, parent, size=15):
    return box(name, size, size, size, P(x, y, z), M['steel'], parent, bevel=1.5)

def cv_body(name, x, y, z, parent, axis='Y'):
    b = cyl(name, 7.5, 40, P(x, y, z), M['steel'], parent, axis=axis, verts=24, bevel=1)
    hexnut(name + '_h1', 8.5, 8, P(x, y, z), M['steel'], parent)  # visual hex at the mid — cheap detail
    return b

def build_piping():
    """Tube runs under the plate, per BSD-PFS-001: QC → tee(PI) → NV → CV → header → NV-04/NV-05; fill line with PSV-01, V-01, PI-04, CV-04; vents to VB-01."""
    # re-orient the needle valve ports along Y (flow runs front→back in the columns)
    for o in list(bpy.data.objects):
        if o.name.endswith('_portL') or o.name.endswith('_portR'): bpy.data.objects.remove(o, do_unlink=True)
    for tag, x, y in (('NV-01', 60, 185), ('NV-02', 135, 185), ('NV-03', 210, 185), ('NV-04', 320, 185), ('NV-05', 400, 185), ('V-01', 425, 235)):
        g = bpy.data.objects[f'{tag}_grp']
        cyl(f'{tag}_portF', 6.5, 30, (0, -17 * MM, (-PLATE_T - 45) * MM), M['steel_dull'], g, axis='Y', verts=24)
        cyl(f'{tag}_portB', 6.5, 30, (0,  17 * MM, (-PLATE_T - 45) * MM), M['steel_dull'], g, axis='Y', verts=24)
    pip = empty('Piping')
    z49, z40, z68, z95 = D(49), D(40), D(68), D(95)
    for i, (x, m) in enumerate(((60, 'o2'), (135, 'he'), (210, 'air'))):
        n = f'L{i+1}'
        tube(f'{n}_qc_run', [(x, 290, D(30)), (x, 290, z49), (x, 265, z49)], pip)
        fitting(f'{n}_tee_pi', x, 265, z49, pip)
        tube(f'{n}_pi_branch', [(x, 265, z49), (x + 22, 265, z40), (x + 22, 90, z40), (x, 90, z40), (x, 75, z40), (x, 75, D(28))], pip)
        tube(f'{n}_to_nv', [(x, 265, z49), (x, 202, z49)], pip)                       # into the NV front port
        tube(f'{n}_nv_to_cv', [(x, 168, z49), (x, 150, z49)], pip)                    # out of the NV back port
        cv_body(f'CV-0{i+1}', x, 150, z49, pip, axis='Y')
        tube(f'{n}_cv_to_hdr', [(x, 150, z49), (x, 120, z49)], pip)
    # common header along y = 120 to the selector valves
    tube('HDR_manifold', [(60, 120, z49), (400, 120, z49)], pip, r=3.6)
    for x in (135, 210, 320): fitting(f'HDR_tee_{x}', x, 120, z49, pip)
    tube('HDR_to_NV04', [(320, 120, z49), (320, 168, z49)], pip)
    tube('HDR_to_NV05', [(400, 120, z49), (400, 168, z49)], pip)
    # fill line: NV-04 front port → y 250 → east to QC-06; PSV-01, CV-04 join, PI-04 branch, V-01 on it
    tube('FILL_from_NV04', [(320, 202, z49), (320, 250, z49), (435, 250, z49), (435, 290, z49), (435, 290, D(30))], pip, r=3.6)
    for x in (340, 360, 372): fitting(f'FILL_tee_{x}', x, 250, z49, pip)
    tube('PI04_branch', [(372, 250, z49), (372, 235, z40), (372, 90, z40), (380, 90, z40), (380, 75, z40), (380, 75, D(30))], pip)
    tube('QC05_to_CV04', [(360, 290, D(30)), (360, 290, z49), (360, 250, z49)], pip)
    cv_body('CV-04', 360, 270, z49, pip, axis='Y')
    # PSV-01 hanging below the fill line
    psv = empty('PSV-01_grp', P(340, 250, z49)); psv.parent = pip
    cyl('PSV-01_body', 9, 40, (0, 0, -32 * MM), M['steel'], psv, bevel=1.2)
    hexnut('PSV-01_cap', 10, 8, (0, 0, -55 * MM), M['steel'], psv)
    tube('VENT_psv', [(340, 250, D(60)), (340, 250, z95), (300, 250, z95), (300, 30, z95), (20, 30, z95), (20, 5, z95), (20, 5, D(29)), (20, -12, D(29))], pip, r=3.2, m=M['steel_dull'])
    tube('VENT_v01', [(425, 218, z49), (425, 205, z49), (425, 205, z95), (300, 205, z95)], pip, r=3.2, m=M['steel_dull'])
    fitting('VENT_tee', 300, 205, z95, pip, size=13)
    # booster loop: NV-05 front port → dive under the fill line → QC-04
    tube('BST_out', [(400, 202, z49), (400, 215, z49), (400, 215, z68), (400, 268, z68), (285, 268, z68), (285, 290, z68), (285, 290, D(30))], pip)
    # V-01 sits on the fill line: its front port is the tee
    tube('V01_stub', [(425, 250, z49), (425, 252, z49)], pip)
    return f'piping ok ({sum(1 for o in bpy.data.objects if o.parent is pip)} parts)'

def arrow_head(name, x, y, ang_deg, m, parent, L=7, Wd=5.5, z_off=0.35):
    bm = bmesh.new(); a = math.radians(ang_deg)
    def rot(px, py): return (px * math.cos(a) - py * math.sin(a), px * math.sin(a) + py * math.cos(a))
    tri = [rot(L/2, 0), rot(-L/2, Wd/2), rot(-L/2, -Wd/2)]
    vs = [bm.verts.new((tx * MM, ty * MM, 0)) for tx, ty in tri]; bm.faces.new(vs)
    bmesh.ops.solidify(bm, geom=bm.faces[:] + bm.edges[:] + bm.verts[:], thickness=0.4 * MM)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.location = P(x, y, PLATE_TOP + z_off); o.parent = parent; me.materials.append(m)
    return o

def line(name, x0, y0, x1, y1, m, parent, w=2.6):
    L = math.hypot(x1 - x0, y1 - y0); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    o = box(name, L, w, 0.5, P(cx, cy, PLATE_TOP + 0.25), m, parent)
    o.rotation_euler = (0, 0, math.atan2(-(y1 - y0), (x1 - x0)))   # GA y runs opposite to Blender Y
    return o

def build_mimic():
    """Painted flow-mimic on the plate top, drawn to the P&ID topology (BSD-PFS-001):
    inlet legs QC → NV with the gauge tap UPSTREAM of the valve (the tap loops round the knob's left side so it reads the
    supply, not the header); header NV-01/02/03 → NV-04/NV-05; fill line NV-04 → PI-04 tee → V-01 → QC-06 with the
    QC-05 return joining it; booster out NV-05 → QC-04. A crossing that is not a connection is drawn with a 12 mm gap.
    Checked with an orthographic top render (Cam_plate) and the GA-mm table in `mimic_report()`."""
    for o in list(bpy.data.objects):
        if o.name.startswith(('Band_', 'lbl_', 'mim_')) or o.name == 'Mimic': bpy.data.objects.remove(o, do_unlink=True)
    mim = empty('Mimic'); mim.location.z = TABLE_H
    lab = bpy.data.objects.get('Labels') or empty('Labels')
    # inlet columns
    for i, (x, m) in enumerate(((60, 'o2'), (135, 'he'), (210, 'air'))):
        line(f'mim_in{i}', x, 268, x, 206, M[m], mim); arrow_head(f'mim_in{i}_a', x, 240, 90, M[m], mim)     # QC → NV (towards the back)
        tx = x - 28                                                                                            # gauge tap: leg → round the knob → gauge
        line(f'mim_tap{i}a', x, 222, tx, 222, M[m], mim, w=1.4); line(f'mim_tap{i}b', tx, 222, tx, 108, M[m], mim, w=1.4); line(f'mim_tap{i}c', tx, 108, x, 108, M[m], mim, w=1.4)
        line(f'mim_hd{i}', x, 166, x, 150, M['mix'], mim)                                                     # NV outlet → header
    line('mim_header', 60, 150, 400, 150, M['mix'], mim, w=3.2)
    for x in (100, 175, 260, 350): arrow_head(f'mim_header_a{x}', x, 150, 0, M['mix'], mim)
    line('mim_to_nv04', 320, 150, 320, 166, M['mix'], mim); line('mim_to_nv05', 400, 150, 400, 166, M['mix'], mim)
    # fill line
    line('mim_fill_a', 320, 204, 320, 250, M['mix'], mim, w=3.2); line('mim_fill_b', 320, 250, 435, 250, M['mix'], mim, w=3.2); line('mim_fill_c', 435, 250, 435, 272, M['mix'], mim, w=3.2)
    for x in (340, 410): arrow_head(f'mim_fill_a{x}', x, 250, 0, M['mix'], mim)
    arrow_head('mim_fill_qc6', 435, 264, -90, M['mix'], mim)
    # PI-04 tap off the fill line up to the gauge stem; gap where it crosses the header
    line('mim_pi4a', 376, 250, 376, 158, M['mix'], mim, w=1.6); line('mim_pi4b', 376, 142, 376, 112, M['mix'], mim, w=1.6)
    line('mim_pi4c', 376, 112, 380, 112, M['mix'], mim, w=1.6); line('mim_pi4d', 380, 112, 380, 96, M['mix'], mim, w=1.6)
    # booster loop; gaps where the out line crosses the fill line (x=400) and the QC-05 return (x=360)
    line('mim_bst_a1', 400, 204, 400, 244, M['mix'], mim); line('mim_bst_a2', 400, 256, 400, 262, M['mix'], mim)
    line('mim_bst_b1', 400, 262, 366, 262, M['mix'], mim); line('mim_bst_b2', 354, 262, 285, 262, M['mix'], mim); line('mim_bst_c', 285, 262, 285, 272, M['mix'], mim)
    arrow_head('mim_bst_a1h', 320, 262, 180, M['mix'], mim); arrow_head('mim_bst_qc4', 285, 268, -90, M['mix'], mim)
    line('mim_qc5', 360, 272, 360, 250, M['mix'], mim); arrow_head('mim_qc5_a', 360, 256, 90, M['mix'], mim)
    line('mim_v01', 425, 250, 425, 242, M['mix'], mim)
    # line captions (3 mm) and equipment tags (4 mm), all placed clear of lines, knobs and neighbours — see mimic_report()
    def T(s, x, y, size, align='CENTER', extrude=0.25): text(f'lbl_{s}', s, size, P(x, y, PLATE_TOP + 0.3), M['ink'], parent=lab, extrude=extrude, align=align)
    T('MANIFOLD  ≤300 bar', 230, 143, 3.2); T('FILL LINE  200 bar', 352, 243, 3.2); T('TO BOOSTER', 302, 257, 2.8)
    T('PORTABLE FILL STATION · MODULE A · O2 SERVICE — NO OIL · 200 bar FILL · PSV 220 bar', 230, 12, 4.6)
    for tag, gas, x in (('PI-01', 'O2', 60), ('PI-02', 'He', 135), ('PI-03', 'AIR', 210)): T(f'{tag} {gas}', x, 120, 4.2)   # centred under the gauge
    T('PI-04 MASTER', 402, 120, 4.2)
    for tag, gas, x in (('NV-01', 'O2', 60), ('NV-02', 'He', 135), ('NV-03', 'AIR', 210), ('NV-04', 'DIRECT', 320), ('NV-05', 'BOOST', 400)): T(f'{tag} {gas}', x + 22, 185, 4.2, 'LEFT')
    T('V-01 BLEED', 433, 207, 3.6)
    for tag, gas, x in (('QC-01', 'O2 IN', 60), ('QC-02', 'He IN', 135), ('QC-03', 'AIR IN', 210), ('QC-04', 'BST OUT', 285), ('QC-05', 'BST IN', 360), ('QC-06', 'PRODUCT', 435)): T(f'{tag} {gas}', x, 322, 3.8)
    return 'mimic + labels ok'

def mimic_report():
    """Every label and mimic segment in GA millimetres next to the component centres — the check that caught pass 4's
    hidden gauge labels and false junctions. Returns the text; also renders Cam_plate (orthographic, straight down)."""
    from mathutils import Vector
    bpy.context.view_layer.update()          # objects created with bpy.data keep an identity matrix_world until the depsgraph runs
    def ga(v): return (round(v.x / MM + PLATE_W / 2), round(PLATE_D / 2 - v.y / MM))
    rows = []
    for o in sorted(bpy.data.objects, key=lambda o: o.name):
        if o.name.startswith('lbl_') and o.type == 'FONT':
            rows.append(f"LABEL {o.name[4:]:40.40s} GA={ga(o.matrix_world.translation)} {round(o.data.size/MM,1)}mm {o.data.align_x} w={round(o.dimensions.x/MM)}")
        elif o.name.startswith('mim_') and o.type == 'MESH':
            pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
            rows.append(f"LINE  {o.name:16s} x {round(min(p.x for p in pts)/MM+PLATE_W/2)}..{round(max(p.x for p in pts)/MM+PLATE_W/2)} y {round(PLATE_D/2-max(p.y for p in pts)/MM)}..{round(PLATE_D/2-min(p.y for p in pts)/MM)}")
    sc = bpy.context.scene; cam = bpy.data.objects.get('Cam_plate')
    if not cam:
        cd = bpy.data.cameras.new('Cam_plate'); cd.type = 'ORTHO'; cd.ortho_scale = 0.56
        cam = bpy.data.objects.new('Cam_plate', cd); sc.collection.objects.link(cam)
    cam.location = (0.0, 0.0, TABLE_H + 1.5); cam.rotation_euler = (0, 0, 0)
    old = (sc.camera, sc.render.resolution_x, sc.render.resolution_y, sc.render.filepath)
    try:
        sc.camera = cam; sc.render.resolution_x, sc.render.resolution_y = 2000, 1520
        sc.render.filepath = f'{OUT_DIR}/renders/plate-ortho.png'; bpy.ops.render.render(write_still=True)
    finally:
        sc.camera, sc.render.resolution_x, sc.render.resolution_y, sc.render.filepath = old
    return '\n'.join(rows)

def industrial_cylinder(name, wx, wy, body_mat, shoulder_mat, parent, label=None):
    """47 L industrial cylinder: Ø229 × ~1.37 m body, shoulder, neck, valve with handwheel and side outlet. Returns the outlet world point (m)."""
    g = empty(f'{name}_grp', (wx, wy, 0)); g.parent = parent
    cyl(f'{name}_body', 114.5, 1300, (0, 0, 0.66), body_mat, g, verts=64)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=114.5 * MM, location=(0, 0, 1.31)); s = bpy.context.active_object; s.name = f'{name}_shoulder'; s.data.materials.append(shoulder_mat); s.parent = g; s.scale.z = 0.55
    cyl(f'{name}_neck', 24, 40, (0, 0, 1.38), M['steel_dull'], g, verts=32)
    box(f'{name}_valve', 34, 30, 60, (0, 0, 1.43), M['brass'], g, bevel=3)
    cyl(f'{name}_wheel', 34, 12, (0, 0, 1.475), M['black'], g, verts=32, bevel=2)
    cyl(f'{name}_outlet', 9, 40, (0.03, 0, 1.42), M['brass'], g, axis='X', verts=24)     # outlet points +X (towards the case)
    hexnut(f'{name}_nut', 12, 14, (0.055, 0, 1.42), M['brass'], g)
    cyl(f'{name}_footring', 118, 18, (0, 0, 0.009), M['rubber'], g, verts=48)
    if label: text(f'{name}_lbl', label, 40, (0.116, 0, 0.95), M['plate'], rot=(math.pi/2, 0, math.pi/2), parent=g, extrude=0.3)
    return (wx + 0.075, wy, 1.42)

def hose_curve(name, pts, parent, r=5.0, m=None):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r * MM; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts): bp.co = Vector(p); bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(o); o.parent = parent; o.data.materials.append(m or M['hose']); return o

def whip_path(chain_x, last_y, chain_z, qx, qy, qz):
    """Supply whip from the chain bleed to its panel socket. On the floor: down beside the case, along the front, over the rim.
    On the bench (TABLE_H > 0): down from the bleed, sagging past the bench's front-left corner, over the front rim."""
    front = -(CASE_EX_Y / 2) * MM                                     # case front outer wall (y, m)
    if TABLE_H:
        return [(chain_x, last_y - 0.067, chain_z), (chain_x + 0.10, last_y - 0.20, chain_z - 0.28), (-0.50, -0.42, TABLE_H + 0.06),
                (qx - 0.02, -0.30, TABLE_H + 0.14), (qx, front - 0.03, TABLE_H + 0.20), (qx, qy - 0.045, qz + 0.03), (qx, qy, qz)]
    return [(chain_x, last_y - 0.067, chain_z), (chain_x + 0.05, last_y - 0.20, 1.20), (-0.36, front - 0.10, 0.10),
            (qx - 0.05, front - 0.10, 0.06), (qx, front - 0.03, 0.20), (qx, qy - 0.045, qz + 0.03), (qx, qy, qz)]

def build_cascade():
    """PM-01 (O2 ×3), PM-02 (He ×2), PM-03 (air) beside the case: bullnose pigtails → check valves → tee chain → bleed → whip to the panel."""
    casc = empty('Cascade')
    o2body = mat('CylO2Black', (0.03, 0.03, 0.032), 0.05, 0.5); white = mat('CylWhite', (0.9, 0.9, 0.88), 0.0, 0.5)
    hebody = mat('CylHeBrown', (0.30, 0.16, 0.07), 0.05, 0.5); airbody = mat('CylAirGrey', (0.20, 0.21, 0.23), 0.05, 0.5)
    sets = (
        ('PM-01', 'o2', -0.78, (0.55, 0.25, -0.05), o2body, white, 'O2', 60),
        ('PM-02', 'he', -1.14, (0.55, 0.25), hebody, hebody, 'He', 135),
        ('PM-03', 'air', -1.14, (-0.20,), airbody, M['black'], 'AIR', 210),
    )
    for tag, key, wx, ys, body, shoulder, gas, qc_x in sets:
        grp = empty(f'{tag}_grp'); grp.parent = casc
        outlets = [industrial_cylinder(f'{tag}_C{i+1}', wx, wy, body, shoulder, grp, gas) for i, wy in enumerate(ys)]
        chain_z = 1.56; chain_x = wx + 0.16
        tees = []
        for i, (ox, oy, oz) in enumerate(outlets):
            tx, ty = chain_x, oy
            hose_curve(f'{tag}_pigtail{i+1}', [(ox, oy, oz), (ox + 0.06, oy, oz + 0.02), (tx, ty - 0.02, chain_z - 0.05), (tx, ty, chain_z - 0.03)], grp, r=4.5)
            cv = cyl(f'{tag}_CV{i+1}', 7.5, 40, (tx, ty, chain_z - 0.04), M['steel'], grp, verts=24, bevel=1)
            t = box(f'{tag}_tee{i+1}', 16, 16, 16, (tx, ty, chain_z), M['steel'], grp, bevel=1.5); tees.append(t)
        for i in range(len(outlets) - 1):
            (ax, ay, _), (bx, by, _) = outlets[i], outlets[i + 1]
            hose_curve(f'{tag}_link{i+1}', [(chain_x, ay, chain_z), (chain_x + 0.04, (ay + by) / 2, chain_z + 0.06), (chain_x, by, chain_z)], grp, r=4.5)
        # cap on the first tee, bleed valve after the last, whip to the panel
        last_y = outlets[-1][1]; first_y = outlets[0][1]
        cyl(f'{tag}_cap', 8, 12, (chain_x, first_y + 0.014, chain_z), M['steel'], grp, axis='Y', verts=16)
        bl = empty(f'{tag}_bleed_grp', (chain_x, last_y - 0.05, chain_z)); bl.parent = grp
        cyl(f'{tag}_bleed_body', 8, 34, (0, 0, 0), M['steel'], bl, axis='Y', verts=24); cyl(f'{tag}_bleed_stem', 3, 18, (0, 0, 0.014), M['steel_dull'], bl, verts=16)
        knurled_knob(f'{tag}_bleed_knob', 11, 9, (0, 0, 0.028), M['black'], bl)
        hose_curve(f'{tag}_chain_to_bleed', [(chain_x, last_y, chain_z), (chain_x, last_y - 0.033, chain_z)], grp, r=4.5)
        qx, qy, qz = P(qc_x, 290, PLATE_TOP + 56)
        hose_curve(f'{tag}_whip', whip_path(chain_x, last_y, chain_z, qx, qy, qz), grp, r=5.0)
    return 'cascade ok'

def realism():
    """Brushed anodised plate, textured case plastic, softer key light; HDRI is set separately if Poly Haven is available."""
    def bump(m, scale, strength, stretch=None):
        nt = m.node_tree; b = nt.nodes.get('Principled BSDF')
        tex = nt.nodes.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = scale; tex.inputs['Detail'].default_value = 6
        bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = strength; bm.inputs['Distance'].default_value = 0.0004
        if stretch:
            mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = stretch
            tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], tex.inputs['Vector'])
        nt.links.new(tex.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    plate = bpy.data.materials['AnodisedAl']; b = plate.node_tree.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = 0.32; b.inputs['Metallic'].default_value = 0.9
    try: b.inputs['Anisotropic'].default_value = 0.6
    except Exception: pass
    bump(plate, 40.0, 0.12, (1.0, 60.0, 60.0))
    bump(bpy.data.materials['CasePlastic'], 250.0, 0.35)
    bump(bpy.data.materials['Rubber'], 120.0, 0.2)
    for n, e in (('Key', 180), ('Fill', 70), ('Rim', 90)):
        if n in bpy.data.lights: bpy.data.lights[n].energy = e
    # cameras for the new views
    focus = bpy.data.objects['Focus']
    def cam(name, loc, lens):
        if name in bpy.data.objects: return bpy.data.objects[name]
        cd = bpy.data.cameras.new(name); cd.lens = lens; o = bpy.data.objects.new(name, cd); bpy.context.collection.objects.link(o); o.location = loc
        c = o.constraints.new('TRACK_TO'); c.target = focus; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'; return o
    cf = bpy.data.objects.get('CascadeFocus') or empty('CascadeFocus', (-0.55, 0.05, 0.62))
    cc = cam('Cam_cascade', (-1.4, -2.9, 1.5), 32); cc.constraints[0].target = cf
    cam('Cam_under', (0.2, -0.95, 0.75), 40)
    return 'realism ok'

def render_under():
    """Plate, mimic and labels hidden → the piping shows."""
    hide = [bpy.data.objects[n] for n in ('Plate',) if n in bpy.data.objects] + [o for o in bpy.data.objects if o.parent and o.parent.name in ('Labels', 'Mimic')]
    for o in hide: o.hide_render = True
    try: return render('under')
    finally:
        for o in hide: o.hide_render = False

_RUN = dict(piping=build_piping, mimic=build_mimic, cascade=build_cascade, realism=realism, under=render_under)
def run(phase):  # noqa: F811 — extends the pass-1 map
    if phase in _RUN: return _RUN[phase]()
    return {'clear': clear_scene, 'case': build_case, 'plate': build_plate, 'components': build_components, 'labels': build_labels,
            'whips': build_whips, 'lights': lights_cameras, 'convert': convert_text_and_curves, 'export': export_glb, 'save': save_blend}[phase]()

# ---------------------------------------------------------------- pass 5: cylinder paint + whip drape (edits an existing scene)
def repaint_cylinders():
    """Cylinder bodies are enamel, not chrome: metallic ≈0 so black/brown/grey read under the HDRI."""
    for n, met in (('CylO2Black', 0.05), ('CylHeBrown', 0.05), ('CylAirGrey', 0.05), ('CylWhite', 0.0)):
        m = bpy.data.materials.get(n)
        if not m: continue
        b = m.node_tree.nodes.get('Principled BSDF'); b.inputs['Metallic'].default_value = met; b.inputs['Roughness'].default_value = 0.5
    bpy.data.materials['CylAirGrey'].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.20, 0.21, 0.23, 1.0)
    return 'repaint ok'

def reroute_whips():
    """Rebuild the three supply whips on the draped path (see whip_path)."""
    casc = bpy.data.objects['Cascade']; n = 0
    for tag, wx, ys, qc_x in (('PM-01', -0.78, (0.55, 0.25, -0.05), 60), ('PM-02', -1.14, (0.55, 0.25), 135), ('PM-03', -1.14, (-0.20,), 210)):
        old = bpy.data.objects.get(f'{tag}_whip')
        if old: cu = old.data; bpy.data.objects.remove(old, do_unlink=True); bpy.data.curves.remove(cu)
        grp = bpy.data.objects[f'{tag}_grp']
        qx, qy, qz = P(qc_x, 290, PLATE_TOP + 56); qz += TABLE_H
        hose_curve(f'{tag}_whip', whip_path(wx + 0.16, ys[-1], 1.56, qx, qy, qz), grp, r=5.0); n += 1
    return f'rerouted {n} whips'

def render_cascade():
    """The wide cascade view is floor-dominated and reads washed out at the panel exposure; render it 0.5 stop darker."""
    sc = bpy.context.scene; e0 = sc.view_settings.exposure
    try:
        sc.view_settings.exposure = -0.7; return render('cascade')
    finally:
        sc.view_settings.exposure = e0

_RUN.update(repaint=repaint_cylinders, whips5=reroute_whips, cascade_render=render_cascade)


# ---------------------------------------------------------------- pass 6: work bench (the case at working height)
TABLE_H = 0.76                      # bench top height (m). 0 = case on the floor (passes 1-5)
BENCH_C, BENCH_L, BENCH_W = (0.05, 0.0), 1000, 700   # bench centre (m) and top size (mm)

def reroute_fill_whip():
    """Fill whip from QC-06 over the front rim, off the bench front-right, down to the 3 L cylinder standing on the floor."""
    old = bpy.data.objects.get('FillWhipHose')
    if old: cu = old.data; bpy.data.objects.remove(old, do_unlink=True); bpy.data.curves.remove(cu)
    w = bpy.data.objects['FillWhip']
    qx, qy, qz = P(435, 290, PLATE_TOP + 56); qz += TABLE_H
    cx, cy = 0.44, -0.44
    if TABLE_H:
        pts = [(qx, qy, qz), (qx, qy - 0.03, qz + 0.09), (qx + 0.07, qy - 0.16, TABLE_H + 0.20), (qx + 0.18, -0.38, TABLE_H + 0.02), (cx + 0.02, cy - 0.10, 0.62), (cx, cy, 0.53)]
    else:
        pts = [(qx, qy, qz), (qx, qy - 0.03, qz + 0.09), (qx + 0.07, qy - 0.16, 0.20), (cx - 0.04, cy + 0.03, 0.40), (cx, cy, 0.50)]
    hose_curve('FillWhipHose', pts, w, r=5.0); return 'fill whip rerouted'

def build_bench():
    """Stainless work bench: 30 mm top, four Ø38 legs on rubber feet, aprons, lower shelf. Lifts the case assembly, its focus,
    the panel cameras and the lights by TABLE_H (cascade cylinders and the 3 L fill cylinder stay on the floor) and reroutes both whip sets."""
    if 'Bench' in bpy.data.objects: return 'bench already built'
    b = empty('Bench'); bx, by = BENCH_C; hl, hw = BENCH_L * MM / 2, BENCH_W * MM / 2
    steel = mat('BenchSteel', (0.62, 0.63, 0.65), 0.9, 0.35)
    box('Bench_top', BENCH_L, BENCH_W, 30, (bx, by, TABLE_H - 0.015), steel, b, bevel=2)
    box('Bench_apron_f', BENCH_L - 100, 30, 60, (bx, by - hw + 0.035, TABLE_H - 0.06), steel, b)
    box('Bench_apron_b', BENCH_L - 100, 30, 60, (bx, by + hw - 0.035, TABLE_H - 0.06), steel, b)
    for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1))):
        lx, ly = bx + sx * (hl - 0.05), by + sy * (hw - 0.05)
        cyl(f'Bench_leg{i+1}', 19, (TABLE_H - 0.03) * 1000, (lx, ly, (TABLE_H - 0.03) / 2), steel, b, verts=24)
        cyl(f'Bench_foot{i+1}', 22, 12, (lx, ly, 0.006), M['rubber'], b, verts=24)
    box('Bench_shelf', BENCH_L - 140, BENCH_W - 140, 20, (bx, by, 0.22), steel, b, bevel=1)
    for n in ('Case', 'LidHinge', 'Panel', 'Labels', 'Mimic', 'Piping', 'Focus', 'Cam_iso', 'Cam_top', 'Cam_front', 'Cam_operator', 'Cam_under', 'Key', 'Fill', 'Rim'):
        o = bpy.data.objects.get(n)
        if o: o.location.z += TABLE_H
    cf = bpy.data.objects.get('CascadeFocus')
    if cf: cf.location = (-0.50, 0.05, 0.85)
    cc = bpy.data.objects.get('Cam_cascade')
    if cc: cc.location = (-1.55, -3.1, 1.75)
    reroute_whips(); reroute_fill_whip()
    return 'bench ok'

_RUN.update(bench=build_bench, fillwhip=reroute_fill_whip, report=mimic_report)

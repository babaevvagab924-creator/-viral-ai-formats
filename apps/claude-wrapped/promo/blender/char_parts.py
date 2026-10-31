# Pixel Claude as police chief: solid extruded pixel parts, rendered one by one (RGBA, orthographic) for 2D rigging.
import bpy, math, sys, os, json
from mathutils import Vector
OUTD = sys.argv[1]; SAMPLES = int(sys.argv[2])
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
def mat(name, color, rough=0.4, metal=0.0, coat=0.2):
    m = bpy.data.materials.new(name); m.use_nodes = True; p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1); p.inputs["Roughness"].default_value = rough; p.inputs["Metallic"].default_value = metal; p.inputs["Coat Weight"].default_value = coat; return m
MATS = {"B": mat("orange", (0.68, 0.19, 0.1), 0.36), "U": mat("navy", (0.006, 0.01, 0.035), 0.55, coat=0.1), "G": mat("gold", (0.85, 0.55, 0.12), 0.25, metal=1.0),
        "D": mat("black", (0.008, 0.008, 0.01), 0.3, coat=0.6), "K": mat("cap", (0.005, 0.008, 0.03), 0.5), "W": mat("white", (0.85, 0.85, 0.82), 0.4)}
MATS["H"] = MATS["B"]   # hands
c = 0.075; DEPTH = 0.3
# Full grid (row 0 = top). Cap rows on top, then the user's sprite dressed in uniform.
GRID = [
    "...KKKKKK...",   # cap crown
    "..KKKKGKKK..",   # cap band with gold cockade
    "..BBBBBBBB..",   # head
    "..BEBBBBEB..",   # eyes
    "HUBBBBBBBBUH",   # face row (mouth here) + sleeves, hands
    "HUUUGUUUUUUH",   # uniform, badge
    "..UUUWUUUU..",   # uniform, white shirt V
    "..DDDGGDDD..",   # belt with buckle
    "..U.U..U.U..",   # trousers
    "..D.D..D.D..",   # shoes
]
ROWS = len(GRID); ZC = ROWS * c / 2   # centre height
def part_cells(name):
    cells = []
    for j, row in enumerate(GRID):
        for i, ch in enumerate(row):
            if ch == ".": continue
            arm = j in (4, 5) and i in (0, 1, 10, 11)
            leg = j in (8, 9)
            if name == "armL" and arm and i <= 1: cells.append((i, j, ch))
            elif name == "armR" and arm and i >= 10: cells.append((i, j, ch))
            elif name.startswith("leg") and leg and i == int(name[3:]): cells.append((i, j, ch))
            elif name == "body" and not arm and not leg: cells.append((i, j, "B" if ch == "E" else ch))
    return cells
def build(name):
    cells = part_cells(name); verts, faces, mats, vid = [], [], [], {}
    keys = sorted(set(ch for _, _, ch in cells)); idx = {k: n for n, k in enumerate(keys)}
    def V(i, j):
        if (i, j) not in vid: vid[(i, j)] = len(verts); verts.append(((i - 6) * c, 0.0, (ROWS - j) * c - ZC))
        return vid[(i, j)]
    for i, j, ch in cells: faces.append((V(i, j + 1), V(i + 1, j + 1), V(i + 1, j), V(i, j))); mats.append(idx[ch])
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    for f, mi in zip(me.polygons, mats): f.material_index = mi
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    for k in keys: ob.data.materials.append(MATS[k])
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    so = ob.modifiers.new("s", "SOLIDIFY"); so.thickness = DEPTH; so.offset = 1.0
    bv = ob.modifiers.new("b", "BEVEL"); bv.width = 0.012; bv.segments = 5; bv.limit_method = "ANGLE"; bv.angle_limit = math.radians(40)
    ob.modifiers.new("wn", "WEIGHTED_NORMAL"); bpy.ops.object.shade_smooth(); ob.select_set(False)
    return ob
parts = {n: build(n) for n in ("body", "armL", "armR", "leg2", "leg4", "leg7", "leg9")}
# front face y of the solid (solidify direction) -> place details on it
dg = bpy.context.evaluated_depsgraph_get(); ev = parts["body"].evaluated_get(dg)
FRONT = min((ev.matrix_world @ Vector(v)).y for v in ev.bound_box)
def detail(size, loc, m, parent):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = size; bpy.ops.object.transform_apply(scale=True)
    md = o.modifiers.new("b", "BEVEL"); md.width = 0.006; md.segments = 3; bpy.ops.object.shade_smooth(); o.data.materials.append(m); o.parent = parent; return o
cz = lambda j: (ROWS - j) * c - ZC - c / 2; cx = lambda i: (i - 6) * c + c / 2
detail((8 * c, 0.09, 0.32 * c), (0, FRONT - 0.04, cz(1) - 0.36 * c), MATS["D"], parts["body"])           # cap visor sticking out
detail((0.7 * c, 0.02, 0.7 * c), (cx(6), FRONT - 0.008, cz(1)), MATS["G"], parts["body"])               # cockade relief
detail((0.75 * c, 0.02, 0.8 * c), (cx(4), FRONT - 0.008, cz(5)), MATS["G"], parts["body"])               # chest badge relief
detail((1.6 * c, 0.02, 0.6 * c), (cx(5) + c / 2, FRONT - 0.008, cz(7)), MATS["G"], parts["body"])        # belt buckle relief
for j in (5, 6): detail((0.22 * c, 0.02, 0.22 * c), (cx(7), FRONT - 0.006, cz(j)), MATS["G"], parts["body"])   # buttons
# eyes: flat squares on the face
for i in (3, 8):
    bpy.ops.mesh.primitive_plane_add(size=c * 0.98, location=(cx(i), FRONT - 0.002, cz(3)), rotation=(math.pi / 2, 0, 0)); e = bpy.context.object; e.data.materials.append(mat("eye", (0.002, 0.002, 0.003), 0.75, coat=0)); e.parent = parts["body"]; e.name = "body_eye"
# lights + ortho camera
def area(loc, energy, size, color, target=(0, 0, 0)):
    bpy.ops.object.light_add(type="AREA", location=loc); l = bpy.context.object; l.data.energy = energy; l.data.size = size; l.data.color = color
    l.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
area((-1.6, -2.5, 2.0), 260, 2.0, (1, 0.92, 0.82)); area((1.8, 1.5, 1.2), 160, 1.2, (1, 0.45, 0.3)); area((1.5, -2.2, -0.3), 50, 2.0, (0.6, 0.7, 1))
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.25
bpy.ops.object.camera_add(location=(0, -5, 0)); cam = bpy.context.object; sc.camera = cam; cam.rotation_euler = (math.pi / 2, 0, 0)
cam.data.type = "ORTHO"; cam.data.ortho_scale = 1.2
r = sc.render; r.engine = "CYCLES"; r.resolution_x = 1080; r.resolution_y = 1080; r.film_transparent = True
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True; sc.cycles.device = "CPU"
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"; r.image_settings.file_format = "PNG"; r.image_settings.color_mode = "RGBA"
PX = 1080 / 1.2   # pixels per metre
to_px = lambda X, Z: [round(540 + X * PX, 1), round(540 - Z * PX, 1)]
meta = {"cell_px": c * PX, "eyes": [to_px(cx(3), cz(3)), to_px(cx(8), cz(3))], "mouth": to_px(0, cz(4)),
        "pivot_armL": to_px((2 - 6) * c, cz(4) - c / 2 + c), "pivot_armR": to_px((10 - 6) * c, cz(4) - c / 2 + c),
        "pivot_legs": {str(i): to_px(cx(i), cz(8) + c / 2) for i in (2, 4, 7, 9)}, "feet": to_px(0, -ZC)}
json.dump(meta, open(os.path.join(OUTD, "chief_meta.json"), "w"))
children = lambda p: [p] + [o for o in sc.objects if o.parent == p]
for n, p in parts.items():
    for o in sc.objects:
        if o.type == "MESH": o.hide_render = o not in children(p)
    r.filepath = os.path.join(OUTD, f"chief_{n}.png"); bpy.ops.render.render(write_still=True); print("rendered", n)

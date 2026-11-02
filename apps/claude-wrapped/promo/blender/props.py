# Hand props for the police chief, same light/scale as char_parts.py (orthographic, 900 px per metre). Grip point = image centre.
import bpy, math, sys, os, json
from mathutils import Vector
OUTD = sys.argv[1]; SAMPLES = int(sys.argv[2]); TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loc")
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
def mat(name, color, rough=0.45, metal=0.0, coat=0.2, img=None, trans=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; p = nt.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1); p.inputs["Roughness"].default_value = rough; p.inputs["Metallic"].default_value = metal; p.inputs["Coat Weight"].default_value = coat
    p.inputs["Transmission Weight"].default_value = trans
    if img: tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = bpy.data.images.load(os.path.join(TEX, img)); nt.links.new(tx.outputs["Color"], p.inputs["Base Color"])
    return m
def box(size, loc, m, bev=0.008, rot=(0, 0, 0), group=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = size; bpy.ops.object.transform_apply(scale=True)
    if bev: md = o.modifiers.new("b", "BEVEL"); md.width = bev; md.segments = 3; bpy.ops.object.shade_smooth()
    o.data.materials.append(m); group.append(o); return o
def cyl(r, d, loc, m, rot=(0, 0, 0), group=None, v=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=v); o = bpy.context.object; bpy.ops.object.shade_smooth(); o.data.materials.append(m); group.append(o); return o
def torus(R, r, loc, m, rot=(0, 0, 0), group=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot); o = bpy.context.object; bpy.ops.object.shade_smooth(); o.data.materials.append(m); group.append(o); return o
def textured_front(w, h, loc, img, group, rough=0.7):   # a plane facing the camera (-Y)
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=(math.pi / 2, 0, 0)); o = bpy.context.object; o.scale = (w, h, 1); o.data.materials.append(mat(img, (1, 1, 1), rough, img=img)); group.append(o); return o
MANILA = mat("manila", (0.62, 0.45, 0.22), 0.7); WHITE = mat("paper", (0.85, 0.84, 0.8), 0.8); RED = mat("red", (0.6, 0.06, 0.04), 0.4)
BLACK = mat("black", (0.01, 0.01, 0.012), 0.3, coat=0.6); BRASS = mat("brass", (0.8, 0.55, 0.15), 0.25, metal=1); STEEL = mat("steel", (0.6, 0.6, 0.62), 0.25, metal=1)
WOODM = mat("wood", (0.25, 0.12, 0.05), 0.5); GLASS = mat("glass", (0.8, 0.9, 1.0), 0.02, trans=1.0); CARD = mat("card", (0.45, 0.32, 0.17), 0.85); MUGM = mat("mug", (0.85, 0.85, 0.82), 0.25, coat=0.6)
P = {}
def prop(name, build): g = []; build(g); P[name] = g
prop("folder", lambda g: (box((0.24, 0.02, 0.3), (0.1, 0, -0.06), MANILA, group=g), box((0.22, 0.012, 0.03), (0.1, -0.012, 0.08), WHITE, 0.003, group=g)))
def folder_open(g):
    box((0.25, 0.015, 0.32), (-0.13, 0, 0), MANILA, rot=(0, 0, 0.12), group=g); box((0.25, 0.015, 0.32), (0.13, 0, 0), MANILA, rot=(0, 0, -0.12), group=g)
    textured_front(0.21, 0.28, (-0.12, -0.03, 0.0), "sheet_lines.png", g); textured_front(0.21, 0.28, (0.12, -0.03, 0.01), "sheet_lines.png", g)
prop("folder_open", folder_open)
prop("paper", lambda g: textured_front(0.16, 0.21, (0.06, 0, -0.04), "sheet_lines.png", g))
def magnifier(g):
    cyl(0.018, 0.12, (0.04, 0, 0.0), WOODM, rot=(0, math.pi / 2, 0), group=g); torus(0.075, 0.013, (0.17, 0, 0.0), BRASS, rot=(math.pi / 2, 0, 0), group=g)
    cyl(0.065, 0.008, (0.17, 0, 0.0), GLASS, rot=(math.pi / 2, 0, 0), group=g)
prop("magnifier", magnifier)
def mug(g):
    cyl(0.07, 0.15, (0.1, 0, 0.0), MUGM, group=g); cyl(0.06, 0.01, (0.1, 0, 0.07), mat("coffee", (0.08, 0.04, 0.02), 0.1, coat=1), group=g)
    torus(0.04, 0.012, (0.02, 0, 0.0), MUGM, rot=(math.pi / 2, 0, 0), group=g); box((0.14, 0.005, 0.03), (0.1, -0.068, -0.02), RED, 0.002, group=g)
prop("mug", mug)
def flashlight(g):
    cyl(0.028, 0.2, (0.06, 0, 0), BLACK, rot=(0, math.pi / 2, 0), group=g); cyl(0.045, 0.06, (0.18, 0, 0), BLACK, rot=(0, math.pi / 2, 0), group=g)
    cyl(0.038, 0.005, (0.212, 0, 0), mat("lens", (1, 0.95, 0.8), 0.1, coat=1), rot=(0, math.pi / 2, 0), group=g)
prop("flashlight", flashlight)
def keys(g):
    torus(0.04, 0.007, (0, 0, -0.03), BRASS, rot=(math.pi / 2, 0, 0), group=g)
    for k, a in enumerate((-0.4, 0.0, 0.45)):
        box((0.02, 0.008, 0.11), (math.sin(a) * 0.08, -0.004 * k, -0.11 - math.cos(a) * 0.02), BRASS if k != 1 else STEEL, 0.003, rot=(0, a, 0), group=g)
prop("keys", keys)
def stamp(g):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(0, 0, 0)); o = bpy.context.object; bpy.ops.object.shade_smooth(); o.data.materials.append(WOODM); g.append(o)
    cyl(0.016, 0.1, (0, 0, -0.06), WOODM, group=g); box((0.12, 0.07, 0.035), (0, 0, -0.125), WOODM, 0.006, group=g); box((0.11, 0.06, 0.012), (0, 0, -0.148), RED, 0.002, group=g)
prop("stamp", stamp)
def cardbox(g): box((0.4, 0.26, 0.28), (0, 0.06, -0.04), CARD, 0.01, group=g); textured_front(0.18, 0.12, (0, -0.072, -0.04), "box.png", g)
prop("box", cardbox)
def placard(g): box((0.5, 0.012, 0.2), (0, 0.0, -0.05), BLACK, 0.006, group=g); textured_front(0.48, 0.182, (0, -0.007, -0.05), "placard.png", g); cyl(0.004, 0.24, (-0.2, 0, 0.12), STEEL, rot=(0, 0.6, 0), group=g); cyl(0.004, 0.24, (0.2, 0, 0.12), STEEL, rot=(0, -0.6, 0), group=g)
prop("placard", placard)
def thick(g):
    box((0.3, 0.09, 0.38), (0, 0.02, -0.04), MANILA, 0.01, group=g)
    for k in range(5): box((0.27, 0.012, 0.35), (0.01 * (k % 2), -0.03 + k * 0.004, -0.035 + k * 0.006), WHITE, 0.002, group=g)
    box((0.05, 0.1, 0.39), (0.06, 0.02, -0.04), RED, 0.004, group=g)
prop("thick", thick)
# light + camera identical to char_parts.py
def area(loc, energy, size, color, target=(0, 0, 0)):
    bpy.ops.object.light_add(type="AREA", location=loc); l = bpy.context.object; l.data.energy = energy; l.data.size = size; l.data.color = color
    l.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
area((-1.6, -2.5, 2.0), 260, 2.0, (1, 0.92, 0.82)); area((1.8, 1.5, 1.2), 160, 1.2, (1, 0.45, 0.3)); area((1.5, -2.2, -0.3), 50, 2.0, (0.6, 0.7, 1))
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.25
bpy.ops.object.camera_add(location=(0, -5, 0)); cam = bpy.context.object; sc.camera = cam; cam.rotation_euler = (math.pi / 2, 0, 0); cam.data.type = "ORTHO"; cam.data.ortho_scale = 512 / 900
r = sc.render; r.engine = "CYCLES"; r.resolution_x = 512; r.resolution_y = 512; r.film_transparent = True
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True; sc.cycles.device = "CPU"; sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
r.image_settings.file_format = "PNG"; r.image_settings.color_mode = "RGBA"; os.makedirs(OUTD, exist_ok=True)
ONLY = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
for name, objs in P.items():
    if ONLY and name not in ONLY: continue
    for o in sc.objects:
        if o.type == "MESH": o.hide_render = o not in objs
    r.filepath = os.path.join(OUTD, f"{name}.png"); bpy.ops.render.render(write_still=True); print("rendered", name)
json.dump({"size": 512, "grip": [256, 256], "px_per_m": 900}, open(os.path.join(OUTD, "props_meta.json"), "w"))

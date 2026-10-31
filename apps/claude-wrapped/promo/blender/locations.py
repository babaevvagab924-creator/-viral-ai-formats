# Police-chief locations for promo v6. Each renders a background plate (and prison a foreground bars plate)
# plus where the character's feet land on screen. Usage: python3 locations.py <name> <out_dir> <samples>
import bpy, math, sys, os, json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
NAME, OUTD, SAMPLES = sys.argv[1], sys.argv[2], int(sys.argv[3]); TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loc")
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
def P(m): return m.node_tree.nodes["Principled BSDF"]
def mat(name, color, rough=0.5, metal=0.0, coat=0.0, emit=0.0, img=None, emit_img=False):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; p = P(m)
    p.inputs["Base Color"].default_value = (*color, 1); p.inputs["Roughness"].default_value = rough; p.inputs["Metallic"].default_value = metal; p.inputs["Coat Weight"].default_value = coat
    if img:
        tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = bpy.data.images.load(os.path.join(TEX, img))
        nt.links.new(tx.outputs["Color"], p.inputs["Emission Color" if emit_img else "Base Color"])
    elif emit: p.inputs["Emission Color"].default_value = (*color, 1)
    p.inputs["Emission Strength"].default_value = emit; return m
def noisy(m, c1, c2, scale=6, bump=0.2):
    nt = m.node_tree; p = P(m); n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = 10
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (*c1, 1); cr.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(n.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], p.inputs["Base Color"])
    b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = bump; nt.links.new(n.outputs["Fac"], b.inputs["Height"]); nt.links.new(b.outputs["Normal"], p.inputs["Normal"]); return m
def cube(size, loc, m, bevel=0.0, rot=(0, 0, 0), name=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = size; bpy.ops.object.transform_apply(scale=True)
    if bevel: md = o.modifiers.new("b", "BEVEL"); md.width = bevel; md.segments = 3; bpy.ops.object.shade_smooth()
    o.data.materials.append(m); o.name = name or o.name; return o
def cyl(r, d, loc, m, rot=(0, 0, 0), v=32, name=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=v); o = bpy.context.object; bpy.ops.object.shade_smooth(); o.data.materials.append(m); o.name = name or o.name; return o
def plane(w, h, loc, m, rot=(math.pi / 2, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = (w, h, 1); o.data.materials.append(m); return o
def light(kind, loc, energy, color, target=None, size=0.5, spot=None):
    bpy.ops.object.light_add(type=kind, location=loc); l = bpy.context.object; l.data.energy = energy; l.data.color = color
    if kind == "AREA": l.data.size = size
    else: l.data.shadow_soft_size = size
    if spot: l.data.spot_size = math.radians(spot); l.data.spot_blend = 0.4
    if target: l.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return l
def haze(density, center=(0, 2, 2), size=(10, 14, 6)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center); v = bpy.context.object; v.scale = size
    vm = bpy.data.materials.new("haze"); vm.use_nodes = True; nt = vm.node_tree; nt.nodes.remove(nt.nodes["Principled BSDF"])
    pv = nt.nodes.new("ShaderNodeVolumePrincipled"); pv.inputs["Density"].default_value = density
    nt.links.new(pv.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"]); v.data.materials.append(vm)
def camera(loc, look, lens):
    bpy.ops.object.camera_add(location=loc); cam = bpy.context.object; sc.camera = cam; cam.data.lens = lens
    cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat("-Z", "Y").to_euler(); return cam
def world(color, strength):
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs["Color"].default_value = (*color, 1); bg.inputs["Strength"].default_value = strength

WOOD = lambda: noisy(mat("wood", (0.1, 0.05, 0.025), 0.45, coat=0.4), (0.13, 0.065, 0.03), (0.05, 0.025, 0.012), 18, 0.08)
CONCRETE = lambda c1=(0.07, 0.07, 0.075), c2=(0.025, 0.025, 0.03): noisy(mat("concrete", c1, 0.9), c1, c2, 5, 0.4)
FEET = None; FG = []
if NAME == "office":
    cube((8, 0.2, 5), (0, 2.0, 2.5), noisy(mat("panel", (0.06, 0.03, 0.02), 0.6), (0.07, 0.035, 0.02), (0.03, 0.015, 0.01), 3, 0.2))
    cube((8, 8, 0.1), (0, 0, -0.05), mat("floor", (0.03, 0.02, 0.015), 0.6))
    plane(1.0, 1.0, (0.62, 1.88, 1.65), mat("city", (0, 0, 0), 0.5, emit=1.6, img="city.png", emit_img=True))
    for i in range(12): cube((1.1, 0.02, 0.045), (0.62, 1.84, 1.18 + i * 0.085), mat("slat", (0.05, 0.045, 0.04), 0.5))
    plane(0.42, 0.5, (-0.55, 1.88, 1.62), mat("star", (1, 1, 1), 0.4, img="star.png"))
    W_ = WOOD(); cube((2.6, 1.1, 0.07), (0, 0.15, 0.745), W_, 0.01); cube((2.5, 0.05, 0.72), (0, -0.37, 0.36), W_, 0.005)
    np_ = plane(0.46, 0.1, (-0.33, -0.3, 0.83), mat("nameplate", (1, 1, 1), 0.3, metal=0.6, img="nameplate.png"), rot=(math.radians(70), 0, 0.12))
    cyl(0.02, 0.32, (-0.52, 0.5, 0.94), mat("brass", (0.6, 0.4, 0.1), 0.3, metal=1)); cube((0.36, 0.14, 0.09), (-0.52, 0.47, 1.12), mat("green", (0.0, 0.25, 0.06), 0.15, coat=1), 0.03)
    light("POINT", (-0.52, 0.43, 1.05), 22, (1, 0.8, 0.5), size=0.05)
    for k in range(5): cube((0.36, 0.26, 0.02), (0.5, 0.42, 0.79 + k * 0.022), mat("folder", (0.55, 0.42, 0.25), 0.8), rot=(0, 0, 0.1 * (k % 2)))
    cube((0.2, 0.15, 0.08), (0.48, 0.0, 0.82), mat("phone", (0.02, 0.02, 0.02), 0.3, coat=0.8), 0.02)
    light("SPOT", (0.1, -0.6, 2.8), 950, (1, 0.72, 0.45), target=(0, 0.1, 0.8), size=0.2, spot=55)
    light("AREA", (2.2, 1.6, 1.8), 220, (0.4, 0.55, 1), target=(0, 0.1, 1.0), size=1.0)
    haze(0.025); world((0.01, 0.01, 0.02), 0.3); FEET = (0, 0.15, 0.78); cam = camera((0, -2.3, 1.22), (0, 0.15, 1.08), 32)
elif NAME == "archive":
    cube((8, 30, 0.1), (0, 10, -0.05), CONCRETE())
    BOX = mat("box", (1, 1, 1), 0.8, img="box.png"); MET = mat("metal", (0.12, 0.12, 0.13), 0.45, metal=0.8)
    for side in (-1, 1):
        x0 = side * 1.0
        for k in range(10):
            yy = 0.5 + k * 1.2
            for z in (0.02, 0.62, 1.22, 1.82): cube((0.7, 1.15, 0.03), (x0, yy, z), MET)
            for z in (0.02, 0.62, 1.22, 1.82):
                for b in range(3):
                    if (k * 7 + b * 3 + int(z * 10)) % 5 == 0: continue
                    cube((0.5, 0.33, 0.28), (x0 - side * 0.05, yy - 0.38 + b * 0.38, z + 0.16), BOX, rot=(0, 0, math.pi / 2 * (1 if side > 0 else -1)))
    for k in range(4):
        yy = 1 + k * 3; cyl(0.05, 0.12, (0, yy, 2.6), mat("bulb", (1, 0.75, 0.45), 0.2, emit=30)); light("POINT", (0, yy, 2.45), 110, (1, 0.72, 0.42), size=0.08)
    light("SPOT", (0.3, -1.2, 0.8), 160, (0.8, 0.9, 1), target=(0, 0.8, 0.35), size=0.03, spot=26)
    haze(0.06, (0, 8, 1.5), (4, 20, 3.5)); world((0.0, 0.0, 0.0), 0); FEET = (0, 0.8, 0.0); cam = camera((0, -1.7, 0.5), (0, 1.6, 0.55), 28)
elif NAME == "roof":
    cube((6, 0.6, 1.0), (0, 0.1, 0.5), CONCRETE((0.09, 0.085, 0.085), (0.03, 0.03, 0.035)))
    plane(40, 16, (0, 18, 6.5), mat("city", (0, 0, 0), 0.5, emit=1.2, img="city.png", emit_img=True))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.9, location=(1.3, 15, 7.2)); bpy.context.object.data.materials.append(mat("moon", (1, 0.93, 0.8), 0.5, emit=6))
    plane(2.2, 0.47, (-1.05, 7, 3.4), mat("neon", (0, 0, 0), 0.5, emit=8, img="neon.png", emit_img=True))
    light("POINT", (-1.05, 6.5, 3.2), 600, (1, 0.15, 0.2), size=0.5)
    cyl(0.7, 1.4, (2.6, 5, 2.6), mat("tank", (0.02, 0.02, 0.025), 0.7)); [cyl(0.03, 1.8, (2.6 + dx, 5 + dy, 1.0), mat("leg", (0.02, 0.02, 0.025))) for dx, dy in ((-0.5, -0.5), (0.5, -0.5), (-0.5, 0.5), (0.5, 0.5))]
    light("SUN", (3, 10, 8), 0.6, (0.55, 0.65, 1.0), target=(0, 0, 0))
    light("AREA", (-1.5, -1.5, 2.0), 40, (0.6, 0.7, 1.0), target=(0, 0.1, 1.2), size=1.5)
    haze(0.012, (0, 10, 4), (30, 30, 10)); world((0.004, 0.008, 0.03), 1.0); FEET = (0, 0.1, 1.0); cam = camera((0, -2.0, 1.32), (0, 1.0, 1.55), 30)
elif NAME == "vault":
    cube((8, 8, 0.1), (0, 0, -0.05), mat("marble", (0.05, 0.045, 0.04), 0.15, coat=1))
    STEEL = noisy(mat("steel", (0.3, 0.3, 0.32), 0.35, metal=1), (0.32, 0.32, 0.34), (0.2, 0.2, 0.22), 30, 0.05)
    for i in range(-6, 7):
        for j in range(0, 9): cube((0.24, 0.05, 0.2), (i * 0.26, 1.6, 0.15 + j * 0.22), STEEL, 0.008)
    door = cyl(0.8, 0.3, (-0.85, 1.0, 0.85), STEEL, rot=(math.pi / 2, 0, math.radians(-70)), v=64)
    for k in range(6): cube((0.04, 0.04, 0.6), (-0.68, 0.92, 0.85), mat("brass", (0.6, 0.42, 0.12), 0.25, metal=1), rot=(0, k * math.pi / 3, math.radians(-70)))
    GOLD = mat("gold", (1.0, 0.7, 0.2), 0.2, metal=1)
    for i in range(5):
        for j in range(3 - (i % 2)): cube((0.16, 0.08, 0.05), (0.42 + j * 0.17 + (i % 2) * 0.08, 0.95, 0.025 + i * 0.055), GOLD, 0.01)
    light("POINT", (0.55, 0.7, 0.5), 14, (1, 0.7, 0.3), size=0.3)
    light("SPOT", (0, -1.0, 2.4), 300, (1, 0.85, 0.6), target=(0, 0.6, 0.3), size=0.1, spot=40)
    light("AREA", (1.5, 0.5, 1.6), 90, (1, 0.5, 0.2), target=(0, 0.5, 0.4), size=1.0)
    haze(0.03); world((0, 0, 0), 0); FEET = (0, 0.5, 0.0); cam = camera((0, -1.6, 0.6), (0, 0.8, 0.62), 28)
elif NAME == "mugshot":
    cube((8, 8, 0.1), (0, 0, -0.05), CONCRETE((0.08, 0.08, 0.085), (0.04, 0.04, 0.045)))
    cube((8, 0.1, 4), (0, 1.1, 2), mat("wall", (0.06, 0.065, 0.07), 0.8))
    plane(1.5, 2.0, (0, 1.04, 1.0), mat("chart", (1, 1, 1), 0.7, img="height.png"))
    light("AREA", (0, -1.4, 0.7), 55, (0.9, 0.95, 1.0), target=(0, 0.6, 0.4), size=0.6)
    light("SPOT", (0, 0.2, 2.6), 160, (1, 0.95, 0.9), target=(0, 0.5, 0.3), size=0.05, spot=45)
    world((0, 0, 0), 0); FEET = (0, 0.55, 0.0); cam = camera((0, -1.55, 0.45), (0, 0.8, 0.5), 32)
elif NAME == "prison":
    cube((8, 30, 0.1), (0, 10, -0.05), CONCRETE())
    for side in (-1, 1):
        cube((0.1, 30, 4), (side * 1.4, 10, 2), CONCRETE((0.08, 0.075, 0.07), (0.03, 0.03, 0.03)))
        for k in range(8):
            for b in range(7): cyl(0.016, 2.2, (side * 1.25, 1.6 + k * 2.2 + b * 0.14, 1.1), mat("bar", (0.05, 0.05, 0.055), 0.35, metal=0.9), v=12)
    for k in range(5): cube((0.08, 1.0, 0.05), (0, 1 + k * 3.5, 2.6), mat("tube", (0.85, 0.95, 1.0), 0.2, emit=8)); light("AREA", (0, 1 + k * 3.5, 2.5), 90, (0.75, 0.9, 1.0), target=(0, 1 + k * 3.5, 0), size=1.0)
    light("POINT", (0.8, 2.5, 0.3), 25, (1, 0.25, 0.15), size=0.2)
    for b in range(-6, 7): FG.append(cyl(0.022, 2.4, (b * 0.17, -0.85, 1.1), mat("fgbar", (0.03, 0.03, 0.035), 0.3, metal=0.9), v=16, name=f"fg_{b}"))
    cube((2.4, 0.05, 0.04), (0, -0.85, 0.75), mat("fgbar", (0.03, 0.03, 0.035), 0.3, metal=0.9), name="fg_rail")
    FG.append(bpy.context.object)
    haze(0.03, (0, 8, 1.5), (3, 20, 3.5)); world((0, 0, 0), 0); FEET = (0, 0.6, 0.0); cam = camera((0, -1.6, 0.5), (0, 1.4, 0.55), 30)

for o in sc.objects:
    if o.type == "LIGHT": o.visible_camera = False; o.visible_glossy = False
r = sc.render; r.engine = "CYCLES"; r.resolution_x = 1080; r.resolution_y = 1920
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True; sc.cycles.device = "CPU"; sc.cycles.max_bounces = 5; sc.cycles.volume_bounces = 1
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - High Contrast"; r.image_settings.file_format = "PNG"; r.image_settings.color_mode = "RGBA"
bpy.context.view_layer.update()
def px(p): v = world_to_camera_view(sc, cam, Vector(p)); return [round(v.x * 1080, 1), round((1 - v.y) * 1920, 1)]
f = px(FEET); top = px((FEET[0], FEET[1], FEET[2] + 0.75))
json.dump({"feet": f, "height_px": round(f[1] - top[1], 1)}, open(os.path.join(OUTD, f"{NAME}.json"), "w"))
for o in FG: o.hide_render = True
r.filepath = os.path.join(OUTD, f"{NAME}.png"); bpy.ops.render.render(write_still=True); print("rendered", NAME)
if FG:
    r.film_transparent = True
    for o in sc.objects:
        if o.type == "MESH": o.hide_render = o not in FG
    r.filepath = os.path.join(OUTD, f"{NAME}_fg.png"); bpy.ops.render.render(write_still=True); print("rendered", NAME, "fg")

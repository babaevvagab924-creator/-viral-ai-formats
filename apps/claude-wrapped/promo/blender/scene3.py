# Noir interrogation room, 9:16. Voxel pixel-Claude (user's sprite) as the detective. Cycles (bpy 5.2).
import bpy, math, sys, os
from mathutils import Vector
D = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]; SAMPLES = int(sys.argv[2]) if len(sys.argv) > 2 else 96
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
def P(m): return m.node_tree.nodes["Principled BSDF"]
def mat(name, color, rough=0.5, coat=0.0, emit=0.0, img=None, alpha=False, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; p = P(m)
    p.inputs["Base Color"].default_value = (*color, 1); p.inputs["Roughness"].default_value = rough; p.inputs["Coat Weight"].default_value = coat; p.inputs["Metallic"].default_value = metal
    if img:
        tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = bpy.data.images.load(os.path.join(D, img)); nt.links.new(tx.outputs["Color"], p.inputs["Base Color"])
        if alpha: nt.links.new(tx.outputs["Alpha"], p.inputs["Alpha"])
    if emit: p.inputs["Emission Color"].default_value = (*color, 1); p.inputs["Emission Strength"].default_value = emit
    return m
def noisy(m, c1, c2, scale=6, bump=0.15):
    nt = m.node_tree; p = P(m); n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = 10
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (*c1, 1); cr.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(n.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], p.inputs["Base Color"])
    b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = bump; nt.links.new(n.outputs["Fac"], b.inputs["Height"]); nt.links.new(b.outputs["Normal"], p.inputs["Normal"]); return m
def cube(size, loc, m, bevel=0.01, seg=2, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = size; bpy.ops.object.transform_apply(scale=True)
    if bevel: md = o.modifiers.new("b", "BEVEL"); md.width = bevel; md.segments = seg; md.limit_method = "NONE"
    bpy.ops.object.shade_smooth(); o.data.materials.append(m); return o
def plane(w, h, loc, m, rz=0.0, rx=0.0):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=(rx, 0, rz)); o = bpy.context.object; o.scale = (w, h, 1); o.data.materials.append(m); return o

TZ = 0.78  # table top height
# room
noisy_wall = noisy(mat("wall", (0.03, 0.03, 0.035), 0.9), (0.035, 0.035, 0.04), (0.012, 0.012, 0.015), 4, 0.3)
cube((8, 0.2, 6), (0, 2.2, 3), noisy_wall, 0); cube((0.2, 8, 6), (-3, 0, 3), noisy_wall, 0)
cube((8, 8, 0.1), (0, 0, -0.05), mat("floor", (0.02, 0.018, 0.016), 0.7), 0)
# table
WOOD = noisy(mat("wood", (0.1, 0.05, 0.025), 0.45, coat=0.4), (0.12, 0.06, 0.03), (0.05, 0.025, 0.012), 18, 0.08)
cube((2.6, 1.5, 0.06), (0, 0.2, TZ - 0.03), WOOD, 0.01)
for x in (-1.2, 1.2):
    for y in (-0.45, 0.85): cube((0.07, 0.07, TZ), (x, y, TZ / 2), WOOD, 0.005)
# props on the table
plane(0.72, 0.515, (0.02, -0.24, TZ + 0.004), mat("folder", (1, 1, 1), 0.7, img="folder.png"), rz=-0.05)
for (x, y, rz) in ((-0.75, -0.1, 0.35), (-0.6, 0.15, -0.2), (0.78, -0.05, 0.5), (0.7, 0.3, -0.3), (-0.95, -0.45, 0.1)):
    plane(0.36, 0.48, (x, y, TZ + 0.002), mat("sheet", (1, 1, 1), 0.85, img="sheet.png"), rz=rz)
plane(0.22, 0.13, (0.72, -0.12, TZ + 0.006), mat("tag", (1, 1, 1), 0.7, img="tag.png"), rz=0.42)
# mug + ashtray for mood
bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.12, location=(-0.85, 0.42, TZ + 0.06)); bpy.ops.object.shade_smooth(); bpy.context.object.data.materials.append(mat("mug", (0.6, 0.58, 0.55), 0.3, coat=0.5))

# ---- pixel Claude, voxel model exactly from the sprite ----
SPRITE = ["..BBBBBBBB..", "..BEBBBBEB..", "AABBBBBBBBAA", "AABBBBBBBBAA", "..BBBBBBBB..", "..BBBBBBBB..", "..L.L..L.L..", "..L.L..L.L.."]
c = 0.075; depth = 0.3; cy_ = 0.4
CLAY = mat("claude", (0.68, 0.19, 0.1), 0.36, coat=0.25); HOLE = mat("hole", (0.0, 0.0, 0.0), 0.9)
# one flat silhouette from the sprite (shared grid vertices), eye cells left open, then extruded into a solid
verts, faces, vid = [], [], {}
def V(i, j):
    if (i, j) not in vid: vid[(i, j)] = len(verts); verts.append(((i - 6) * c, 0.0, (8 - j) * c))
    return vid[(i, j)]
for j, row in enumerate(SPRITE):
    for i, ch in enumerate(row):
        if ch in "BALE": faces.append((V(i, j + 1), V(i + 1, j + 1), V(i + 1, j), V(i, j)))
me = bpy.data.meshes.new("claude"); me.from_pydata(verts, [], faces); me.update()
body = bpy.data.objects.new("claude", me); bpy.context.collection.objects.link(body); body.location = (0, cy_ - depth / 2, TZ)
bpy.context.view_layer.objects.active = body; body.select_set(True)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT"); bpy.ops.mesh.dissolve_limited(angle_limit=0.01); bpy.ops.object.mode_set(mode="OBJECT")
so = body.modifiers.new("solid", "SOLIDIFY"); so.thickness = depth; so.offset = 1.0; so.use_even_offset = True
bv = body.modifiers.new("round", "BEVEL"); bv.width = 0.014; bv.segments = 6; bv.limit_method = "ANGLE"; bv.angle_limit = math.radians(40)
body.modifiers.new("wn", "WEIGHTED_NORMAL"); bpy.ops.object.shade_smooth(); body.data.materials.append(CLAY)
# eyes: flat black squares on the real front face of the evaluated solid
dg = bpy.context.evaluated_depsgraph_get(); ev = body.evaluated_get(dg)
front_y = min((ev.matrix_world @ Vector(v)).y for v in ev.bound_box)
for j, row in enumerate(SPRITE):
    for i, ch in enumerate(row):
        if ch == "E":
            bpy.ops.mesh.primitive_plane_add(size=c * 0.98, location=((i - 5.5) * c, front_y - 0.002, TZ + (7 - j) * c + c / 2), rotation=(math.pi / 2, 0, 0))
            bpy.context.object.data.materials.append(mat("eye", (0.002, 0.002, 0.003), 0.75))

# ---- hanging lamp with volumetric cone ----
LZ = 2.05; tilt = 0.05
bpy.ops.mesh.primitive_cone_add(radius1=0.32, radius2=0.07, depth=0.26, location=(0.05, 0.1, LZ), rotation=(0, tilt, 0), vertices=64)
shade = bpy.context.object; bpy.ops.object.shade_smooth(); sol = shade.modifiers.new("s", "SOLIDIFY"); sol.thickness = 0.01
shade.data.materials.append(mat("shade", (0.05, 0.06, 0.05), 0.35, metal=0.8))
bpy.ops.mesh.primitive_cylinder_add(radius=0.004, depth=2.0, location=(0.05 - math.sin(tilt) * 1.1, 0.1, LZ + 1.12), rotation=(0, tilt, 0)); bpy.context.object.data.materials.append(mat("cord", (0.01, 0.01, 0.01), 0.5))
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(0.05 + math.sin(tilt) * 0.06, 0.1, LZ - 0.07)); bpy.context.object.data.materials.append(mat("bulb", (1, 0.62, 0.3), 0.2, emit=40))
bpy.ops.object.light_add(type="SPOT", location=(0.05 + math.sin(tilt) * 0.08, 0.1, LZ - 0.08)); sp = bpy.context.object
sp.data.energy = 850; sp.data.color = (1, 0.6, 0.32); sp.data.spot_size = math.radians(58); sp.data.spot_blend = 0.3; sp.data.shadow_soft_size = 0.06; sp.rotation_euler = (math.radians(-6), 0, 0)
# cold moonlight through blinds onto the back wall
bpy.ops.object.light_add(type="SPOT", location=(2.6, -0.6, 2.6)); mn = bpy.context.object
mn.data.energy = 2200; mn.data.color = (0.45, 0.55, 1.0); mn.data.spot_size = math.radians(30); mn.data.shadow_soft_size = 0.01
mn.rotation_euler = (Vector((-0.8, 2.1, 2.2)) - mn.location).to_track_quat("-Z", "Y").to_euler()
for i in range(12): cube((0.02, 0.9, 0.05), (2.25, -0.3, 2.2 + i * 0.09), mat("slat", (0.02, 0.02, 0.02)), 0, rot=(0, 0, 0.0))
# red rim from the right on Claude
bpy.ops.object.light_add(type="AREA", location=(1.8, 1.4, 1.3)); rm = bpy.context.object; rm.data.energy = 200; rm.data.color = (1, 0.18, 0.12); rm.data.size = 0.6
rm.rotation_euler = (Vector((0, 0.45, 1.0)) - rm.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.object.light_add(type='AREA', location=(-0.6, -1.6, 1.3)); fl = bpy.context.object; fl.data.energy = 5; fl.data.color = (1, 0.8, 0.6); fl.data.size = 1.0
fl.rotation_euler = (Vector((0, 0.4, 1.05)) - fl.location).to_track_quat('-Z', 'Y').to_euler()
# smoky air
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.3, 1.6)); vol = bpy.context.object; vol.scale = (5, 4.4, 3.2)
vm = bpy.data.materials.new("smoke"); vm.use_nodes = True; nt = vm.node_tree; nt.nodes.remove(nt.nodes["Principled BSDF"])
pv = nt.nodes.new("ShaderNodeVolumePrincipled"); pv.inputs["Density"].default_value = 0.0
nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.6; nz.inputs["Detail"].default_value = 6
mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 0.35; mr.inputs["From Max"].default_value = 0.75; mr.inputs["To Min"].default_value = 0.05; mr.inputs["To Max"].default_value = 0.2
nt.links.new(nz.outputs["Fac"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], pv.inputs["Density"])
nt.links.new(pv.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"]); vol.data.materials.append(vm)

w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
bpy.ops.object.camera_add(location=(0.0, -2.35, 1.2)); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 32
cam.rotation_euler = (Vector((0, 0.25, 1.24)) - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.dof.use_dof = True; cam.data.dof.focus_distance = (Vector((0, cy_ - 0.13, TZ + 0.25)) - cam.location).length; cam.data.dof.aperture_fstop = 2.0
r = sc.render; r.engine = "CYCLES"; r.resolution_x = 1080; r.resolution_y = 1920
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True; sc.cycles.device = "CPU"; sc.cycles.max_bounces = 5; sc.cycles.volume_bounces = 1
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - High Contrast"
r.image_settings.file_format = "PNG"; r.filepath = OUT
bpy.ops.render.render(write_still=True); print("rendered", OUT)

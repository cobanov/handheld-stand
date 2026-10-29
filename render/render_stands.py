# Product renders of the stand family on an oak desk, for the model card.
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b -P render/render_stands.py [-- shot ...]
# choso-wsl (4090, ~2.7x faster): rsync render/ stl/ to ~/handheld-stand, then ~/opt/blender-5.2.3-linux-x64/blender -b -P render/render_stands.py
# Assets (CC0, Poly Haven): artist_workshop HDRI, oak_veneer_01 texture, in render/assets/.
import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(ROOT, "images")
WIDTH = {"N": 0.050, "M": 0.080, "W": 0.120}
RES = (1800, 1350) if "PREVIEW" not in os.environ else (600, 450)
SAMPLES = 256 if "PREVIEW" not in os.environ else 32


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for dev in ("OPTIX", "CUDA", "METAL"):   # choso-wsl 4090 → OPTIX, Mac → METAL
        try:
            prefs.compute_device_type = dev
        except TypeError:   # not in this build
            continue
        if any(d.type == dev for d in prefs.get_devices_for_type(dev)):
            break
    print("compute device:", prefs.compute_device_type)
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    sc.cycles.device = "GPU"
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = 0.6   # bright product look
    return sc


def world():
    w = bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(os.path.join(ASSETS, "artist_workshop_2k.hdr"))
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value[2] = math.radians(110)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    bg = nt.nodes["Background"]
    bg.inputs["Strength"].default_value = 1.0
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])


def pla_material():
    m = bpy.data.materials.new("White PLA")
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (0.85, 0.84, 0.81, 1)
    p.inputs["Roughness"].default_value = 0.42
    p.inputs["Subsurface Weight"].default_value = 0.15
    p.inputs["Subsurface Scale"].default_value = 0.002
    # 0.2 mm layer lines: printed on its side, so layers stack along the width (local Y)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = "BANDS"
    wave.bands_direction = "Y"
    wave.inputs["Scale"].default_value = 1571.0   # period 0.314 / scale = 0.2 mm
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.12
    bump.inputs["Distance"].default_value = 0.00004
    nt.links.new(tc.outputs["Object"], wave.inputs["Vector"])
    nt.links.new(wave.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], p.inputs["Normal"])
    return m


def desk():
    bpy.ops.mesh.primitive_plane_add(size=1)
    d = bpy.context.object
    d.name = "Desk"
    d.scale = (1.6, 1.0, 1)
    m = bpy.data.materials.new("Oak")
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.6, 1.0, 1)   # texture tile = 1 m
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])

    def tex(name, colorspace):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(os.path.join(ASSETS, name))
        t.image.colorspace_settings.name = colorspace
        nt.links.new(mp.outputs["Vector"], t.inputs["Vector"])
        return t

    nt.links.new(tex("oak_veneer_01_diff_2k.jpg", "sRGB").outputs["Color"], p.inputs["Base Color"])
    nt.links.new(tex("oak_veneer_01_rough_2k.jpg", "Non-Color").outputs["Color"], p.inputs["Roughness"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(tex("oak_veneer_01_nor_gl_2k.jpg", "Non-Color").outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
    d.data.materials.append(m)


def stand(name, mat, x, y, rot_z=0.0):
    """Import stl/stand-<name>.stl (lying on its side, mm), stand it up, centre it at (x, y) on the desk."""
    bpy.ops.wm.stl_import(filepath=os.path.join(ROOT, "stl", "stand-%s.stl" % name),
                          global_scale=0.001, forward_axis="Y", up_axis="Z")
    o = bpy.context.selected_objects[0]
    o.name = name
    me = o.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bm.to_mesh(me)
    bm.free()
    me.transform(Matrix.Rotation(-math.pi / 2, 4, "X"))   # back to standing
    lo = Vector([min(v.co[i] for v in me.vertices) for i in range(3)])
    hi = Vector([max(v.co[i] for v in me.vertices) for i in range(3)])
    me.transform(Matrix.Translation(-Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z))))
    for poly in me.polygons:
        poly.use_smooth = True
    bpy.context.view_layer.objects.active = o
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
    except Exception:
        bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    o.location = (x, y, 0)
    o.rotation_euler.z = rot_z
    me.materials.append(mat)
    return o


def camera(target, dist, az, el, lens, fstop, focus=None):
    """Camera orbiting target: az from +X (the stands' front) towards +Y, el above the desk, degrees."""
    a, e = math.radians(az), math.radians(el)
    loc = Vector(target) + dist * Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
    c = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    bpy.context.scene.collection.objects.link(c)
    c.location = loc
    c.rotation_euler = (Vector(target) - loc).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    c.data.dof.use_dof = True
    c.data.dof.aperture_fstop = fstop
    c.data.dof.focus_distance = (Vector(focus or target) - loc).length
    bpy.context.scene.camera = c


def render(name):
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print("wrote", sc.render.filepath)


def setup():
    reset()
    world()
    desk()
    return pla_material()


def shot_family():
    mat = setup()
    gap = 0.035
    for row, (tiers, x) in enumerate(((3, -0.17), (2, -0.03), (1, 0.10))):
        y = -(sum(WIDTH.values()) + 2 * gap) / 2
        for k, w in WIDTH.items():
            stand("%d%s" % (tiers, k), mat, x, y + w / 2)
            y += w + gap
    camera((-0.05, 0.0, 0.05), 1.0, 30, 26, 50, 8.0)
    render("render-01-family.png")


def shot_trio():
    mat = setup()
    stand("3M", mat, -0.06, -0.10)
    stand("2M", mat, -0.01, 0.0)
    stand("1M", mat, 0.04, 0.10)
    camera((-0.01, 0.0, 0.055), 0.70, 35, 18, 60, 4.0)
    render("render-02-trio.png")


def shot_detail():
    mat = setup()
    stand("2M", mat, 0.0, 0.0)
    camera((0.0, 0.0, 0.048), 0.48, 38, 16, 85, 2.8, focus=(0.03, 0.02, 0.03))
    render("render-03-detail-2M.png")


def shot_profile():
    mat = setup()
    stand("3W", mat, 0.0, 0.0)
    camera((0.0, 0.0, 0.07), 0.75, 78, 8, 70, 5.6, focus=(0.0, 0.06, 0.07))
    render("render-04-profile-3W.png")


SHOTS = {"family": shot_family, "trio": shot_trio, "detail": shot_detail, "profile": shot_profile}
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(SHOTS)
for a in args:
    SHOTS[a]()

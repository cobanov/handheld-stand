# Tiered display stand family for handheld consoles and old phones (devices stand closed).
#
# Variants are named <tiers><width>: 1N 1M 1W 2N 2M 2W 3N 3M 3W
#   N = narrow 50 mm, M = medium 80 mm, W = wide 120 mm.
#
# One side profile extruded along Y, printed on its side (no supports).
# Model coordinates: X = forward (towards the viewer), Z = up, Y = width.
# Each tier is the same cradle: a back plate leaning TILT degrees and a ledge square to it.
# In multi-tier stands the back plate of tier i rises into the front lip of tier i+1,
# so the profile zigzags upwards and every back plate also runs down to the base.
#
# Run inside FreeCAD:  exec(open("build_stand.py").read())
# or headless:         freecadcmd build_stand.py
# Writes stl/ (print orientation) and step/ (standing orientation) next to this file
# and prints a tipping table for the heaviest supported device of each width.
import math
import os
import FreeCAD as App
import Part
import Mesh

WIDTHS = {"N": 50.0, "M": 80.0, "W": 120.0}
T = 3.0         # wall thickness
TILT = 20.0     # lean from vertical, degrees
H0 = 10.0       # height of the front inner corner above the table (lower leaves a facet too short to round)
LEDGE = 26.0    # inner ledge depth: fits the thickest device (PSP-1000, 23 mm)
BACK = 60.0     # back plate above the ledge on the last tier
LIP = 6.0       # front lip height above the ledge
STEP = 54.0     # tier spacing along the back plate: ~41 mm higher, ~46 mm further back
REAR = 40.0     # base reach behind the last corner: backward tipping is the weak direction
R = 1.4         # profile corner rounding (just under T/2: plate ends come out nearly half-round)
R_SIDE = 1.0    # rounding of the side face that is up when printing
C_BED = 0.8     # 45 deg chamfer on the side face on the bed (a fillet there would overhang)

# closed devices: width, height, thickness (mm), mass (g); approximate public specs
DEVICES = {
    "N": {"BlackBerry Bold": (66, 114, 15, 136), "Miyoo Mini Plus": (78.5, 108, 22, 160)},
    "M": {"DS Lite": (133, 74, 21.5, 218), "3DS": (134, 74, 21, 235), "PSP-1000": (170, 74, 23, 280),
          "PSP Go": (128, 69, 16.5, 158), "PS Vita": (182, 83.5, 18.6, 260),
          "Retroid Pocket 4": (184, 81, 16, 280)},
    "W": {"Switch": (239, 102, 14, 398), "Switch OLED": (242, 102, 14, 420), "Switch Lite": (208, 91, 14, 275)},
}
PLA = 1.24 * 0.70   # g/cm3 x printed fill (2 walls + 20 % core, ~70 % of solid), for the stand's own weight in the tipping check

th = math.radians(TILT)
u = App.Vector(-math.sin(th), 0, math.cos(th))   # up along a back plate
v = App.Vector(math.cos(th), 0, math.sin(th))    # forward along a ledge


def strip(p0, d, length, n, w):
    """Rectangle p0 -> p0 + d*length, thickness T towards n, extruded w along Y."""
    pts = [p0, p0 + d * length, p0 + d * length + n * T, p0 + n * T, p0]
    return Part.Face(Part.makePolygon(pts)).extrude(App.Vector(0, w, 0))


def on_face(e, y):
    return all(abs(p.Point.y - y) < 1e-6 for p in e.Vertexes) and abs(e.BoundBox.YLength) < 1e-6


def corners(tiers):
    cs = [App.Vector(0, 0, H0)]
    for _ in range(1, tiers):
        cs.append(cs[-1] - v * (LEDGE + T) + u * STEP)
    return cs


def footprint(tiers):
    """Front and rear tipping edges on the table (x)."""
    c = corners(tiers)
    front = c[0] + v * (LEDGE + T) - u * T
    return front.x - R, c[-1].x - REAR + R


def build(tiers, w):
    cs = corners(tiers)
    parts = []
    for i, c in enumerate(cs):
        s = c.z / math.cos(th) + 2                # run down below the table, clipped later
        top = STEP + LIP if i < tiers - 1 else BACK
        parts.append(strip(c - u * s, u, s + top, v * -1, w))   # back plate
        parts.append(strip(c, v, LEDGE + T, u * -1, w))         # ledge
    c0 = cs[0]
    parts.append(strip(c0 + v * LEDGE - u * T, u, LIP + T, v, w))   # front lip (rear lips are back plates)
    f = c0 + v * (LEDGE + T) - u * T                                # front ledge underside
    parts.append(Part.makeBox(T, w, f.z, App.Vector(f.x - T, 0, 0)))    # front leg
    x0 = cs[-1].x - REAR
    parts.append(Part.makeBox(f.x - x0, w, T, App.Vector(x0, 0, 0)))  # base
    shape = parts[0].fuse(parts[1:]).removeSplitter()
    shape = shape.common(Part.makeBox(600, w, 600, App.Vector(-400, 0, 0))).removeSplitter()
    shape = shape.makeFillet(R, [e for e in shape.Edges
                                 if abs(e.Vertexes[0].Point.y - e.Vertexes[-1].Point.y) > w - 0.01])
    # soften the side faces: printed on its side with y = 0 on the bed
    shape = shape.makeFillet(R_SIDE, [e for e in shape.Edges if on_face(e, w)])
    shape = shape.makeChamfer(C_BED, [e for e in shape.Edges if on_face(e, 0.0)])
    return shape.Solids[0]   # makeChamfer wraps the solid in a compound


def tipping(shape, tiers, load):
    """Table tilt (deg) that tips the loaded stand forward / backward. load: [(tier, (w, h, t, g))]."""
    cs = corners(tiers)
    pts = [(shape.CenterOfMass, shape.Volume / 1000 * PLA)]
    pts += [(cs[i] + v * (d[2] / 2) + u * (d[1] / 2), d[3]) for i, d in load]
    m = sum(g for _, g in pts)
    x = sum(p.x * g for p, g in pts) / m
    z = sum(p.z * g for p, g in pts) / m
    xf, xr = footprint(tiers)
    return math.degrees(math.atan2(xf - x, z)), math.degrees(math.atan2(x - xr, z))


try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.path.expanduser("~/Developer/handheld-stand")
os.makedirs(os.path.join(HERE, "stl"), exist_ok=True)
os.makedirs(os.path.join(HERE, "step"), exist_ok=True)

gui = App.GuiUp
if gui:
    doc = App.ActiveDocument if App.ActiveDocument and App.ActiveDocument.Name == "Stand" else App.newDocument("Stand")
    for o in doc.Objects:
        doc.removeObject(o.Name)

print("name  size (D x W x H, standing)   volume   tip fwd / back (worst load)")
y = 0.0
for wk, w in WIDTHS.items():
    heavy = max(DEVICES[wk].values(), key=lambda d: d[3])
    for n in (1, 2, 3):
        name = "%d%s" % (n, wk)
        shape = build(n, w)
        assert shape.isValid(), name
        # worst cases: every tier loaded, front tier only, rear tier only, plus every device on its own
        loads = [[(i, heavy) for i in range(n)], [(0, heavy)], [(n - 1, heavy)]]
        loads += [[(n - 1, d)] for d in DEVICES[wk].values()]
        fw = min(tipping(shape, n, ld)[0] for ld in loads)
        bw = min(tipping(shape, n, ld)[1] for ld in loads)
        bb = shape.BoundBox
        print("%-4s  %3.0f x %3.0f x %3.0f mm        %5.1f cm3  %4.1f / %4.1f deg" % (
            name, bb.XLength, bb.YLength, bb.ZLength, shape.Volume / 1000, fw, bw))
        shape.exportStep(os.path.join(HERE, "step", "stand-%s.step" % name))
        p = shape.copy()
        p.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 90)   # chamfered side face (y = 0) onto the bed
        bb = p.BoundBox
        p.translate(App.Vector(-bb.XMin, -bb.YMin, -bb.ZMin))
        Mesh.Mesh(p.tessellate(0.05)).write(os.path.join(HERE, "stl", "stand-%s.stl" % name))
        if gui:
            shape.translate(App.Vector(-(n - 1) * 200, y, 0))      # grid: tiers along X, widths along Y
            doc.addObject("Part::Feature", "stand_" + name).Shape = shape
    y += w + 60
if gui:
    doc.recompute()

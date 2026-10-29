# Tiered Handheld Display Stand

Display stands for handheld consoles and old phones, standing closed. One, two or three tiers in three widths,
nine variants from one parametric FreeCAD script. In the multi-tier stands every device sits about 41 mm higher
than the one in front of it, so each screen stays in view. Prints on its side with no supports.

![All nine variants on a desk](images/render-01-family.png)

## Highlights

- **One profile, nine stands.** Named `<tiers><width>`: 1N 1M 1W 2N 2M 2W 3N 3M 3W, where **N** is 50 mm,
  **M** 80 mm and **W** 120 mm wide.
- **Fits the whole shelf.** PSP, PS Vita, PSP Go, 3DS, DS Lite, Miyoo Mini, Switch, Switch Lite, Switch OLED,
  Retroid Pocket 4, BlackBerry Bold and anything else up to 23 mm thick.
- **No supports, strong plates.** The stand prints on its side, so every layer is the full profile: no overhangs,
  no bridges, and the back plates are as strong as the material gets.
- **Soft edges.** 1.4 mm rounds on the profile, a 1 mm round on the top face, a 0.8 mm chamfer where it meets the bed.
- **Checked for tipping.** Every variant stays up on a table tilted at least 24° with its heaviest device on the
  worst tier.

![1M, 2M and 3M side by side](images/render-02-trio.png)

## Variants

| Variant | Tiers | Width | Size D × W × H (mm) | PLA | Time (K1) |
|---|---|---|---|---|---|
| 1N | 1 | 50 | 68 × 50 × 66 | 24 g | 48 min |
| 1M | 1 | 80 | 68 × 80 × 66 | 38 g | 1 h 15 min |
| 1W | 1 | 120 | 68 × 120 × 66 | 56 g | 1 h 50 min |
| 2N | 2 | 50 | 114 × 50 × 107 | 48 g | 1 h 18 min |
| 2M | 2 | 80 | 114 × 80 × 107 | 76 g | 2 h 1 min |
| 2W | 2 | 120 | 114 × 120 × 107 | 113 g | 2 h 57 min |
| 3N | 3 | 50 | 160 × 50 × 148 | 78 g | 2 h 3 min |
| 3M | 3 | 80 | 160 × 80 × 148 | 123 g | 3 h 10 min |
| 3W | 3 | 120 | 160 × 120 × 148 | 184 g | 4 h 41 min |

Weights and times are OrcaSlicer estimates for a Creality K1: 0.4 mm nozzle, 0.2 mm layers, 2 walls, 20 % infill.
Each 3 mm wall prints as two perimeters a side around a thin infill core: about 70 % of the solid weight,
with nearly all of its bending stiffness.

## Which width

| Width | For | Device, closed (W × H × D mm) |
|---|---|---|
| N, 50 mm | phones and small portrait devices | BlackBerry Bold 66 × 114 × 15, Miyoo Mini Plus 78.5 × 108 × 22 |
| M, 80 mm | DS family, PSP family, Vita, Retroid | DS Lite 133 × 74 × 21.5, 3DS 134 × 74 × 21, PSP-1000 170 × 74 × 23, PSP Go 128 × 69 × 16.5, PS Vita 182 × 83.5 × 18.6, Retroid Pocket 4 184 × 81 × 16 |
| W, 120 mm | Switch family | Switch 239 × 102 × 14, Switch OLED 242 × 102 × 14, Switch Lite 208 × 91 × 14 |

Device sizes are approximate public figures. The ledge takes any device up to 23 mm thick at its bottom edge;
devices wider than the stand overhang it on both sides.

![Devices on 1N, 2M and 1W](images/02-with-devices.png)

## Geometry

| | |
|---|---|
| Lean | 20° back from vertical |
| Ledge | 26 mm deep, square to the back plate, so a device slides into the corner |
| Front lip | 6 mm |
| Back plate | 60 mm above the ledge on the top tier |
| Tier step | about 41 mm up and 46 mm back |
| Walls | 3 mm |

The side profile zigzags: the back plate of each tier rises into the front lip of the tier behind it, and every
back plate also runs down to the base.

![Side profiles of 1M, 2M and 3M](images/03-profiles.png)

![3W from the side](images/render-04-profile-3W.png)

## Stability

The table tilt it takes to tip a loaded stand over, worst case over these loads: every tier loaded, front tier
only, rear tier only, and each listed device alone on the top tier, always with the heaviest device of the width
class (Miyoo Mini Plus, PSP-1000, Switch OLED).

| Variant | Forward | Backward |
|---|---|---|
| 1N | 30.3° | 25.4° |
| 1M | 32.5° | 35.1° |
| 1W | 33.6° | 27.7° |
| 2N | 34.6° | 21.8° |
| 2M | 37.2° | 25.9° |
| 2W | 37.3° | 21.9° |
| 3N | 39.7° | 22.5° |
| 3M | 41.9° | 24.1° |
| 3W | 41.5° | 21.4° |

Backward is the weak direction because the devices lean back. The stand's own weight is taken as printed (about
70 % of solid). `build_stand.py` prints this table on every run.

## Printing

- **Orientation:** on its side, as the STLs come, with the chamfered side face on the bed.
- **Material:** PLA or PETG.
- **Settings:** 0.2 mm layers, 2 walls, 15–20 % infill, no supports.
- **Adhesion:** the side face on the bed is chamfered, so each 3 mm wall touches the bed with only about 1.4 mm.
  Use an 8 mm brim with no gap to the part, a 60 °C bed and no side (auxiliary) fan, and keep the door closed;
  without these the ends lift. The chamfer hides the brim scar once it is snapped off.

![2M close-up](images/render-03-detail-2M.png)

## Files

| Path | What |
|---|---|
| `build_stand.py` | The whole design. All dimensions are parameters at the top. |
| `stl/stand-*.stl` | Print-ready STLs, already on their side |
| `step/stand-*.step` | STEP files, standing upright |
| `stand.FCStd` | FreeCAD document with all nine variants |
| `profiles/k1_stand_process.json` | OrcaSlicer process for the Creality K1 |
| `slice_k1.sh` | Slices every variant with that profile and generic PLA into `gcode/k1-pla/`, plus a test plate with 1M and 2M |
| `render/render_stands.py` | Blender (Cycles) scene for the renders; HDRI and oak texture from Poly Haven (CC0) in `render/assets/` |
| `images/` | `render-*.png` are the Blender renders, the numbered PNGs FreeCAD views |

```sh
freecadcmd build_stand.py                        # STL + STEP for all nine variants, tipping table
./slice_k1.sh                                    # G-code for a K1 (needs OrcaSlicer)
blender -b -P render/render_stands.py            # renders into images/ (PREVIEW=1 for a quick low-res pass)
```

Inside the FreeCAD GUI, `exec(open("build_stand.py").read())` also adds the nine stands to a document.
For a device thicker than 23 mm raise `LEDGE`; for another width add an entry to `WIDTHS`.

## Licence

Code (`build_stand.py`, `slice_k1.sh`, `render/render_stands.py`) is MIT, see [LICENSE](LICENSE). The models
(`stl/`, `step/`, `stand.FCStd` and the geometry `build_stand.py` produces) and the images are
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), see [LICENSE-models.md](LICENSE-models.md).

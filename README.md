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
| 1N | 1 | 50 | 68 × 50 × 66 | 33 g | 46 min |
| 1M | 1 | 80 | 68 × 80 × 66 | 53 g | 1 h 11 min |
| 1W | 1 | 120 | 68 × 120 × 66 | 80 g | 1 h 43 min |
| 2N | 2 | 50 | 114 × 50 × 107 | 67 g | 1 h 24 min |
| 2M | 2 | 80 | 114 × 80 × 107 | 107 g | 2 h 11 min |
| 2W | 2 | 120 | 114 × 120 × 107 | 160 g | 3 h 12 min |
| 3N | 3 | 50 | 160 × 50 × 148 | 108 g | 2 h 9 min |
| 3M | 3 | 80 | 160 × 80 × 148 | 173 g | 3 h 21 min |
| 3W | 3 | 120 | 160 × 120 × 148 | 259 g | 4 h 57 min |

Weights and times are OrcaSlicer estimates for a Creality K1: 0.4 mm nozzle, 0.2 mm layers, 3 walls, 20 % infill.
At these settings the 3 mm walls come out nearly solid.

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
| 1N | 31.0° | 26.9° |
| 1M | 33.3° | 36.2° |
| 1W | 34.2° | 28.9° |
| 2N | 36.7° | 24.6° |
| 2M | 39.3° | 28.2° |
| 2W | 39.0° | 24.3° |
| 3N | 40.6° | 26.0° |
| 3M | 42.7° | 27.5° |
| 3W | 42.2° | 24.9° |

Backward is the weak direction because the devices lean back. `build_stand.py` prints this table on every run.

## Printing

- **Orientation:** on its side, as the STLs come, with the chamfered side face on the bed.
- **Material:** PLA or PETG.
- **Settings:** 0.2 mm layers, 3 walls, 15–20 % infill, no supports. A 5 mm outer brim helps the tall W variants;
  N and M print fine without one.

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

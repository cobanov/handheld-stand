#!/bin/bash
# Slice every stand variant plus the 1M+2M test plate for a Creality K1 with generic PLA, into gcode/k1-pla/.
# Profiles: profiles/k1_stand_process.json + profiles/k1_pla_filament.json (Creality Generic PLA @K1-all, inherits resolved).
H=$(cd "$(dirname "$0")" && pwd)
P=/Applications/OrcaSlicer.app/Contents/Resources/profiles/Creality
O=/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer
mkdir -p "$H/gcode/k1-pla"
sl() {
  out=$1; shift
  t=$(mktemp -d)
  "$O" --load-settings "$P/machine/Creality K1 (0.4 nozzle).json;$H/profiles/k1_stand_process.json" \
       --load-filaments "$H/profiles/k1_pla_filament.json" \
       --arrange 1 --slice 0 --outputdir "$t" "$@" > "$t/log.txt" 2>&1
  if [ -f "$t/plate_1.gcode" ]; then
    f="$H/gcode/k1-pla/$out"; mv "$t/plate_1.gcode" "$f"
    # the CLI fills settings it can't resolve with its own defaults (a system profile's inherits gave 200 °C, 20 % fan),
    # so refuse a gcode that doesn't carry the PLA profile
    for k in nozzle_temperature fan_min_speed additional_cooling_fan_speed filament_flow_ratio filament_density cool_plate_temp_initial_layer; do
      want=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]][0])" "$H/profiles/k1_pla_filament.json" $k)
      grep -q "^; $k = $want\$" "$f" || { echo "$out: $k is not $want"; exit 1; }
    done
    echo "$out | $(grep -m1 'estimated printing time (normal mode)' "$f" | sed 's/.*= //') | $(grep -m1 '^; filament used \[g\]' "$f" | sed 's/.*= //') g"
  else
    echo "$out FAILED"; tail -3 "$t/log.txt"
  fi
}
for n in 1N 1M 1W 2N 2M 2W 3N 3M 3W; do sl "stand-${n}_PLA.gcode" "$H/stl/stand-$n.stl"; done
sl "test-1M+2M_PLA.gcode" "$H/stl/stand-1M.stl" "$H/stl/stand-2M.stl"
sl "plate-2x1M_PLA.gcode" "$H/stl/stand-1M.stl" "$H/stl/stand-1M.stl"

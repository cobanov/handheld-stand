#!/bin/bash
# Slice every stand variant plus the 1M+2M test plate for a Creality K1 with generic PLA, into gcode/k1-pla/.
H=$(cd "$(dirname "$0")" && pwd)
P=/Applications/OrcaSlicer.app/Contents/Resources/profiles/Creality
O=/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer
mkdir -p "$H/gcode/k1-pla"
sl() {
  out=$1; shift
  t=$(mktemp -d)
  "$O" --load-settings "$P/machine/Creality K1 (0.4 nozzle).json;$H/profiles/k1_stand_process.json" \
       --load-filaments "$P/filament/Creality Generic PLA @K1-all.json" \
       --arrange 1 --slice 0 --outputdir "$t" "$@" > "$t/log.txt" 2>&1
  if [ -f "$t/plate_1.gcode" ]; then
    f="$H/gcode/k1-pla/$out"; mv "$t/plate_1.gcode" "$f"
    mm=$(grep -m1 '^; filament used \[mm\]' "$f" | sed 's/.*= //')
    # the generic PLA profile has no density, so grams come from length (1.75 mm, 1.24 g/cm3)
    echo "$out | $(grep -m1 'estimated printing time (normal mode)' "$f" | sed 's/.*= //') | $(python3 -c "print(round($mm*2.405*1.24/1000))") g"
  else
    echo "$out FAILED"; tail -3 "$t/log.txt"
  fi
}
for n in 1N 1M 1W 2N 2M 2W 3N 3M 3W; do sl "stand-${n}_PLA.gcode" "$H/stl/stand-$n.stl"; done
sl "test-1M+2M_PLA.gcode" "$H/stl/stand-1M.stl" "$H/stl/stand-2M.stl"

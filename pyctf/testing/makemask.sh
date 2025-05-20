#! /bin/sh

template="$1"
maskname="8mm"

3dfractionize -template $template -input mask+orig -prefix maskA -clip 0
3dcalc -a maskA+orig -expr 'step(a-4000)' -prefix mask${maskname}.nii
rm maskA+orig.*

#3dcalc -a $template -b mask${maskname}.nii -expr 'a*b' -prefix mu.nii

#3dAutomask -prefix Temp -dilate 1 TT_N27+tlrc
#3dresample -rmode NN -dxyz 8 8 8 -prefix Mask8mm -inset Temp+tlrc

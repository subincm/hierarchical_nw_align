#!/bin/bash

GEN=( CG_set DMC_set DMR_set)
FAM=( Family_1 Family_2 Family_3 Family_4 Family_5 )

for g in "${GEN[@]}"
do
   :
    for f in "${FAM[@]}"
    do
      :      
      list2leda ../Data/NAPAbench/5-way/${g}/${f}/A.net >A.gw
      list2leda ../Data/NAPAbench/5-way/${g}/${f}/B.net >B.gw
      python MI-GRAALRunner.py B.gw A.gw ${g}_${f}_A_B -p 3
      rm -rf A.gw B.gw
    done
done
#!/bin/bash

grep -R --include="OURS_result.txt" 'ICS = ' $1 | sed -r 's/:ICS =//' >./ours_ics.txt
grep -R --include="OURS_result.txt" 'Edge correctness' $1 | sed -r 's/:Edge correctness [0-9]+ \/ [0-9]+ =//' >./ours_ec.txt
grep -R --include="PROF_result.txt" 'ICS = ' $1 | sed -r 's/:ICS =//' >./prof_ics.txt
grep -R --include="PROF_result.txt" 'Edge correctness' $1 | sed -r 's/:Edge correctness [0-9]+ \/ [0-9]+ =//' >./prof_ec.txt

sed -n -e '0~3p' ./ours_ics.txt >./ours_ics_curated.txt
sed -n -e '0~3p' ./ours_ec.txt >./ours_ec_curated.txt
sed -n -e '0~3p' ./prof_ics.txt >./prof_ics_curated.txt
sed -n -e '0~3p' ./prof_ec.txt >./prof_ec_curated.txt

./compare.py ./ours_ec_curated.txt ./prof_ec_curated.txt
./compare.py ./ours_ics_curated.txt ./prof_ics_curated.txt

rm -f ./ours_*.txt ./prof_*.txt
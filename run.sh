#!/bin/bash

f=$1
echo $f
out=reg.rs

python3 generate_define.py $f> $out
python3 generate_typedef_struct.py $f >> $out


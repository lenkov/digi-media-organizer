#!/bin/bash
# make md5 checksums of all files in each folder/sub-folder
# and saves md5.txt in each top-level folder

IFS=$'\n'

for i in `find * -type d -maxdepth 0`; do
    cd $i
    files=(`find * -type f | egrep -v "md5.txt|DS_Store"`) 
    echo "Scanning folder $i, files: ${#files[@]}"
    md5 ${files[*]} > md5.txt
    cd ..
done




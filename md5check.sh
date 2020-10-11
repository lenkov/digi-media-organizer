#!/bin/bash
# Compare the md5 checksums of all files with the content of md5.txt and prints the difference
# Only top-level folders have md5.txt

IFS=$'\n'

for i in `find * -type d -maxdepth 0`; do
    cd $i
    files=(`find * -type f | egrep -v "md5.txt|DS_Store"`) 
    echo "Scanning folder $i, files: ${#files[@]}"
    (cat md5.txt ; md5 ${files[*]}) | sort | uniq -c | grep -v "^   2 "
    cd ..
done

# Calculates the md5 sum of all files in the current folder (with all sub-folders) 
# and saves it in a md5.txt
# Compatible with the command line:
# find * -type f  \( ! -iname "md5.txt" -and ! -iname "*DS_Store"  \) -print0 | xargs -0 md5 > md5-new.txt
# usage:
#     python3.8 md5.py

import os
import hashlib

IGNORE_FILES = ["md5.txt", ".DS_Store"]
MD5_FILE = "md5.txt"

cur_dir = os.getcwd()

md5s = {}

def calc_md5(file):
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    
    return file_hash.hexdigest()

def save_md5_to_file(dir, file_md5s):
    fn = os.path.join(cur_dir, dir, MD5_FILE)
    print (f"Writing {fn}, with {len(file_md5s.keys())} md5s")
    with open(fn, "w") as f:
        for key in file_md5s.keys():
            f.write (f"MD5 ({key}) = {file_md5s[key]}\n")

# collect all MD5 for all files
for root, dirs, files in os.walk(cur_dir, topdown=True):
    rel_dir = root.replace(cur_dir,"").lstrip("/");
    top_dir = rel_dir.split("/",1)[0]
    sub_dir = "".join(rel_dir.split("/",1)[1:])

    # skip the root folder (we don't expect files here)
    if (len(top_dir)==0):
        continue

    print (f"Processing folder [{rel_dir}] with {len(files)} files...")    

    # create an empty dict for all new dirs
    if (top_dir not in md5s.keys()):
        md5s[top_dir] = {}

    for fname in files:
        # Ignore the files we need to skip
        if (fname in IGNORE_FILES):
            continue

        # put the md5s in a dict with key the top folder name
        md5s[top_dir][os.path.join(sub_dir, fname)] = calc_md5(os.path.join(root, fname))

# write all md5s to files
for dir in md5s.keys():
    save_md5_to_file(dir,md5s[dir])


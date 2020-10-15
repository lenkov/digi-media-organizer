# Checks or updated the the md5 sum of all files in the current folder (with all sub-folders)
# The md5 sums are stored in a file md5.txt in each sub-folder
# Compatible with the command line:
# find * -type f  \( ! -iname "md5.txt" -and ! -iname "*DS_Store"  \) -print0 | xargs -0 md5 > md5-new.txt
# Usage:
#     python3.8 md5.py comp     - checks the MD5 sums of all files against the md5.txt file
#     python3.8 md5.py update   - updates (overwrites if exist) the md5.txt file in each folder


import os
import sys
import hashlib

IGNORE_FILES = ["md5.txt", ".DS_Store"]
MD5_FILE     = "md5.txt"
CUR_DIR      = os.getcwd()

md5s    = {}
stats   = {"n_folders": 0, "n_files": 0, "n_md5_txt": 0, "n_md5_sums": 0, "n_matched_md5s": 0, 
           "n_wrong_md5s": 0, "n_missing_on_fs": 0, "n_missing_in_txt": 0}

def calc_md5(file):
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    
    return file_hash.hexdigest()


def save_md5s_to_file(top_dir, md5s):
    fn = os.path.join(CUR_DIR, top_dir, MD5_FILE)
    print (f"Writing [{len(md5s.keys())}] md5s to [{top_dir}/{MD5_FILE}]")
    with open(fn, "w") as f:
        stats["n_md5_txt"] += 1
        for key in md5s.keys():
            f.write (f"MD5 ({key}) = {md5s[key]}\n")
            stats["n_md5_sums"] += 1


def comp_md5s_to_file(top_dir, md5s):
    fn = os.path.join(CUR_DIR, top_dir, MD5_FILE)
    print (f"Comparing md5s in [{top_dir}]")
    with open(fn, "r") as f:
        md5_txt = f.readlines()

    stats["n_md5_txt"] += 1
    for line in md5_txt:
        stats["n_md5_sums"] += 1
        line = line.rstrip('\n')                # remove the trailing newline
        md5 = line[-32:]                        # extract the md5 sum (last 32 chars)
        fn = line[5:-36]

        if (fn in md5s.keys()):
            if (md5 == md5s[fn]):
                stats["n_matched_md5s"] += 1
            else:
                print (f"Failed md5 sum: [{top_dir}/{fn}], md5(from fs): [{md5s[fn]}], from {MD5_FILE}: [{md5}]")
                stats["n_wrong_md5s"] += 1
            del md5s[fn]                        # remove this file as the md5 matches
        
        else:
            print (f"File [{top_dir}/{fn}] exist in {MD5_FILE}, but not on the file system")
            stats["n_missing_on_fs"] += 1

    # if a key is not removed -> the file was missing in the md5.txt
    for fn in md5s.keys():
        print (f"File [{top_dir}/{fn}] exist on the file system, but not in {MD5_FILE}")
        stats["n_missing_in_txt"] += 1


# collect all MD5 for all files in "CUR_DIR" in the "md5s" dictionary 
def calc_md5s():
    for root, dirs, files in os.walk(CUR_DIR, topdown=True):
        rel_dir = root.replace(CUR_DIR,"").lstrip("/");
        top_dir = rel_dir.split("/",1)[0]
        sub_dir = "".join(rel_dir.split("/",1)[1:])

        # skip the root folder (we don't expect files here)
        if (len(top_dir)==0):
            continue

        print (f"Computing md5s in [{rel_dir}] with [{len(files)}] files...")
        stats["n_folders"] +=1 

        # create an empty dict for all new dirs
        if (top_dir not in md5s.keys()):
            md5s[top_dir] = {}

        for fname in files:
            # Ignore the files we need to skip
            if (fname in IGNORE_FILES):
                continue

            # put the md5s in a dict with a key = top folder name
            md5s[top_dir][os.path.join(sub_dir, fname)] = calc_md5(os.path.join(root, fname))
            stats["n_files"] += 1



##################################################
# main ###########################################
##################################################

# validate command-line arguments
if (len(sys.argv)<2 or sys.argv[1].lower() not in ["comp","update"]):
    print (f"Usage md5.py [ comp | update ]")
    exit()

# calculate the md5s on all files
calc_md5s()

# on update write all md5s to files
if (sys.argv[1].lower() == "update"):
    for top_dir in md5s.keys():
        save_md5s_to_file(top_dir,md5s[top_dir])
# on compare, check the current md5s against the content of md5.txt in each folder
elif (sys.argv[1].lower() == "comp"):
    for top_dir in md5s.keys():
        comp_md5s_to_file(top_dir,md5s[top_dir])

# show the stats
print (stats)


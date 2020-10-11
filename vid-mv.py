# Move the video files to a separate dir in the same folder.
# before using adjust the SRC_DIR and DEST_DIR
# usage:
#     python3.8 vid-mv.py


import os

SRC_DIR     = "/Volumes/1TB/Photos"
DEST_DIR    = "/Volumes/1TB/Videos"
VIDEO_EXT   = ("MOV", "MP4", "AVI", "M4V", "MTS")

total = 0
moved = 0
size  = 0

for root, dirs, files in os.walk(SRC_DIR, topdown=True):
   for fname in files:
        file_full_path = os.path.join(root, fname)
        _, file_ext = os.path.splitext(fname)


        # We will only move video files
        if file_ext.upper()[1:] in VIDEO_EXT:
            total += 1
            size += os.path.getsize(file_full_path)

            # compose the destination folder
            rel_path = root.replace(SRC_DIR,"").lstrip("/")
            dest_folder = os.path.join(DEST_DIR, rel_path)

            # make (recursively) the folder if not exist        
            if (not os.path.isdir(dest_folder)):
                print (f"creating {dest_folder} because it does not exist")
                os.makedirs(dest_folder) 
            # move the video file to the dest location
            print (f"moving {file_full_path} to {os.path.join(dest_folder,fname)}")
            os.rename(file_full_path, os.path.join(dest_folder,fname))
            moved += 1

print (f" total: {total}, moved: {moved}, total size: {size/1024/1024/1024:.2f}GB")


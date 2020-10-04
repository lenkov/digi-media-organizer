# Digital Media Organizer - main file
# before using adjust the SRC_DIR and DEST_DIR
# usage:
#     python3.8 dmo.py


import os
import time
import sys
import subprocess
from datetime import datetime, timezone
import pytz

SRC_DIR                 = "/Users/lenkov/Desktop/Photos/Masters"
DEST_DIR                = "/Users/lenkov/Desktop/Photos/Dest/"
SUPPORTED_MEDIA_EXT     = ("HEIC", "JPG", "JPEG", "MOV", "PNG", "MP4")
EXIF_PARAM_DATE         = "kMDItemFSCreationDate"
EXIF_PARAM_LONG         = "kMDItemLongitude"
EXIT_PARAM_LATI         = "kMDItemLatitude"
GEO_LOCATIONS           = ( #                            Lati         Long    
                            #  City(0)              Min(1)  Max(2) Min(3)  Max(4)
                            ( "LosAltos",           37.34 , 37.41,  -122.12, -122.06),
                            ( "Saratoga",           37.23 , 37.30,  -122.08, -121.99),
                            ( "Woodside",           37.36 , 37.46,  -122.28, -122.24),
                            ( "PaloAlto",           37.39 , 37.45,  -122.20, -122.09),
                            ( "SanFrancisco",       37.70 , 37.81,  -122.52, -122.36),
                            ( "RanchoSanAntonio",   37.32 , 37.35,  -122.15, -122.08),
                            ( "Aptos",              36.92 , 37.00,  -121.94, -121.85),
                            ( "MossBeach",          37.50 , 37.55,  -122.53, -122.49),
                            ( "SeaRanch",           38.40 , 39.50,  -123.86, -123.05),
                            ( "Truckee",            39.31 , 39.50,  -120.30, -120.09),
                            ( "CastlePeak",         39.34 , 39.37,  -120.38, -120.32),
                            ( "Kirkwood",           38.62 , 38.72,  -120.12, -120.00),
                            ( "KingsBeach",         39.18 , 39.26,  -120.12, -120.00),
                            ( "SquawValley",        39.18 , 39.22,  -120.30, -120.19),
                            ( "InclineVillage",     39.22 , 39.37,  -120.00, -119.91),
                            ( "MtRose",             39.27 , 39.35,  -119.94, -119.84),
                            ( "SugarBowl",          39.28 , 39.32,  -120.36, -120.30),
                            ( "SoutLakeTahoe",      38.91 , 38.98,  -120.03, -119.92),
                            ( "EmeraldBay",         38.93 , 38.98,  -120.14, -120.04),
                            ( "Yosemite",           37.52 , 37.95,  -120.13, -119.07),
                            ( "JoshuaTreePark",     33.66 , 34.11,  -116.47, -115.22),
                            ( "Independence",       44.79 , 44.90,  -123.22, -123.00),
                            ( "Maui",               20.57 , 21.03,  -156.73, -155.90),
                            ( "LakeGeorge",         43.39 , 43.78,   -73.72,  -73.46),
                            ( "Barcelona",          41.17 , 42.43,     1.81,    3.45),
                            ( "Limnos",             39.72 , 40.10,    24.88,   25.52)
                          )

# GEO_LOCATIONS columns
GL_CITY                 = 0
GL_MIN_LATI             = 1
GL_MAX_LATI             = 2
GL_MIN_LONG             = 3
GL_MAX_LONG             = 4

total = 0
has_geo = 0
found_city = 0
no_city = 0
moved = 0

for root, dirs, files in os.walk(SRC_DIR, topdown=True):
   for fname in files:
        file_full_path = os.path.join(root, fname)
        _, file_ext = os.path.splitext(fname)
        
        # We will only process media files
        if file_ext.upper()[1:] in SUPPORTED_MEDIA_EXT:
            total += 1

            # get the file date in YYYY-MM-DD format from the file name
            tm = time.localtime(os.path.getmtime(file_full_path))         
            file_date_year = time.strftime("%Y", tm)
            file_date_mm   = time.strftime("%m", tm)
            file_date_mmdd = time.strftime("%m-%d", tm)

            # zero the long/lati/date
            exif_long = 0
            exif_lati = 0
            match_city = ""

            # use the "mdls" to get the Exif information
            proc = subprocess.Popen(['mdls', file_full_path],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,_ = proc.communicate()
            list = stdout.splitlines()

            # iterate over all Exif params to find date and geo-location (long/lati)
            for i in list:
                s = i.decode("utf-8").strip("'")
                x = s.split("=")
                if (len(x) < 2):        # if we don't have param = value, go to next line
                    continue
                param = x[0].strip()
                value = x[1].strip()

                # Try to gået the media creation date and geo-location
                if (param == EXIF_PARAM_DATE):
                    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S %z")    # convert them to PST (UTC-7) from GMT (UTC+0)
                    ndt = dt.astimezone(pytz.timezone('US/Pacific'))
                    file_date_year = ndt.strftime("%Y")
                    file_date_mm   = ndt.strftime("%m")
                    file_date_mmdd = ndt.strftime("%m-%d")
                elif (param == EXIF_PARAM_LONG):
                    exif_long = float(value)
                elif (param == EXIT_PARAM_LATI):
                    exif_lati = float(value)

            # componse the folder name based on long/lati 
            if (exif_long != 0 and exif_lati != 0):
                has_geo += 1
                # iterate over all know locations and try to find the city
                for loc in GEO_LOCATIONS:
                    if (loc[GL_MIN_LONG] < exif_long < loc[GL_MAX_LONG] and loc[GL_MIN_LATI] < exif_lati < loc[GL_MAX_LATI]):
                        match_city = loc[GL_CITY]
                        
                if (len(match_city) > 0):
                    found_city += 1
                    folder = os.path.join(DEST_DIR, file_date_year, file_date_mm + "-" + match_city)
                else:
                    no_city += 1
                    str_long = str(abs(round(exif_long*10)))
                    str_lati = str(abs(round(exif_lati*10)))
                    folder = os.path.join(DEST_DIR, file_date_year, file_date_mm + "-" + str_long + "-" + str_lati)
            else:
                folder = os.path.join(DEST_DIR, file_date_year, file_date_mmdd)

            # make (recursively) the folder if not exist        
            if (not os.path.isdir(folder)):
                print (f"creating {folder} because it does not exist")
                os.makedirs(folder) 
            # move the media file to the right location
            print (f"moving {fname} to {folder}")
            os.rename(file_full_path, os.path.join(folder,fname))
            moved += 1

print (f" total: {total}, has_geo: {has_geo}, found_city : {found_city}, no_city: {no_city}, moved: {moved}")


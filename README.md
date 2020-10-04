# digi-media-organizer
Digital Media Organizer will sort your photos and videos in folders. It starts by scanning a source folder, identifies all media (photos, videos) files and then moves them into the destination folder organied in sub-folders. The first sub-folder is always the year when the media was created (got from file name or Exif info) and the second folder is either:
MM-City (if we can resolve the exif geo data to a city) 
MM-Long-Lat (if we can't find the city based on the geo data)
MM-DD (if no geo-data)

The current version is using a static DB for mapping Long,Lati to a city. 

Note: this app requires [mdls](https://ss64.com/osx/mdls.html) in order to extract the Exif info. It works only on Mac.

# TODO
* Start using an API to resolve Long,Lati to a city. 
* Group same events in the same folder even when in different days/months.

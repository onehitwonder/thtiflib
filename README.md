# thtiflib
parsing Tif files with a pure python library (no external dependencies)

  - read metadata (Tif-tags) for single or multipage Tif-files
  - split a multipage tif or save selected pages as a new tif
  - quite easy to use command-line interface

right now, this project should be considered as experimental


###example code
```
from thtiflib import Tiff

# load file
tif = Tiff("test.tif")

# print out the number of pages
print tif.pagecount()

# accessing field tags
# ifds is a list, each element represents one page
print tif.ifds[0]["fields"]["ImageWidth"]
print tif.ifds[0]["fields"]["ImageLength"]

# split the tif into tifs with 1 page max and save them as test-splitted-.tif
tif.split(pageperfile=1, basename="test-splitted")

# save pages 1, 4 and 10 as test-1_4_10.tif
tif.savepages([1, 4, 10], filename="test-1_4_10.tif")

# you should always close the tif
tif.close()
```
###command-line interface usage
```
usage: thtif_cmd.py [-h] [-m] [-a] [-c] [-s SPLIT]
                    [-p SAVEPAGES [SAVEPAGES ...]]
                    [-pft SAVEPAGEFT SAVEPAGEFT] [-o OUTFILE]
                    infile

positional arguments:
  infile                input tif file

optional arguments:
  -h, --help            show this help message and exit
  -m, --showmeta        display tif metadata (only first page)
  -a, --showallmeta     display tif metadata for every page
  -c, --countpages      display the number of pages
  -s SPLIT, --split SPLIT
                        split into tifs with maximum SPLIT pages
  -p SAVEPAGES [SAVEPAGES ...], --savepages SAVEPAGES [SAVEPAGES ...]
                        save the given pages, for example "--savepages 1 3 10"
                        saves page 1,3 and 10 in that order. requires -o / --outfile
  -pft SAVEPAGEFT SAVEPAGEFT, --savepageft SAVEPAGEFT SAVEPAGEFT
                        save all pages from n to m, for example "--savepageft 2 5"
                        saves all pages from 2 to 5. requires -o / --outfile
  -o OUTFILE, --outfile OUTFILE
                        basename of outfile (without extension, just the basename)
```

# -*- coding: utf-8 -*-
#
#  thtif_cmd.py
#  
#  Copyright 2016 Thomas Haßler
#  
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Dieses Programm ist Freie Software: Sie können es unter den Bedingungen
#    der GNU Lesser General Public License, wie von der Free Software Foundation,
#    Version 3 der Lizenz oder (nach Ihrer Wahl) jeder neueren
#    veröffentlichten Version, weiterverbreiten und/oder modifizieren.
#
#    Dieses Programm wird in der Hoffnung, dass es nützlich sein wird, aber
#    OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
#    Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
#    Siehe die GNU Lesser General Public License für weitere Details.
#
#    Sie sollten eine Kopie der GNU Lesser General Public License zusammen mit diesem
#    Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.


import argparse
import os
from thtiflib import Tiff

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="input tif file")
parser.add_argument("-m", "--showmeta", help="display tif metadata (only first page)", action="store_true")
parser.add_argument("-a", "--showallmeta", help="display tif metadata for every page", action="store_true")
parser.add_argument("-c", "--countpages", help="display the number of pages", action="store_true")
group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--split", help="split into tifs with maximum SPLIT pages", type=int)
group.add_argument("-p", "--savepages", help="save the given pages, for example \"--savepages 1 3 10\" saves page 1,3 and 10 in that order. requires -o / --outfile", type=int, nargs='+')
group.add_argument("-pft", "--savepageft", help="save all pages from n to m, for example \"--savepageft 2 5\" saves all pages from 2 to 5. requires -o / --outfile", type=int, nargs=2)
parser.add_argument("-o", "--outfile", help="basename of outfile (without extension, just the basename)", type=str)
args = parser.parse_args()

if (args.savepages or args.savepageft or args.split) and (args.outfile is None):
    parser.error('-o / --outfile argument is required for splitting/saving.')
if not os.path.isfile(args.infile):
    print "infile not found"
    sys.exit(2)
try:
    tif = Tiff(args.infile)
except Exception as e:
    print "error parsing tif"
    print e
    sys.exit(2)

if args.countpages:
    print "***countpages***"
    print "%d" %tif.pagecount()
    print "***/countpages***"

if args.showmeta:
    tif._readtags([0])
    print "***showmeta***"
    print
    ifd = tif.ifds[0]
    for field in sorted(ifd["fields"]):
        if type(ifd["fields"][field])==list:
            if len(ifd["fields"][field])==1:
                print "%s:" %field, ifd["fields"][field][0]
            elif len(ifd["fields"][field])>4:
                print "%s:" %field, str(ifd["fields"][field][:4])[:-1]+", ...]"
            else:
                print "%s:" %field, str(ifd["fields"][field])
        else:
            print "%s:" %field, ifd["fields"][field]
    print
    print "***/showmeta***"

if args.showallmeta:
    tif._readtags()
    print "***showallmeta***"
    print
    pageno = 1
    for ifd in tif.ifds:
        print "Page: %d" %pageno
        pageno +=1
        for field in sorted(ifd["fields"]):
            if type(ifd["fields"][field])==list:
                if len(ifd["fields"][field])==1:
                    print "%s:" %field, ifd["fields"][field][0]
                elif len(ifd["fields"][field])>4:
                    print "%s:" %field, str(ifd["fields"][field][:4])[:-1]+", ...]"
                else:
                    print "%s:" %field, str(ifd["fields"][field])
            else:
                print "%s:" %field, ifd["fields"][field]
        print
    print "***/showallmeta***"  
  
if args.split:
  tif.split(pageperfile=args.split, basename=args.outfile) 
  print args.outfile+".tif's saved"
  
if args.savepageft:
    tif.savepages(range(args.savepageft[0], args.savepageft[1]+1), filename=args.outfile+".tif")
    print args.outfile+".tif saved"
    
if args.savepages:
    tif.savepages(args.savepages, filename=args.outfile+".tif")
    print args.outfile+".tif saved"

tif.close()

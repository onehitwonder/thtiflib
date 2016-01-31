# -*- coding: utf-8 -*-
#
#  thtiflib.py
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

import struct
import cStringIO
import os
import sys
import time


TIFFTAGS = {
    254: {"name":"NewSubfileType", "type":("LONG")}, 
    255: {"name":"SubfileType", "type":("SHORT")}, 
    256: {"name":"ImageWidth", "type":("SHORT", "LONG")}, 
    257: {"name":"ImageLength", "type":("SHORT", "LONG")}, 
    258: {"name":"BitsPerSample", "type":("SHORT")}, 
    259: {"name":"Compression", "type":("SHORT"), 
                "valuenames":{
                    1:"Uncompressed", 
                    2:"CCITT 1D", 
                    3:"Group 3 Fax", 
                    4:"Group 4 Fax", 
                    5:"LZW", 
                    6:"JPEG", 
                    32773:"PackBits"
                }}, 
    262: {"name":"PhotometricInterpretation", "type":("SHORT"), 
                "valuenames":{
                    0:"WhiteIsZero", 
                    1:"BlackIsZero", 
                    2:"RGB", 
                    3:"RGB Palette", 
                    4:"Transparency mask", 
                    5:"CMYK", 
                    6:"YCbCr", 
                    8:"CIELab"
                }},  
    263: {"name":"Threshholding", "type":("SHORT")}, 
    264: {"name":"CellWidth", "type":("SHORT")}, 
    265: {"name":"CellLength", "type":("SHORT")}, 
    266: {"name":"FillOrder", "type":("SHORT")}, 
    269: {"name":"DocumentName", "type":("ASCII")}, 
    270: {"name":"ImageDescription", "type":("ASCII")}, 
    271: {"name":"Make", "type":("ASCII")}, 
    272: {"name":"Model", "type":("ASCII")}, 
    273: {"name":"StripOffsets", "type":("SHORT", "LONG")}, 
    274: {"name":"Orientation", "type":("SHORT")}, 
    
    277: {"name":"SamplesPerPixel", "type":("SHORT")}, 
    278: {"name":"RowsPerStrip", "type":("SHORT", "LONG")}, 
    279: {"name":"StripByteCounts", "type":("SHORT", "LONG")}, 
    280: {"name":"MinSampleValue", "type":("SHORT")}, 
    281: {"name":"MaxSampleValue", "type":("SHORT")}, 
    282: {"name":"XResolution", "type":("RATIONAL")}, 
    283: {"name":"YResolution", "type":("RATIONAL")}, 
    284: {"name":"PlanarConfiguration", "type":("SHORT")}, 
    285: {"name":"PageName", "type":("ASCII")}, 
    286: {"name":"XPosition", "type":("RATIONAL")}, 

    287: {"name":"YPosition", "type":("RATIONAL")}, 
    288: {"name":"FreeOffsets", "type":("LONG")}, 
    289: {"name":"FreeByteCounts", "type":("LONG")}, 
    290: {"name":"GrayResponseUnit", "type":("SHORT")}, 
    291: {"name":"GrayResponseCurve", "type":("SHORT")}, 
    292: {"name":"T4Options", "type":("LONG")}, 
    293: {"name":"T6Options", "type":("LONG")}, 
    296: {"name":"ResolutionUnit", "type":("SHORT")}, 
    297: {"name":"PageNumber", "type":("SHORT")}, 
    301: {"name":"TransferFunction", "type":("SHORT")},
    
    305: {"name":"Software", "type":("ASCII")}, 
    306: {"name":"DateTime", "type":("ASCII")}, 
    315: {"name":"Artist", "type":("ASCII")}, 
    316: {"name":"HostComputer", "type":("ASCII")}, 
    317: {"name":"Predictor", "type":("SHORT")}, 
    318: {"name":"WhitePoint", "type":("RATIONAL")}, 
    319: {"name":"PrimaryChromaticities", "type":("RATIONAL")}, 
    320: {"name":"ColorMap", "type":("SHORT")}, 
    321: {"name":"HalftoneHints", "type":("SHORT")}, 
    322: {"name":"TileWidth", "type":("SHORT", "LONG")}, 
    323: {"name":"TileLength", "type":("SHORT", "LONG")},
    324: {"name":"TileOffsets", "type":("LONG")}, 
    325: {"name":"TileByteCounts", "type":("SHORT", "LONG")}, 
    332: {"name":"InkSet", "type":("SHORT")}, 
    333: {"name":"InkNames", "type":("ASCII")}, 
    334: {"name":"NumberOfInks", "type":("SHORT")}, 
    336: {"name":"DotRange", "type":("SHORT", "BYTE")}, 
    337: {"name":"TargetPrinter", "type":("ASCII")}, 
    338: {"name":"ExtraSamples", "type":("BYTE")}, 
    339: {"name":"SampleFormat", "type":("SHORT")},
    340: {"name":"SMinSampleValue", "type":("any")}, 
    341: {"name":"SMaxSampleValue", "type":("any")}, 
    342: {"name":"TransferRange", "type":("SHORT")}, 
    512: {"name":"JPEGProc", "type":("SHORT")}, 
    513: {"name":"JPEGInterchangeFormat", "type":("LONG")}, 
    514: {"name":"JPEGInterchangeFormatLngth", "type":("LONG")},
    
    515: {"name":"JPEGRestartInterval", "type":("SHORT")}, 
    517: {"name":"JPEGLosslessPredictors", "type":("SHORT")}, 
    518: {"name":"JPEGPointTransforms", "type":("SHORT")}, 
    519: {"name":"JPEGQTables", "type":("LONG")}, 
    520: {"name":"JPEGDCTables", "type":("LONG")}, 
    521: {"name":"JPEGACTables", "type":("LONG")}, 
    529: {"name":"YCbCrCoefficients", "type":("RATIONAL")}, 
    530: {"name":"YCbCrSubSampling", "type":("SHORT")}, 
    531: {"name":"YCbCrPositioning", "type":("SHORT")}, 
    532: {"name":"ReferenceBlackWhite", "type":("LONG")}, 
    33432: {"name":"Copyright", "type":("ASCII")}

}

FIELDTYPES = {
    1:"BYTE", 
    2:"ASCII", 
    3:"SHORT", 
    4:"LONG", 
    5:"RATIONAL", 
    6:"SBYTE", 
    7:"UNDEFINED", 
    8:"SSHORT", 
    9:"SLONG", 
    10:"SRATIONAL", 
    11:"FLOAT", 
    12:"DOUBLE"
}

FIELDLENGTHS = {
    1: 1, 
    2: 1, 
    3: 2, 
    4: 4, 
    5: 8, 
    6: 1, 
    7: 1, 
    8: 2, 
    9: 4, 
    10: 8, 
    11: 4, 
    12: 8
}

class Tiff():
    def __init__(self, filepath=None, fromstring = None, withmeta=True, timeit=False):
        if timeit is True:
            starttime = time.time()
        self.infilepath = filepath
        self.withmeta = withmeta

        self.byteorder = None
        self.magicnumber = None
        self.offset_firstIFD = None
        self.ifds = []

        if self.infilepath is not None:
            if not os.path.isfile(self.infilepath):
                raise Exception('__init__', 'file not found')
            self.stream = open(self.infilepath, "rb")
        elif fromstring is not None:
            self.stream = cStringIO.StringIO()
            self.stream.write(fromstring)
        
        self.stream.seek(0, 2)
        self.maxbyte=self.stream.tell()
        self.stream.seek(0)
        
        try:
            self._read_byteorder()
        except Exception as e:
            raise e
            
        try:
            self._check_magicnumber()
        except Exception as e:
            raise e
            
        try:
            self._read_offset_firstIFD()
        except Exception as e:
            raise e
        
        try:
            self._read_ifds(readtags=withmeta)
        except Exception as e:
            raise e  
        if timeit is True:
            print "loading took %.5f seconds" %(time.time()-starttime)

    def __exit__(self):
        self.stream.close()
        
    def _get_stripbytes(self, ifdindex):
        stripbytes = []
        IFD = self.ifds[ifdindex]
        stripoffsets = IFD["fields"]["StripOffsets"]
        stripbytecounts = IFD["fields"]["StripByteCounts"]
        rowsperstrip = IFD["fields"]["RowsPerStrip"]
        for i in range(len(stripoffsets)):
            self.stream.seek(stripoffsets[i])
            data = self.stream.read(stripbytecounts[i])
            stripbytes.append(data)
        return stripbytes

    def _check_magicnumber(self):
        assert(self.byteorder!=None)
        self.stream.seek(2)
        magicnumber = self.stream.read(2)
        if self.byteorder == "little-endian":
            fmtstr = "<h"
        else:
            fmtstr = ">h"
        if struct.unpack(fmtstr, magicnumber)[0]==42:
            self.magicnumber = 42
            return True
        else:
            raise Exception('stream-error', 'invalid magic number')

    def _get_int(self, data):
        if self.byteorder == "little-endian":
            fmtstr = "<"
        else:
            fmtstr = ">"
        if len(data) == 0:
            return 0
        elif len(data)==1:
            print "now"
            fmtstr += "B"
        elif len(data)==2:
            fmtstr += "H"
        elif len(data)==4:
            fmtstr += "L"
        else:
            print len(data)
        try:
            val = struct.unpack(fmtstr, data)[0]
        except Exception as e:
            print e
            print len(data)
            print fmtstr, data
        return val
            
            
    def _get_value(self, data, dtype):
        value = 0
        #print data, dtype
        if dtype == 1:
            return self._get_int(data)
        elif dtype in (4, 3):
            return self._get_int(data)
        elif dtype == 5:
            return(float( self._get_int(data[:4]) / self._get_int(data[4:]) ))
        elif dtype in (2, 7):
            return data
        elif dtype == 6:
            return self._get_int(data)
        else:
            #print dtype
            return data
        # TODO: add parser for other dtype values, maybe its a good idea to combine _get_value and _get_int
        return value
        
    def _readtags(self, ifds=None):
        if ifds is None:
            ifds = range(len(self.ifds))
        for i in ifds:
            for bytestr in self.ifds[i]["fieldbytes"]:
                dtag = self._get_int(bytestr[0:2])
                dtype = self._get_int(bytestr[2:4])
                dcount = self._get_int(bytestr[4:8])
                
                dtagb = bytestr[0:2]
                dtypeb = bytestr[2:4]
                dcountb = bytestr[4:8]
                
                if dtag in TIFFTAGS:
                    name=TIFFTAGS[dtag]["name"]
                    self.ifds[i]["fields"][name]={}
                else:
                    name = str(dtag)
                    self.ifds[i]["unknownfields"][name]={}
                self.ifds[i]["tags"][dtag]={}
                #print name
                if dtype in FIELDTYPES:
                    bytecount = dcount*FIELDLENGTHS[dtype]
                    if bytecount <= 4:
                        # bytes represent a left adjust value
                        offset = None
                        offsetb = None
                        dvals = [self._get_value(bytestr[8:8+bytecount], dtype)]
                        dvalsb = [bytestr[8:12]]
                    else:
                        # bytes represent offset to list of dcount values
                        # each value has the size FIELDLENGTHS[dtype]
                        offset = self._get_int(bytestr[8:12])
                        offsetb = bytestr[8:12]
                        self.stream.seek(offset)
                        dvals = []
                        dvalsb = []
                        for c in range(dcount):
                            dvalb = self.stream.read(FIELDLENGTHS[dtype])
                            dval = self._get_value(dvalb, dtype)
                            dvals.append(dval)
                            dvalsb.append(dvalb)
                        if dtype in (2, 7):
                            s = "".join(dvals).strip("\x00")
                            dvals=s
                    #if len(dvals)==1:
                        #dvals=dvals[0]
                    #if len(dvalsb)==1:
                        #dvalsb=dvalsb[0]
                #print dvals[0:4]
                self.ifds[i]["tags"][dtag]["offset"]=offset
                self.ifds[i]["tags"][dtag]["dtagb"]=dtagb
                self.ifds[i]["tags"][dtag]["dtypeb"]=dtypeb
                self.ifds[i]["tags"][dtag]["dtype"]=dtype
                self.ifds[i]["tags"][dtag]["dcountb"]=dcountb
                self.ifds[i]["tags"][dtag]["dcount"]=dcount
                self.ifds[i]["tags"][dtag]["dvalsb"]=dvalsb
                

                
                if dtag in TIFFTAGS:
                    self.ifds[i]["fields"][name] = dvals
                else:
                    self.ifds[i]["unknownfields"][name] = dvals

    
        
    def _read_ifds(self, readtags=True):
        assert(self.byteorder!=None)
        offset = self.offset_firstIFD
        self.ifds = []
        while offset:
            self.ifds.append({})
            self.stream.seek(offset)
            fieldcountb = self.stream.read(2)
            fieldcount = self._get_int(fieldcountb)
            fieldbytes = []
            for i in range(fieldcount):
                fieldbytes.append(self.stream.read(12))
            data = self.stream.read(4)
            offset = self._get_int(data)
            self.ifds[-1]["fieldbytes"] = fieldbytes
            self.ifds[-1]["fields"] = {}
            self.ifds[-1]["fieldcountb"] = fieldcountb
            self.ifds[-1]["fieldcount"] = fieldcount
            self.ifds[-1]["tags"] = {}
            self.ifds[-1]["unknownfields"] = {}
        if readtags is True:
            self._readtags()
        return
       
    def _set_int(self, data, bytelength):
        if self.byteorder=="little-endian":
            fmtstr = "<"
        else:
            fmtstr = ">"
        if bytelength==1:
            fmtstr += "B"
        elif bytelength==2:
            fmtstr += "H"
        elif bytelength==4:
            fmtstr += "L"
        try:
            return struct.pack(fmtstr, data)
        except:
            print fmtstr
            print data
            sys.exit()

    def _read_offset_firstIFD(self):
        """
        The offset (in bytes) of the first IFD. The directory may be at any location in the
        file after the header but 
        must begin on a word boundary
        . In particular, an Image
        File Directory may follow the image data it describes. Readers must follow the
        pointers wherever they may lead.
        """
        assert(self.byteorder!=None)
        self.stream.seek(4)
        offset = self.stream.read(4)
        if self.byteorder == "little-endian":
            fmtstr = "<L"
        elif self.byteorder == "big-endian":
            fmtstr = ">L"
        self.offset_firstIFD = self._get_int(offset)

    def pagecount(self):
        return len(self.ifds)
    
    def get_resolution(self, pageno=1):
        ifdindex = pageno-1
        return [self.ifds[ifdindex]["fields"]["ImageWidth"][0], self.ifds[ifdindex]["fields"]["ImageLength"][0]]
        

    def _read_byteorder(self):
        self.stream.seek(0)
        bostr = self.stream.read(2)
        if bostr == "II":
            self.byteorder = "little-endian"
        elif bostr == "MM":
            self.byteorder = "big-endian"
        else:
            raise Exception('stream-error', 'invalid byteorder')

    def close(self):
        self.stream.close()

    def savepages(self, pages, filename):
        
        newstream = cStringIO.StringIO()
        self.stream.seek(0)
        # write byteorder and magic number
        newstream.write(self.stream.read(4))
        # write first offset which will be right behind the header at byte 8
        offset_firstIFD = self._set_int(8, 4)
        newstream.write(offset_firstIFD)
        dir_offset = newstream.tell()
        nextifdoffsetadress = None
        newpageno = 0
        for pageno in pages:
            #print "appending page %d" %pageno
            newpageno += 1
            if nextifdoffsetadress is not None:
                newstream.seek(nextifdoffsetadress)
                newstream.write(self._set_int(data_offset, 4))
            newstream.seek(dir_offset)
            ifdindex = pageno-1
            ifd = self.ifds[ifdindex]
            # write the number of directory entries
            nrod = self._set_int(len(ifd["tags"]), 2)
            newstream.write(nrod)
            dir_offset = newstream.tell()
            # fill up the directory entries
            newstream.write(len(ifd["tags"])*12*"\x00")
            # write next ifd offset which will be \x00\x00\x00\x00 (1 page exactly)
            nextifdoffsetadress = newstream.tell()
            newstream.write(4*"\x00")
            data_offset = newstream.tell()
            
            for tag in ifd["tags"]:
                newstream.seek(dir_offset)
                if tag !=273: # stripoffsets needs update
                    newstream.write(ifd["tags"][tag]['dtagb'])
                    newstream.write(ifd["tags"][tag]['dtypeb'])
                    newstream.write(ifd["tags"][tag]['dcountb'])
                    dir_offset = newstream.tell()
                    if tag == 297: # pagenumber needs update 
                        newstream.write(self._set_int(newpageno, 4))
                        dir_offset = newstream.tell()
                    elif ifd["tags"][tag]['offset'] is None:
                        # write value
                        newstream.write("".join(ifd["tags"][tag]['dvalsb']))
                        dir_offset = newstream.tell()
                    else:
                        # write new offset
                        newstream.write(self._set_int(data_offset, 4))
                        dir_offset = newstream.tell()
                        # write values at data_offset
                        newstream.seek(data_offset)
                        for value in ifd["tags"][tag]['dvalsb']:
                            newstream.write(value)
                        data_offset = newstream.tell()
                else: # now stripoffsets
                    newstream.write(ifd["tags"][tag]['dtagb'])
                    newstream.write(self._set_int(4, 2))    # we are using dtype LONG for offsets
                    newstream.write(ifd["tags"][tag]['dcountb'])
                    dir_offset = newstream.tell()
                    # write all stripes at dataoffset, remembering the offsets
                    newstream.seek(data_offset)
                    stripoffsets=[]
                    for strip in self._get_stripbytes(ifdindex):
                        stripoffsets.append(self._set_int(newstream.tell(), 4))
                        newstream.write(strip)
                    
                    data_offset = newstream.tell()
                    newstream.seek(dir_offset)
                    if len(stripoffsets)==1:
                        # write value
                        newstream.write(stripoffsets[0])
                        dir_offset = newstream.tell()
                    else:
                        newstream.write(self._set_int(data_offset, 4))
                        dir_offset = newstream.tell()
                        # write offset to list
                        newstream.seek(data_offset)
                        newstream.write("".join(stripoffsets))
                        data_offset = newstream.tell()
            dir_offset = data_offset
                        
        f = open(filename, "wb")
        newstream.seek(0)
        f.write(newstream.read())
        f.close()
    
    def split(self, pageperfile, first=None, last=None, basename="temp"):
        if first is None:
            first=1
        if last is None:
            last = len(self.ifds)+1
        if first < 1:
            first = 1
        if first > len(self.ifds):
            first = len(self.ifds)
        if last < first:
            last = first+1
        if last > len(self.ifds)+1:
            last = len(self.ifds)+1
        for frompage in range(first, last, pageperfile):
            topage = frompage + pageperfile
            if topage > last:
                topage=last
            pages = range(frompage, topage)
            #print frompage, topage
            filename = basename+"%d-%d.tif" %(frompage, topage-1)
            self.savepages(pages, filename)
        
        
        

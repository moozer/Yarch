#!/usr/bin/env python
#
#       ProcessDirTree.py
#       
#       Copyright 2010  <morten@leon>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from md5dirlist.diskwalk_api import diskwalk
from md5dirlist.Dirlist import Dirlist

def main():
    d = diskwalk('.')
    dirs = d.enumerateDir()
    print "processing %d directories" % len( dirs )
    print dirs
    for Dir in dirs:
        print "Processing dir:", Dir
        dl = Dirlist( Dir )
        dl.getDirlist()
    return 0

if __name__ == '__main__': main()

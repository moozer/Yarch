#!/usr/bin/env python
#
#       ArchiveCheck.py
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

#from diskwalk_api import diskwalk
from optparse import OptionParser
from find_dupes import findDupes
from diskwalk_api import diskwalk


def PrintFileList( FileList, FileCountToShow = 10 ):
	''' Dumps the filename to screen. Shows on the first "FileCountToShow"'''
	if len( FileList ) > FileCountToShow:
		print "(Filelist is long. Truncating to first %d files)" % FileCountToShow
		for file in FileList[0:FileCountToShow]:
			print " -", file
	else:
		# List all files
		for file in FileList:
			print " -", file
	

def findSpecific(path = '/tmp', Extention = 'iso'):
	dup = []
	ErrorFiles = []
	record = {}
	d = diskwalk(path)
	files = d.enumerateFilesByExt( Extention )
	return { Extention: files }


def ArchCheck( DirToCheck, FileCountToShow = 10 ):
	print "Checking dir for duplicates"
	Files = findDupes( DirToCheck )
	print "Found %d dupplicates and %d problem files" % (len( Files['DupFiles'] ), len( Files['BadFiles'] ))
	if len( Files['DupFiles'] ) > 0:
		print "Duplicate files"
		PrintFileList( Files['DupFiles'], FileCountToShow )

	if len( Files['BadFiles'] ) > 0:
		print "Bad files"
		PrintFileList( Files['BadFiles'], FileCountToShow )

	print "checking dir for ISOs"
	IsoExtString = 'iso'
	IsoFiles = findSpecific( DirToCheck, IsoExtString )[IsoExtString]
	print "Fount %d files with extension %s" % ( len( IsoFiles ), IsoExtString)
	if len( IsoFiles ) > 0:
		PrintFileList( IsoFiles, FileCountToShow )

	return 0

if __name__ == '__main__': 

	parser = OptionParser()
	parser.add_option("-d", "--directory", dest="dir",
					  help="write report to FILE", metavar="DIR", default=".")
	(options, args) = parser.parse_args()
	
	ArchCheck( options.dir )

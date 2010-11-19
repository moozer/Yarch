#!/usr/bin/env python
#
#       testDirlisttestDirlist.py
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

# imports
import unittest
from md5dirlist.Dirlist import Dirlist
from md5dirlist.DirlistError import DirlistError
import datetime
import os

# test data
DirNonExist = "./ThisDirectoryDoesNotExist"

# No md5 file data
Data1Dir = "./DirWithoutDirlist"
Data1Result =  [{'mtime': datetime.datetime(2010, 5, 15, 21, 31, 50), 'md5': '\x08x@3\x90\xb7\xe5\xf0*}\x7f\xc0\xeb\xc8Y9', 'file': 'file3.txt', 'size': 9L}, {'mtime': datetime.datetime(2010, 5, 15, 21, 31, 50), 'md5': '\x08x@3\x90\xb7\xe5\xf0*}\x7f\xc0\xeb\xc8Y9', 'file': 'file2.txt', 'size': 9L}, {'mtime': datetime.datetime(2010, 5, 15, 21, 31, 50), 'md5': '\x08x@3\x90\xb7\xe5\xf0*}\x7f\xc0\xeb\xc8Y9', 'file': 'file1.txt', 'size': 9L}]
Data1Output = '''file3.txt	9	2010-05-15 21:31:50	CHhAM5C35fAqfX/A68hZOQ==
file2.txt	9	2010-05-15 21:31:50	CHhAM5C35fAqfX/A68hZOQ==
file1.txt	9	2010-05-15 21:31:50	CHhAM5C35fAqfX/A68hZOQ==
'''

# No md5 file data
Data2Dir = "./DirWithDirlist"
Data2Result = [
    {'mtime': datetime.datetime(2010, 5, 14, 15, 42, 57), 'md5': '\x08x@3\x90\xb7\xe5\xf0*}\x7f\xc0\xeb\xc8Y9', 
        'file': 'file3.txt', 'size': 9L}, 
    {'mtime': datetime.datetime(2010, 5, 14, 15, 42, 55), 'md5': '\x08x@3\x90\xb7\xe5\xf0*}\x7f\xc0\xeb\xc8Y9', 
        'file': 'file2.txt', 'size': 9L}, 
    {'mtime': datetime.datetime(2010, 5, 14, 15, 42, 52), 'md5': '\x08x@3\x90\xb7\xe5\xf0*}\x7f\xc0\xeb\xc8Y9', 
        'file': 'file1.txt', 'size': 9L}]

# directory without file but with a bad link.
Data3Dir = "./DirWithBadLink"
Data3Result =  [
    {'mtime': datetime.datetime(2010, 5, 15, 21, 31, 50), 'md5': '\x08x@3\x90\xb7\xe5\xf0*}\x7f\xc0\xeb\xc8Y9', 
        'file': 'file3.txt', 'size': 9L}, 
    {'mtime': datetime.datetime(2010, 5, 15, 21, 31, 50), 'md5': '\x08x@3\x90\xb7\xe5\xf0*}\x7f\xc0\xeb\xc8Y9', 
        'file': 'file2.txt', 'size': 9L}, 
    {'mtime': datetime.datetime(2010, 5, 15, 21, 31, 50), 'md5': '\x08x@3\x90\xb7\xe5\xf0*}\x7f\xc0\xeb\xc8Y9', 
        'file': 'file1.txt', 'size': 9L}]


class testmd5Dirlist(unittest.TestCase):                           
    def testInstantiate( self ):
        """ Simple instantiation and basedir check """
        dl = Dirlist( Data1Dir )
        self.assertEqual( dl.getBasedir(), Data1Dir, "Basedir and supplied dir does not match");

    def testBadInstantiate( self ):
        """ Simple instantiation and basedir check of bad basedir """
        self.assertRaises( DirlistError, Dirlist, DirNonExist)
        
    def testGenerateDirlist( self ):
        ''' create the dirlistfile '''
        dl = Dirlist( Data1Dir )
        res = dl.createDirlist()
        #~ print res
        #~ print Data1Result

        self.assertEqual( res, Data1Result, "Processed data does not match expectations" )

    def testDirlistOutput( self ):
        ''' Testing file content output function '''
        dl = Dirlist( Data1Dir )
        DirlistData = dl.createDirlist()
        output = dl.generateOutput( DirlistData )
        #~ print output
        #~ print Data1Output
        self.assertEqual( output, Data1Output, "Output does not match expectations" )

    def testGetDirlistFromOutput( self ):
        ''' test use the output to return to the processed data '''
        dl = Dirlist( Data1Dir )
        DirlistData = dl.createDirlist()
        Output = dl.generateOutput( DirlistData )
        self.assertEqual( dl.extractDirlist( Output ), DirlistData, "Extracted data does not match input" )
        
    def testCheckExistingDirlistFile( self ):
        ''' check for existing dirlist file '''
        dl = Dirlist( Data2Dir )
        self.assertTrue( dl.isDirlistPresent() )        

    def testCheckNonexistingDirlistFile( self ):
        ''' check for non-existing dirlist file '''
        dl = Dirlist( Data1Dir )
        self.assertFalse( dl.isDirlistPresent() ) 
        
    def testGetDirlistFromFile( self ):
        ''' test reads the dirlist from file '''
        dl = Dirlist( Data2Dir )
        self.assertEqual( dl.readDirlistFromFile(), Data2Result, "Bad data read from dirlist file" )
        
    def testWriteDirlistToFile( self ):
        ''' test writes the dirlist to file '''
        # cleanup before we start
        if os.path.isfile( os.path.join( Data1Dir, '.dirlist.md5' ) ):
            os.remove( os.path.join( Data1Dir, '.dirlist.md5' ) )
        
        dl = Dirlist( Data1Dir )
        self.assertFalse( dl.isDirlistPresent() )  # prerequisite for the test
        
        dl.writeDirlistToFile( Data1Result )
        self.assertEqual( dl.readDirlistFromFile(), Data1Result, "Bad data read from dirlist file" )
        
        # cleanup
        os.remove( os.path.join( Data1Dir, '.dirlist.md5' ) )
        
    def testGetDirlistNoFile( self ):
        ''' testing the getDirlist function for directory with no dirlist file '''
        dl = Dirlist( Data1Dir )
        res = dl.getDirlist()
        #~ print dl.generateOutput( res )
        #~ print dl.generateOutput( Data1Result )
        self.assertEqual( res, Data1Result, "Bad data read from dirlist file" )
        os.remove( os.path.join( Data1Dir, '.dirlist.md5' ) )
  
    def testGetDirlistUsingFile( self ):
        ''' testing the getDirlist function for directory with a dirlist file '''
        dl = Dirlist( Data2Dir )
        self.assertEqual( dl.getDirlist(), Data2Result, "Bad data read from dirlist file" )
        
    def testGetDirlistBadLink( self ):
        ''' testing the getDirlist function for directory with a bad link '''
        if os.path.isfile( os.path.join( Data3Dir, '.dirlist.md5' ) ):
            os.remove( os.path.join( Data3Dir, '.dirlist.md5' ) )
  
        dl = Dirlist( Data3Dir )
        res = dl.getDirlist()
        #~ print res
        #~ print Data3Result
        self.assertEqual( res, Data3Result, "Bad data read from dirlist file" )
        os.remove( os.path.join( Data3Dir, '.dirlist.md5' ) )
   

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
Data1Result =  [
    {'mtime': datetime.datetime(2010, 5, 14, 21, 43, 17), 'md5': '0878403390b7e5f02a7d7fc0ebc85939', 
        'file': 'file1.txt', 'size': 9L}, 
    {'mtime': datetime.datetime(2010, 5, 14, 21, 43, 17), 'md5': '0878403390b7e5f02a7d7fc0ebc85939', 
        'file': 'file3.txt', 'size': 9L}, 
    {'mtime': datetime.datetime(2010, 5, 14, 21, 43, 17), 'md5': '0878403390b7e5f02a7d7fc0ebc85939', 
        'file': 'file2.txt', 'size': 9L}]
Data1Output = '''file1.txt\t9\t2010-05-14 21:43:17\tMDg3ODQwMzM5MGI3ZTVmMDJhN2Q3ZmMwZWJjODU5Mzk=
file3.txt\t9\t2010-05-14 21:43:17\tMDg3ODQwMzM5MGI3ZTVmMDJhN2Q3ZmMwZWJjODU5Mzk=
file2.txt\t9\t2010-05-14 21:43:17\tMDg3ODQwMzM5MGI3ZTVmMDJhN2Q3ZmMwZWJjODU5Mzk=
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
    {'mtime': datetime.datetime(2010, 5, 15, 21, 37, 57), 'md5': '0878403390b7e5f02a7d7fc0ebc85939', 
        'file': 'file1.txt', 'size': 9L}, 
    {'mtime': datetime.datetime(2010, 5, 15, 21, 37, 57), 'md5': '0878403390b7e5f02a7d7fc0ebc85939', 
        'file': 'file3.txt', 'size': 9L}, 
    {'mtime': datetime.datetime(2010, 5, 15, 21, 37, 57), 'md5': '0878403390b7e5f02a7d7fc0ebc85939', 
        'file': 'file2.txt', 'size': 9L}]

class testmd5Dirlist(unittest.TestCase):
    def setUp( self ):
        # Running a script to init data.      
        self._CurrentDir = os.getcwd()
        try:
            os.chdir('tests')
        except OSError:
            pass
        
    def tearDown( self):
        # run script to undo stuff in setUp
        os.chdir( self._CurrentDir )
                          
    def testInstantiate( self ):
        """ Dirlist : Simple instantiation and basedir check """
        dl = Dirlist( Data1Dir )
        self.assertEqual( dl.getBasedir(), Data1Dir, "Basedir and supplied dir does not match");

    def testBadInstantiate( self ):
        """ Dirlist : Simple instantiation and basedir check of bad basedir """
        self.assertRaises( DirlistError, Dirlist, DirNonExist)
        
    def testGenerateDirlist( self ):
        ''' Dirlist : create the dirlistfile '''
        dl = Dirlist( Data1Dir )
        res = dl.createDirlist()
        #self.assertEqual( res, Data1Result, "Processed data does not match expectations" )
        self.assertEqual( res, Data1Result )

    def testDirlistOutput( self ):
        ''' Dirlist : Testing file content output function '''
        dl = Dirlist( Data1Dir )
        DirlistData = dl.createDirlist()
        output = dl.generateOutput( DirlistData )
        self.assertEqual( output, Data1Output, "Output does not match expectations" )

    def testGetDirlistFromOutput( self ):
        ''' Dirlist : test use the output to return to the processed data '''
        dl = Dirlist( Data1Dir )
        DirlistData = dl.createDirlist()
        Output = dl.generateOutput( DirlistData )
        self.assertEqual( dl.extractDirlist( Output ), DirlistData, "Extracted data does not match input" )
        
    def testCheckExistingDirlistFile( self ):
        ''' Dirlist : check for existing dirlist file '''
        dl = Dirlist( Data2Dir )
        self.assertTrue( dl.isDirlistPresent() )        

    def testCheckNonexistingDirlistFile( self ):
        ''' Dirlist : check for non-existing dirlist file '''
        dl = Dirlist( Data1Dir )
        self.assertFalse( dl.isDirlistPresent() ) 
        
    def testGetDirlistFromFile( self ):
        ''' Dirlist : test reads the dirlist from file '''
        dl = Dirlist( Data2Dir )
        self.assertEqual( dl.readDirlistFromFile(), Data2Result )
        #self.assertEqual( dl.readDirlistFromFile(), Data2Result, "Bad data read from dirlist file" )
        
    def testWriteDirlistToFile( self ):
        ''' Dirlist : test writes the dirlist to file '''
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
        ''' Dirlist : testing the getDirlist function for directory with no dirlist file '''
        dl = Dirlist( Data1Dir )
        res = dl.getDirlist()
        #~ print dl.generateOutput( res )
        #~ print dl.generateOutput( Data1Result )
        self.assertEqual( res, Data1Result, "Bad data read from dirlist file" )
        os.remove( os.path.join( Data1Dir, '.dirlist.md5' ) )
  
    def testGetDirlistUsingFile( self ):
        ''' Dirlist : testing the getDirlist function for directory with a dirlist file '''
        dl = Dirlist( Data2Dir )
        self.assertEqual( dl.getDirlist(), Data2Result, "Bad data read from dirlist file" )
        
    def testGetDirlistBadLink( self ):
        ''' Dirlist : testing the getDirlist function for directory with a bad link '''
        if os.path.isfile( os.path.join( Data3Dir, '.dirlist.md5' ) ):
            os.remove( os.path.join( Data3Dir, '.dirlist.md5' ) )
  
        dl = Dirlist( Data3Dir )
        res = dl.getDirlist()
        #~ print res
        #~ print Data3Result
        self.assertEqual( res, Data3Result )
        os.remove( os.path.join( Data3Dir, '.dirlist.md5' ) )
   

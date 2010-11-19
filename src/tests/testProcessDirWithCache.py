#!/usr/bin/env python
#
#       testProcessDir.py
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
from ProcessDir.ProcessDir import ProcessDir, DumpFilelist, FileCache
import os

TestcaseBaseDir = './tests/data_tmp/ProcessDirWithCache/'

# testdirA is simple: two files, no subdirs
TestDirA = TestcaseBaseDir + 'BadMd5Sum/'
TestDirA_FileA = 'FileA.txt'
TestDirA_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
TestDirA_FileA_md5_cached = 'ThisIsABadMd5Sum'
TestDirA_list_cached = [   { 'md5': TestDirA_FileA_md5_cached, 'filename': TestDirA_FileA, 'duplicates': [], 'directory': TestDirA }]

# testdirB: no dirlist file
TestDirB = TestcaseBaseDir + 'NoDirlistfile/'
TestDirB_FileA = 'FileA.txt'
TestDirB_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
TestDirB_result = [   { 'md5': TestDirB_FileA_md5, 'filename': TestDirB_FileA, 'duplicates': [], 'directory': TestDirB }]

# testdirB: no dirlist file
TestDirC = TestcaseBaseDir + 'BadDirlistFile/'
TestDirC_FileA = 'FileA.txt'
TestDirC_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
TestDirC_result = [   { 'md5': TestDirC_FileA_md5, 'filename': TestDirC_FileA, 'duplicates': [], 'directory': TestDirB }]

# testdirD dir with link
TestDirD = TestcaseBaseDir + 'DirWithLink/'
TestDirD_FileA = 'FileA.txt'
TestDirD_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
TestDirD_list = [   { 'md5': TestDirD_FileA_md5, 'filename': TestDirD_FileA, 'duplicates': [], 'directory': TestDirD }]

# progress indicator test function
SavedList = []
def SaveOutputToList( Entry ):
    SavedList.append( Entry )
    return

# tests
class testProcessDirWithCache(unittest.TestCase):     
    def setUp( self ):
        # Running a script to init data.        
        os.system( 'sh ./tests/ProcessDirDataInit.sh' )
        
    def tearDown( self):
        # run script to undo stuff in setUp
        os.system( 'sh ./tests/ProcessDirDataCleanup.sh' )
        
    def testWithoutCache( self ):
        """ Check that processDir accept the UseCache parameter """
        PD =  ProcessDir( TestDirA )
        self.assertEqual( PD.Process(), PD.Process( UseCache = False ) )

    def testDirWithCache( self ):
        """ Check that processDir returns cached values """
        PD =  ProcessDir( TestDirA )
        self.assertEqual( PD.Process( UseCache = True ), FileCache( Data = TestDirA_list_cached ) )

    def testDirWithBadCache( self ):
        """ Check that processDir returns cached values and also non-cached values"""
        PD =  ProcessDir( TestDirA )
        self.assertNotEqual( PD.Process( UseCache = True ), PD.Process( UseCache = False ) )

    def testWriteCache( self ):
        """ Check that processDir writes the cache"""
        PD =  ProcessDir( TestDirB )
        if os.path.exists( TestDirB+'.md5dirlist' ):
            raise IOError( ".md5dirlist must no be present" )
        
        PD.Process( UseCache = True ) # no .md5dirlist in directory
        self.assertTrue( os.path.isfile( TestDirB+'.md5dirlist' ) )

        # clean up
        if os.path.exists( TestDirB+'.md5dirlist' ):
            os.remove( TestDirB+'.md5dirlist' )

    def testCacheResult( self ):
        """ Check if resulting cache value corresponds to expected values """
        if os.path.exists( TestDirB+'.md5dirlist' ):
            raise IOError( ".md5dirlist must no be present" )
 
        PD = ProcessDir( TestDirB )
        PD.Process( UseCache = True ) # generates the cache
        
        PD2 = ProcessDir( TestDirB )
        res = PD2.Process( UseCache = True )

        self.assertEqual( res, FileCache( Data = TestDirB_result ))
        
    def testBadDirlistFile( self ):
        """ check proper IOError ecception when dirlist file is malformed """
        PD = ProcessDir( TestDirC )
        self.assertRaises( ValueError, PD.Process, UseCache = True )
 
    def testDirWithLink( self ):
        """ Check that processDir ignores links"""
        self.assertEqual( ProcessDir( TestDirD ).Process(), FileCache( Data = TestDirD_list ))

    def testDirWithLink_Fatal( self ):
        """ Check that processDir fails om links"""
        self.assertRaises( IOError, ProcessDir( TestDirD ).Process, LinksAreFatal = True )

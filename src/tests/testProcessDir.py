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
from ProcessDir.ProcessDir import ProcessDir, FileCache
from DirUtils import * #@UnusedWildImport
from testData import * #@UnusedWildImport

# progress indicator test function
SavedList = []
def SaveVerboseToList( Entry ):
    SavedList.append( Entry )
    return

# tests
class testProcessDir(unittest.TestCase):     
    def setUp( self ):
        # Running a script to init data.      
        self._CurrentDir = InitTempDir()
        
    def tearDown( self):
        # run script to undo stuff in setUp
        CleanTempDir(self._CurrentDir)

    def testExistingDir( self ):
        """ Simple instantiation with existing directory"""
        ProcessDir( TestDirA )

    def testNonExistingDir( self ):
        """ Simple instationtion  with non-existing directory"""
        self.assertRaises( IOError, ProcessDir, NonexistentDir )
        
    def testSingleDepth( self ):
        """ Check return value of single depth dir tree """
        PD = ProcessDir( TestDirA )
        self.assertEqual( PD.Process(), FileCache( Data = TestDirA_list ) )
        
    def testRecursive( self ):
        """ Check return value of multilevel dir tree """
        PD = ProcessDir( TestDirB )
        self.assertEqual( PD.Process(), FileCache( Data = TestDirB_list ) )
    
    def testFindDuplicates( self ):
        """ Check to find duplicate files (based on md5)"""
        PD_A = ProcessDir( TestDirB )
        CompareCache = FileCache( Directory = TestDirA, Data = TestDirA_list )
        ProcessResult = PD_A.Process( CompareCache )
        ExpectedResult = FileCache( Data = TestDirB_duppA_list )
        self.assertEqual( ProcessResult, ExpectedResult )
        
    def testProgressIndicator( self ):
        """ check that all data is piped to progress indicator also """
        PD = ProcessDir( TestDirA )
        Res = PD.Process( ProgressFunction = SaveVerboseToList )
        self.assertEqual( Res.getAllEntries(), SavedList )
        
    def testRecursiveEmptyTopLevel( self ):
        """ Check return value of multilevel dir tree with empty toplevel dir"""
        PD = ProcessDir( TestDirEmptyTopLevel )
        Res = PD.Process()
        ExpRes = FileCache( Data = TestDirEmptyTopLevel_list )

        Res.getAllEntries().sort(lambda x,y : cmp(x['directory'], y['directory']))
          
        self.assertEqual( Res.getNumberOfEntries(), ExpRes.getNumberOfEntries() )        
        self.assertTrue( Res.getAllEntries() == ExpRes.getAllEntries() )

        
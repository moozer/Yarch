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
from ProcessDir.ProcessDir import ProcessDir, DumpFilelist,FileCache
import os

from testData import *

# progress indicator test function
SavedList = []
def SaveVerboseToList( Entry ):
    SavedList.append( Entry )
    return

# tests
class testProcessDir(unittest.TestCase):     
    def setUp( self ):
        #w Running a script to init data.        
        os.system( 'sh ./tests/ProcessDirDataInit.sh' )
        
    def tearDown( self):
        # run script to undo stuff in setUp
        os.system( 'sh ./tests/ProcessDirDataCleanup.sh' )
        
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
        self.assertEqual( PD_A.Process( FileCache( Data = TestDirA_list ) ), FileCache( Data = TestDirB_duppA_list ) )
        
    def testProgressIndicator( self ):
        """ check that all data is piped to progress indicator also """
        PD = ProcessDir( TestDirA )
        Res = PD.Process( ProgressFunction = SaveVerboseToList )
        self.assertEqual( Res.getAllEntries(), SavedList )

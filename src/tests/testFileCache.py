#!/usr/bin/env python
#
#       testFileCache.py
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
from ProcessDir.FileCache import FileCache
from DirUtils import * #@UnusedWildImport
from testData import * #@UnusedWildImport

# test data
TestDirA = './data_tmp/ProcessDir/TestDirA/'
TestDirA_FileA = TestDirA + 'FileA.txt'
TestDirA_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
TestDirA_FileA_Entry = { 'filename': TestDirA_FileA, 'md5': TestDirA_FileA_md5 }

# restore test data
TestRestoreDir = './data_tmp/FileCache/RestoreDirlist/'
TestRestoreDir_Entries = [{'md5': 'b9fe47a96c549d293adaff557ab64328', 'filename': 'asgeroth-080422.tgz'}]
RelLoadDir = "RelLoadDir"
TestRestoreDirRelDir_Entries = [{'directory': RelLoadDir, 'md5': 'b9fe47a96c549d293adaff557ab64328', 
                           'filename': 'asgeroth-080422.tgz'}]

# test save dirlist
TestSaveDir = './data_tmp/FileCache/SaveDirlist/'
TestSaveDir_FileA = 'FileA.txt'
TestSaveDir_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
TestSaveDir_FileB = 'FileB.txt'
TestSaveDir_FileB_md5 = '9b36b2e89df94bc458d629499d38cf86'
TestSaveDir_entries = [{ 'md5': TestSaveDir_FileA_md5, 'filename': TestSaveDir_FileA }, 
                       { 'md5': TestSaveDir_FileB_md5, 'filename': TestSaveDir_FileB }]
TestSaveDir_list_complete = [{  'md5': TestSaveDir_FileA_md5, 'filename': TestSaveDir_FileA, 
                                'duplicates': [], 'directory': TestSaveDir }, 
                             {  'md5': TestSaveDir_FileB_md5, 'filename': TestSaveDir_FileB, 
                                'duplicates': [], 'directory': TestSaveDir }]


# addEntry
MalformedEntry = { 'md5': 'sdfsdf', 'xxx': 'dvsdv' }

# Bad Dirlist
TestBadDirlistDir = './data_tmp/FileCache/' + 'MalformedDirlistfile/'

# add test
AddObjectsList = [{  'md5': 'SomeMd5Sum', 'filename': 'SomeFileName', 'duplicates': [], 'directory': '.' } ]

# tests
class testFileCache(unittest.TestCase):     
    def setUp( self ):
        # Running a script to init data.      
        self._CurrentDir = InitTempDir()
        
    def tearDown( self):
        # run script to undo stuff in setUp
        CleanTempDir(self._CurrentDir)
                
    def testInstatiation( self ):
        """ Simple instantiation """
        FileCache()

    def testGetAllEntries( self ):
        """ Checking entries against known result """
        FC = FileCache( Data = TestSaveDir_entries )
        self.assertEqual( FC.getAllEntries(), TestSaveDir_entries )
                
    def testGetAllEntriesMulitDir( self ):
        """ Checking entries against known result (with multiple directories) """
        FC = FileCache( Data = TestDirB_duppA_list )
        self.assertEqual( FC.getAllEntries(), TestDirB_duppA_list )
    
    def testEntriesCount( self ):
        """ Testing adding the number of entries when adding """
        FC = FileCache()
        self.assertTrue( FC.getNumberOfEntries() == 0 )
        FC.addEntry( TestDirA_FileA_Entry )
        self.assertTrue( FC.getNumberOfEntries() == 1 )
        
    def testAddentry( self ):
        """ Testing adding an new entry and retrieving it """
        FC = FileCache()
        FC.addEntry( TestDirA_FileA_Entry )
        self.assertTrue( FC.getEntry( TestDirA_FileA ) == TestDirA_FileA_Entry )

    def testAddBadEntry( self ):
        """ check for exception when adding a bad malformed entry """
        FC = FileCache()
        self.assertRaises( ValueError, FC.addEntry, MalformedEntry )

    def testReset( self ):
        """ test clearing the cache """
        FC = FileCache()
        FC.addEntry( TestDirA_FileA_Entry )
        FC.reset()
        self.assertTrue( FC.getNumberOfEntries() == 0 )

    def testRestoreCache( self ):
        """ test reading from cache file """
        FC = FileCache( TestRestoreDir )
        self.assertEqual( FC.loadCache(), len(TestRestoreDir_Entries)  )
        self.assertEqual( FC.getEntry(), TestRestoreDir_Entries )
        
    def testRestoreCacheWithRelativeDir( self ):
        """ test reading from cache file while applying relative directory"""
        FC = FileCache( TestRestoreDir, BaseDir = RelLoadDir )
        self.assertEqual( FC.loadCache(), len(TestRestoreDir_Entries)  )
        self.assertEqual( FC.getEntry(), TestRestoreDirRelDir_Entries )
        
    def testSaveRestoreCache( self ):
        """ test writing to and reading from cache file """
        FC = FileCache( Directory = TestSaveDir, Data =  TestSaveDir_entries)
        self.assertEqual( FC.saveCache(), len( TestSaveDir_entries ) )
        
        FC2 = FileCache( Directory = TestSaveDir )
        self.assertEqual( FC2.loadCache(), len( TestSaveDir_entries )  )
        self.assertEqual( FC2.getAllEntries(), TestSaveDir_entries )
        
    def testMalformedDirlist( self ):
        """ test if we get a ValueError when dirlist is bad """
        FC = FileCache( TestBadDirlistDir )
        self.assertRaises( ValueError, FC.loadCache )

    def testEquality( self ):
        """ test the equality operator """
        self.assertTrue( FileCache(  Data = TestSaveDir_entries) == FileCache(  Data = TestSaveDir_entries) )

    def testEqualityFalse( self ):
        """ test the equality operator (false)"""
        self.assertFalse( FileCache( Data = TestSaveDir_entries) == FileCache(  Data =  TestRestoreDir_Entries) )

    def testCompleteEntries( self ):
        """ tests if all entries gets filled with 'duplicates' and 'directory' """
        res = FileCache( Directory = TestSaveDir, Data = TestSaveDir_entries )
        res.completeEntries()
        ExpectedResult = FileCache( Data = TestSaveDir_list_complete )
        self.assertTrue(  res == ExpectedResult )

    def testDisconnectedEntries( self ):
        """ tests if all entries gets filled with 'duplicates' and 'directory' """
        res = FileCache( Directory = TestSaveDir, Data = TestSaveDir_entries )
        res.completeEntries()
        self.assertFalse( 'duplicates' in TestSaveDir_entries[0].keys() )

    def testEqualityAppleAndPears( self ):
        """ test for exception when comparing with non-FileCache object """
        self.assertRaises( TypeError, FileCache( Directory = TestSaveDir, Data = TestSaveDir_entries ).__eq__, 'SomeString' )

    def testObjectAddition( self ):
        """ test of add-equal of FilaCache objects """
        FC1 = FileCache( Data = TestSaveDir_list_complete )
        FC2 = FileCache( Data = AddObjectsList )
        
        AllEntries = TestSaveDir_list_complete + AddObjectsList
        FC1 += FC2
        
        self.assertEqual( FC1.getAllEntries(), AllEntries )
        
    def testAddingExistingEntry( self ):
        """ When adding an existing entry, it should update the old """
        FC = FileCache( Data = [TestDirA_FileA_Entry] )
        Entry = TestDirA_FileA_Entry.copy()
        
        Entry['directory'] = '.'
        Entry['duplicates'] = []
        FC.addEntry( Entry )
        self.assertEqual( FC.getNumberOfEntries(), 1 ) # not 2
        self.assertEqual( FC.getEntry( Entry['filename'] ), Entry ) 
        
    def testGetDirectoryDefault(self):
        """ directory getter (default directory) """
        FC = FileCache()
        self.assertEqual( '.', FC.GetDirectory() )        
        
    def testGetDirectoryNonDefault(self):
        """ directory getter """
        FC = FileCache( TestRestoreDir )
        self.assertEqual( TestRestoreDir, FC.GetDirectory() )
        

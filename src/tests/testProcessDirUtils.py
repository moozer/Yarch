#!/usr/bin/env python
#
#       testProcessDirUtilssh
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
from ProcessDir.ProcessDir import DeleteByList, ProcessDir, FileCache
from DirUtils import * #@UnusedWildImport

# duplicate data list
DeleteListDir = './data_tmp/ProcessDirUtils/DeleteListDir/'
DeleteListDir_FileA = 'FileA.txt'
DeleteListDir_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
DeleteListDir_FileB = 'FileB.txt'
DeleteListDir_FileB_md5 = '9b36b2e89df94bc458d629499d38cf86'
DeleteListDir_list = [   { 'md5': DeleteListDir_FileA_md5, 'filename': DeleteListDir_FileA, 
                          'duplicates': [2], 'directory': '.' },
                         { 'md5': DeleteListDir_FileA_md5, 'filename': DeleteListDir_FileB, 
                          'duplicates': [], 'directory': '.' }]
DeleteListDir_AfterDelete = [ { 'md5': DeleteListDir_FileB_md5, 'filename': DeleteListDir_FileB, 
                               'duplicates': [], 'directory': '.' }]

# progress indicator test function
SavedList = []
def SaveOutputToList( Entry ):
    SavedList.append( Entry )
    return
    
# tests
class testProcessDirUtils(unittest.TestCase):     
    def setUp( self ):
        # Running a script to init data.      
        self._CurrentDir = InitTempDir()
        
    def tearDown( self):
        # run script to undo stuff in setUp
        CleanTempDir(self._CurrentDir)

    def testDelete( self ):
        """ Check that processDir accept the UseCache parameter """
        DeleteByList( FileCache( Directory = DeleteListDir, Data = DeleteListDir_list ) )
        Result = ProcessDir( DeleteListDir ).Process( UseCache = False )
        self.assertTrue( Result ==  FileCache( Data = DeleteListDir_AfterDelete ) )
        
    def testDeleteVerboseOutput( self ):
        """ Checks if the verbose output is called for every file """
        DeleteByList( FileCache( Directory = DeleteListDir, Data = DeleteListDir_list ), VerboseFunction = SaveOutputToList )
        self.assertTrue( len(SavedList) >= len( DeleteListDir_list ) )

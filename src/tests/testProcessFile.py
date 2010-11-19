#!/usr/bin/env python
#
#       testProcessFile.py
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
from ProcessFile.ProcessFile import ProcessFile

# test data
TestBaseDir = './tests/data/ProcessFile/'
TestFileA = TestBaseDir + 'ExistingTestFile.txt'    # file with some blabla content
TestFileA_md5 = 'bb1fc7a8eef4e86a76f9ccd65e603f51'  # md5 calculated using "md5sum" command
NonexistingTestFile = TestBaseDir + 'NonexistingTestFile.txt' # non-existent, but in existing dir
TestListWithTestFileA = [ {'md5': TestFileA_md5, 'Filename': TestFileA } ]
TestListWithoutTestFileA = [ {'md5': 'VeryBadMd5Sum', 'Filename': NonexistingTestFile } ]

# tests
class testProcessFile(unittest.TestCase):                           
    def testExistingFile( self ):
        """ Simple function run with existing file"""
        ProcessFile( TestFileA )
           
    def testNonExistingFile( self ):
        """ Simple function run with bad filename. Raises IOError exception"""
        self.assertRaises( IOError, ProcessFile, NonexistingTestFile )

    def testVerifyMD5sum( self ):
        """ Check MD5 result against known MD5"""
        Res = ProcessFile( TestFileA )
        self.assertEqual( Res['md5'], TestFileA_md5 ) 
        
    def testIsInList( self ):
        """ Check if file is found in supplied list"""
        Res = ProcessFile( TestFileA, TestListWithTestFileA )
        self.assertEqual( Res['duplicates'], [ 0 ] )
        
    def testIsNotInList( self ):
        """ Check if file is not found in supplied list"""
        Res = ProcessFile( TestFileA, TestListWithoutTestFileA )
        self.assertEqual( Res['duplicates'], [ ] )
        

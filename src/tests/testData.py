#!/usr/bin/env python
#
#       testData.py
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


# test data used by ProcessDir
NonexistentDir = './ThisDirectoryDoesNotExist'

# testdirA is simple: two files, no subdirs
TestDirA = './data_tmp/ProcessDir/TestDirA/'
TestDirA_FileA = 'FileA.txt'
TestDirA_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
TestDirA_FileB = 'FileB.txt'
TestDirA_FileB_md5 = '9b36b2e89df94bc458d629499d38cf86'
TestDirA_list = [   { 'md5': TestDirA_FileA_md5, 'filename': TestDirA_FileA, 
                     'duplicates': [], 'directory': '.' },
                    { 'md5': TestDirA_FileB_md5, 'filename': TestDirA_FileB, 
                     'duplicates': [], 'directory': '.' }]

# testdirB has two file, and a subdor with two files.
TestDirB = './data_tmp/ProcessDir/TestDirB/'
TestDirB_FileA = 'FileA.txt'
TestDirB_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
TestDirB_FileB = 'FileB.txt'
TestDirB_FileB_md5 = '9b36b2e89df94bc458d629499d38cf86'
SubDirA = 'SubdirA'
SubDirB = 'SubdirB'
TestDirB_subA = TestDirB + SubDirA
TestDirB_SubdirA_FileA = 'FileA.txt'
TestDirB_SubdirA_FileA_md5 = 'd1bf8fc6af9166875316587ad697a719'
TestDirB_SubdirA_FileB = 'FileB.txt'
TestDirB_SubdirA_FileB_md5 = '9b36b2e89df94bc458d629499d38cf86'

TestDirB_list = [   { 'md5': TestDirB_FileA_md5, 'filename': TestDirB_FileA, 
                     'duplicates': [], 'directory': '.' },
                    { 'md5': TestDirB_FileB_md5, 'filename': TestDirB_FileB, 
                     'duplicates': [], 'directory': '.' },
                    { 'md5': TestDirB_SubdirA_FileA_md5, 'filename': TestDirB_SubdirA_FileA, 
                     'duplicates': [], 'directory': SubDirA },
                    { 'md5': TestDirB_SubdirA_FileB_md5, 'filename': TestDirB_SubdirA_FileB, 
                     'duplicates': [], 'directory': SubDirA }]
TestDirB_duppA_list = [   
                    { 'md5': TestDirB_FileA_md5, 'filename': TestDirB_FileA, 
                     'duplicates': [0], 'directory': '.' },
                    { 'md5': TestDirB_FileB_md5, 'filename': TestDirB_FileB, 
                     'duplicates': [1], 'directory': '.' },
                    { 'md5': TestDirB_SubdirA_FileA_md5, 'filename': TestDirB_SubdirA_FileA, 
                     'duplicates': [0], 'directory': SubDirA },
                    { 'md5': TestDirB_SubdirA_FileB_md5, 'filename': TestDirB_SubdirA_FileB, 
                     'duplicates': [1], 'directory': SubDirA }]

TestDirB_selfdup_list = [   
                    { 'md5': TestDirB_FileA_md5, 'filename': TestDirB_FileA, 'duplicates': [0, 2] },
                    { 'md5': TestDirB_SubdirA_FileA_md5, 'filename': TestDirB_SubdirA_FileA, 
                     'duplicates': [0, 2] },
                    { 'md5': TestDirB_FileB_md5, 'filename': TestDirB_FileB, 'duplicates': [1, 3] },
                    { 'md5': TestDirB_SubdirA_FileB_md5, 'filename': TestDirB_SubdirA_FileB, 
                     'duplicates': [1, 3] }]

TestDirEmptyTopLevel = './data_tmp/ProcessDir/TestDirEmptyTopLevel/'
TestDirEmptyTopLevel_list = [   
                    { 'md5': TestDirB_SubdirA_FileA_md5, 'filename': TestDirB_SubdirA_FileA, 
                     'duplicates': [], 'directory': SubDirA},
                    { 'md5': TestDirB_SubdirA_FileB_md5, 'filename': TestDirB_SubdirA_FileB, 
                     'duplicates': [], 'directory': SubDirA },
                    { 'md5': TestDirB_SubdirA_FileA_md5, 'filename': TestDirB_SubdirA_FileA, 
                     'duplicates': [], 'directory': SubDirB },
                    { 'md5': TestDirB_SubdirA_FileB_md5, 'filename': TestDirB_SubdirA_FileB, 
                     'duplicates': [], 'directory': SubDirB }]


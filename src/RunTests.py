#!/usr/bin/env python
#
#       RunTests.py
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

# include program sourcecode in search path
import sys
sys.path.append('./Yarch')

import unittest
#from tests.testDirlist import testmd5Dirlist
from tests.testProcessFile import testProcessFile
from tests.testProcessDir import testProcessDir
from tests.testProcessDirWithCache import testProcessDirWithCache
from tests.testProcessDirUtils import testProcessDirUtils
from tests.testFileCache import testFileCache

if __name__ == '__main__':
#    suite = unittest.TestLoader().loadTestsFromTestCase(testmd5Dirlist)
    suite_a = unittest.TestLoader().loadTestsFromTestCase( testProcessFile )
    suite_b = unittest.TestLoader().loadTestsFromTestCase( testProcessDir)
    suite_c = unittest.TestLoader().loadTestsFromTestCase( testProcessDirWithCache)
    suite_d = unittest.TestLoader().loadTestsFromTestCase( testProcessDirUtils)
    suite_e = unittest.TestLoader().loadTestsFromTestCase( testFileCache )
    alltests = unittest.TestSuite([ suite_a, 
                                    suite_b, 
                                    suite_c, 
                                    suite_d, 
                                    suite_e])

    unittest.TextTestRunner(verbosity=3).run(alltests)


'''
Created on Nov 20, 2010

@author: morten
'''
import unittest
from ProcessDir.ProcessDir import ProcessDir, FileCache
import os

TestDirWI = "data_tmp/DirWithIssues"
TestDirWIWithCache = "data_tmp/DirWithIssuesWithMd5"

SubDirA = "prosilver"
SubDirAFileCount = 223
SubDirB = "subsilver2"
SubDirBFileCount = 190

DirWIFileCount = SubDirAFileCount + SubDirBFileCount

class Test(unittest.TestCase):
    def setUp( self ):
        # Running a script to init data.      
        self._CurrentDir = os.getcwd()
        try:
            os.chdir('tests')
        except OSError:
            pass
        cmd = 'sh ./ProcessDirDataInit.sh'
        res = os.system( cmd )
        if res:
            raise IOError( 'Failed to run setUp command: %s' % cmd)
        
    def tearDown( self):
        # run script to undo stuff in setUp
        os.system( 'sh ./ProcessDirDataCleanup.sh' )
        os.chdir( self._CurrentDir )

    def testRetrieveAllFiles(self):
        ''' ProcessDirWithIssues : get all files from dirwithissues '''
        PD = ProcessDir( TestDirWI )
        Res = PD.Process()
        self.assertEqual( len(Res.getAllEntries()), DirWIFileCount )

    def testRetrieveAllFilesWithCache(self):
        ''' ProcessDirWithIssues : get all files using cached values'''
        PD = ProcessDir( TestDirWIWithCache )
        Res = PD.Process()
        self.assertEqual( len(Res.getAllEntries()), DirWIFileCount )

    def testRetrieveFilesInSubdir(self):
        ''' ProcessDirWithIssues : Check subdirs '''
        PD = ProcessDir( os.path.join(TestDirWI, SubDirA ) )
        Res = PD.Process()
        self.assertEqual( len(Res.getAllEntries()), SubDirAFileCount )
        
        PD = ProcessDir( os.path.join(TestDirWI, SubDirB ) )
        Res = PD.Process()
        self.assertEqual( len(Res.getAllEntries()), SubDirBFileCount )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
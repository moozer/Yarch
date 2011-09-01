'''
Created on Sep 1, 2011

@author: morten
'''

import os

def InitTempDir():
    CurrentDir = os.getcwd()
    try:
        os.chdir('tests')
    except OSError:
        pass
    cmd = 'sh ./ProcessDirDataInit.sh'
    res = os.system(cmd)
    if res:
        raise IOError('Failed to run setUp command: %s' % cmd)
    
    return CurrentDir

def CleanTempDir( OriginalDir ):
    os.system('sh ./ProcessDirDataCleanup.sh')
    os.chdir( OriginalDir )
    
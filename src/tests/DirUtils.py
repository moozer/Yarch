'''
Created on Sep 1, 2011

@author: morten
'''

import os

def InitTempDir( Silent = True ):
    CurrentDir = os.getcwd()
    try:
        os.chdir('tests')
    except OSError:
        pass
    cmd = 'sh ./ProcessDirDataInit.sh'
    if Silent:
        cmd += "> /dev/null 2>&1"
    
    res = os.system(cmd)
    if res:
        raise IOError('Failed to run setUp command: %s' % cmd)
    
    return CurrentDir

def CleanTempDir( OriginalDir, Silent = True ):
    cmd = 'sh ./ProcessDirDataCleanup.sh'
    if Silent:
        cmd += "> /dev/null 2>&1"
    os.system(cmd)
    os.chdir( OriginalDir )
    
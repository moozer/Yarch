'''
Created on Sep 16, 2011

@author: morten
'''

from ProcessDir.ProcessDir import ProcessDir
import sys

# TODO: moveme somewhere else 
def ShowProgressAllFiles( InputDict ):
    global FileCount
    FileCount = FileCount +1
    print "%d\t%s" % (FileCount,InputDict['filename'] )

# TODO: moveme somewhere else 
def ShowProgressSparse( InputDict ):
    print "\r%s" %(InputDict['filename'], ),
    sys.stdout.flush()


def MakeDirlist( config ):
# 1) go though the directory and generate the .md5listdir files.
    print "Processing files in and below %s" % ( config['SourceDir'], )
    PD = ProcessDir(config['SourceDir'])
    
    global FileCount
    FileCount = 0
    
    Manifest = PD.Process(UseCache=True, ProgressFunction=config['ProgressFunction'])
    print "\rDone calculating md5 sums."
# 1.1) save manifest for later...
    if Manifest.getNumberOfEntries() != FileCount:
        print "File count and manifest size mismatch"
        print "Try deleting all .md5listdir cache files and try again"
        exit(2)
    print "Saving manifest file"
    Manifest.saveCache("%s.manifest" % (config['SourceDir']), UseFullPath=True)
    return FileCount, Manifest

def ParseCmdLineOptions():
    from optparse import OptionParser

    """ utility function to handle command line options. """
    parser = OptionParser()
                
    parser.add_option( "-d", dest="SourceDir", 
                       help="The directory to read from", default = '.' )
    parser.add_option( "--showfiles",
                  action="store_true", dest="showfiles", default=False,
                  help="print all filenames to stdout (debug option)" )
    (options, args) =  parser.parse_args() #@UnusedVariable
    
    return options
 

if __name__ == '__main__':
    print "MakeDirlist"
    opt = ParseCmdLineOptions()

    Config = { 'SourceDir': opt.SourceDir}
    
    if opt.showfiles:
        Config['ProgressFunction'] = ShowProgressAllFiles
    else:
        Config['ProgressFunction'] = ShowProgressSparse

    print "Params are %s"%(Config)
  
    MakeDirlist(Config)
      
    
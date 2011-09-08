'''
Created on Sep 6, 2011

@author: morten
'''
from PythonPathUtil import AppendSrcToPythonPath #@UnusedImport
from optparse import OptionParser
from ProcessDir.ProcessDir import ProcessDir
import sys, os
from time import sleep

def ParseCmdLineOptions():
    """ utility function to handle command line options. """
    parser = OptionParser()
                
    parser.add_option( "-d", dest="SourceDir", 
                       help="The directory to read from", default = '.' )
    parser.add_option( "-o", dest="OutputDir", default='.',
                      help="The directory to dump the squashfsfile to"  )                 
    parser.add_option( "-a", dest="AccessDir", default='/mnt/squashfs',
                       help="The directory where the squashfs file is accessible (done by automount)" )
 
    (options, args) =  parser.parse_args() #@UnusedVariable
    
    return options
 
 
def ShowProgress( InputDict ):
    #print "\r%s" %(InputDict['filename'], ),
    #sys.stdout.flush()
    global FileCount
    FileCount = FileCount +1
    print "\rFilecount %d"%(FileCount,),
                
if __name__ == '__main__':
    opt = ParseCmdLineOptions()
    
    print "SquashDir"
    print "Parameters are %s"%(opt,)
    
    # 1) go though the directory and generate the .md5listdir files.
    print "Processing filen in and below %s"%(opt.SourceDir,)
    PD = ProcessDir(opt.SourceDir)
    FileCount = 0
    Manifest = PD.Process(UseCache=True, ProgressFunction=ShowProgress)
    print "\rDone calculating md5 sums."
    
    # 1.1) save manifest for later...
    if Manifest.getNumberOfEntries() != FileCount:
        print "Filecount and manifest size mismatch"
        print "Try deleting all .md5listdir cache files and try again"
        print Manifest
        exit(2)
    print "Saving manifest file"
    Manifest.saveCache( "%s.manifest"%(opt.SourceDir), UseFullPath = True )
    
    # 2) squashfs the dir
    (SourceTop, SqfsFileBase) = os.path.split( opt.SourceDir )
    SqfsFile = os.path.join( opt.OutputDir, "%s.squashfs" % (SqfsFileBase,) )
    print "Creating squashfs file %s" %(SqfsFile)
    # This creates a squashfs with the current user as owner.
    # TODO: Uid mismatch when copying between PCs
    cmd = "mksquashfs %s %s -noappend" %(opt.SourceDir, SqfsFile)
    #os.system(cmd)
    
    AccessLink = os.path.join( opt.AccessDir, SqfsFileBase )
    cmd2 = "ln --symbolic %s %s" % (AccessLink, os.path.join(SourceTop, "%s.sqmnt"%(SqfsFileBase,) ))
    os.system( cmd2 )
    
    # 3) compare manifest with actual files.
    FailCount = 0
    FileCount = 0
    
    while not os.path.isfile( os.path.join(AccessLink, Manifest[0]['directory'], Manifest[0]['filename']) ):
        print "First file not found"
        print "access dir is %s" % AccessLink
        print "Sleeping for 30 s before trying aging"
        sleep(30)
        
    for entry in Manifest:
        FileToCheck = os.path.join(AccessLink, entry['directory'], entry['filename'])
        if not os.path.isfile( FileToCheck ):
            print "\rWarning: File not found %s" % FileToCheck
            FailCount += 1
        
        FileCount += 1
        print "\rFilecount %d (%d failed)"%(FileCount, FailCount),
    
    if FailCount > 0:
        print "Warning: Files missing in archive."
        exit( 3 )

    print "Checked %d filenames" % FileCount
    
    # 4) validated the .md5listdir values
    print "Validating md5 values in archive"    
    FileCount = 0
    ValidationSuccess = ProcessDir(opt.AccessDir).Validate( ValidateProgressFunction=ShowProgress)
    print "\nValidation done. %d files checked"%FileCount

    if ValidationSuccess:
        print "Archive matches cache"
    else:
        print "Warning: md5 validation failed"
        exit( 3 )
        
    print "Done creating and validating squashfs archive"
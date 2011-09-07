'''
Created on Sep 6, 2011

@author: morten
'''
from optparse import OptionParser
from ProcessDir.ProcessDir import ProcessDir
import sys, os

def ParseCmdLineOptions():
    """ utility function to handle command line options. """
    parser = OptionParser()
#    parser.add_option("-M", "--master", dest="MasterDir", default=".",
#                      help="Primary directory", metavar="MASTERDIR")
#    parser.add_option("-m", "--master-list", dest="MasterList", 
#                      help="Read from file instead of doing the work" )
#    parser.add_option("-D", "--dump-to-file", dest="DumpFile", 
#                      help="Save entire list to disk" )    
#                      
#    parser.add_option("-S", "--secondary", dest="SecondaryDir", default="",
#                      help="Secondary directory", metavar="SECONDARYDIR")
#    parser.add_option( "-q", action="store_false", dest="verbose", default=True,
#                      help="quiet mode (opposite of verbose)" )              
#    parser.add_option( "-v", action="store_true", dest="verbose",
#                      help="verbose mode (opposite of quiet)" )                 
    parser.add_option( "-d", dest="SourceDir", 
                       help="The directory to read from", default = '.' )
    parser.add_option( "-o", dest="OutputDir", default='.',
                      help="The directory to dump the squashfsfile to"  )                 
    parser.add_option( "-a", dest="AccessDir", default='/mnt/squashfs',
                       help="The directory where the squashfs file is accessible (done by automount)" )
 
    (options, args) =  parser.parse_args() #@UnusedVariable
    
    return options
 
def ShowProgress( InputDict ):
    print "\r%s" %(InputDict['filename'], ),
    sys.stdout.flush()
                
if __name__ == '__main__':
    opt = ParseCmdLineOptions()
    
    print "SquashDir"
    print "Parameters are %s"%(opt,)
    
    # 1) go though the directory and generate the .md5listdir files.
    print "Processing filen in and below %s"%(opt.SourceDir,)
    PD = ProcessDir(opt.SourceDir)
    Manifest = PD.Process(UseCache=True, ProgressFunction=ShowProgress)
    print "\rDone calculating md5 sums."
    
    # 1.1) save manifest for later...
    # Manifest.saveCache( "%s.manifest"%(opt.SourceDir) )
    # TODO: Manifest list is wrong. 
    
    # 2) squashfs the dir
    (SourceTop, SqfsFileBase) = os.path.split( opt.SourceDir )
    SqfsFile = os.path.join( opt.OutputDir, "%s.squashfs" % (SqfsFileBase,) )
    print "Creating squashfs file %s" %(SqfsFile)
    # This creates a squashfs with the current user as owner.
    # TODO: Uid mismatch when copying...
    cmd = "mksquashfs %s %s -noappend" %(opt.SourceDir, SqfsFile)
    os.system(cmd)
    
    AccessLink = os.path.join( opt.AccessDir, SqfsFileBase )
    cmd2 = "ln --symbolic %s %s" % (AccessLink, os.path.join(SourceTop, "%s.sqmnt"%(SqfsFileBase,) ))
    os.system( cmd2 )
    
    # 3) validated the .md5listdir values
    print "Validating archive"
    ValidationSuccess = ProcessDir(opt.AccessDir).Validate()
    if ValidationSuccess:
        print "Archive matches precalculated sums"
    else:
        print "Warning: md5 validation failed"
    pass
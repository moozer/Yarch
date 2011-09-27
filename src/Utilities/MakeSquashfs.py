'''
Created on Sep 16, 2011

@author: morten
'''
import os

def MakeSquashfs( Config ):
    
    Config['SourceDir'] = os.path.normpath(Config['SourceDir'])
    SourceTop, SqfsFileBase = os.path.split(Config['SourceDir'])
    
    if not 'SqfsMountLink' in Config.keys():
        Config['SqfsMountLink'] = os.path.join(SourceTop, "%s.sqmnt" % (SqfsFileBase, ))
    if not 'OutputDir' in Config.keys():
        Config['OutputDir'] = SourceTop
    if not 'SqfsFile' in Config.keys():
        Config['SqfsFile'] = os.path.join(Config['OutputDir'], "%s.squashfs" % (SqfsFileBase, ))
        
    # This creates a squashfs with the current user as owner.
    print "Creating squashfs file %s" % (Config['SqfsFile']) 
    print "Config is %s"%(Config,)
# TODO: Uid mismatch when copying between PCs
    cmd = "mksquashfs %s %s -noappend" % (Config['SourceDir'], Config['SqfsFile'])
    os.system(cmd)

    if 'SqfsAccessDir' in Config.keys():
        if not 'SqfsAccessLink' in Config.keys():
            Config['SqfsAccessLink'] = os.path.join(Config['SqfsAccessDir'], SqfsFileBase)
           
        # make symbolic link to access dir.
        cmd2 = "ln --symbolic %s %s" % (Config['SqfsAccessLink'], Config['SqfsFile'])
        os.system(cmd2)
    
    return Config

def ParseCmdLineOptions():
    from optparse import OptionParser

    """ utility function to handle command line options. """
    parser = OptionParser()
                
    parser.add_option( "-d", dest="SourceDir", 
                       help="The directory to read from", default = '.' )
    parser.add_option( "-o", dest="OutputDir", default=None,
                      help="The directory to dump the squashfsfile to"  )                 
    parser.add_option( "-a", dest="AccessDir", default=None,
                       help="The directory where the squashfs file is accessible (done by automount)" )    
    parser.add_option( "--showfiles",
                  action="store_true", dest="showfiles", default=False,
                  help="print all filenames to stdout (debug option)" )
    (options, args) =  parser.parse_args() #@UnusedVariable
    
    return options


if __name__ == '__main__':
    opt = ParseCmdLineOptions()


    Config = { 'SourceDir': opt.SourceDir}
    if opt.AccessDir:
        Config['SqfsAccessDir'] = opt.AccessDir
    if opt.OutputDir:
        Config['OutputDir'] = opt.OutputDir
    
    MakeSquashfs( Config )
    pass
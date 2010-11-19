#!/usr/bin/env python
#
#       SkemaToIcs.py
#       
#       Copyright 2009  <morten@Epia>
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
from optparse import OptionParser
from ProcessDir.ProcessDir import ProcessDir, DeleteByList, FileCache
import sys, os

def ParseCmdLineOptions():
    """ utility function to handle command line options. """
    parser = OptionParser()
    parser.add_option("-M", "--master", dest="MasterDir", default=".",
                      help="Primary directory", metavar="MASTERDIR")
    parser.add_option("-m", "--master-list", dest="MasterList", help="Read from file instead of doing the work" )
    parser.add_option("-D", "--dump-to-file", dest="DumpFile", help="Save entire list to disk" )    
                      
    parser.add_option("-S", "--secondary", dest="SecondaryDir", default="",
                      help="Secondary directory", metavar="SECONDARYDIR")
    parser.add_option( "-q", action="store_false", dest="verbose", default=True )                 
    parser.add_option( "-v", action="store_true", dest="verbose" )                 
    parser.add_option( "-c", action="store_true", dest="useCache", default=False,
                        help="Use cache (writes .md5listdir to all directories)" )
    parser.add_option( "-l", action="store_true", dest="AllowLinks", default=False )                 
    parser.add_option( "--delete-duplicates", action="store_true", dest="deletedups", default=False )
 
    (options, args) =  parser.parse_args() #@UnusedVariable
    
    if options.SecondaryDir == "":
        options.SecondaryDir = options.MasterDir
    return options
 
def ShowDuplicates( CacheList, CompareCacheList ):
    """ dump duplicates list to std output 
    
    @param Filelist The filelist with duplication info
    @param Comparelist The filelist that 'Filelist' refers to
    """
    Filelist = CacheList.getAllEntries()
    CompareList = CompareCacheList.getAllEntries()
    for i in range( len( Filelist ) ):
        if len( Filelist[i]['duplicates'] ) > 0:
            print   Filelist[i]['md5'], Filelist[i]['filename']
            for dup in Filelist[i]['duplicates']:
                print "\t", CompareList[dup]['filename']

def ShowDuplicatesSelfCompare( CacheList ):
    """ dump duplicates list to std output 
    
    @param Filelist The filelist with duplication info
    """    
    Filelist = CacheList.getAllEntries()
    for i in range( len( Filelist ) ):
        if len( Filelist[i]['duplicates'] ) > 1:
            # don't show if the current index is higher than the first duplicates entry
            if Filelist[i]['duplicates'][0] < i:
                continue

            print   Filelist[i]['md5'], os.path.join( Filelist[i]['directory'], Filelist[i]['filename'] )
            for dup in Filelist[i]['duplicates']:
                print "\t", os.path.join( Filelist[dup]['directory'], Filelist[dup]['filename'] )

def ProgressIndicator( Entry ):
    print Entry['filename'], "-", Entry['md5']

def OutputToStderr( SomeString ):
    sys.stderr.write( SomeString + "\n" )

def main():
    opt = ParseCmdLineOptions()

    # Function to call at each iteration
    if not opt.verbose:
        PF = None
    else:
        PF = ProgressIndicator

    # Read or process the master directory
    if opt.MasterList:
        print "Retrieving information from file:", opt.MasterList
        MasterCache = FileCache()
        MasterCache.loadCache( opt.MasterList )
    else:
        print "Processing master directory"
        MasterCache = ProcessDir( opt.MasterDir ).Process( ProgressFunction = PF, UseCache = opt.useCache, 
                    LinksAreFatal = not opt.AllowLinks )

    # save dirlist file?
    if opt.DumpFile:
        print "Saving masterlist to file:", opt.DumpFile
        MasterCache.saveCache( Filename = opt.DumpFile, UseFullPath = True )

    # After master dir is don, process second dir and compare.    
    print "Processing secondary directory"
    SecCache = ProcessDir( opt.SecondaryDir).Process( CompareList=MasterCache, ProgressFunction = PF, 
                    UseCache = opt.useCache, 
                    LinksAreFatal = not opt.AllowLinks )
    
    # and output
    print "Dumping duplicates list (if any)"
    if opt.MasterDir == opt.SecondaryDir:
        ShowDuplicatesSelfCompare( SecCache )
    else:
        ShowDuplicates( SecCache, MasterCache )

    # optionally delete duplicates
    if opt.deletedups:
        if opt.MasterDir == opt.SecondaryDir:
            print "Duplicates will only be erased from secondary (and Sec. and master are the same)"
        else:
            print "Deleting duplicates"
            DeleteByList( SecCache, VerboseFunction = OutputToStderr )
    
    
    return 0

if __name__ == '__main__': main()

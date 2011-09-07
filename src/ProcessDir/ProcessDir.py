#!/usr/bin/env python 
#
#       ProcessDir.py
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

import os
from ProcessFile.checksum import create_checksum
from FileCache import FileCache

def DumpFilelist( SomeText, Filelist ):
    ''' Utility function for nice output
    @param SomeText: The text to output before the list
    @param Filelist: The list with filenames, md5sum and, optionaly, the duplikates
    '''  
    print SomeText
    for i in range( len( Filelist ) ):
        if 'duplicates' in Filelist[i]:
            print   Filelist[i]['md5'], '\t',  \
                    Filelist[i]['filename'], '\t', \
                    Filelist[i]['duplicates']
        else:
            print   Filelist[i]['md5'], '\t',  \
                    Filelist[i]['filename']

class ProcessDir:
    """ class that handles recursing throught the directory structure
    When Process is called the actual processing is started
    """
    def __init__( self, BaseDir ):
        """ class constructor
        
        @param BaseDir The directory to process
        """
        if not os.path.isdir( BaseDir ):
            raise IOError( "Directory does not exist: %s"%BaseDir )
        self._BaseDir = BaseDir
        self._CacheFilename = '.md5dirlist'
        self._ValidationFailed = False

    def Validate(self, ValidateProgressFunction = None):
        """ processes the directory and compare the calculated md5 with the stored from cachefile
        @return True on succesful validation"""
        self.Process(Validate = True, UseCache = False, ProgressFunction = ValidateProgressFunction)
        return not self._ValidationFailed
        
    def Process( self,  CompareList = FileCache(), ProgressFunction = None, 
                        UseCache = False, LinksAreFatal = False,
                        Validate = False ):
        """ Processes the directory supplied in the constructor 
            recursively and returns the information extracted 
            a list of dictionaries with 'md5', 'filename' and 'duplicate' 
            (a list referring to the indices of CompareList)
        @param ProgressFunction: An optional function to enables showing progress. \
            It takes the current ('md5', 'filelist', 'duplicates') dictionary as parameter
        @param UseCache: If true, any cache is true if found, otherwise ignored
        @param Validate:if true, calculated md5 sum are compared to stored ones.
        """

        self._CompareList = CompareList.getAllEntries()
        self._ProgressFunction = ProgressFunction
        self._UseCache = UseCache
        self._LinksAreFatal = LinksAreFatal
        self._Validate = Validate
        return self._ProcessDir( self._BaseDir )


    def _ProcessDuplicate(self, FileData):
        ''' Checks the current file against the previous ones for duplicates (based on md5)'''
        Duplicates = []
        for i in range(len(self._CompareList)):
            if self._CompareList[i]['md5'] == FileData['md5']:
                Duplicates.append(i)
        
        return Duplicates



    def _ProcessFile(self, DirToProcess, Cache, CurDir, filename):
        # skip the cache file
        if filename == self._CacheFilename:
            return None
        
        FullFilename = os.path.join(CurDir, filename)
        if os.path.islink(FullFilename):
            if self._LinksAreFatal:
                raise IOError("File is a link: " + FullFilename) 
            else: 
                return None # skip
        # else: just continue

        # load cache if appropriate file
        if self._UseCache or self._Validate:
            FileData = Cache.getEntry(filename)
        else:
            FileData = None

        if self._Validate:
            if not FileData:
                self._ValidationFailed = True
            else:
                NewMd5 = create_checksum( FullFilename )
                if FileData['md5'] != NewMd5:
                    self._ValidationFailed = True
            
        # if not using the cache or file not in cache
        if not FileData:
            md5 = create_checksum( FullFilename )
            FileData = {"md5": md5}
            
        # check for duplicates and build return dict
        ResDict = {'md5':FileData['md5'], 'filename':filename, 
                   'duplicates':self._ProcessDuplicate(FileData), 
                   'directory':os.path.relpath(CurDir, DirToProcess)}
        
        return ResDict

    def _ProcessDir( self, DirToProcess ):
        """ internal function to do the actual processing """
        # we always use cache (might be in memory)
        Cache = FileCache( DirToProcess )

        # loop through all entries
        for CurDir, dirs, files in os.walk( DirToProcess ): #@UnusedVariable
      
            # Cache handling
            if self._UseCache or self._Validate:
                if CurDir != Cache.GetDirectory():
                    if self._UseCache:
                        Cache.saveCache() # save before new cache is initialized
                    Cache = FileCache( CurDir )
                try:
                    Cache.loadCache()
                except IOError:
                    pass # IOError here means that cache file does not exist

            # loop through files
            for filename in files:
                ResDict = self._ProcessFile(DirToProcess, Cache, CurDir, filename)
                
                # checking if file was skipped for some reason
                if ResDict == None:
                    continue

                # always add to Cache (might be in memory only)
                Cache.addEntry( ResDict )
         
                # output/update/whatever for each file
                if self._ProgressFunction:
                    self._ProgressFunction( ResDict )
                   
        # Cache handling. save to disk
        if self._UseCache:
            Cache.saveCache()

        return Cache


def DeleteByList( CacheList, VerboseFunction = None ):
    """ delete every item on supplied list with duplicates
    @param CacheList a FileCache object that hold the files to be deleted 
    @param VerboseFunction A function that takes a string as parameter. Used for progress indication. 
    """
    for Entry in CacheList.getAllEntries():
        if len( Entry['duplicates'] ) == 0:
            if VerboseFunction:
                VerboseFunction( "Skipping " + Entry['filename'] );
        else:
            if VerboseFunction:
                VerboseFunction( "Deleting " + Entry['filename'] );
            os.remove( os.path.join( CacheList.GetDirectory(), Entry['directory'], Entry['filename'] ) )
    

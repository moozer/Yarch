#!/usr/bin/env python
#
#       FileCache.py
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

import os, csv

class FileCache:
    """ class to handle caching of md5 sums """
    
    def __init__( self, Directory = '.', BaseDir = '.', Data = None, 
                  CacheFilename = '.md5dirlist' ):
        """ class constructor 
        @param Directory: The directory to work in
        @param Data: Initial data to use (uses addEntry)  
        @param CacheFilename: The filename to use for the datafile 
        @param BaseDir: The directory to be appended to 'directory' in entries
        """
        self._FileCache = []
        self._Directory = Directory
        self._MandatoryKeys = ['filename', 'md5', 'directory']
        self._BaseDir = BaseDir
        self._IteratorIndex = 0
        
        if not os.path.isdir( Directory ):
            raise IOError( "Directory specified is not a directory: %s"% Directory )
        
        self._CacheFilename = CacheFilename
    
        if Data:
            for Entry in Data:
                self.addEntry( Entry )
    
    def __iter__(self):
        return self
    
    def next(self):
        self._IteratorIndex = self._IteratorIndex + 1
        if self._IteratorIndex > len(self._FileCache):
            raise StopIteration
        return self._FileCache[self._IteratorIndex -1]
    
    def __eq__( self, other ):
        """ the equality operator 
        
        @param other The FileCache object to compare with 
        @raises TypeError when the other object is non-FileCache
        """
        if type( self ) != type( other ):
            raise TypeError( 'Cannot compare with objects of type ' + str( type( other ) ) )
        return (self._FileCache == other.getAllEntries())
    
    def __str__( self ):
        """ toString function. Just outputs something fairly readable 
        
        @return Human readable (not pretty) text of FileCache content
        """
        Output = ""
        for i in range( len( self._FileCache ) ):
            Output += str( self._FileCache[i] ) + '\n'
        return Output
                    
    def __iadd__( self, other ):
        """ handling of +=
        Use other.completeEntries() id the directories are to be correct
        
        @param other The FileCache object to add  
        @raises TypeError when the other object is non-FileCache
        @returns The 'self' object
        """
        if type( self ) != type( other ):
            raise TypeError( 'Cannot compare with objects of type ' + str( type( other ) ) )
        
        for Entry in other.getAllEntries():
            self.addEntry( Entry )
        
        return self
        
    def getNumberOfEntries( self ):
        """ @returns the number of files in the cache """
        return len( self._FileCache )
        
    def addEntry( self, Entry ):
        """ adds the entry to the cache 
        
        @param Entry The entry to add (a dictionary with 'filename' and 'md5' )
        """
        # directory defaults to current dir.
        if not 'directory' in Entry.keys():
            Entry['directory'] = self._BaseDir
    
        keys = Entry.keys()    
        for mkey in self._MandatoryKeys:
            if ( mkey not in keys):
                raise ValueError( "Malformed entry supplied ('%s' not found)" % mkey )

        # overwrite dupplicates.
        for i in range( len( self._FileCache ) ):
            if  self._FileCache[i]['filename'] == Entry['filename'] \
                and self._FileCache[i]['directory'] == Entry['directory']:
                self._FileCache[i] = Entry.copy()
                return
        
        self._FileCache.append( Entry.copy() )
        
    def getEntry( self, FilenameIdentifier = None ):
        """ return the first entry corresponding to the filename
        
        @param FilenameIdentifier The filename used as identifier in the cache. If omitted, all entries are returned
        @returns A file entry. None if not in list
        """
        if not FilenameIdentifier:
            return self.getAllEntries()
        
        for Entry in self._FileCache:
            if Entry['filename'] == FilenameIdentifier:
                return Entry
                
        return None

    def getAllEntries( self ):
        """ returns all cached entries """
        return self._FileCache

    def reset( self ):
        """ Removes all entries from the cache """
        self._FileCache = []

    def loadCache( self, Filename = None ):
        """ loads data from file on disc and saves in the internal var  self._FileCache
        using filenames as keys 
        """
        if not Filename:
            Filename = self._CacheFilename
        
        self.reset()
        FullCacheFilename = os.path.join( self._Directory, Filename )

        # if the file does not exist, the list is empty
        if not os.path.exists( FullCacheFilename ):
            raise IOError( "Cache file not found: " + FullCacheFilename )
        
        # otherwise read from file
        CacheReader = csv.reader(open(FullCacheFilename), delimiter='\t', quotechar='|')
        for row in CacheReader:
            if len( row ) != 2:
                raise ValueError( "Malformed cache file: " + FullCacheFilename)
                
            # use filename as key
            self.addEntry( { 'directory': self._BaseDir, 'filename': row[1], 'md5': row[0] } )
            
        # and return the number of entries read
        return  self.getNumberOfEntries()

    def saveCache( self, Filename = None, UseFullPath = False ):
        """ Saves the current file cache list to disk 
        
        @param Directory The current work directory.
        """
        if not Filename:
            Filename = self._CacheFilename
            
        FullCacheFilename = os.path.join( self._Directory, Filename  )
        CacheWriter = csv.writer(open(FullCacheFilename, 'w'), delimiter='\t', 
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

        Count = 0
        for Entry in self.getAllEntries():
            if UseFullPath:
                CacheWriter.writerow( [Entry['md5'], os.path.join( Entry['directory'], Entry['filename'] ) ] )
            else:
                CacheWriter.writerow( [Entry['md5'], Entry['filename']] )
            Count += 1

        return Count

    def completeEntries( self ):
        """ check each entry and adds 'directory' and 'duplicates' where needed """
        for i in range( len( self._FileCache ) ):
            keys = self._FileCache[i].keys()
            if not 'duplicates' in keys:
                self._FileCache[i]['duplicates'] = []
            if not 'duplicates' in keys:
                self._FileCache[i]['directory'] = self._Directory
 
    def GetDirectory(self):
        """ returns the current directory """
        return self._Directory
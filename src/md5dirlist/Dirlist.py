#!/usr/bin/env python
#
#       Dirlist.py
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

import os.path
from DirlistError import DirlistError
import datetime
from ProcessFile.ProcessFile import create_checksum
import base64

class Dirlist:
    ''' Class to handle caching of md5 sums '''
    
    class DlEntry:
        ''' enumerator class '''
        file, size, mtime, md5, EntryCount = range( 0, 5 )
    
    def __init__(self, Basedir = '.', DirlistFilename = '.dirlist.md5' ):
        ''' Class constructor '''
        if not os.path.isdir( Basedir ):
            raise DirlistError( "Directory does not exist: %s"%Basedir )
            
        self._Basedir = Basedir
        self._Seperator = '\t'
        self._TimeFormatString = "%Y-%m-%d %H:%M:%S"
        self._DirlistFilename = DirlistFilename
        return

    # --- Accessors ---
    def getBasedir( self ):
        ''' Basedir accesor function '''
        return self._Basedir

    # --- Creating or whatever to get the dirlist ---
    def getDirlist( self ):
        ''' check for dirlist file, other wise it generates a new one '''
        if self.isDirlistPresent():
            return self.readDirlistFromFile();
        
        dl = self.createDirlist();
        self.writeDirlistToFile( dl )
        return dl
    
    def createDirlist( self ):
        ''' creates the list of (filename, md5, time, size) for 
            the dirlist file '''
        file_collection = []
        for filename in os.listdir(self._Basedir):
            try:
                # magic filename that gets ignored
                if filename == self._DirlistFilename:
                    continue

                # sanity check of files
                fullpath = os.path.join(self._Basedir, filename)
                if not os.path.isfile( fullpath ):
                    continue

                filestat = os.stat( fullpath )
                mtime =  datetime.datetime.fromtimestamp( filestat.st_mtime )
                size = filestat.st_size
                md5 = create_checksum(fullpath)
                file_collection.append( {'file': filename, 'size': size, 'mtime': mtime, 'md5': md5} )
            except OSError:
                # file level exception are ignored.
                print "Bad stuff in", filename
                pass
    
        return file_collection
        
    def extractDirlist( self, Input ):
        ''' Use output data as input to recreate the dirlist. '''
        Dirlist = []
        Lines = Input.splitlines()
        for Line in Lines:
            Entries = Line.split( self._Seperator )
            
            if len(Entries) != self.DlEntry.EntryCount:
                raise DirlistError( "Bad number of entries. " + "Expected " + str( self.DlEntry.EntryCount ) 
                                        + " got " + str( len(Entries) ) )
                
            file = {}
            file['file'] = Entries[self.DlEntry.file]
            file['size'] = long( Entries[self.DlEntry.size] )
            file['mtime'] = datetime.datetime.strptime( Entries[self.DlEntry.mtime], self._TimeFormatString)
            file['md5'] = base64.b64decode( Entries[self.DlEntry.md5] )
            
            Dirlist.append( file )
            
        return Dirlist

    # --- Output to be saved to file ---
    def generateOutput( self, Data ):
        ''' generate ouput based on data from createDirlist '''
        Output = ""
        for file in Data:
            FileEntryText = file['file'] + self._Seperator 
            FileEntryText += str( file['size'] ) + self._Seperator 
            FileEntryText += str( file['mtime'] ) + self._Seperator 
            FileEntryText += base64.b64encode( file['md5'] )
            Output += FileEntryText + '\n'
        
        return Output
            
    # --- File IO ---
    def readDirlistFromFile( self ):
        ''' reads from the designated dirlist file. '''
        f = open( os.path.join(self._Basedir, self._DirlistFilename), "r" )
        data = f.read();
        f.close()
        return self.extractDirlist( data )
        
    def writeDirlistToFile( self, Data ):
        ''' writes the supplied data to file '''
        output = self.generateOutput( Data )
        
        f = open( os.path.join(self._Basedir, self._DirlistFilename), "w" )
        f.write( output )
        f.close()

    # --- utility functions ---
    def isDirlistPresent( self ):
        ''' Returns true if there exists an dirlist file already '''
        Filename = os.path.join(self._Basedir, self._DirlistFilename)
        return os.path.isfile( Filename )

   

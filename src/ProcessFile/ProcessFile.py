#!/usr/bin/env python
#
#       ProcessFile.py
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

from checksum import create_checksum
def ProcessFile( Filename, Filelist = [] ):
    """ Calculates MD5 sum and compares it with the supplied list
        returns a dictionary with 'md5' sum, 'dupplicates' list
        
    """
    md5 = create_checksum( Filename )

    Duplicates = []    
    for i in range( len( Filelist ) ):
        if Filelist[i]['md5'] == md5:
            Duplicates.append( i )

    return {'md5': md5, 'duplicates': Duplicates }

    

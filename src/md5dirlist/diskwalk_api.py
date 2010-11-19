import os

class diskwalk(object):
    """API for getting directory walking collections"""
    def __init__(self, path):
        self.path = path

    def enumeratePaths(self):
        """Returns the path to all the files in a directory as a list"""
        path_collection = []
        for dirpath, dirnames, filenames in os.walk(self.path): #@UnusedVariable
            for file in filenames:
                fullpath = os.path.join(dirpath, file)
                path_collection.append(fullpath)

        return path_collection

    def enumerateFiles(self):
        """Returns all the files in a directory as a list"""
        file_collection = []
        for dirpath, dirnames, filenames in os.walk(self.path): #@UnusedVariable
            for file in filenames:
                file_collection.append(file)

        return file_collection

    def enumerateDir(self):
        """Returns all the directories in a directory as a list"""
        dir_collection = []
        for dirpath, dirnames, filenames in os.walk(self.path): #@UnusedVariable
            for dir in dirnames:
                dir_collection.append(os.path.join(dirpath, dir))

        return dir_collection
        
    def enumerateFilesByExt(self, Extension ):
        """Returns all the files in a directory """
        file_collection = []
        for dirpath, dirnames, filenames in os.walk(self.path): #@UnusedVariable
            for file in filenames:
                (unused, sep, ext) = file.rpartition('.')
                if sep == '.' and ext == Extension:
                    file_collection.append( file )

        return file_collection


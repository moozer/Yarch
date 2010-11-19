# This file is from the book
# "Python for unix and linux system administrators"
# http://www.p4
import hashlib

def create_checksum(path):
        """
        Reads in file.  Creates checksum of file line by line.
        Returns complete checksum total for file.

        """
        fp = open(path)
        checksum = hashlib.md5()
        while True:
            buffer = fp.read(8192)
            if not buffer:break
            checksum.update(buffer)
        fp.close()
        # changed .digest() to .hexdigest() for easier verification using md5sum command
        checksum = checksum.hexdigest()
        return checksum


import os
import math
from bitarray import bitarray


# Read file - return content
def read_file(file_name):
    file = open(file_name, 'r')
    return file.read()

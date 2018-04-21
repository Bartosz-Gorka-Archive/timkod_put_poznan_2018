import os
import math
from bitarray import bitarray


# Read file - return content
def read_file(file_name):
    file = open(file_name, 'r')
    return file.read()


# Analyze content - calculate probability
def analyze_content(content):
    letters = {}
    counter = 0

    for _, letter in enumerate(content):
        cardinality = letters.get(letter, 0)
        letters.update({letter: cardinality + 1})
        counter += 1

    return letters, counter


# Cardinality to probability change
def to_probability(dictionary, counter):
    for letter in dictionary:
        dictionary.update({letter: dictionary.get(letter) / counter})
    return dictionary

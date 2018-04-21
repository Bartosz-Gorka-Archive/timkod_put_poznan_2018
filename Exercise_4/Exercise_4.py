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


# Create code
def create(dictionary):
    code_dictionary = {}
    unique_characters = len(dictionary.keys())
    length = math.ceil(math.log(unique_characters + 1, 2))

    for index, key in enumerate(dictionary.keys()):
        base = int_to_bits(length, index)
        code_dictionary.update({key: base})
    return code_dictionary, length


# Convert integer value to bit array
def int_to_bits(length, value):
    bits_array = [1 if digit == '1' else 0 for digit in bin(value)[2:]]
    bits = bitarray(length - len(bits_array))
    bits.setall(0)
    for bit in bits_array:
        bits.append(bit)
    return bits


# Encode text
def encode(code_dict, text):
    encoded = bitarray()

    for letter in text:
        for bit in code_dict.get(letter):
            encoded.append(bit)

    return encoded

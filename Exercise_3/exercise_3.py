import math
import numpy as np


def read_file(name):
    # Open file
    file = open(name, 'r')

    # Return content
    return file.read()


def exercise_1_generator(size, alphabet, probability):
    # Result
    results = ""

    # Loop to generate size-long text
    for _ in range(size):
        results += np.random.choice(alphabet, p=probability)

    # Return prepared text
    return results


def entropy(dictionary):
    # Entropy sum
    entropy_result = 0.0

    # Loop to analyze
    for key, value in dictionary.items():
        entropy_result += value * math.log(value, 2)

    # Return result
    return -entropy_result


def analyze_content(content):
    # Letters dictionary
    letters = {}

    # Letters counter to prepare probability of single letter
    counter = 0

    # Loop to analyze content
    for _, letter in enumerate(content):
        cardinality = letters.get(letter, 0)
        letters.update({letter: cardinality + 1})
        counter += 1

    # Loop to change cardinality to probability
    for letter in letters:
        letters.update({letter: letters.get(letter) / counter})

    # Return letters dictionary
    return letters


def main():
    debug = True

    file_name = '../Exercise_1/norm_wiki_sample.txt'
    content = read_file(file_name)

    #
    # Exercise 1 - Random, all letters with probability 1/37
    #

    letters = list('qwertyuiopasdfghjklzxcvbnm0123456789 ')
    probability = [1/37 for _ in letters]
    size = 10_000
    text = exercise_1_generator(size=size, alphabet=letters, probability=probability)
    letters_dictionary = analyze_content(text)
    entropy_result = entropy(letters_dictionary)

    if debug:
        print('Exercise 1 - Raw, random text')
        print('\tEntropy =>', entropy_result)

    #
    # Exercise 1 - Analyze content from sample Wiki
    #

    size = 10_000
    letters_dictionary = analyze_content(content)
    text = exercise_1_generator(size=size, alphabet=list(letters_dictionary.keys()), probability=list(letters_dictionary.values()))
    letters_dictionary = analyze_content(text)
    entropy_result = entropy(letters_dictionary)

    if debug:
        print('Exercise 1 - Based on text')
        print('\tEntropy =>', entropy_result)

    #
    # Exercise 2
    #


if __name__ == '__main__': main()

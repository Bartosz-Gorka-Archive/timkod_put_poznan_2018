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


def analyze_characters(content, row):
    # Results - dictionary with letters
    letters = {}

    # Last characters
    last_characters = []

    # Counter
    counter = 0

    # Loop to iterate
    for char in content:
        if len(last_characters) == row:
            # Fetch dictionary
            selected_dictionary = letters.get(''.join(last_characters), {})

            # Update total counter
            total = selected_dictionary.get('--TOTAL--', 0)
            selected_dictionary.update({'--TOTAL--': total + 1})

            # Update counter this letter
            cardinality = selected_dictionary.get(char, 0)
            selected_dictionary.update({char: cardinality + 1})

            # Update selected dictionary
            letters.update({''.join(last_characters): selected_dictionary})

            # Update counter
            counter += 1

        # Append char to list
        last_characters.append(char)

        # Check length - if greater than row -> delete first char (FIFO)
        if len(last_characters) > row:
            del (last_characters[0])

    # Return letters dictionary with counter
    return letters, counter


def cardinality_to_probability(dictionary, counter):
    # Result dictionary to speed up actions - add values to new dictionary
    result = {}

    # Separator
    separator = ''

    # Loop to change cardinality to probability
    for key, value_dict in dictionary.items():
        # Fetch cardinality from special key
        cardinality = value_dict.pop('--TOTAL--')

        # Add single key to result's dictionary as probability value
        result.update({key: cardinality / counter})

        # Loop to iterate - values in dictionary
        for value_key, value in value_dict.items():
            # Set value
            result[key + separator + value_key] = value / cardinality

    # Return updated dictionary
    return result


def main():
    debug = True

    file_name = 'short_sample.txt'
    content = read_file(file_name)

    value, counter = analyze_characters(content, 1)
    value = cardinality_to_probability(value, counter)
    # for key, value in value.items():
    #     print(key, value)

    #
    # Exercise 1 - Random, all letters with probability 1/37
    #

    # letters = list('qwertyuiopasdfghjklzxcvbnm0123456789 ')
    # probability = [1/37 for _ in letters]
    # size = 10_000
    # text = exercise_1_generator(size=size, alphabet=letters, probability=probability)
    # letters_dictionary = analyze_content(text)
    # entropy_result = entropy(letters_dictionary)
    #
    # if debug:
    #     print('Exercise 1 - Raw, random text')
    #     print('\tEntropy =>', entropy_result)

    #
    # Exercise 1 - Analyze content from sample Wiki
    #

    # size = 10_000
    # letters_dictionary = analyze_content(content)
    # text = exercise_1_generator(size=size, alphabet=list(letters_dictionary.keys()), probability=list(letters_dictionary.values()))
    # letters_dictionary = analyze_content(text)
    # entropy_result = entropy(letters_dictionary)
    #
    # if debug:
    #     print('Exercise 1 - Based on text')
    #     print('\tEntropy =>', entropy_result)

    #
    # Exercise 2
    #


if __name__ == '__main__':
    main()

    # TODO list
    # * Analyze entropy for single letter in text
    # * Analyze entropy for word in text
    # * Conditional entropy for letters - generic function with row as parameter
    # * Conditional entropy for word - generic function with row as parameter
    # * Loop to make ^ calculations for all files

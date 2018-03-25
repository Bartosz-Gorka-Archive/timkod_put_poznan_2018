import random
import operator
import numpy as np


# Read file's content
def read_file(name):
    file = open(name, 'r')
    return file.read()


# Roulette wheel
def roulette_wheel(words, probability):
    value = random.random()
    probability_sum = 0.0
    selected = 0

    for ind, val in enumerate(probability):
        probability_sum += val
        if probability_sum >= value:
            selected = ind
            break

    return words[selected]


# Simple stats file's content
def file_to_work_dict(filename):
    content = read_file(filename)
    words = content.split()
    result = {}
    total = 0

    for word in words:
        total += 1
        result = modify_dict(result, '', word)

    return result, total


# Modify dictionary - upgrade counters
def modify_dict(dictionary, key, word):
    selected = dictionary.get(key, {})
    value = selected.get(word, 0) + 1
    selected.update({word: value})
    dictionary.update({key: selected})

    return dictionary


# Generator - exercise 2
def exercise_2_generator(dictionary, length):
    result = ''
    keys = list(dictionary.keys())
    probability = list(dictionary.values())
    total = sum(dictionary.values())

    # Normalize
    for ind, val in enumerate(probability):
        probability[ind] = val / total

    # Generate content
    for _ in range(length):
        word = np.random.choice(keys, p=probability)
        result += word
        result += ' '

    return result


# Fetch details about n-rows dictionary (required in Markov chains)
def dictionary_n_row(filename, row):
    content = read_file(filename)
    words = content.split()
    result = {}
    last_words = []

    for word in words:
        if len(last_words) == row:
            result = modify_dict(result, ' '.join(last_words), word)

        last_words.append(word)
        if len(last_words) > row:
            del (last_words[0])

    return result


# Exercise 3 - generator Markov's chains
def generate_content(dictionary, row, start_word='', length=200, dict_first_row={}, dict_second_row={}):
    last_words = []
    content = ''

    # Start value
    if start_word != '':
        last_words.append(start_word)
        content += start_word
        content += ' '

    # Generate content
    for _ in range(length):
        len_words = len(last_words)
        if len_words == 0:
            selected = dictionary
        elif len_words == 1:
            selected = dict_first_row
        else:
            selected = dict_second_row

        selected_dictionary = selected.get(' '.join(last_words), {})
        words = list(selected_dictionary.keys())
        probability = list(selected_dictionary.values())
        total_probability = sum(selected_dictionary.values())
        for ind, val in enumerate(probability):
            probability[ind] = val / total_probability

        generated = roulette_wheel(words, probability)
        content += generated
        content += ' '

        last_words.append(generated)
        if len_words >= row:
            del(last_words[0])

    return content


# Main function
def main():
    files = ['test.txt', 'norm_wiki_sample.txt']

    # Exercise 1
    dictionary, total_words = file_to_work_dict(files[1])
    sorted_x = sorted(dictionary.get('', {}).items(), key=operator.itemgetter(1), reverse=True)

    print('Exercise 1:')
    total = 0
    for i in range(30_000):
        total += sorted_x[i][1]
    print('30 tys -', str(total / total_words)[:4])

    total = 0
    for i in range(6_000):
        total += sorted_x[i][1]
    print('6 tys -', str(total / total_words)[:4])

    # Exercise 2
    exercise_2 = exercise_2_generator(dictionary.get(''), 100)
    print('\nExercise 2:')
    print(exercise_2)

    # # Exercise 3
    print('\nExercise 3:')
    print('Analyze ...')
    dictionary_first_row = dictionary_n_row(files[1], 1)
    dictionary_second_row = dictionary_n_row(files[1], 2)
    print('Analyze completed')

    print('\nPart 1:')
    content = generate_content(dictionary, 1, '', 200, dictionary_first_row, dictionary_second_row)
    print(content)

    print('\nPart 2:')
    content = generate_content(dictionary, 2, '', 200, dictionary_first_row, dictionary_second_row)
    print(content)

    print('\nPart 3:')
    content = generate_content(dictionary, 2, 'probability', 200, dictionary_first_row, dictionary_second_row)
    print(content)


if __name__ == '__main__':
    main()

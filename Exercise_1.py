import numpy as np
import operator
from collections import Counter


# TODO
def exercise_1(size):
    alphabet = list("qazxswedcvfrtgbnhyujmkilop ")
    total_length = 0
    for _ in range(size):
        total_length += len(exercise_1_single_word(alphabet))

    return total_length / size


# TODO
def exercise_1_single_word(alphabet):
    word = ""
    while True:
        char = np.random.choice(alphabet)
        if char != " ":
            word += char
        else:
            break
    return word


# TODO
def read_file(name):
    file = open(name, 'r')
    return file.read()


# TODO
def file_parameters(filename):
    content = read_file(filename)
    total_length = 0
    words = content.split(" ")

    for word in words:
        total_length += len(word)

    return total_length / len(words)


# TODO
def exercise_2(filename):
    content = read_file(filename)
    letters = {}
    counter = 0

    for _, letter in enumerate(content):
        cardinality = letters.get(letter, 0)
        letters.update({letter: cardinality + 1})
        counter += 1

    for letter in letters:
        letters.update({letter: letters.get(letter) / counter})

    return letters


# TODO
def exercise_3(size, frequency):
    keys = list(frequency.keys())
    probability_list = list(frequency.values())
    total_length = 0

    for _ in range(size):
        total_length += len(exercise_3_word_generator(keys, probability_list))

    return total_length / size

# TODO
def exercise_3_word_generator(alphabet, probability):
    word = ""
    while True:
        char = np.random.choice(alphabet, p=probability)
        if char != " ":
            word += char
        else:
            break
    return word


# TODO
def exercise_4(filename):
    content = read_file(filename)
    letters = {}
    counter = 0
    old_letter = ""

    for _, letter in enumerate(content):
        if old_letter != "":
            dictionary_item = letters.get(old_letter, {})
            cardinality = dictionary_item.get(letter, 0)
            cardinality_total = dictionary_item.get("total", 0)

            dictionary_item.update({letter: cardinality + 1})
            dictionary_item.update({"total": cardinality_total + 1})
            letters.update({old_letter: dictionary_item})
            counter += 1
        old_letter = letter

    return letters, counter


# TODO
def main():
    # File details
    print("File details:")
    # files = ["norm_hamlet.txt", "norm_romeo_and_juliet.txt", "norm_wiki_sample.txt"]
    files = ["norm_hamlet2.txt"] # TODO delete
    for filename in files:
        print("\tFile =", filename, "\tAverage length =", file_parameters(filename), "characters")

    # Exercise 1
    words_size = 2000
    print("\nExercise 1:\n\tWords =", words_size, "\tAverage length =", exercise_1(words_size), "characters")

    # Exercise 2
    frequency = {}
    print("\nExercise 2:")
    for filename in files:
        frequency = exercise_2(filename)
        print("\tFile =", filename, "\tLetters:", frequency)

    # Exercise 3
    print("\nExercise 3:\n\tWords = ", words_size, "\tAverage length =", exercise_3(words_size, frequency), "characters")

    # Exercise 4
    frequency_first = {}
    sorted_x = sorted(frequency.items(), key=operator.itemgetter(1))
    exercise_4_first_letter = sorted_x.pop()[0]
    exercise_4_second_letter = sorted_x.pop()[0]

    print("\nExercise 4:")
    for filename in files:
        frequency_first, counter = exercise_4(filename)
        print("\tFile =", filename, "\tLetters:", frequency_first)

        print("\n\tSelected top used - starts with `" + exercise_4_first_letter + "` or `" + exercise_4_second_letter + "`")
        results = {exercise_4_first_letter: frequency_first.get(exercise_4_first_letter, {}), exercise_4_second_letter: frequency_first.get(exercise_4_second_letter, {})}
        for dictionary in results:
            for (key, value) in results.get(dictionary).items():
                if key != "total":
                    print("\t\t", dictionary + key, value / counter)
        print("\n\t------------------------------------------\n")

    # Exercise 5


if __name__ == "__main__":
    main()

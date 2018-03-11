import numpy as np
import operator
import random


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
def update_dictionary(dictionary, letters, index):
    single = dictionary.get(letters[index], {})
    cardinality_total = single.get("total", 0)
    single.update({"total": cardinality_total + 1})
    dictionary.update({letters[index]: single})

    return dictionary


# TODO
def modify_dictionaries(dictionary, letters_list):
    list_index = len(letters_list)
    rows = list_index

    for i in range(list_index):
        rows -= 1
        selected_dictionary = dictionary

        for j in range(rows):
            selected_dictionary = selected_dictionary.get(letters_list[i + j], {})

        update_dictionary(selected_dictionary, letters_list, list_index - 1)

    return dictionary


# TODO
def exercise_5_analyze(filename, row):
    content = read_file(filename)
    # content = content[:1_000_000]
    dictionary = {}
    counter = 0
    letters = []

    for _, letter in enumerate(content):
        letters.append(letter)
        if len(letters) > row:
            del(letters[0])

        dictionary = modify_dictionaries(dictionary, letters)
        counter += 1

    dictionary.update({"total": counter})
    return dictionary


# TODO
def roulette_wheel(letters, probability):
    value = random.random()
    probability_sum = 0.0
    selected = 0

    for ind, val in enumerate(probability):
        probability_sum += val
        if probability_sum >= value:
            selected = ind
            break

    return letters[selected]


# TODO
def exercise_5_generator(dictionary, row, length):
    result = "probability"
    letters = list(result)
    for _ in range(len(letters) - row):
        del(letters[0])

    for i in range(length):
        selected_dictionary = dictionary

        for ind, value in enumerate(letters):
            selected_dictionary = selected_dictionary.get(value, {})

        total = selected_dictionary.get("total")
        letters_to_random = list()
        probability_to_random = list()

        for (key, value) in selected_dictionary.items():
            if key != "total":
                letters_to_random.append(key)
                probability_to_random.append(value.get("total") / total)

        if probability_to_random:
            char = roulette_wheel(letters_to_random, probability_to_random)
        else:
            char = np.random.choice(list("qazxswedcvfrtgbnhyujmkilop "))

        result += char

        letters.append(char)
        if len(letters) > row:
            del(letters[0])

    return result


# TODO
def main():
    # File details
    print("File details:")
    files = ["norm_hamlet.txt", "norm_romeo_and_juliet.txt", "norm_wiki_sample.txt"]
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
    print("\nExercise 5:")
    filename = files[len(files) - 1]
    print("Analyze file", filename)
    statistics = exercise_5_analyze(filename, 6)
    for row in [1, 3, 5]:
        content = exercise_5_generator(statistics, row, 10000)

        last_char = ""
        words = 0
        for char in content:
            if char == " " and last_char != " ":
                words += 1

        print("Row =", row, "\tAverage length:", len(content) / words)


if __name__ == "__main__":
    main()
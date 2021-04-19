import sys
import os
import math
import string
import json
import pickle

def main():
    file_list = []
    documents = {}
    inverted_index = {}
    sentence_lengths = {}
    max_sentence_freqs = {}


    pickled_file_tokenized = open(sys.argv[1], "rb")
    pickled_file_raw = open(sys.argv[2], "rb")

    raw_files = []
    try:
        while True:
            file = pickle.load(pickled_file_raw)
            raw_files.append(file)
    except EOFError:
        print("end of file")
    tokenized_files = []
    try:
        while True:
            file = pickle.load(pickled_file_tokenized)
            tokenized_files.append(file)
    except EOFError:
        print("end of file")


     # For each sentence, obtain the content and add it to the inverted index
    for sentence in range(len(tokenized_files)):
        print(sentence)
        inverted_index, term_freqs = indexSentence(tokenized_files[sentence], sentence, inverted_index)

        # Exit the program if multiple identical IDs are found
        if sentence in sentence_lengths:
            print("sentence_ID already in sentence_lengths and was overwritten")
            sys.exit()

        # Find the max term frequency in the sentence
        sentence_lengths[sentence] = term_freqs
        max_frequency = 0
        for frequency in term_freqs.values():
             if frequency > max_frequency:
                 max_frequency = frequency
        max_sentence_freqs[sentence] = max_frequency

        # Calculate sentence lengths given its term frequencies according to the nxc weighting scheme
        sum = 0
        for term, frequency in term_freqs.items():
            sum += (.5 + (.5 * frequency / max_frequency)) ** 2
        sentence_lengths[sentence] = math.sqrt(sum)

    with open("inverted_index.json", "w") as file:
        json.dump(inverted_index, file)
    with open("max_sentence_freqs.json", "w") as file:
        json.dump(max_sentence_freqs, file)
    with open("sentence_lengths.json", "w") as file:
        json.dump(sentence_lengths, file)


''' Adds a sentence to the inverted_index '''
def indexSentence(sentence, ID, inverted_index):
    term_freqs = {}

    for token in sentence:
        # Get term frequences in the sentence
        if token in term_freqs:
            term_freqs[token] += 1
        else:
            term_freqs[token] = 1

        # Add or update tokens in inverted_index
        if token in inverted_index:
            if ID in inverted_index[token]:
                inverted_index[token][ID] += 1
            else:
                inverted_index[token][ID] = 1
        else:
            new_ID = {}
            new_ID[ID] = 1
            inverted_index[token] = new_ID

    return inverted_index, term_freqs

if __name__ == "__main__":
    main()

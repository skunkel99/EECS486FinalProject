#!/usr/bin/env python3

#vectorspace.py - EECS 486 Final project group, derived from Assignment 1 (ndcotton)

'''
 Assumptions for proper use:

 preprocess.py accurately tokenizes the CORD-19 dataset into sentences
 sys.argv[1] and sys.argv[2] are the the folders containing CORD-19 documents
 Remaining arguments are the question to be answered

 '''

import sys
import os
import math
import string
import json
import pickle
import json
import zipfile
from preprocess import tokenizeText, removeStopwords, stemWords, getDocs



def main():
    file_list = []
    documents = {}
    inverted_index = {} #map that holds token -> list of docs containing word & doc frequencies
    sentence_lengths = {}
    max_sentence_freqs = {}
    inverted_index_file = sys.argv[1]
    max_sentence_freqs_file = sys.argv[2]
    sentence_lengths_file = sys.argv[3]

    #load all data structures needed to calculate cosine similarity
    with zipfile.ZipFile(inverted_index_file, "r") as z:
        for filename in z.namelist():
            with z.open(filename) as f:
                data = f.read()
                inverted_index = json.loads(data.decode("utf-8"))
    with open(max_sentence_freqs_file) as json_file:
        max_sentence_freqs = json.load(json_file)
    with open(sentence_lengths_file) as json_file:
        sentence_lengths = json.load(json_file)

    #read raw files to return answer
    raw_files = []
    pickled_file_raw = open(sys.argv[4], "rb")
    try:
        while True:
            file = pickle.load(pickled_file_raw)
            raw_files.append(file)
    except EOFError:
        print()

    #either run list of test queries or read query from user input
    if len(sys.argv) == 6:
        ground_truth = open(sys.argv[5], "r")
        queries = json.load(ground_truth)
        output_dict = computeAnswer(queries, inverted_index, sentence_lengths, max_sentence_freqs, raw_files)
        with open("output_answers.json", "w") as file:
            json.dump(output_dict, file)
    else:
        query = input("What would you like to ask about COVID-19? (type exit to end Q&A system) ")
        if (query[-1] == '?'): #remove ? from question to avoid tokenizing issues
            query = query[:-1]
        while (query != "exit"): #continue to read user questions until they enter "exit"
            queries = []
            queries.append(query)
            output_dict = computeAnswer(queries, inverted_index, sentence_lengths, max_sentence_freqs, raw_files)
            print(output_dict[query]) #print answer
            query = input("What would you like to ask about COVID-19? (type exit to end Q&A system) ")
            if (query[-1] == '?'):
                query = query[:-1]
    return 0


''' Computes an answer based on similiarty from the inputted query/queries '''
def computeAnswer(queries, inverted_index, sentence_lengths, max_sentence_freqs, raw_files):
    output_dict = {}
    for query in queries:
        # Find the list of relevant sentences and their similarity scores
        similarities = list(retrieveSentences(query, inverted_index, sentence_lengths, max_sentence_freqs).items())
        similarities = sorted(similarities, reverse=True, key=lambda sentence:sentence[1])

        if (len(similarities) > 0):
            answer_loc = similarities[0][0]
            output_dict[query] = (raw_files[int(answer_loc)]).strip()
        else:
            output_dict[query] = ""
            print("No answer could be found in the database.\n")
    return output_dict

''' Retrieves a dictionary of similarity scores for each sentence for a given query '''
def retrieveSentences(query, inverted_index, sentence_lengths, max_sentence_freqs):
    query_scheme = "tfx"
    if len(query) < 5:
        query_scheme = "nfx"

    # Apply tokenizeText, removeStopwords, stemWords to query
    tokens, returned_sentences = tokenizeText(query, [])
    tokens = removeStopwords(tokens)
    tokens = stemWords(tokens)

    rel_sentences = {}
    query_terms = {}
    max_query_freq = 0
    for token in tokens:
        # Get term frequencies in the query
        if token in query_terms:
            query_terms[token] += 1
        else:
            query_terms[token] = 1

        # Update the max query term frequency if necessary
        if query_terms[token] > max_query_freq:
            max_query_freq = query_terms[token]

        # Determine the set of sentences from the inverted index that include at least one token from the query
        if token in inverted_index:
            for ID in inverted_index[token]:
                if ID not in rel_sentences:
                    rel_sentences[ID] = ID

    # Calculate the similarity between the query and each of the sentences in this the set
    # In the case that no term is found in the query or the document, do not add to the similarity score
    similarities = {}
    for term, frequency in query_terms.items():
        query_weight = 0
        if term in inverted_index:
            if query_scheme == "tfx":
                query_weight = frequency * math.log(len(sentence_lengths) / len(inverted_index[term]))
            else:
                query_weight = (.5 + (.5 * frequency / max_query_freq)) * math.log(len(sentence_lengths) / len(inverted_index[term]))
        else:
            if query_scheme == "tfx":
                query_weight = 0
            else:
                query_weight = .5

        # Calculate similarities using nxc sentence weighting scheme
        for ID in rel_sentences.values():
            if term in inverted_index and ID in inverted_index[term]:
                term_freq = .5 + (.5 * inverted_index[term][ID] / max_sentence_freqs[ID])

                if ID in similarities:
                    similarities[ID] += (term_freq / sentence_lengths[ID]) * query_weight
                else:
                    similarities[ID] = (term_freq  / sentence_lengths[ID])  * query_weight

            elif ID not in similarities:
                similarities[ID] = .5 / sentence_lengths[ID]

    return similarities



if __name__ == "__main__":
    main()

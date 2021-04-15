#!/usr/bin/env python3

#vectorspace.py - EECS 486 Final project group, derived from Assignment 1 (ndcotton)

'''
 Assumptions for proper use: 

 preprocess.py accurately tokenizes the CORD-19 dataset into sentences
 sys.argv[1] is the folder containing CORD-19 documents
 Remaining arguments are the question to be answered

 '''

import sys
import os
import math
import string
from preprocess import tokenizeText, removeStopwords, stemWords, processFolder



def main():
    file_list = []
    documents = {}
    inverted_index = {}
    sentence_lengths = {}
    max_sentence_freqs = {}
    path = sys.argv[1]
    query = str(' '.join(sys.argv[2:]))
    print(query)

    for file in os.listdir(path):
        file_list.append(os.path.join(path, file))
    documents, return_ID = processFolder(file_list, 0, documents)

    # For each sentence, obtain the content and add it to the inverted index
    for doc_ID, sentences in documents.items():
        for sentence_ID, sentence in enumerate(sentences):
            current_ID = str(doc_ID) + "-" + str(sentence_ID)
            inverted_index, term_freqs = indexSentence(sentence, current_ID, inverted_index)

            # Exit the program if multiple identical IDs are found
            if current_ID in sentence_lengths:
                print("sentence_ID already in sentence_lengths and was overwritten")
                sys.exit()
        
            # Find the max term frequency in the sentence
            sentence_lengths[current_ID] = term_freqs
            max_frequency = 0
            for frequency in term_freqs.values():
                 if frequency > max_frequency:
                     max_frequency = frequency
            max_sentence_freqs[current_ID] = max_frequency

            # Calculate sentence lengths given its term frequencies according to the nxc weighting scheme
            sum = 0
            for term, frequency in term_freqs.items():
                sum += (.5 + (.5 * frequency / max_frequency)) ** 2
            sentence_lengths[current_ID] = math.sqrt(sum)

    # Find the list of relevant sentences and their similarity scores
    similarities = list(retrieveSentences(query, inverted_index, sentence_lengths, max_sentence_freqs).items())
    similarities = sorted(similarities, reverse=True, key=lambda sentence:sentence[1])

    # TODO - change to however we want to output the answer
    if (len(similarities) > 0):
        answer_loc = str(similarities[0][0]).split("-")
        print(" ".join(documents[int(answer_loc[0])][int(answer_loc[1])]))
        print("Answer found in document " + str(int(answer_loc[0])) + " in sentence " + str(int(answer_loc[0])) + "\n")
    else:
        print("No answer could be found in the database.\n")



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



''' Retrieves a dictionary of similarity scores for each sentence for a given query '''
def retrieveSentences(query, inverted_index, sentence_lengths, max_sentence_freqs):
    # TODO - determine what a "short query" is and only use nfx in that case
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
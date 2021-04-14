#vectorspace.py - EECS 486 Final project group, derived from Assignment 1 (ndcotton)

'''
 Assumptions for proper use: 

 preprocess.py accurately tokenizes the CORD-19 dataset into sentences
 sys.argv[1] is the question to be answered

 '''

import sys
import os
import math
import string
from preprocess import removeSGML, tokenizeText, removeStopwords, stemWords, getSentences
#TODO - remove imported functions if necessary



def main():
    inverted_index = {}
    sentence_lengths = {}
    max_sentence_freqs = {}
    query = sys.argv[1]
    # TODO - change to correct function call
    sentences = getSentences()

    # For each sentence, obtain the content and add it to the inverted index
    for sentence in sentences:
        inverted_index, sentence_ID, term_freqs = indexSentence(sentence, inverted_index)

        # Exit the program if multiple identical IDs are found
        if sentence_ID in sentence_lengths:
            print("sentence_ID already in sentence_lengths and was overwritten")
            sys.exit()
        
        # Find the max term frequency in the sentence
        sentence_lengths[sentence_ID] = term_freqs
        max_frequency = 0
        for frequency in terms.values():
             if frequency > max_frequency:
                 max_frequency = frequency
        max_sentence_freqs[sentence_ID] = max_frequency

        # Calculate sentence lengths given its term frequencies according to the nxc weighting scheme
        sum = 0
        for term, frequency in terms.items():
            sum += (.5 + (.5 * frequency / max_frequency)) ** 2
        sentence_lengths[ID] = math.sqrt(sum)

    # Find the list of relevant sentences and their similarity scores
    similarities = list(retrieveSentences(query, inverted_index, sentence_lengths, max_sentence_freqs).items())
    similarities = sorted(similarities, reverse=True, key=lambda document:document[1])

    # TODO - change to however we want to output the answer
    print(str(similarity[0]))



''' Adds a sentence to the inverted_index '''
def indexSentence(sentence, inverted_index):
    tokens = []
    term_freqs = {}

    # TODO - remove these lines if tokenization is already taken care of in preprocess.py
    # Apply removeSGML, tokenizeText, removeStopwords, stemWords to sentence
    sentence = removeSGML(sentence)
    tokens = tokenizeText(sentence)
    tokens = removeStopwords(tokens)
    tokens = stemWords(tokens)

    # TODO - read sentence ID correctly
    ID = sentence[0]
    for token in tokens:
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

    # TODO - remove ID if extracted before function call
    return inverted_index, ID, term_freqs



''' Retrieves a dictionary of similarity scores for each sentence for a given query '''
def retrieveSentences(query, inverted_index, sentence_lengths, max_sentence_freqs):
    # TODO - determine what a "short query" is and only use nfx in that case
    query_scheme = "tfx"
    if len(query_scheme) < 5:
        query_scheme = "nfx"

    #TODO - remove these lines if tokenization is already taken care of in preprocess.py
    # Apply removeSGML, tokenizeText, removeStopwords, stemWords to query
    query = removeSGML(query)
    tokens = tokenizeText(query)
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
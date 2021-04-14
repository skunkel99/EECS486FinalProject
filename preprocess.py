#preprocess.py - EECS 486 Final project group, derived from Assignment 1 (ljhale and sharifma)

# Assumptions for proper use: 
#
# All results are safe to transcribe to only lowercase, including proper nouns. 
# SGML tag description info not contained in the tag itself will be tokenized
#
# Date Formats: 
#     A date format like 01.10.2020 iare not supported for date style tokenization
#
# Quote Formats: 
#     Quotation marks of the form << >> are not supported

import os
import re
import sys
from stemmer import PorterStemmer

class tokFlags:
    tokenize_punc = False
    tokenize_word = False
    special_tokenize = False
    tokenize_contr = False
    found_fullstop = False
    tokenize_list = []
    contr_handled = False
    slash_count =  0

class sentenceText: 
    raw = ""
    tokenized = []


# a. Function that removes the SGML tags.
# Name: removeSGML;
# Input: string;
# Output: string
# Assumptions: Descriptive content between tags (eg <AUTHOR> John Smith </AUTHOR>) is not removed
#               - John Smith is not removed, quotes formatted like << content >> are not present
def removeSGML(file):
    found_left = False
    found_both = False
    ret_str = ""
    left_i = 0
    right_i = 0
    last = len(file) - 1
    for i, x in enumerate(file): 
        if found_left and x == '>':
            found_both = True
        elif x == '<': 
            found_left = True
            right_i = i
        if found_both == True or i == len(file) - 1:
            if i == len(file) - 1:
                right_i = i + 1
            ret_str += file[left_i : right_i]
            left_i = i + 1
            found_both = False
            found_left = False
    return ret_str

def is_basic_punc(character):
    if character in ['!','>','<', '?', ';', '~', '\"', '{', "}", '`']:
        ret_bool = True
        return True
    return False


def maybe_date(word, date_flag):
    lower_word = word.casefold()
    month_res = False
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    days = ["1", "2", "3", "4", "5", "6", "7", "8", "9","10", "11", "12","13","14", "15", "16","17","18", "19","20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
    for i,x in enumerate(months):
        month_res = lower_word.find(months[i].casefold())!= -1
        if month_res:
            return True
    if date_flag and not month_res:
        return False
    for i,x in enumerate(days): 
        if lower_word.find(days[i]) != -1:
            return True
    return False


def tokenize_str(word, tokens): 
    if(word):            
        tokens.append(word)
    return tokens

        
def tok_special_punc(character, i, num_flagged, date_detected, possible_token, special_flags, prev_char, next_char, char_2_after, file_len):
    ret_flags = special_flags
    # Contractions list based off of: https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
    contractions = {
        "aren't": "are not",
        "can't": "can not",
        "could've": "could have", 
        "couldn't": "could not", 
        "didn't": "did not", 
        "doesn't": "does not", 
        "don't": "do not", 
        "'em": "them",
        "g'day": "good day", 
        "hadn't": "had not", 
        "hasn't": "has not", 
        "haven't": "have not", 
        "he'd": "he would", 
        "he'll" : "he will", 
        "he's": "he is", 
        "here's": "here is", 
        "how'd": "how did", 
        "how'll": "how will", 
        "how's": "how is", 
        "I'd": "I would", 
        "I'll": "I will", 
        "I'm": "I am", 
        "I've": "I have", 
        "isn't": "is not", 
        "it'd": "it would", 
        "it'll": "it will", 
        "it's": "it is", 
        "let's": "let us", 
        "ma'am": "madam", 
        "may've": "may have", 
        "might've": "might have", 
        "mustn't": "must not", 
        "must've": "must have", 
        "needn't": "need not", 
        "oughtn't": "ought not", 
        "she'd": "she would", 
        "she'll": "she will", 
        "she's": "she is", 
        "shouldn't": "should not", 
        "should've": "should have", 
        "that'll": "that will", 
        "that's": "that is", 
        "that'd": "that would", 
        "there's": "there is", 
        "they'd": "the would", 
        "they'll": "they will", 
        "they're": "they are", 
        "wasn't": "was not", 
        "we'd": "we would", 
        "we'll": "we will", 
        "we're": "we are", 
        "we've": "we have", 
        "weren't": "were not", 
        "what'd": "what did", 
        "what'll": "what will", 
        "what're": "what are", 
        "what's": "what is", 
        "when's": "when is", 
        "which'll": "which will", 
        "who'd": "who would", 
        "who'll": "who will", 
        "who's": "who is", 
        "why'd": "why did", 
        "won't": "will not", 
        "would've": "would have", 
        "wouldn't": "would not", 
        "you'd": "you would" ,
        "you'll": "you will", 
        "you're": "you are"
    }
    if character in ['(', ')', ',', '/'] and not num_flagged:
        if not(character == ','and date_detected):
            ret_flags.tokenize_punc = True
            ret_flags.tokenize_word = True
            ret_flags.special_tokenize = True
            return ret_flags; 
        else: 
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = False
            ret_flags.special_tokenize = False
            return  ret_flags; 
    elif character == ":":
        if not next_char.isdecimal():
            ret_flags.tokenize_punc = True
            ret_flags.tokenize_word = True
            ret_flags.special_tokenize = True
            return ret_flags; 
        else: 
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = False
            ret_flags.special_tokenize = False
            return  ret_flags; 
    elif character == '.':
        ret_flags.found_fullstop = True
        if next_char.isspace() or i + 1 == file_len:
            ret_flags.tokenize_punc = True
            ret_flags.tokenize_word = True
            ret_flags.special_tokenize = True
            return ret_flags
        else:
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = False
            ret_flags.special_tokenize = False
            return ret_flags
    elif character == ','and (date_detected or num_flagged):
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = False
            ret_flags.special_tokenize = False
            return ret_flags; 
    elif character == '\'':
        word_w_next= possible_token + character + next_char
        word_w_next = word_w_next.casefold()
        word_w_two_after = possible_token + character + next_char + char_2_after
        word_w_two_after = word_w_two_after.casefold()
        if word_w_next in contractions:
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = False
            ret_flags.special_tokenize = True
            ret_flags.tokenize_list = contractions[word_w_next].split(' ')
            ret_flags.tokenize_contr = True
            ret_flags.contr_handled = True
            return ret_flags 
        elif word_w_two_after in contractions:
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = False
            ret_flags.special_tokenize = True
            ret_flags.tokenize_list = contractions[word_w_two_after].split(' ')
            ret_flags.tokenize_contr = True
            ret_flags.contr_handled = True
            return ret_flags 
        elif character + next_char + char_2_after == "'em":
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = False
            ret_flags.special_tokenize = True
            ret_flags.tokenize_list.append(possible_token)
            ret_flags.tokenize_list.append("them")
            ret_flags.tokenize_contr = True
            ret_flags.contr_handled = True
            return ret_flags 
        else:
            if next_char == ' ':
                ret_flags.tokenize_punc = True
            else: 
                ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = True
            ret_flags.special_tokenize = True
            return ret_flags 
    elif character == '/':
        if num_flagged and special_flags.slash_count < 2 :
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = False
            ret_flags.special_tokenize = False
            ret_flags.slash_count += 1
            return ret_flags
        else:
            ret_flags.tokenize_punc = True
            ret_flags.tokenize_word = True
            ret_flags.special_tokenize = True
            return ret_flags
    elif character == '-':
        if prev_char.isdecimal:
            ret_flags.tokenize_punc = True
            ret_flags.tokenize_word = True
        elif next_char.isdecimal():
            is_neg = True
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = True
        elif prev_char == ' ' and next_char == ' ': 
            ret_flags.tokenize_punc = True
            ret_flags.tokenize_word = True
        else: 
            ret_flags.tokenize_punc = False
            ret_flags.tokenize_word = False
            ret_flags.special_tokenize = False
            return ret_flags
        ret_flags.special_tokenize = True
        return ret_flags
    ret_flags.special_tokenize = False
    return ret_flags
    

def check_date_format(word, tokens):
    lower_word = word.casefold()
    comp = lower_word.replace(",", "")
    true_phrase = word.split(" ")
    phrase = comp.split(" ")
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    days = ["1", "2", "3", "4", "5", "6", "7", "8", "9","10", "11", "12","13","14", "15", "16","17","18", "19","20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
    days_suf = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th","10th", "11th", "12th","13th","14th", "15th", "16th","17th","18th", "19th","20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th", "28th", "29th", "30th", "31st"]
    found_month = False
    found_date = False
    first_found_i = 0
    has_date = False
    date_start = 0 
    date_end = 0
    for i,x in enumerate(phrase):
        if has_date and i == first_found_i + 2:
            if len(x) <=4 and x.isnumeric():
                date_end = i
            else:
                date_end = i - 1
        elif 0 < months.count(x)  and not found_month: 
            found_month = True
            if not found_date: 
                first_found_i = i
            elif found_date and first_found_i == i-1: 
                has_date = True
                date_start = first_found_i
                date_end = i
        elif 0 < days.count(x) and not found_date: 
            found_date = True
            if not found_month: 
                first_found_i = i
            elif found_month and first_found_i == i-1:
                has_date = True
                date_start = first_found_i
                date_end = i
        elif 0 < days_suf.count(x) and not found_date: 
            found_date = True
            if not found_month: 
                first_found_i = i
            elif found_month and first_found_i != i:
                has_date = True
                date_start = first_found_i
                date_end = i
    date = ""
    for i, x in enumerate(true_phrase): 
        if i < date_start or date_end < i: 
            res = tokenize_str(x, tokens)
        elif i !=date_end: 
            date = date + x + " "
        else: 
            date += x
            res = tokenize_str(date, tokens)
    return res

    
# b. Function that tokenizes the text.
# Name: tokenizeText; input: string; output: list (of tokens)
def tokenizeText(file, sentencesFound):
    entry_start = 0
    tokens = []
    possible_date = False
    found_num = False
    space_count = 0
    prev_char = ""
    file_len = len(file)
    special_flags = tokFlags()
    sentence_start_in_tokens = 0
    sentence_start_in_string = 0
    for i,x in enumerate(file):
        next_char = ""
        char_2_after = ""
        if( i + 1 < len(file)):
            next_char = file[i+1]
        if(i + 2 < len(file)):
            char_2_after = file[i+2]
        if x.isspace():
            did_reserve = possible_date
            possible_date =  maybe_date(file[entry_start: i], possible_date)
            if possible_date:
                if space_count < 2: 
                    space_count += 1
                else: 
                    tokens = check_date_format(file[entry_start:i], tokens)
                    found_num = False
                    possible_date = False
                    entry_start = i + 1
                    space_count = 0
            elif not possible_date and did_reserve:
                for j, y in enumerate(file[entry_start:i].split(" ")): 
                    tokens = tokenize_str(y, tokens)
                    entry_start = i + 1
                    found_num = False
                    possible_date = False
            elif not possible_date and not special_flags.contr_handled: 
                tokens = tokenize_str(file[entry_start:i], tokens)
                entry_start = i + 1
                found_num = False
                possible_date = False
            if special_flags.contr_handled:
                entry_start = i + 1
                special_flags.contr_handled = False
        elif x.isdecimal():
            found_num = True
        elif is_basic_punc(x):
            if(not possible_date): 
                tokens = tokenize_str(file[entry_start:i], tokens)
                found_num = False
            else: 
                tokens = check_date_format(file[entry_start:i], tokens)
                space_count = 0
                found_num = False
                possible_date = False            
            tokens = tokenize_str(x, tokens)
            entry_start = i + 1
            found_num = False
            possible_date = False
        special_flags = tok_special_punc(x, i, found_num, possible_date, file[entry_start:i], special_flags, prev_char, next_char, char_2_after, file_len)
        if (special_flags.special_tokenize):
            if(special_flags.tokenize_word):
                if(not possible_date): 
                    tokens = tokenize_str(file[entry_start:i], tokens)
                else: 
                    tokens = check_date_format(file[entry_start:i], tokens)
                    space_count = 0
                    found_num = False
                    possible_date = False
                if(special_flags.found_fullstop and special_flags.tokenize_punc):
                    sentenceContent = sentenceText()
                    sentenceContent.tokenized = tokens[sentence_start_in_tokens:]
                    sentenceContent.raw = file[entry_start:i]
                    sentencesFound.append(sentenceContent)
                entry_start = i + 1
            if(special_flags.tokenize_punc):
                tokens = tokenize_str(x, tokens)
                entry_start = i + 1
                if(special_flags.found_fullstop):
                    sentence_start_in_tokens = len(tokens)
                    sentence_start_in_string = entry_start
                    special_flags.found_fullstop = False
            if(special_flags.tokenize_contr):
                for y in special_flags.tokenize_list:
                    tokens = tokenize_str(y,tokens)
                entry_start = i + 1
                special_flags.tokenize_list.clear()
    if not special_flags.contr_handled:
        tokens = tokenize_str(file[entry_start:len(file)], tokens)
    if sentence_start_in_string != entry_start:
        sentenceContent = sentenceText()
        sentenceContent.tokenized = tokens[sentence_start_in_tokens:]
        sentenceContent.raw = file[entry_start:i]
        sentencesFound.append(sentenceContent)
    return tokens, sentencesFound           


# c. Function that removes the stopwords.
# Name: removeStopwords; input: list (of tokens); output: list (of tokens)
def removeStopwords(tokens):
    stopwords = os.path.abspath("stopwords")
    stopword_file = open(stopwords, 'r')
    stopword_list = stopword_file.read()  
    stopword_file.close()  
    no_stop = tokens
    to_pop = []
    for i,x in enumerate(no_stop): 
        if x.casefold() in stopword_list: 
            to_pop.append(i)
    to_pop.reverse()
    for x in to_pop:
        no_stop.pop(x)
    return no_stop


# d. Function that stems the words.
# Name: stemWords;
# Input: list (of tokens);
# Output: list (of stemmed tokens)
def stemWords(tokens):
    stemmed = []
    stem = PorterStemmer()
    for x in tokens: 
        y = stem.stem(x,0, len(x) -1)
        stemmed.append(y)
    return stemmed


def processFolder(file_list, tokens, passStartId, documents):
    idProcessed = passStartId
    for i,x in enumerate(file_list):
        file = open(x, "r")
        current_file = removeSGML(file.read())
        #divide into sentences
        documents[idProcessed] = []
        curr_file_tokens, documents[idProcessed] = tokenizeText(current_file, documents[idProcessed])
        for j, y in enumerate(documents[idProcessed]):
            documents[idProcessed][j].tokenized = removeStopwords(y.tokenized)
            documents[idProcessed][j].tokenized = stemWords(y.tokenized)
            tokens.extend(documents[idProcessed][j].tokenized)
        idProcessed += i
        file.close()
    return tokens, idProcessed

# The main program should perform the following sequence of steps:
# i. open the folder containing the data collection, provided as the first argument on the command
# line (e.g., cranfieldDocs/), and read one file at a time from this folder.
# ii. for each file, apply, in order: removeSGML, tokenizeText, removeStopwords, stemWords
# iii. in addition, write code to determine (this is after step ii above):
# - the total number of words in the collection (numbers should be counted as words)
# - vocabulary size (i.e., number of unique terms)
# - most frequent 50 words in the collection, along with their frequencies (list in reverse order
# of their frequency, i.e., from most to least frequent)

def main():
    cwd = os.getcwd
    arg1 = sys.argv[1]
    # arg2 = sys.argv[2]
    collection_1 = os.path.abspath(arg1)
    # collection_2 = os.path.abspath(arg2)
    file_list_1 = os.scandir(collection_1)
    # file_list_2 = os.scandir(collection_2)
    tokens =[]
    nextPassStartId = 0
    documents  = {}

    tokens, nextPassStartId = processFolder(file_list_1, tokens, nextPassStartId, documents)
    # tokens, nextPassStartId = processFolder(file_list_1, tokens, nextPassStartId, documents)
    vocab = {}
    word_count = 0
    for x in tokens: 
        if x not in ['!','>','<', '?', ';', '~', '\"', '.', ',', '-', '_', '\'', ':', '/', '-', '_', '=', '`', '%', '^', '&', '(', ')', '{', '}', '$', '*', '[', ']', '@', '#']:
            word_count += 1
            if x not in vocab:
                vocab[x] = 1
            else: 
                vocab.update({x: vocab[x] + 1})
    
# TODO: Address formatting output with team
#       Current format is the format from Assignment 1, determine whether this needs to be modified in any way. 
    output_str = ""
    answers_str = "".join(("Words: ", str(word_count), '\n',"Vocabulary: ", str(len(vocab)),'\n'))
    output_str = "".join((answers_str, "Top 50 words\n"))
    res_val = sorted(vocab.values())
    res_key = sorted(vocab, key = vocab.get)
    res_val.reverse()
    res_key.reverse()
    for i,x in enumerate(res_val): 
        if not (i < 50): 
            break
        else:
            output_str = "".join((output_str, res_key[i]," ", str(x), '\n'))
        
    output_file = open("preprocess_new_thing.output", 'w')
    output_file.write(output_str)
    output_file.close()


if __name__ == "__main__":
    main()
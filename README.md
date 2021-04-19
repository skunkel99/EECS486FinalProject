## COVID-19 Question & Answer System
For our final project, we will be implementing a COVID-19 question and answer system. This program will be effective in answering many different types of queries. The overall goal is to create a single program that utilizes a dataset that can quickly and efficiently search through related materials and present the most relevant answer in an easy-to-read format. 

## Motivation
In a bid to prevent further loss of life and negative economic impact, scientists have been working around the clock to learn more about COVID-19 and present relevant information to the public. Since COVID is a relatively new threat, the ever-changing information regarding COVID-19 can be overwhelming and difficult to follow, especially alongside the spread of misinformation through social media and other unreliable media outlets. Our system hopes to provide a quick and easy way for users to get their questions about the quickly evolving COVID-19 pandemic answered. 

## How to use?
First, the dataset needs to be tokenized in order to create our inverted index. To do this, use the following command once you have downloaded the CORD-19 dataset:

python3 preprocess.py 2021-04-13/document_parses/pmc_json 2021-04-13/document_parses/pdf_json

Alternatively, the tokenized version of 25% of the CORD-19 dataset is already processed and stored in processed_documents_tokenized.txt.zip, and the corresponding raw sentences  are stored in processed_documents_raw.txt.zip. These files are passed into invertedindex.py, where the tokens will be added to our inverted index data structure. The following command can be used to do this:

python3 invertedindex.py processed_documents_tokenized.txt processed_documents_raw.txt

However, because the dataset is so large, we have included a file that contains all of the processed data structures that will be needed to compute the cosine similarities needed for our system. These are stored in inverted_index.json, sentence_lengths.json, and max_sentence_freqs.json. 
In order to run our system and output queries, use the following command:

python3 vectorspace.py inverted_index.json max_sentence_freqs.json sentence_lengths.json ground_truth.json processed_documents_raw.txt

ground_truth.json contains the compiled ground truth question and answers that are used for the evaluation of our system. 

## Credits
This project was created with the help of the entire EECS 486 staff at the University of Michigan. Our system utilized the CORD-19 database.


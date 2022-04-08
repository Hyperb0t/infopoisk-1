import math
import os

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer


def filter_tokens(tokens_list):
    tokens_list = (map(lambda x: x.lower(), tokens_list))
    stop_words = set(stopwords.words('english'))
    tokens_list = [w for w in tokens_list if not w in stop_words]
    stop_char_list = '0123456789./%*+=:!&?$()'
    tokens_list = [ele for ele in tokens_list if all(ch not in ele for ch in stop_char_list)]
    tokens_list = [w for w in tokens_list if not (w.startswith('-') or w.endswith('-'))]
    return tokens_list

def tf(word, repeated_word_list):
    return repeated_word_list.count(word) / len(repeated_word_list)


def idf(word_occur_doc_count, docs_count):
    return abs(math.log(docs_count / word_occur_doc_count))

if __name__ == '__main__':
    lemmatizer = WordNetLemmatizer()
    doc_count = len(os.listdir('pages'))
    token_occur_doc_count = {}
    lemma_occur_doc_count = {}

    for file in os.listdir('pages'):
        with open('pages/' + file, 'r') as f:
            text = f.read()
            repeated_tokens = word_tokenize(text)
            file_tokens = set(filter_tokens(repeated_tokens))
            for token in file_tokens:
                if token not in token_occur_doc_count:
                    token_occur_doc_count[token] = 1
                else:
                    token_occur_doc_count[token] += 1
            file_lemmas = map(lambda x: lemmatizer.lemmatize(x), file_tokens)
            for lemma in file_lemmas:
                if lemma not in lemma_occur_doc_count:
                    lemma_occur_doc_count[lemma] = 1
                else:
                    lemma_occur_doc_count[lemma] += 1

    if not os.path.exists('tf-idf-tokens'):
        os.mkdir("tf-idf-tokens")
    if not os.path.exists('tf-idf-lemmas'):
        os.mkdir("tf-idf-lemmas")

    for file in os.listdir('pages'):
        with open('pages/' + file, 'r') as f:
            text = f.read()
            repeated_tokens = filter_tokens(word_tokenize(text))
            file_tokens = set(repeated_tokens)
            repeated_lemmas = list(map(lambda x: lemmatizer.lemmatize(x), repeated_tokens))
            file_lemmas = set(repeated_lemmas)
            with open('tf-idf-tokens/' + file, 'w') as f:
                for token in file_tokens:
                    token_tf = tf(token, repeated_tokens)
                    token_idf = idf(token_occur_doc_count[token], doc_count)
                    f.write('{} {} {}\n'.format(token, token_tf, token_tf * token_idf))
            with open('tf-idf-lemmas/' + file, 'w') as f:
                for lemma in file_lemmas:
                    lemma_tf = tf(lemma, repeated_lemmas)
                    lemma_idf = idf(lemma_occur_doc_count[lemma], doc_count)
                    f.write('{} {} {}\n'.format(lemma, lemma_tf, lemma_tf * lemma_idf))

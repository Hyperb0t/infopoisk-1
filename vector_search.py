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


def get_lemma_occur_doc_count():
    lemmatizer = WordNetLemmatizer()
    lemma_occur_doc_count = {}
    for file in os.listdir('pages'):
        with open('pages/' + file, 'r') as f:
            text = f.read()
            repeated_tokens = word_tokenize(text)
            file_tokens = set(filter_tokens(repeated_tokens))
            file_lemmas = map(lambda x: lemmatizer.lemmatize(x), file_tokens)
            for lemma in file_lemmas:
                if lemma not in lemma_occur_doc_count:
                    lemma_occur_doc_count[lemma] = 1
                else:
                    lemma_occur_doc_count[lemma] += 1
    return lemma_occur_doc_count


def get_index(lemma_occur_doc_count):
    lemmatizer = WordNetLemmatizer()
    doc_count = len(os.listdir('pages'))
    index = {}

    for file in os.listdir('pages'):
        with open('pages/' + file, 'r') as f:
            index[file] = {}
            text = f.read()
            repeated_tokens = filter_tokens(word_tokenize(text))
            repeated_lemmas = list(map(lambda x: lemmatizer.lemmatize(x), repeated_tokens))
            file_lemmas = set(repeated_lemmas)
            for lemma in file_lemmas:
                lemma_tf = tf(lemma, repeated_lemmas)
                lemma_idf = idf(lemma_occur_doc_count[lemma], doc_count)
                index[file][lemma] = lemma_tf * lemma_idf
    return index


def get_query_tfidf(query, lemma_occur_doc_count):
    result = {}
    lemmatizer = WordNetLemmatizer()
    doc_count = len(os.listdir('pages'))
    repeated_tokens = filter_tokens(word_tokenize(query))
    repeated_lemmas = list(map(lambda x: lemmatizer.lemmatize(x), repeated_tokens))
    query_lemmas = set(repeated_lemmas)
    for lemma in query_lemmas:
        lemma_occurencies = 1 if lemma not in lemma_occur_doc_count else lemma_occur_doc_count[lemma]
        lemma_tf = tf(lemma, repeated_lemmas)
        lemma_idf = idf(lemma_occurencies, doc_count)
        result[lemma] = lemma_tf * lemma_idf
    return result


def get_ranked_search_result(index, query, query_tfidf):
    lemmatizer = WordNetLemmatizer()
    repeated_tokens = filter_tokens(word_tokenize(query))
    repeated_lemmas = list(map(lambda x: lemmatizer.lemmatize(x), repeated_tokens))
    query_lemmas = set(repeated_lemmas)
    result = {}
    for doc in index.keys():
        cos_sim = 0
        query_len_square = 0
        for lemma in query_lemmas:
            if lemma in index[doc].keys():
                cos_sim += index[doc][lemma] * query_tfidf[lemma]
                query_len_square += query_tfidf[lemma] ** 2
        if cos_sim > 0:
            result[doc] = cos_sim / (math.sqrt(query_len_square) * math.sqrt(sum(value ** 2 for value in index[doc].values())))
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    return result


if __name__ == '__main__':
    lemma_occur_doc_count = get_lemma_occur_doc_count()
    index = get_index(lemma_occur_doc_count)
    query = input("enter query\n")
    query_tfidf = get_query_tfidf(query, lemma_occur_doc_count)
    print(get_ranked_search_result(index, query, query_tfidf))
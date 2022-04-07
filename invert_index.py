import os

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer


def filter_tokens(tokens_list):
    tokens_list = set((map(lambda x: x.lower(), tokens_list)))
    stop_words = set(stopwords.words('english'))
    tokens_list = [w for w in tokens_list if not w in stop_words]
    stop_char_list = '0123456789./%*+=:!&?$()'
    tokens_list = [ele for ele in tokens_list if all(ch not in ele for ch in stop_char_list)]
    tokens_list = [w for w in tokens_list if not (w.startswith('-') or w.endswith('-'))]
    return tokens_list


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def union(lst1, lst2):
    return set(lst1 + lst2)


if __name__ == '__main__':
    tokens = set()
    inv_index = {}
    lemmatizer = WordNetLemmatizer()
    print('creating inverted index')
    for file in os.listdir('pages'):
        with open('pages/' + file, 'r') as f:
            text = f.read()
            file_tokens = set(word_tokenize(text))
            filtered_tokens = filter_tokens(file_tokens)
            tokens.update(filtered_tokens)
            for token in filtered_tokens:
                lemma = lemmatizer.lemmatize(token)
                if lemma not in inv_index:
                    inv_index[lemma] = list()
                    inv_index[lemma].append(str(file))
                else:
                    if str(file) not in inv_index[lemma]:
                        inv_index[lemma].append(str(file))
    with open('inverted_index.txt', 'w') as f:
        for key, value in inv_index.items():
            f.write('{}: {}\n'.format(key, value))
    query = input("enter search query\n")
    print('searching for ' + query)
    splitted_query = query.split()
    result = inv_index[splitted_query[0]]
    i = 2
    while i < len(splitted_query):
        if (splitted_query[i - 1] == '&'):
            result = intersection(result, inv_index[splitted_query[i]])
        elif (splitted_query[i - 1] == '|'):
            result = union(result, inv_index[splitted_query[i]])
        else:
            print('unknown operator: {}', splitted_query[i - 1])
        i += 2
    print(result)

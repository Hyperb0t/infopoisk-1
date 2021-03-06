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

if __name__ == '__main__':
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    tokens = set()
    for file in os.listdir('pages'):
        with open('pages/' + file, 'r') as f:
            text = f.read()
            file_tokens = set(word_tokenize(text))
            # print(file_tokens)
            tokens.update(file_tokens)
    #
    # tokens = set((map(lambda x: x.lower(), tokens)))
    # stop_words = set(stopwords.words('english'))
    # tokens = [w for w in tokens if not w in stop_words]
    # stop_char_list = '0123456789./%'
    # tokens = [ele for ele in tokens if all(ch not in ele for ch in stop_char_list)]
    # tokens = [w for w in tokens if not (w.startswith('-') or w.endswith('-'))]

    tokens = filter_tokens(tokens)

    with open('tokens.txt', 'w') as f:
        for t in tokens:
            f.write("%s\n" % t)
    lemmas_and_tokens = dict()
    lemmatizer = WordNetLemmatizer()
    for t in tokens:
        l = lemmatizer.lemmatize(t)
        if l in lemmas_and_tokens:
            lemmas_and_tokens[l].append(t)
        else:
            lemmas_and_tokens[l] = list()
            lemmas_and_tokens[l].append(t)
    with open('lemmas.txt', 'w') as f:
        for key, value in lemmas_and_tokens.items():
            f.write('{}: {}\n'.format(key, value))

from flask import Flask, render_template, redirect, request, url_for, send_from_directory
from nltk import word_tokenize

import vector_search

template_dir = 'templates'
print('creating indexes')
lemma_occur_doc_count = vector_search.get_lemma_occur_doc_count()
index = vector_search.get_index(lemma_occur_doc_count)
app = Flask(__name__, template_folder=template_dir, static_url_path="/static", static_folder='static')


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def get_text(filename, query):
    result = ""
    with open('pages/' + filename, 'r') as f:
        words = word_tokenize(f.read())
        words = vector_search.filter_tokens(words)
        query_words = word_tokenize(query)
        i = 0
        while i < 40 and i < len(words):
            word = words[i]
            if word in query_words:
                word = '<strong>{}</strong>'.format(word)
            result += word + ' '
            i += 1
    return result


def get_template_results(result, query):
    r = list()
    for key, value in result.items():
        r.append({'filename': key, 'cos_sim': value, 'text': get_text(key, query)})
    return r

@app.route('/')
def start_page():
    return render_template('start_page.html')


@app.route('/search')
def query_page():
    query = request.args.get('q')
    query_tfidf = vector_search.get_query_tfidf(query, lemma_occur_doc_count)
    result = vector_search.get_ranked_search_result(index, query, query_tfidf)
    print(query_tfidf)
    print(result)
    return render_template('query_page.html', query=query, results=get_template_results(result, query), query_tfidf=query_tfidf)


@app.route('/open/<filename>')
def open_page(filename):
    return send_from_directory('pages', filename)
    # return redirect(redirect_url())


if __name__ == '__main__':
    app.run(debug=True)

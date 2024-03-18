from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import trafilatura
import requests
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googlesearch import search

app = Flask(__name__)
app.secret_key = 'your secret key'

genai.configure(api_key='AIzaSyBVLp9qzlaM3791iAVhku_RyF9gZwjQENA')
model = genai.GenerativeModel('gemini-pro')

def news_sources(query, limit=5):
    results = []
    for result in search(query, num_results=limit, sleep_interval=2):
        if requests.get(result).ok:
            results.append(result)
    return results

def extract_text_from_url(url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    return text if text else ""  # Handle empty text extraction

def textrank_summarize(text, num_sentences=1):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return ' '.join([str(sentence) for sentence in summary])

def extract_keywords(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    return set([word for word in filtered_words if len(word) > 2])

def llm_response(corpus, statement):
    prompt = f'''
        Given a set of news articles (Corpus) and a statement to analyze (Statement), please assess the following:

        * Bias: Identify any potential biases within the statement. 
        * Factuality: Determine if the statement is likely true, false, or misleading. Provide evidence to support your claim (e.g., citing articles from the corpus).
        * Summary: Generate a concise summary of the key points from the verified information in the corpus, attributing sources where appropriate (e.g., "According to [Article 1]...").

        **Note:** Focus only on information that can be corroborated by multiple sources within the corpus. 
        corpus: {corpus} AND statement: {statement}
        '''
    response = model.generate_content(prompt)
    return jsonify(response.text)

@app.route('/insights', methods=['POST'])
def insights():
    statement = request.form.get('statement')
    session['status'] = 'Getting news sources...'
    urls = news_sources(statement)
    session['status'] = 'Successfully got news sources'
    corpus = '\n\n'.join(extract_text_from_url(url) for url in urls)
    session['status'] = 'Getting LLM response...'
    return llm_response(corpus, statement)

@app.route('/status')
def status():
    return jsonify(status=session.get('status', ''))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)

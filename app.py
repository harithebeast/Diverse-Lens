from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai  # Assuming GenAI library is installed
import trafilatura
import requests
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googlesearch import search
from flask_cors import CORS

# Flask app initialization
app = Flask(__name__)
CORS(app)
app.secret_key = 'your secret key'

# Configure GenAI (replace with your API key)
genai.configure(api_key='YOUR_GENAI_API_KEY')
model = genai.GenerativeModel('gemini-pro')


def news_sources(query, limit=5):
  """Fetches news article URLs related to a query using googlesearch."""
  results = []
  for result in search(query, num_results=limit, sleep_interval=2):
    if requests.get(result).ok:
      results.append(result)
  return results


def extract_text_from_url(url):
  """Extracts text content from a URL using trafilatura."""
  downloaded = trafilatura.fetch_url(url)
  text = trafilatura.extract(downloaded)
  return text if text else ""  # Handle empty text extraction


def textrank_summarize(text, num_sentences=1):
  """Summarizes text using TextRank algorithm from sumy library."""
  parser = PlaintextParser.from_string(text, Tokenizer("english"))
  summarizer = TextRankSummarizer()
  summary = summarizer(parser.document, num_sentences)
  return ' '.join([str(sentence) for sentence in summary])


def extract_keywords(text):
  """Extracts keywords by removing stop words and filtering word length."""
  words = word_tokenize(text.lower())
  stop_words = set(stopwords.words('english'))
  filtered_words = [word for word in words if word not in stop_words]
  return set([word for word in filtered_words if len(word) > 2])


def llm_response(corpus, statement):
  """Uses GenAI to analyze a statement based on the provided corpus."""
  prompt = f'''
        Given a set of news articles (Corpus) and a statement to analyze (Statement), please assess the following:

        * Bias: Identify any potential biases within the statement.
        * Factuality: Determine if the statement is likely true, false, or misleading. Provide evidence to support your claim (e.g., citing articles from the corpus).
        * Summary: Generate a concise summary of the key points from the verified information in the corpus, attributing sources where appropriate (e.g., "According to [Article 1]...").

        Note:** Focus only on information that can be corroborated by multiple sources within the corpus.
        corpus: {corpus} AND statement: {statement}
  '''
  response = model.generate_content(prompt)
  return jsonify(response.text)


@app.route('/insights', methods=['POST'])
def insights():
  """API endpoint to process user statement and return analysis using GenAI."""
  statement = request.json.get('statement')
  session['status'] = 'Getting news sources...'
  try:
    urls = news_sources(statement)
    corpus = '\n\n'.join(extract_text_from_url(url) for url in urls)
    response = llm_response(corpus, statement)
  except Exception as e:
    return jsonify({'error': str(e)}), 500  # Internal Server Error
  return response


@app.route('/status')
def status():
  """API endpoint to retrieve the current processing status."""
  return jsonify(status=session.get('status', ''))


@app.route('/')
def index():
  """Renders the main HTML template for user input."""
  return render_template('index.html')


if __name__ == '_main_':
  app.run(debug=False)
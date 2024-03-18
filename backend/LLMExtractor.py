import trafilatura
import textwrap
import requests
from googlesearch import search
from urllib.parse import urlparse 
from IPython.display import Markdown
import google.generativeai as genai
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

genai.configure(api_key='AIzaSyCWBI36ib_X-6RYSBoq9SHWxuKlUXPfRHc')
model = genai.GenerativeModel('gemini-pro')

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

def news_sources(query, limit=2):
    results = []
    for result in search(query, num_results=limit, sleep_interval=2):
        r = requests.get(result)
        if r.ok:
            results.append(result)
    return results

def extract_text_from_url(url):
   if not is_url(url):
      return
   downloaded = trafilatura.fetch_url(url)
   text = trafilatura.extract(downloaded)
   if text:
      return text
   
def textrank_summarize(text, num_sentences=1):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return ' '.join([str(sentence) for sentence in summary])

def extract_keywords(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    tagged_words = pos_tag(filtered_words)
    keywords = [word for word, pos in tagged_words if pos.startswith('NN') or pos.startswith('JJ') and len(word) > 2]
    return set(keywords)
   
def llm_response(corpus, statement):
    prompt =f'''
     Given a set of news articles (Corpus) and a statement to analyze (Statement), please assess the following:

    * Bias: Identify any potential biases within the statement. 
    * Factuality: Determine if the statement is likely true, false, or misleading. Provide evidence to support your claim (e.g., citing articles from the corpus).
    * Summary: Generate a concise summary of the key points from the verified information in the corpus, attributing sources where appropriate (e.g., "According to [Article 1]...").

    **Note:** Focus only on information that can be corroborated by multiple sources within the corpus. 
    corpus: {corpus} AND statement: {statement}
    '''
    response = model.generate_content(prompt)
    # print(response.prompt_feedback)
    return to_markdown(response.text) 

def insights(statement):
    urls = news_sources(statement)
    corpus = ''
    for url in urls:
        text = extract_text_from_url(url)
        if text:
            corpus += f'source:{url}, Text:{text}\n\n'
    return llm_response(corpus, statement)

# url = input("Enter the URL: ")
# text = extract_text_from_url(url)
# statement = textrank_summarize(text)
insights('Tata ipl 2024 is cancelled')
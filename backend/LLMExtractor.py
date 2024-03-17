from urllib.parse import urlparse
import trafilatura
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from googlesearch import search
import textwrap
from IPython.display import Markdown
import google.generativeai as genai
from gnews import GNews


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def news_query(query, limit=5):
    results = []
    google_news = GNews()
    news = google_news.get_news(query)
    for i in range(limit):
        results.append(news[i]['url'])
    return results

def extract_heading_from_url(url):
    r = requests.get(url, headers={'User-Agent': UserAgent().random}
)
    soup = BeautifulSoup(r.text, 'html.parser')
    heading = [heading.text for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])][0]
    return heading if heading else 'No Heading'

def extract_text_from_url(url):
   downloaded = trafilatura.fetch_url(url)
   return trafilatura.extract(downloaded)

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

def predict(my_news):
    query = my_news

    if is_url(my_news):
       my_news = extract_text_from_url(my_news)  
       query = extract_heading_from_url(my_news) 
    
    corpus_of_links = ''
    for url in news_query(query):
        corpus_of_links += extract_text_from_url(url) + '\n'

    genai.configure(api_key='AIzaSyAx90CfmOJc3qUC_Y5f7OmQGhrcbYlYjDQ')
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
       f'''Analyze the provided links: {corpus_of_links}.can you answer whether the following statement with explanation is baised/unbaised or truth/fake: {my_news}'''
    )
    return to_markdown(response.text) 

if __name__ == "__main__":
   info = input("Enter the input: ")
   predict(info)
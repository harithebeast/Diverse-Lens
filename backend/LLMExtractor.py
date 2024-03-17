from urllib.parse import urlparse
import trafilatura
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from googlesearch import search
import textwrap
from IPython.display import Markdown
import google.generativeai as genai

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def news_query(query, limit=5):
    results = []
    for i in search(query, num_results=limit, sleep_interval=2):
        results.append(i)
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

def get_article_info(url):
   return {'heading': extract_heading_from_url(url), 'text': extract_text_from_url(url)}

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

def predict(info):
    #check if input is url
    results = {}
    if is_url(info):
       temp = get_article_info(info)
       results.update(temp)
    
    text = ''
    for i in news_query(temp['heading']):
        text += i + '\n'

    # join results in format haeding, text in str
    print(text)

    genai.configure(api_key='AIzaSyAx90CfmOJc3qUC_Y5f7OmQGhrcbYlYjDQ')
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"can you check this article {temp['text']} for genre, fake news and bias with source using this text info: {text} and return the results in format Genre, fake news and bias")
    return to_markdown(response.text) 

if __name__ == "__main__":
   info = input("Enter the input: ")
   predict(info)
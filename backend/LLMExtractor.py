from urllib.parse import urlparse
import trafilatura
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from googlesearch import search
import textwrap
from IPython.display import Markdown
import google.generativeai as genai

ua = UserAgent()

headers = {
    'User-Agent': ua.random
}

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key='AIzaSyAx90CfmOJc3qUC_Y5f7OmQGhrcbYlYjDQ')
model = genai.GenerativeModel('gemini-pro')

'''def check(url):
    response = model.generate_content(f"read this article {url} and check on web and only return fake/original and bias/unbiased: ")
    return to_markdown(response.text)'''

def news_query(query, limit=5):
    search_results = search(query, num_results=limit)
    return search_results


def extract_heading_from_url(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return [heading.text for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])][0]

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

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(keywords)

def predict(input):
    #check if input is url
    if is_url(input):
       input = get_article_info(input)
    
    for i in news_query(input['heading']):
       print(i)

    
       

if __name__ == "__main__":
   input = input("Enter the input: ")
   predict(input)
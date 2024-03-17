import trafilatura
import textwrap
from googlesearch import search
from urllib.parse import urlparse 
from IPython.display import Markdown
import google.generativeai as genai

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

def news_sources(query, limit=5):
    results = []
    for j in search(query, num_results=limit, sleep_interval=2):
        results.append(j)
    return results

def extract_text_from_url(url):
   if not is_url(url):
      return
   downloaded = trafilatura.fetch_url(url)
   text = trafilatura.extract(downloaded)
   if text:
      return text
   
def llm_response(corpus, statement):
    genai.configure(api_key='AIzaSyAlRtzd89OYpN0VXhdZ8R3w3oWGcIUAFs0')
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
       f'''Analyze the provided text in format url, text from url: {corpus}. from the above text can you answer whether the following statement is baised/unbaised and truth/fake and genre like politics/sports/entertainment/business/education or any field related. Explain your claims with url from above: {statement}'''
    )
    return to_markdown(response.text) 

def main(statement):
    urls = news_sources(statement)
    corpus = ''
    for url in urls:
        text = extract_text_from_url(url)
        if text:
            corpus += f'{url}: {text}\n\n'

    return llm_response(corpus, statement)

main(input("Input: "))

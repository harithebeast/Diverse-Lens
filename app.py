from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key='AIzaSyCWBI36ib_X-6RYSBoq9SHWxuKlUXPfRHc')
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return '''
    <html>
        <body>
            <form action="/call_llm" method="post">
                <label for="corpus">Corpus:</label><br>
                <textarea name="corpus" rows="10" cols="30"></textarea><br>
                <label for="statement">Statement:</label><br>
                <textarea name="statement" rows="10" cols="30"></textarea><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    '''

def news_sources(query, limit=2):
    results = []
    for result in search(query, num_results=limit, sleep_interval=2):
        if requests.get(result).ok:
            results.append(result)
    return results

def extract_text_from_url(url):
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

def insights(statement):
    urls = news_sources(statement)
    corpus = ''
    for url in urls:
        text = extract_text_from_url(url)
        if text:
            # corpus += f'source:{url}, Text:{text}\n\n'
           corpus += text +'\n\n'
    return llm_response(corpus, statement)
   
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
    return josnify(response.text)

@app.route('/call_llm', methods=['POST'])
def llm_response():
    corpus = request.form.get('corpus')
    statement = request.form.get('statement')
    prompt =f'''
     Given a set of news articles (Corpus) and a statement to analyze (Statement), please assess the following:

    * Bias: Identify any potential biases within the statement. 
    * Factuality: Determine if the statement is likely true, false, or misleading. Provide evidence to support your claim (e.g., citing articles from the corpus).
    * Summary: Generate a concise summary of the key points from the verified information in the corpus, attributing sources where appropriate (e.g., "According to [Article 1]...").

    **Note:** Focus only on information that can be corroborated by multiple sources within the corpus. 
    corpus: {corpus} AND statement: {statement}
    '''

    content = model.generate_content(prompt)
    return jsonify(content)

if __name__ == '__main__':
    app.run(debug=True)
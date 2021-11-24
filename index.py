import requests
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from text2ipa import get_IPA
from gtts import gTTS
import os

from functions.extract import scrapingDataTraductor, getSentencesTraductor

PEOPLE_FOLDER = os.path.join('static', 'people_photo')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def index():
    word =  request.args.get('word')
    if word is not None:
        word = word.lower()
    else:
        return render_template('pages/index.html')
    phrases_en, examples, language, count_phrases, translations = scrapingDataTraductor(word)
    urlSentences = f"https://examples1.ingles.com/explore?lang={language}&q={word}&numExplorationSentences=100"
    count_examples = getSentencesTraductor(urlSentences)
    return render_template('pages/index.html',
    title=word,
    translations=translations,
    count_phrases=count_phrases,
    language=language,
    count_examples=count_examples,
    examples=examples,
    phrases_en=phrases_en)

@app.route('/phrases')
def vocabulary():
    word =  request.args.get('word')
    if(word):
        word = word.lower()
    data = requests.get(f"https://www.ingles.com/traductor/{word}")
    soup = BeautifulSoup(data.text, 'html.parser')
    phrases_en = soup.find_all('td', {'class': 'AAmLzBFI', 'lang': 'en'})
    phrases_es = soup.find_all('td', {'class': 'AAmLzBFI', 'lang': 'es'})
    phrases = []
    for i, val in enumerate(phrases_en):
        phrases.append({"spanish": phrases_es[i].text, "english": phrases_en[i].text})
    return render_template('pages/phrases.html', phrases=phrases, title=word)
@app.route('/examples')
def examples():
    language = request.args.get('lang')
    word = request.args.get('word').lower()
    urlSentences = f"https://examples1.ingles.com/explore?lang={language}&q={word}&numExplorationSentences=100"
    search = requests.get(urlSentences)
    data = search.json()
    if(language == 'es'):
        sentences = []
        for sentence in data["data"]["sentences"]:
            sentences.append({"target": sentence["source"], "source": sentence["target"]})
        data = {"sentences": sentences, "lang": data['params']['lang']}
    else:
        data = {"sentences": data["data"]["sentences"], "lang": data['params']['lang']}
    print(jsonify(data), data)
    return render_template('pages/examples.html', data=data, title=word)

@app.route('/phonetic')
def phonetic():
    text = request.args.get('text')
    language = 'am'
    ipa = get_IPA(text,language)
    output_file = f"static/mp3/{text.lstrip().replace(' ','-')}.mp3"
    output = gTTS(text=text, slow=False, lang="en")
    output.save(output_file)
    return jsonify(phonetic=ipa, pronunciation=output_file)
if __name__ == '__main__':
    app.run(debug=False, host='192.168.1.14')
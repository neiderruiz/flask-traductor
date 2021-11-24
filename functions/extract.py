from bs4 import BeautifulSoup
import requests
def scrapingDataTraductor(word):
    if(word):
        word = word.lower()
    data = requests.get(f"https://www.ingles.com/traductor/{word}")
    soup = BeautifulSoup(data.text, 'html.parser')
    translation_get = soup.find_all('div',{"class": "_2lEPxxeg _3qA_h9SE"})
    phrases_en = soup.find_all('td', {'class': 'AAmLzBFI', 'lang': 'en'})
    examples = soup.find_all('div',{'class': 'utrhOaHS'})
    exist_en = soup.find('div',{"id": "headword-en"})
    count_phrases = len(phrases_en)
    translations = []
    for i, val in enumerate(translation_get):
        translations.append(translation_get[i].text)
    language = "es"
    if(exist_en):
        language = 'en'
    return  phrases_en, examples, language, count_phrases, translations

def getSentencesTraductor(urlSentences):
    n = requests.get(urlSentences)
    count_examples = n.json()["data"]["totalHits"]
    return count_examples
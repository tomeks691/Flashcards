import json
from mtranslate import translate



def translate_words():
    with open("wordlist_tom.json") as f:
        words = json.load(f)
    for word in words:
        translated_word = translate(word, "pl")
        words[word] = translated_word
    with open("wordlist_tom.json", "w", encoding="UTF-8") as f:
        json.dump(words, f, indent=4, ensure_ascii=False)


translate_words()
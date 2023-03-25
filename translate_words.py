import json

from mtranslate import translate


def translate_words():
    with open("Time Travel.json") as f:
        words = json.load(f)
    for word in words:
        translated_word = translate(word, "pl")
        words[word] = translated_word
    with open("Time Travel.json", "w", encoding="UTF-8") as f:
        json.dump(words, f, indent=4, ensure_ascii=False)


translate_words()
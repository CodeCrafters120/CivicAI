from langdetect import detect

def detect_and_translate(text):
    lang = detect(text)
    return lang, text

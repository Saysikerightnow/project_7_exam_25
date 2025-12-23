
import spacy
en = spacy.load("en_core_web_lg")
stopwords = en.Defaults.stop_words
print(stopwords)


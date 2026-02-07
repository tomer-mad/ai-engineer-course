import nltk

# Download the new tokenizer models
nltk.download('punkt_tab')

from nltk.tokenize import word_tokenize

text = "Natural Language Processing with Python is fun!"
tokens = word_tokenize(text)
print(tokens)


from nltk.tokenize import word_tokenize
from collections import Counter
import nltk
nltk.download('punkt', quiet=True)

text = "Python is great. Python is simple. NLP with Python is powerful!"
tokens = [t.lower() for t in word_tokenize(text)]
freq = Counter(tokens)

print("Tokens:", tokens)
print("Frequencies:", freq)
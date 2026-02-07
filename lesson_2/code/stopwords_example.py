from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

text = "This is an example showing how tokenization and stopword removal work."
tokens = [t.lower() for t in word_tokenize(text)]
filtered = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]

print("Original tokens:", tokens)
print("Filtered tokens:", filtered)
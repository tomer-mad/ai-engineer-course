from gensim.models import Word2Vec, FastText
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt', quiet=True)

sentences = [
    "I like playing soccer",
    "He enjoys playing football",
    "She loves sports and games",
]

tokenized = [word_tokenize(s.lower()) for s in sentences]

# Train Word2Vec and FastText on same data
w2v = Word2Vec(tokenized, vector_size=20, window=2, min_count=1, sg=1)
ft = FastText(tokenized, vector_size=20, window=2, min_count=1, sg=1)

# Word that was seen
print("Word2Vec similarity between 'playing' and 'soccer':",
      w2v.wv.similarity("playing", "soccer"))
print("FastText similarity between 'playing' and 'soccer':",
      ft.wv.similarity("playing", "soccer"))

# Slightly misspelled / unseen word
misspelled = "playng"  # missing 'i'
print("\nWord2Vec knows 'playng'?", misspelled in w2v.wv.key_to_index)
try:
    print("Word2Vec similarity 'playng' vs 'playing':",
          w2v.wv.similarity(misspelled, "playing"))
except KeyError:
    print("Word2Vec: 'playng' is out of vocabulary (no vector)")

print("FastText knows 'playng' by subwords and similarity to 'playing':",
      ft.wv.similarity(misspelled, "playing"))


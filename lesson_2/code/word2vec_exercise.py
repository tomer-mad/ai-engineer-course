import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from gensim.models import Word2Vec, FastText


nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

STOP = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def wn_pos(tag):
    return {
        'J': wordnet.ADJ,
        'V': wordnet.VERB,
        'N': wordnet.NOUN,
        'R': wordnet.ADV
    }.get(tag[0], wordnet.NOUN)

def preprocess(s):
    tokens = word_tokenize(s.lower())
    tagged = pos_tag(tokens)
    final_preprocess = [
        lemmatizer.lemmatize(t, wn_pos(p))
        for t, p in tagged
        if t.isalpha() and t not in STOP
    ]
    print("Final preprocess:", final_preprocess)
    return final_preprocess

corpus = [
    "I love NLP.",
    "Natural language processing is fun.",
    "Learning about language helps."
]
docs = [preprocess(s) for s in corpus]

# Train embeddings
w2v = Word2Vec(docs, vector_size=30, window=2, min_count=1, sg=1)
ft = FastText(docs, vector_size=30, window=2, min_count=1, sg=1)

# Similar to "language"
print("Word2Vec similar to 'language':", w2v.wv.most_similar("language", topn=2))
print("FastText similar to 'language':", ft.wv.most_similar("language", topn=2))

# Typo case
typo = "languge"
print("\nWord2Vec has typo?", typo in w2v.wv.key_to_index)
try:
    print("Word2Vec similarity typo→language:", w2v.wv.similarity(typo, "language"))
except KeyError:
    print("Word2Vec: typo out of vocab")

print("FastText similarity typo→language:", ft.wv.similarity(typo, "language"))

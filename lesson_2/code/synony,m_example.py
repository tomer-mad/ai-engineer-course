import nltk
from nltk.corpus import wordnet
from gensim.downloader import load
from scipy.spatial.distance import cosine

nltk.download('wordnet')
model = load("glove-wiki-gigaword-50")

def top_synonyms(word, n=5):
    lemmas = set(
        l.name().replace('_',' ')
        for syn in wordnet.synsets(word)
        for l in syn.lemmas()
        if l.name().lower() != word.lower()
    )
    print("Lemmas", lemmas)
    candidates = [w for w in lemmas if w in model]
    print("Candidates", candidates)
    scored = sorted(
        [(w, 1 - cosine(model[word], model[w])) for w in candidates],
        key=lambda x: -x[1]
    )
    print("Scored", scored)
    return scored[:n]

print("Top synonyms for ‘happy’:", top_synonyms("happy"))
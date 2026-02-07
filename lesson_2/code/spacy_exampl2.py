import spacy

# Load the small English model
nlp = spacy.load("en_core_web_sm")

text = "Apple is looking at buying U.K. startup for $1 billion. I love processing text with spaCy!"

doc = nlp(text)  # run the pipeline

# Tokens, lemmas, POS
print("Token | Lemma | POS")
for token in doc:
    print(f"{token.text:8} | {token.lemma_:8} | {token.pos_}")

# Named Entities
print("\nNamed Entities:")
for ent in doc.ents:
    print(f"{ent.text} ({ent.label_})")

# Simple similarity (requires vectors; small model has limited vectors but still works)
sent1 = nlp("I enjoy natural language processing.")
sent2 = nlp("I like working with text.")
print("\nSimilarity between sentences:", round(sent1.similarity(sent2), 3))

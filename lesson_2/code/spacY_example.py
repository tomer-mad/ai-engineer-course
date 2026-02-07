import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is buying a startup in the U.K. for $1 billion.")

for ent in doc.ents:
    print(ent.text, "→", ent.label_)




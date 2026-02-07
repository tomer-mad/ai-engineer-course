"""
NLTK + Word2Vec Exercises Solutions
===================================
This file contains solutions for 10 NLP exercises using NLTK and Word2Vec.
Each exercise is implemented as a function with detailed comments for beginners.

Before running, make sure to install required packages:
    pip install nltk gensim scikit-learn numpy

And download NLTK data (run once):
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from nltk import pos_tag
from nltk.probability import FreqDist
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK data (uncomment if running for the first time)
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')


# =============================================================================
# Exercise 1: Lemmatization with POS Awareness
# =============================================================================
# Example text:
# "The children were playing in the park while their parents watched from the bench."
# Task:
# 1. Tokenize and POS tag the text.
# 2. Lemmatize all words twice: once without POS tags and once with POS tags.
# 3. Compare how the results differ.
# 4. Count how many words changed due to POS-based lemmatization.
# 5. Discuss why POS information improves lemmatization accuracy.
# =============================================================================

def exercise_1():
    """
    Lemmatization with POS Awareness

    KEY CONCEPTS:
    - Lemmatization: Reducing words to their base/dictionary form (e.g., "running" -> "run")
    - POS (Part of Speech): Identifying if a word is a noun, verb, adjective, etc.
    - POS helps lemmatizer understand context (e.g., "better" as adjective -> "good")
    """
    print("\n" + "="*60)
    print("Exercise 1: Lemmatization with POS Awareness")
    print("="*60)

    # Our example text
    text = "The children were playing in the park while their parents watched from the bench."
    print(f"\nOriginal text: {text}")

    # Step 1: Tokenize the text (split into individual words)
    # word_tokenize is smarter than split() - it handles punctuation properly
    tokens = word_tokenize(text)
    print(f"\nStep 1 - Tokenized words: {tokens}")

    # Step 2: POS tag the tokens (identify each word's part of speech)
    # pos_tag returns tuples like: ('children', 'NNS') where NNS = plural noun
    pos_tags = pos_tag(tokens)
    print(f"\nStep 2 - POS Tags: {pos_tags}")

    # Create a lemmatizer object
    lemmatizer = WordNetLemmatizer()

    # Helper function to convert NLTK POS tags to WordNet format
    # IMPORTANT: WordNet uses different tags than NLTK!
    # NLTK: NN (noun), VB (verb), JJ (adjective), RB (adverb)
    # WordNet: 'n' (noun), 'v' (verb), 'a' (adjective), 'r' (adverb)
    def get_wordnet_pos(nltk_tag):
        """Convert NLTK POS tag to WordNet POS tag"""
        if nltk_tag.startswith('J'):    # JJ, JJR, JJS = adjectives
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):  # VB, VBD, VBG, etc. = verbs
            return wordnet.VERB
        elif nltk_tag.startswith('N'):  # NN, NNS, NNP = nouns
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):  # RB, RBR, RBS = adverbs
            return wordnet.ADV
        else:
            return wordnet.NOUN  # Default to noun if unknown

    # Step 3a: Lemmatize WITHOUT POS tags (default assumes noun)
    lemmas_without_pos = [lemmatizer.lemmatize(word.lower()) for word in tokens]
    print(f"\nStep 3a - Lemmas WITHOUT POS: {lemmas_without_pos}")

    # Step 3b: Lemmatize WITH POS tags (more accurate!)
    lemmas_with_pos = []
    for word, tag in pos_tags:
        # Get the correct WordNet POS tag
        wn_pos = get_wordnet_pos(tag)
        # Lemmatize with the POS information
        lemma = lemmatizer.lemmatize(word.lower(), pos=wn_pos)
        lemmas_with_pos.append(lemma)
    print(f"\nStep 3b - Lemmas WITH POS: {lemmas_with_pos}")

    # Step 4: Count differences
    differences = 0
    print("\nStep 4 - Comparing results:")
    for i, (without, with_pos) in enumerate(zip(lemmas_without_pos, lemmas_with_pos)):
        if without != with_pos:
            differences += 1
            print(f"  '{tokens[i]}': without POS='{without}' vs with POS='{with_pos}'")

    print(f"\nTotal words that changed due to POS-based lemmatization: {differences}")

    # Step 5: Discussion
    print("\n" + "-"*40)
    print("Discussion: Why POS improves lemmatization?")
    print("-"*40)
    print("""
    Without POS: The lemmatizer assumes all words are NOUNS by default.
    - 'were' stays as 'were' (noun assumption fails)
    - 'playing' becomes 'playing' (not recognized as verb)
    - 'watched' stays as 'watched'

    With POS: The lemmatizer knows the correct word type.
    - 'were' (verb) -> 'be' (correct base form!)
    - 'playing' (verb) -> 'play' (correct!)
    - 'watched' (verb) -> 'watch' (correct!)

    CONCLUSION: POS tagging is essential for accurate lemmatization,
    especially for verbs and adjectives!
    """)


# =============================================================================
# Exercise 2: Lemmatization Comparison Across Languages
# =============================================================================
# Example text:
# English: "She was running quickly and finished early."
# French: "Elle courait rapidement et a terminé tôt."
# Task:
# 1. Use NLTK's WordNet lemmatizer for English and another lemmatizer for French.
# 2. Compare how each handles verb conjugation and noun forms.
# 3. Discuss challenges of multilingual lemmatization.
# =============================================================================

def exercise_2():
    """
    Lemmatization Comparison Across Languages

    KEY CONCEPTS:
    - Different languages have different grammatical rules
    - NLTK's WordNet only works well for English
    - Multilingual NLP requires language-specific tools
    """
    print("\n" + "="*60)
    print("Exercise 2: Lemmatization Comparison Across Languages")
    print("="*60)

    # English text
    english_text = "She was running quickly and finished early."
    # French text (note: we'll use a simplified approach)
    french_text = "Elle courait rapidement et a terminé tôt."

    print(f"\nEnglish text: {english_text}")
    print(f"French text: {french_text}")

    # ----- ENGLISH LEMMATIZATION -----
    print("\n--- English Lemmatization (using WordNet) ---")

    lemmatizer = WordNetLemmatizer()

    # Tokenize and POS tag English text
    eng_tokens = word_tokenize(english_text)
    eng_pos_tags = pos_tag(eng_tokens)

    # Helper function (same as Exercise 1)
    def get_wordnet_pos(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # Lemmatize English
    eng_lemmas = []
    for word, tag in eng_pos_tags:
        wn_pos = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(word.lower(), pos=wn_pos)
        eng_lemmas.append(lemma)
        print(f"  '{word}' ({tag}) -> '{lemma}'")

    # ----- FRENCH LEMMATIZATION (Simplified approach) -----
    print("\n--- French Lemmatization (simplified dictionary approach) ---")

    # Since NLTK doesn't have a French lemmatizer, we'll use a simple dictionary
    # In real projects, you would use spaCy with French model: python -m spacy download fr_core_news_sm
    # or use other libraries like Stanza, TreeTagger, etc.

    # Simple French lemma dictionary (for demonstration)
    french_lemmas_dict = {
        'elle': 'elle',          # she (pronoun, no change)
        'courait': 'courir',     # was running -> to run (imparfait -> infinitive)
        'rapidement': 'rapide',  # quickly -> quick (adverb -> adjective base)
        'et': 'et',              # and
        'a': 'avoir',            # has (auxiliary) -> to have
        'terminé': 'terminer',   # finished -> to finish
        'tôt': 'tôt',            # early (no change for adverbs in French)
        '.': '.'
    }

    # Simple tokenization for French (basic split)
    french_tokens = french_text.replace('.', ' .').split()

    print("\nFrench lemmatization using dictionary lookup:")
    for token in french_tokens:
        token_lower = token.lower()
        lemma = french_lemmas_dict.get(token_lower, token_lower)
        print(f"  '{token}' -> '{lemma}'")

    # Discussion
    print("\n" + "-"*40)
    print("Discussion: Challenges of Multilingual Lemmatization")
    print("-"*40)
    print("""
    1. VERB CONJUGATION:
       - English: 'running' -> 'run', 'finished' -> 'finish'
       - French: 'courait' (imparfait) -> 'courir' (infinitive)
       - French has MORE verb forms than English (6+ conjugations per tense!)

    2. GENDER AND NUMBER:
       - English: mostly neutral
       - French: nouns have gender (le/la), adjectives must agree

    3. TOOL AVAILABILITY:
       - English: Many tools (NLTK, spaCy, etc.)
       - French: Fewer options, need spaCy French model or TreeTagger

    4. COMPOUND WORDS:
       - German: 'Handschuh' (hand + shoe = glove)
       - Need special handling for compound decomposition

    RECOMMENDATION for French: Use spaCy with 'fr_core_news_sm' model
    Example:
        import spacy
        nlp = spacy.load('fr_core_news_sm')
        doc = nlp("Elle courait rapidement")
        for token in doc:
            print(token.text, token.lemma_)
    """)


# =============================================================================
# Exercise 3: Domain-Specific Lemmatization
# =============================================================================
# Example text:
# "The data scientists are analyzing the datasets and building predictive models."
# Task:
# 1. Create a dictionary of domain-specific corrections (e.g., "datasets" → "dataset").
# 2. Apply lemmatization, and then apply your corrections.
# 3. Compare the text before and after.
# 4. Discuss when such manual normalization is necessary.
# =============================================================================

def exercise_3():
    """
    Domain-Specific Lemmatization

    KEY CONCEPTS:
    - Standard lemmatizers don't know domain-specific terms
    - Technical/scientific fields need custom normalization
    - Post-processing can fix lemmatizer mistakes
    """
    print("\n" + "="*60)
    print("Exercise 3: Domain-Specific Lemmatization")
    print("="*60)

    text = "The data scientists are analyzing the datasets and building predictive models."
    print(f"\nOriginal text: {text}")

    # Step 1: Create domain-specific corrections dictionary
    # These are terms that standard lemmatizers might not handle correctly
    domain_corrections = {
        'datasets': 'dataset',           # Technical plural
        'scientists': 'scientist',       # Standard lemmatizer should catch this
        'data': 'data',                  # Keep as is (already singular in data science context)
        'models': 'model',               # Technical term
        'predictive': 'predictive',      # Keep as adjective (don't convert to 'predict')
        'analyzing': 'analyze',          # Verb form
        'building': 'build',             # Verb form
    }

    print("\nStep 1 - Domain-specific corrections dictionary:")
    for original, corrected in domain_corrections.items():
        if original != corrected:
            print(f"  '{original}' -> '{corrected}'")

    # Step 2: Apply standard lemmatization first
    print("\nStep 2 - Standard lemmatization:")

    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)

    def get_wordnet_pos(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # First pass: standard lemmatization
    lemmas_standard = []
    for word, tag in pos_tags:
        wn_pos = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(word.lower(), pos=wn_pos)
        lemmas_standard.append(lemma)

    print(f"After standard lemmatization: {' '.join(lemmas_standard)}")

    # Step 3: Apply domain-specific corrections
    print("\nStep 3 - Applying domain-specific corrections:")

    lemmas_corrected = []
    for lemma in lemmas_standard:
        # Check if this lemma needs correction
        if lemma in domain_corrections:
            corrected = domain_corrections[lemma]
            if corrected != lemma:
                print(f"  Correcting: '{lemma}' -> '{corrected}'")
            lemmas_corrected.append(corrected)
        else:
            lemmas_corrected.append(lemma)

    print(f"\nAfter domain corrections: {' '.join(lemmas_corrected)}")

    # Step 4: Compare before and after
    print("\n" + "-"*40)
    print("Comparison: Before vs After")
    print("-"*40)
    print(f"Original tokens:    {' '.join([t.lower() for t in tokens])}")
    print(f"Standard lemmas:    {' '.join(lemmas_standard)}")
    print(f"Domain-corrected:   {' '.join(lemmas_corrected)}")

    # Discussion
    print("\n" + "-"*40)
    print("Discussion: When is manual normalization necessary?")
    print("-"*40)
    print("""
    Manual normalization is needed when:

    1. TECHNICAL JARGON:
       - 'APIs' -> 'API' (standard lemmatizer might not know this)
       - 'JSONs' -> 'JSON'
       - 'datasets' -> 'dataset'

    2. BRAND NAMES / PROPER NOUNS:
       - 'iPhones' -> 'iPhone'
       - 'Kubernetes' (don't lemmatize to something wrong)

    3. DOMAIN-SPECIFIC MEANINGS:
       - Medical: 'carcinomas' -> 'carcinoma'
       - Legal: 'torts' -> 'tort'

    4. ABBREVIATIONS:
       - 'ML' should stay 'ML' not 'ml' (milliliter)
       - 'NLP' -> 'NLP' (not 'nlp')

    5. COMPOUND TECHNICAL TERMS:
       - 'machine learning' should stay together
       - 'deep learning' shouldn't become 'deep learn'

    BEST PRACTICE: Create a domain dictionary BEFORE processing your data!
    """)


# =============================================================================
# Exercise 4: Frequency Distribution After Lemmatization
# =============================================================================
# Example text:
# "Dogs are running faster than the cats that were sleeping under the table."
# Task:
# 1. Perform tokenization, stopword removal, and lemmatization.
# 2. Compute a frequency distribution of the lemmas.
# 3. Compare it with the frequency distribution before lemmatization.
# 4. Discuss the effect on feature sparsity for NLP models.
# =============================================================================

def exercise_4():
    """
    Frequency Distribution After Lemmatization

    KEY CONCEPTS:
    - Frequency Distribution: Counting how often each word appears
    - Stopwords: Common words (the, is, are) that don't add meaning
    - Feature Sparsity: Having too many unique features (words) makes models harder to train
    """
    print("\n" + "="*60)
    print("Exercise 4: Frequency Distribution After Lemmatization")
    print("="*60)

    text = "Dogs are running faster than the cats that were sleeping under the table."
    print(f"\nOriginal text: {text}")

    # Step 1: Tokenization
    tokens = word_tokenize(text.lower())
    print(f"\nStep 1a - Tokens: {tokens}")
    print(f"Number of tokens: {len(tokens)}")

    # Remove punctuation (keep only alphabetic tokens)
    tokens_clean = [token for token in tokens if token.isalpha()]
    print(f"\nStep 1b - After removing punctuation: {tokens_clean}")

    # Step 2: Stopword removal
    # Stopwords are common words that usually don't carry meaning
    stop_words = set(stopwords.words('english'))
    print(f"\nSome English stopwords: {list(stop_words)[:10]}...")

    tokens_no_stop = [token for token in tokens_clean if token not in stop_words]
    print(f"\nStep 2 - After stopword removal: {tokens_no_stop}")
    print(f"Removed words: {[t for t in tokens_clean if t in stop_words]}")

    # Step 3: Lemmatization (with POS tags for accuracy)
    lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # Get POS tags for remaining tokens
    pos_tags = pos_tag(tokens_no_stop)

    lemmas = []
    for word, tag in pos_tags:
        wn_pos = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(word, pos=wn_pos)
        lemmas.append(lemma)

    print(f"\nStep 3 - Lemmatized words: {lemmas}")

    # Step 4: Compute frequency distributions
    print("\n" + "-"*40)
    print("Frequency Distributions")
    print("-"*40)

    # Before lemmatization (original tokens without stopwords)
    freq_before = FreqDist(tokens_no_stop)
    print("\nBEFORE lemmatization:")
    print(f"  Unique words: {len(freq_before)}")
    print(f"  Word frequencies: {dict(freq_before)}")

    # After lemmatization
    freq_after = FreqDist(lemmas)
    print("\nAFTER lemmatization:")
    print(f"  Unique words: {len(freq_after)}")
    print(f"  Word frequencies: {dict(freq_after)}")

    # Compare
    print("\n" + "-"*40)
    print("Comparison")
    print("-"*40)
    reduction = len(freq_before) - len(freq_after)
    percentage = (reduction / len(freq_before)) * 100 if len(freq_before) > 0 else 0
    print(f"Unique words BEFORE: {len(freq_before)}")
    print(f"Unique words AFTER:  {len(freq_after)}")
    print(f"Reduction: {reduction} words ({percentage:.1f}%)")

    # Discussion
    print("\n" + "-"*40)
    print("Discussion: Effect on Feature Sparsity")
    print("-"*40)
    print("""
    WHAT IS FEATURE SPARSITY?
    - In NLP, each unique word becomes a 'feature' for machine learning
    - More unique words = more features = 'sparser' data
    - Sparse data makes models harder to train and less accurate

    HOW LEMMATIZATION HELPS:
    1. REDUCES VOCABULARY SIZE:
       - 'dogs', 'dog' -> 'dog' (2 features become 1)
       - 'running', 'ran', 'runs' -> 'run' (3 features become 1)

    2. IMPROVES WORD MATCHING:
       - "I love dogs" and "I love dog" now match better
       - Better similarity calculations between documents

    3. FASTER TRAINING:
       - Fewer features = smaller matrices
       - Less memory usage
       - Faster model training

    4. BETTER GENERALIZATION:
       - Model learns patterns, not specific word forms
       - Works better on new/unseen data

    IN THIS EXAMPLE:
    - 'dogs' -> 'dog', 'cats' -> 'cat'
    - 'running' -> 'run', 'sleeping' -> 'sleep'
    - This reduces feature count and makes the text easier to analyze!
    """)


# =============================================================================
# Exercise 5: Word Similarity Using Word2Vec Embeddings
# =============================================================================
# Example text:
# "King, Queen, Man, Woman, Prince, Princess."
# Task:
# 1. Train a small Word2Vec model on this mini text.
# 2. Compute similarity scores between pairs like ("king", "queen"), ("man", "woman").
# 3. Identify the most similar pairs.
# 4. Discuss what semantic relationships the model captures.
# =============================================================================

def exercise_5():
    """
    Word Similarity Using Word2Vec Embeddings

    KEY CONCEPTS:
    - Word2Vec: Converts words to numbers (vectors) that capture meaning
    - Similar words have similar vectors
    - Words used in similar contexts get similar vectors
    """
    print("\n" + "="*60)
    print("Exercise 5: Word Similarity Using Word2Vec Embeddings")
    print("="*60)

    # IMPORTANT: Word2Vec needs more training data to learn meaningful relationships!
    # With just one sentence, the model won't learn much.
    # We'll create multiple sentences to give it more context.

    # Training sentences (we need more context for Word2Vec to learn)
    training_sentences = [
        ['king', 'queen', 'prince', 'princess', 'royal', 'crown'],
        ['king', 'man', 'ruler', 'kingdom', 'throne'],
        ['queen', 'woman', 'ruler', 'kingdom', 'throne'],
        ['man', 'woman', 'person', 'human', 'adult'],
        ['prince', 'princess', 'young', 'royal', 'heir'],
        ['prince', 'man', 'young', 'boy', 'son'],
        ['princess', 'woman', 'young', 'girl', 'daughter'],
        ['king', 'queen', 'married', 'royal', 'couple'],
        ['man', 'husband', 'father', 'male', 'person'],
        ['woman', 'wife', 'mother', 'female', 'person'],
    ]

    print("\nTraining Word2Vec model on royal family context...")
    print(f"Number of training sentences: {len(training_sentences)}")

    # Step 1: Train Word2Vec model
    # Parameters explained:
    # - sentences: our training data
    # - vector_size: dimension of word vectors (100 is common, we use 50 for small data)
    # - window: how many words to consider as context (2 means 2 words before and after)
    # - min_count: ignore words that appear less than this (1 = keep all)
    # - workers: number of CPU cores to use
    # - epochs: how many times to train on the data (more = better, but slower)

    model = Word2Vec(
        sentences=training_sentences,
        vector_size=50,      # Small vectors for our small dataset
        window=3,            # Context window
        min_count=1,         # Keep all words
        workers=1,           # Single thread
        epochs=100,          # Train more times for better results
        seed=42              # For reproducibility
    )

    print(f"\nModel vocabulary: {list(model.wv.key_to_index.keys())}")

    # Step 2: Compute similarity scores
    print("\n" + "-"*40)
    print("Step 2: Computing similarity scores")
    print("-"*40)

    # Define pairs to compare
    pairs_to_compare = [
        ('king', 'queen'),
        ('man', 'woman'),
        ('king', 'man'),
        ('queen', 'woman'),
        ('prince', 'princess'),
        ('king', 'prince'),
    ]

    # Calculate similarities
    similarities = []
    for word1, word2 in pairs_to_compare:
        if word1 in model.wv and word2 in model.wv:
            # similarity() returns a value between -1 and 1
            # 1 = identical, 0 = unrelated, -1 = opposite
            sim = model.wv.similarity(word1, word2)
            similarities.append((word1, word2, sim))
            print(f"  Similarity('{word1}', '{word2}'): {sim:.4f}")
        else:
            print(f"  Word not in vocabulary: {word1} or {word2}")

    # Step 3: Identify most similar pairs
    print("\n" + "-"*40)
    print("Step 3: Ranking pairs by similarity")
    print("-"*40)

    # Sort by similarity (highest first)
    similarities_sorted = sorted(similarities, key=lambda x: x[2], reverse=True)

    print("\nMost similar pairs (ranked):")
    for i, (w1, w2, sim) in enumerate(similarities_sorted, 1):
        print(f"  {i}. ('{w1}', '{w2}'): {sim:.4f}")

    # Step 4: Discussion
    print("\n" + "-"*40)
    print("Discussion: What relationships does Word2Vec capture?")
    print("-"*40)
    print("""
    Word2Vec captures semantic relationships through context:

    1. GENDER RELATIONSHIPS:
       - king/queen, man/woman, prince/princess
       - These pairs appear in similar contexts but differ by gender

    2. ROYALTY vs COMMON:
       - king/man: both male, but king is royal
       - queen/woman: both female, but queen is royal

    3. AGE/HIERARCHY:
       - king/prince: both male royalty, but different ages
       - king is parent, prince is child

    HOW WORD2VEC LEARNS:
    - "king" and "queen" appear together -> similar vectors
    - "man" and "king" share some contexts -> somewhat similar
    - Words used interchangeably get close vectors

    LIMITATIONS WITH SMALL DATA:
    - Our model has limited training data
    - Real Word2Vec models train on millions of sentences
    - Results would be much better with more data!

    TIP: For real projects, use pre-trained models like:
    - Google News Word2Vec (3 million words!)
    - GloVe embeddings
    - FastText
    """)


# =============================================================================
# Exercise 6: Finding Analogies with Word2Vec
# =============================================================================
# Example text:
# "Paris is the capital of France, and Berlin is the capital of Germany."
# Task:
# 1. Train a small Word2Vec model on related sentences.
# 2. Use vector arithmetic to solve analogy queries like:
#    "France" is to "Paris" as "Germany" is to ?
# 3. Discuss how Word2Vec captures analogy through vector space operations.
# =============================================================================

def exercise_6():
    """
    Finding Analogies with Word2Vec

    KEY CONCEPTS:
    - Word vectors can be added/subtracted like regular numbers!
    - king - man + woman ≈ queen
    - This is called "vector arithmetic" or "analogy solving"
    """
    print("\n" + "="*60)
    print("Exercise 6: Finding Analogies with Word2Vec")
    print("="*60)

    # We need more training data for analogies to work
    # Let's create sentences about countries and capitals
    training_sentences = [
        ['paris', 'is', 'capital', 'of', 'france'],
        ['berlin', 'is', 'capital', 'of', 'germany'],
        ['rome', 'is', 'capital', 'of', 'italy'],
        ['madrid', 'is', 'capital', 'of', 'spain'],
        ['london', 'is', 'capital', 'of', 'england'],
        ['france', 'country', 'europe', 'paris', 'french'],
        ['germany', 'country', 'europe', 'berlin', 'german'],
        ['italy', 'country', 'europe', 'rome', 'italian'],
        ['spain', 'country', 'europe', 'madrid', 'spanish'],
        ['england', 'country', 'europe', 'london', 'english'],
        ['paris', 'france', 'city', 'capital'],
        ['berlin', 'germany', 'city', 'capital'],
        ['rome', 'italy', 'city', 'capital'],
        ['madrid', 'spain', 'city', 'capital'],
        ['london', 'england', 'city', 'capital'],
        # Add more context sentences
        ['france', 'paris', 'eiffel', 'tower'],
        ['germany', 'berlin', 'wall', 'history'],
        ['italy', 'rome', 'colosseum', 'ancient'],
    ]

    print("\nTraining Word2Vec on country-capital data...")

    # Train model with more epochs for better learning
    model = Word2Vec(
        sentences=training_sentences,
        vector_size=50,
        window=5,
        min_count=1,
        workers=1,
        epochs=200,  # More training for better analogies
        seed=42
    )

    print(f"Vocabulary: {list(model.wv.key_to_index.keys())}")

    # Step 2: Vector arithmetic for analogies
    print("\n" + "-"*40)
    print("Step 2: Solving Analogies with Vector Arithmetic")
    print("-"*40)

    # The formula: france - paris + berlin = ?
    # This asks: "What is to Germany as Paris is to France?"
    # Expected answer: germany

    print("\nAnalogy: 'france' is to 'paris' as '?' is to 'berlin'")
    print("Formula: france - paris + berlin = ?")

    try:
        # most_similar with positive and negative words
        # positive: words to add
        # negative: words to subtract
        result = model.wv.most_similar(
            positive=['france', 'berlin'],
            negative=['paris'],
            topn=3  # Return top 3 results
        )

        print("\nResults (word, similarity):")
        for word, score in result:
            print(f"  {word}: {score:.4f}")

        print(f"\nBest answer: '{result[0][0]}' (expected: 'germany')")

    except KeyError as e:
        print(f"Error: Word not in vocabulary - {e}")

    # Try another analogy
    print("\n" + "-"*40)
    print("Another Analogy: 'italy' is to 'rome' as '?' is to 'madrid'")
    print("Formula: italy - rome + madrid = ?")

    try:
        result2 = model.wv.most_similar(
            positive=['italy', 'madrid'],
            negative=['rome'],
            topn=3
        )

        print("\nResults:")
        for word, score in result2:
            print(f"  {word}: {score:.4f}")

        print(f"\nBest answer: '{result2[0][0]}' (expected: 'spain')")

    except KeyError as e:
        print(f"Error: {e}")

    # Discussion
    print("\n" + "-"*40)
    print("Discussion: How Word2Vec Captures Analogies")
    print("-"*40)
    print("""
    VECTOR ARITHMETIC EXPLAINED:

    Think of each word as a point in space:

    1. 'france' and 'paris' are related (country-capital)
    2. 'germany' and 'berlin' are related the SAME way

    The vector from 'paris' to 'france' represents "capital -> country"

    So: france - paris = the "capital-to-country" direction
        Adding this to berlin = "berlin + capital-to-country" = germany!

    MATHEMATICALLY:
    france - paris ≈ germany - berlin

    Therefore:
    france - paris + berlin ≈ germany

    FAMOUS EXAMPLE:
    king - man + woman ≈ queen

    This works because:
    - king and queen differ by gender
    - man and woman differ by gender the same way
    - The "gender direction" is captured in the vectors!

    LIMITATIONS:
    - Needs LOTS of training data
    - Our small dataset may not give perfect results
    - Pre-trained models (like Google's) work much better
    """)


# =============================================================================
# Exercise 7: Sentence Semantic Similarity
# =============================================================================
# Example text:
# Sentence 1: "The man is playing guitar."
# Sentence 2: "A person performs music on stage."
# Task:
# 1. Tokenize and lemmatize both sentences.
# 2. Use pretrained Word2Vec or gensim model to compute average word vectors.
# 3. Measure cosine similarity between the sentences.
# 4. Discuss how similar they are semantically vs. lexically.
# =============================================================================

def exercise_7():
    """
    Sentence Semantic Similarity

    KEY CONCEPTS:
    - Semantic similarity: Do sentences MEAN the same thing?
    - Lexical similarity: Do sentences use the same WORDS?
    - Average word vectors: Simple way to represent a sentence as one vector
    - Cosine similarity: Measures angle between vectors (1 = same, 0 = unrelated)
    """
    print("\n" + "="*60)
    print("Exercise 7: Sentence Semantic Similarity")
    print("="*60)

    sentence1 = "The man is playing guitar."
    sentence2 = "A person performs music on stage."

    print(f"\nSentence 1: {sentence1}")
    print(f"Sentence 2: {sentence2}")

    # Step 1: Tokenize and lemmatize
    print("\n" + "-"*40)
    print("Step 1: Tokenization and Lemmatization")
    print("-"*40)

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    def get_wordnet_pos(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def preprocess(sentence):
        """Tokenize, remove stopwords, and lemmatize a sentence"""
        # Tokenize
        tokens = word_tokenize(sentence.lower())
        # Remove punctuation and stopwords
        tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
        # POS tag
        pos_tags = pos_tag(tokens)
        # Lemmatize
        lemmas = []
        for word, tag in pos_tags:
            wn_pos = get_wordnet_pos(tag)
            lemma = lemmatizer.lemmatize(word, pos=wn_pos)
            lemmas.append(lemma)
        return lemmas

    lemmas1 = preprocess(sentence1)
    lemmas2 = preprocess(sentence2)

    print(f"Sentence 1 lemmas: {lemmas1}")
    print(f"Sentence 2 lemmas: {lemmas2}")

    # Step 2: Train a Word2Vec model (or use pretrained)
    # For this example, we'll train on related sentences
    print("\n" + "-"*40)
    print("Step 2: Creating Word2Vec Model")
    print("-"*40)

    # Training data with related vocabulary
    training_sentences = [
        ['man', 'person', 'human', 'male', 'adult'],
        ['woman', 'person', 'human', 'female', 'adult'],
        ['play', 'perform', 'music', 'instrument'],
        ['guitar', 'instrument', 'music', 'string'],
        ['stage', 'perform', 'concert', 'music'],
        ['man', 'play', 'guitar', 'music'],
        ['person', 'perform', 'music', 'stage'],
        ['musician', 'play', 'instrument', 'perform'],
        ['concert', 'stage', 'music', 'play'],
    ]

    model = Word2Vec(
        sentences=training_sentences,
        vector_size=50,
        window=3,
        min_count=1,
        workers=1,
        epochs=100,
        seed=42
    )

    print(f"Model vocabulary: {list(model.wv.key_to_index.keys())}")

    # Step 3: Compute average word vectors for each sentence
    print("\n" + "-"*40)
    print("Step 3: Computing Sentence Vectors")
    print("-"*40)

    def get_sentence_vector(lemmas, model):
        """
        Compute average of all word vectors in a sentence.
        This is a simple but effective way to represent a sentence.
        """
        vectors = []
        words_found = []
        words_missing = []

        for word in lemmas:
            if word in model.wv:
                vectors.append(model.wv[word])
                words_found.append(word)
            else:
                words_missing.append(word)

        if vectors:
            # Average all word vectors
            avg_vector = np.mean(vectors, axis=0)
            return avg_vector, words_found, words_missing
        else:
            return None, words_found, words_missing

    vec1, found1, missing1 = get_sentence_vector(lemmas1, model)
    vec2, found2, missing2 = get_sentence_vector(lemmas2, model)

    print(f"Sentence 1: found {found1}, missing {missing1}")
    print(f"Sentence 2: found {found2}, missing {missing2}")

    # Step 4: Compute cosine similarity
    print("\n" + "-"*40)
    print("Step 4: Measuring Cosine Similarity")
    print("-"*40)

    if vec1 is not None and vec2 is not None:
        # Reshape for sklearn's cosine_similarity function
        vec1_2d = vec1.reshape(1, -1)
        vec2_2d = vec2.reshape(1, -1)

        similarity = cosine_similarity(vec1_2d, vec2_2d)[0][0]

        print(f"\nCosine Similarity: {similarity:.4f}")
        print(f"\nInterpretation:")
        if similarity > 0.8:
            print("  Very similar sentences!")
        elif similarity > 0.5:
            print("  Moderately similar sentences")
        elif similarity > 0.2:
            print("  Somewhat similar sentences")
        else:
            print("  Not very similar sentences")
    else:
        print("Could not compute similarity (missing word vectors)")

    # Calculate lexical similarity (word overlap)
    print("\n" + "-"*40)
    print("Lexical vs Semantic Similarity Comparison")
    print("-"*40)

    set1 = set(lemmas1)
    set2 = set(lemmas2)
    common_words = set1.intersection(set2)

    # Jaccard similarity (lexical)
    if set1.union(set2):
        lexical_sim = len(common_words) / len(set1.union(set2))
    else:
        lexical_sim = 0

    print(f"\nLexical Analysis:")
    print(f"  Sentence 1 words: {set1}")
    print(f"  Sentence 2 words: {set2}")
    print(f"  Common words: {common_words}")
    print(f"  Jaccard Similarity (lexical): {lexical_sim:.4f}")

    # Discussion
    print("\n" + "-"*40)
    print("Discussion: Semantic vs Lexical Similarity")
    print("-"*40)
    print("""
    LEXICAL SIMILARITY:
    - Measures: Do the sentences share the same words?
    - Method: Count overlapping words
    - Problem: "man" and "person" are different words but same meaning!

    SEMANTIC SIMILARITY:
    - Measures: Do the sentences have the same meaning?
    - Method: Compare word vectors
    - Advantage: Captures synonyms and related concepts

    IN THIS EXAMPLE:
    - Lexically: Low similarity (different words)
    - Semantically: Higher similarity (same meaning!)

    Why?
    - "man" ≈ "person" (both humans)
    - "playing" ≈ "performs" (both doing music)
    - "guitar" ≈ "music" (related concepts)

    REAL-WORLD APPLICATIONS:
    - Search engines: Find pages that MEAN what you searched
    - Chatbots: Understand different phrasings of same question
    - Plagiarism detection: Find paraphrased content
    - Document clustering: Group similar documents
    """)


# =============================================================================
# Exercise 8: POS and Lemmatization-Based Keyword Extraction
# =============================================================================
# Example text:
# "Artificial intelligence and machine learning are transforming modern industries
# through data-driven solutions."
# Task:
# 1. POS-tag and lemmatize the sentence.
# 2. Extract only nouns and verbs as keywords.
# 3. Rank the keywords by frequency or importance.
# 4. Discuss why lemmatization improves keyword consistency.
# =============================================================================

def exercise_8():
    """
    POS and Lemmatization-Based Keyword Extraction

    KEY CONCEPTS:
    - Keywords: Important words that describe the main topic
    - Usually nouns (things) and verbs (actions) are most important
    - Lemmatization helps group different forms of same word
    """
    print("\n" + "="*60)
    print("Exercise 8: POS and Lemmatization-Based Keyword Extraction")
    print("="*60)

    text = "Artificial intelligence and machine learning are transforming modern industries through data-driven solutions."
    print(f"\nOriginal text: {text}")

    # Step 1: Tokenize and POS tag
    print("\n" + "-"*40)
    print("Step 1: POS Tagging")
    print("-"*40)

    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)

    print("\nPOS Tags (word, tag):")
    for word, tag in pos_tags:
        # Explain some common tags
        tag_meanings = {
            'NN': 'noun (singular)',
            'NNS': 'noun (plural)',
            'NNP': 'proper noun',
            'VB': 'verb (base)',
            'VBG': 'verb (-ing)',
            'VBP': 'verb (present)',
            'JJ': 'adjective',
            'RB': 'adverb',
            'CC': 'conjunction',
            'IN': 'preposition',
            'DT': 'determiner',
        }
        meaning = tag_meanings.get(tag, tag)
        print(f"  '{word}': {tag} ({meaning})")

    # Step 2: Lemmatize
    print("\n" + "-"*40)
    print("Step 2: Lemmatization")
    print("-"*40)

    lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    lemmatized_tags = []
    for word, tag in pos_tags:
        wn_pos = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(word.lower(), pos=wn_pos)
        lemmatized_tags.append((word, lemma, tag))
        if word.lower() != lemma:
            print(f"  '{word}' -> '{lemma}'")

    # Step 3: Extract nouns and verbs only
    print("\n" + "-"*40)
    print("Step 3: Extracting Keywords (Nouns and Verbs)")
    print("-"*40)

    keywords = []

    for word, lemma, tag in lemmatized_tags:
        # Check if it's a noun (NN*) or verb (VB*)
        if tag.startswith('NN') or tag.startswith('VB'):
            # Skip common/stopwords even if they're verbs
            stop_words = set(stopwords.words('english'))
            if lemma not in stop_words and lemma.isalpha():
                keywords.append({
                    'original': word,
                    'lemma': lemma,
                    'pos': 'NOUN' if tag.startswith('NN') else 'VERB'
                })
                print(f"  Keyword: '{lemma}' ({tag} -> {'NOUN' if tag.startswith('NN') else 'VERB'})")

    # Step 4: Rank keywords by frequency
    print("\n" + "-"*40)
    print("Step 4: Ranking Keywords")
    print("-"*40)

    # Count frequency of each lemma
    lemma_counts = {}
    for kw in keywords:
        lemma = kw['lemma']
        if lemma in lemma_counts:
            lemma_counts[lemma]['count'] += 1
        else:
            lemma_counts[lemma] = {'count': 1, 'pos': kw['pos']}

    # Sort by count (descending)
    sorted_keywords = sorted(lemma_counts.items(), key=lambda x: x[1]['count'], reverse=True)

    print("\nRanked Keywords:")
    for rank, (lemma, info) in enumerate(sorted_keywords, 1):
        print(f"  {rank}. '{lemma}' ({info['pos']}) - frequency: {info['count']}")

    # Discussion
    print("\n" + "-"*40)
    print("Discussion: Why Lemmatization Improves Keyword Consistency")
    print("-"*40)
    print("""
    WITHOUT LEMMATIZATION:
    - "learning" and "learns" would be separate keywords
    - "industries" and "industry" would be counted separately
    - Keyword rankings would be fragmented

    WITH LEMMATIZATION:
    - "learning" -> "learn" (all forms grouped)
    - "industries" -> "industry" (singular form)
    - More accurate frequency counts

    BENEFITS:
    1. BETTER TOPIC IDENTIFICATION:
       - All variations of "learn" combine into one count
       - Truly important words rise to the top

    2. IMPROVED SEARCH:
       - Searching for "learn" finds all related forms
       - Better document matching

    3. REDUCED NOISE:
       - Fewer unique keywords to consider
       - Focus on meaning, not spelling variations

    4. CROSS-DOCUMENT COMPARISON:
       - "The model learns" and "models learning"
       - Both produce keywords: "model", "learn"
       - Makes document comparison more accurate

    WHY NOUNS AND VERBS?
    - Nouns: The "what" (things, concepts)
    - Verbs: The "action" (what's happening)
    - Adjectives/adverbs often less important for core meaning
    - "AI transforms industries" vs "AI quickly transforms large industries"
    - Core meaning is the same!
    """)


# =============================================================================
# Exercise 9: Context Window Analysis with Word2Vec
# =============================================================================
# Example text:
# "The doctor prescribed medicine to the patient who was recovering in the hospital."
# Task:
# 1. Train a small Word2Vec model with different context window sizes (2, 5, 10).
# 2. Observe how changing the window size affects word relationships.
# 3. Discuss which window size best captures meaningful relationships.
# =============================================================================

def exercise_9():
    """
    Context Window Analysis with Word2Vec

    KEY CONCEPTS:
    - Context window: How many neighboring words to consider when learning
    - Small window (2): Captures syntax (word order, grammar)
    - Large window (10): Captures semantics (topic, meaning)
    """
    print("\n" + "="*60)
    print("Exercise 9: Context Window Analysis with Word2Vec")
    print("="*60)

    # We need more training data for meaningful comparisons
    training_sentences = [
        ['the', 'doctor', 'prescribed', 'medicine', 'to', 'the', 'patient'],
        ['the', 'patient', 'was', 'recovering', 'in', 'the', 'hospital'],
        ['doctor', 'works', 'at', 'the', 'hospital', 'treating', 'patient'],
        ['medicine', 'helps', 'patient', 'recover', 'from', 'illness'],
        ['hospital', 'has', 'many', 'doctor', 'and', 'patient'],
        ['patient', 'takes', 'medicine', 'prescribed', 'by', 'doctor'],
        ['doctor', 'examines', 'patient', 'in', 'hospital', 'room'],
        ['recovering', 'patient', 'leaves', 'hospital', 'soon'],
        ['hospital', 'pharmacy', 'provides', 'medicine', 'to', 'patient'],
        ['doctor', 'patient', 'medicine', 'hospital', 'health', 'care'],
    ]

    print("\nTraining Word2Vec with different window sizes...")
    print(f"Training sentences: {len(training_sentences)}")

    # Train models with different window sizes
    window_sizes = [2, 5, 10]
    models = {}

    for window in window_sizes:
        print(f"\n{'='*40}")
        print(f"Window Size: {window}")
        print("="*40)

        model = Word2Vec(
            sentences=training_sentences,
            vector_size=50,
            window=window,
            min_count=1,
            workers=1,
            epochs=100,
            seed=42
        )
        models[window] = model

        # Show word relationships for this window size
        print("\nMost similar words to 'doctor':")
        try:
            similar = model.wv.most_similar('doctor', topn=5)
            for word, score in similar:
                print(f"  {word}: {score:.4f}")
        except KeyError:
            print("  'doctor' not in vocabulary")

        print("\nMost similar words to 'patient':")
        try:
            similar = model.wv.most_similar('patient', topn=5)
            for word, score in similar:
                print(f"  {word}: {score:.4f}")
        except KeyError:
            print("  'patient' not in vocabulary")

    # Compare specific relationships across window sizes
    print("\n" + "="*60)
    print("Comparison: doctor-patient similarity across window sizes")
    print("="*60)

    for window in window_sizes:
        model = models[window]
        try:
            sim = model.wv.similarity('doctor', 'patient')
            print(f"  Window {window}: similarity = {sim:.4f}")
        except KeyError as e:
            print(f"  Window {window}: Error - {e}")

    print("\n" + "-"*40)
    print("Comparison: doctor-hospital similarity across window sizes")
    print("-"*40)

    for window in window_sizes:
        model = models[window]
        try:
            sim = model.wv.similarity('doctor', 'hospital')
            print(f"  Window {window}: similarity = {sim:.4f}")
        except KeyError as e:
            print(f"  Window {window}: Error - {e}")

    # Discussion
    print("\n" + "-"*40)
    print("Discussion: How Window Size Affects Relationships")
    print("-"*40)
    print("""
    SMALL WINDOW (2):
    - Looks at immediate neighbors only
    - Captures SYNTACTIC relationships (grammar)
    - "the doctor" - "the" and "doctor" are close
    - Words that REPLACE each other are similar
    - Example: "doctor" similar to "nurse" (both can be "the ___")

    MEDIUM WINDOW (5):
    - Balanced view
    - Captures both syntax and some semantics
    - Good default for most applications

    LARGE WINDOW (10):
    - Looks at entire sentence context
    - Captures SEMANTIC relationships (meaning/topic)
    - "doctor" similar to "hospital" (same topic)
    - Words in same DOMAIN are similar
    - Example: "doctor", "patient", "medicine", "hospital" all similar

    WHICH IS BEST?

    Use SMALL window (2-3) when you need:
    - Word substitution (find synonyms)
    - Grammar analysis
    - Similar word forms

    Use LARGE window (5-10) when you need:
    - Topic modeling
    - Document similarity
    - Semantic search

    RECOMMENDATION:
    - For general NLP: window=5 is a good balance
    - For semantic similarity: window=10
    - For syntactic patterns: window=2

    NOTE: Our training data is small, so results may vary.
    Real models train on millions of sentences!
    """)


# =============================================================================
# Exercise 10: Document Clustering with Word2Vec + NLTK Preprocessing
# =============================================================================
# Example texts:
# Text A: "Deep learning improves image recognition accuracy."
# Text B: "Stock predictions rely on time-series analysis."
# Text C: "Language models are used in machine translation."
# Task:
# 1. Preprocess all texts (tokenization, stopword removal, lemmatization).
# 2. Generate sentence embeddings using Word2Vec average vectors.
# 3. Cluster the texts using K-Means (2 or 3 clusters).
# 4. Discuss which documents fall together and why.
# =============================================================================

def exercise_10():
    """
    Document Clustering with Word2Vec + NLTK Preprocessing

    KEY CONCEPTS:
    - Document embedding: Represent a document as a single vector
    - Clustering: Grouping similar documents together
    - K-Means: Algorithm that finds K groups in data
    """
    print("\n" + "="*60)
    print("Exercise 10: Document Clustering with Word2Vec")
    print("="*60)

    # Our documents
    documents = {
        'A': "Deep learning improves image recognition accuracy.",
        'B': "Stock predictions rely on time-series analysis.",
        'C': "Language models are used in machine translation.",
    }

    print("\nDocuments:")
    for doc_id, text in documents.items():
        print(f"  {doc_id}: {text}")

    # Step 1: Preprocess all texts
    print("\n" + "-"*40)
    print("Step 1: Preprocessing (tokenize, remove stopwords, lemmatize)")
    print("-"*40)

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    def get_wordnet_pos(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def preprocess(text):
        """Full preprocessing pipeline"""
        # Tokenize
        tokens = word_tokenize(text.lower())
        # Remove punctuation and stopwords
        tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
        # POS tag and lemmatize
        pos_tags = pos_tag(tokens)
        lemmas = []
        for word, tag in pos_tags:
            wn_pos = get_wordnet_pos(tag)
            lemma = lemmatizer.lemmatize(word, pos=wn_pos)
            lemmas.append(lemma)
        return lemmas

    preprocessed_docs = {}
    for doc_id, text in documents.items():
        lemmas = preprocess(text)
        preprocessed_docs[doc_id] = lemmas
        print(f"  {doc_id}: {lemmas}")

    # Step 2: Train Word2Vec and create document embeddings
    print("\n" + "-"*40)
    print("Step 2: Creating Word2Vec Model and Document Embeddings")
    print("-"*40)

    # Training data - we need vocabulary that covers our documents
    training_sentences = [
        ['deep', 'learning', 'machine', 'learning', 'ai', 'neural', 'network'],
        ['image', 'recognition', 'computer', 'vision', 'accuracy'],
        ['stock', 'market', 'prediction', 'financial', 'analysis'],
        ['time', 'series', 'analysis', 'data', 'pattern'],
        ['language', 'model', 'nlp', 'text', 'translation'],
        ['machine', 'translation', 'language', 'processing'],
        ['deep', 'learning', 'improve', 'accuracy', 'model'],
        ['predict', 'stock', 'rely', 'analysis', 'data'],
        ['translation', 'use', 'language', 'model', 'text'],
        ['recognition', 'image', 'deep', 'learning', 'neural'],
    ]

    # Add our preprocessed documents to training
    for doc_id, lemmas in preprocessed_docs.items():
        training_sentences.append(lemmas)

    model = Word2Vec(
        sentences=training_sentences,
        vector_size=50,
        window=5,
        min_count=1,
        workers=1,
        epochs=100,
        seed=42
    )

    print(f"Vocabulary size: {len(model.wv.key_to_index)}")

    # Create document embeddings (average of word vectors)
    def get_doc_embedding(lemmas, model):
        """Create document embedding as average of word vectors"""
        vectors = []
        for word in lemmas:
            if word in model.wv:
                vectors.append(model.wv[word])
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(model.vector_size)

    doc_embeddings = {}
    for doc_id, lemmas in preprocessed_docs.items():
        embedding = get_doc_embedding(lemmas, model)
        doc_embeddings[doc_id] = embedding
        print(f"  {doc_id}: embedding shape = {embedding.shape}")

    # Step 3: Cluster using K-Means
    print("\n" + "-"*40)
    print("Step 3: K-Means Clustering")
    print("-"*40)

    # Prepare data for clustering
    doc_ids = list(doc_embeddings.keys())
    X = np.array([doc_embeddings[doc_id] for doc_id in doc_ids])

    # Try with 2 clusters (since we have 3 documents)
    print("\nClustering with K=2:")
    kmeans_2 = KMeans(n_clusters=2, random_state=42, n_init=10)
    labels_2 = kmeans_2.fit_predict(X)

    for doc_id, label in zip(doc_ids, labels_2):
        print(f"  Document {doc_id}: Cluster {label}")

    # Show cluster groupings
    print("\nCluster groupings (K=2):")
    for cluster in range(2):
        docs_in_cluster = [doc_id for doc_id, label in zip(doc_ids, labels_2) if label == cluster]
        print(f"  Cluster {cluster}: {docs_in_cluster}")

    # Also compute similarities between documents
    print("\n" + "-"*40)
    print("Document Similarities (Cosine)")
    print("-"*40)

    for i, doc1 in enumerate(doc_ids):
        for j, doc2 in enumerate(doc_ids):
            if i < j:
                sim = cosine_similarity(
                    doc_embeddings[doc1].reshape(1, -1),
                    doc_embeddings[doc2].reshape(1, -1)
                )[0][0]
                print(f"  {doc1} <-> {doc2}: {sim:.4f}")

    # Discussion
    print("\n" + "-"*40)
    print("Discussion: Why Documents Cluster Together")
    print("-"*40)
    print("""
    EXPECTED GROUPINGS:

    Documents A and C might cluster together because:
    - Both are about AI/ML topics
    - "Deep learning" and "Language models" are related
    - Both involve "learning" or "models"

    Document B might be separate because:
    - It's about finance/stock market
    - Different domain vocabulary
    - "Stock", "predictions", "time-series" are distinct

    THE CLUSTERING PROCESS:

    1. PREPROCESSING: Clean and normalize text
       - Remove noise (punctuation, stopwords)
       - Lemmatize for consistency

    2. EMBEDDING: Convert words to vectors
       - Each word becomes a point in space
       - Average them for document vector

    3. CLUSTERING: Group similar vectors
       - K-Means finds centers of clusters
       - Each document goes to nearest center

    REAL-WORLD APPLICATIONS:
    - News article categorization
    - Customer feedback grouping
    - Research paper organization
    - Email/spam classification

    LIMITATIONS OF THIS EXAMPLE:
    - Only 3 documents (very small)
    - Limited training data
    - Real systems use pre-trained embeddings

    IMPROVEMENT SUGGESTIONS:
    - Use more documents
    - Use pre-trained Word2Vec (Google News)
    - Try other embeddings (BERT, Doc2Vec)
    - Use TF-IDF weighting for word importance
    """)


# =============================================================================
# INTERACTIVE MENU
# =============================================================================

def show_menu():
    """Display the exercise menu"""
    print("\n" + "="*60)
    print("   NLTK + Word2Vec Exercises Menu")
    print("="*60)
    print("""
    1. Lemmatization with POS Awareness
    2. Lemmatization Comparison Across Languages
    3. Domain-Specific Lemmatization
    4. Frequency Distribution After Lemmatization
    5. Word Similarity Using Word2Vec Embeddings
    6. Finding Analogies with Word2Vec
    7. Sentence Semantic Similarity
    8. POS and Lemmatization-Based Keyword Extraction
    9. Context Window Analysis with Word2Vec
   10. Document Clustering with Word2Vec + NLTK

    0. Exit
    """)


def main():
    """Main function with interactive menu"""
    # Dictionary mapping choices to functions
    exercises = {
        '1': exercise_1,
        '2': exercise_2,
        '3': exercise_3,
        '4': exercise_4,
        '5': exercise_5,
        '6': exercise_6,
        '7': exercise_7,
        '8': exercise_8,
        '9': exercise_9,
        '10': exercise_10,
    }

    while True:
        show_menu()
        choice = input("Enter exercise number (0 to exit): ").strip()

        if choice == '0':
            print("\nGoodbye! Happy learning!")
            break
        elif choice in exercises:
            try:
                exercises[choice]()
            except Exception as e:
                print(f"\nError running exercise: {e}")
                print("Make sure all required packages are installed:")
                print("  pip install nltk gensim scikit-learn numpy")
                print("\nAnd download NLTK data:")
                print("  import nltk")
                print("  nltk.download('punkt')")
                print("  nltk.download('averaged_perceptron_tagger')")
                print("  nltk.download('wordnet')")
                print("  nltk.download('stopwords')")

            input("\nPress Enter to continue...")
        else:
            print("\nInvalid choice. Please enter a number between 0 and 10.")


if __name__ == "__main__":
    main()
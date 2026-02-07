from nltk.tokenize import word_tokenize
import nltk
import os

# Create a local directory for NLTK data and add it to the path
local_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'nltk_data')
nltk.data.path.append(local_data_dir)

# Download required resources to the local directory
nltk.download('punkt', download_dir=local_data_dir, quiet=True)
nltk.download('punkt_tab', download_dir=local_data_dir, quiet=True)

text = "Don't stop believing! It's amazing."

print("split():", text.split())
print("word_tokenize():", word_tokenize(text))
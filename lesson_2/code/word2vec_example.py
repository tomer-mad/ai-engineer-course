import gensim.downloader as api
import os

# Set the download directory for gensim models to a local folder
local_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'gensim-data')
os.environ['GENSIM_DATA_DIR'] = local_data_dir

# this is a one‑time download + cache
model = api.load("glove-wiki-gigaword-50")

print("king ~ queen:", model.similarity("king", "queen"))
print("paris + germany - france →",
      [w for w,_ in model.most_similar(
          positive=["paris","germany"],
          negative=["france"],
          topn=10)])
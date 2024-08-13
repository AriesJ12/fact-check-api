# This is currently broken, do not run; please read the README.md for instructions on how to download the model
import os
from transformers import AutoModel

# Set the cache directory
cache_dir = 'nli'
os.environ['TRANSFORMERS_CACHE'] = cache_dir

model_name = 'ctu-aic/xlm-roberta-large-squad2-ctkfacts_nli'
model_path = os.path.join(cache_dir, 'pytorch_model.bin')

# Check if the model is already downloaded
if os.path.exists(model_path):
    print("Model already downloaded.")
else:
    print("Downloading model...")
    # Download the model
    model = AutoModel.from_pretrained(model_name)
    # Save the model to the cache directory
    model.save_pretrained(cache_dir)
    print("Model downloaded to", model_path)
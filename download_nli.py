import os
from transformers import AutoModel
import torch

# Set the cache directory
cache_dir = 'nli'
os.environ['TRANSFORMERS_CACHE'] = cache_dir

model_name = 'ctu-aic/xlm-roberta-large-squad2-ctkfacts_nli'
model_path = os.path.join(cache_dir, model_name)

# Check if the model is already downloaded
if os.path.exists(model_path) and os.path.isfile(os.path.join(model_path, 'pytorch_model.bin')):
    print("Model already downloaded.")
else:
    print("Downloading model...")
    # Download the model
    model = AutoModel.from_pretrained(model_name)
    print("Model downloaded to", model_path)
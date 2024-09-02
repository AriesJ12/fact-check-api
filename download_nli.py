import os
import requests

# Set the cache directory
cache_dir = 'nli'
os.makedirs(cache_dir, exist_ok=True)

model_url = 'https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7/resolve/main/model.safetensors'
model_path = os.path.join(cache_dir, 'model.safetensors')

# Check if the model is already downloaded
if os.path.exists(model_path):
    print("Model already downloaded.")
else:
    print("Downloading model...")
    # Download the model
    response = requests.get(model_url)
    response.raise_for_status()  # Ensure we notice bad responses
    with open(model_path, 'wb') as f:
        f.write(response.content)
    print("Model downloaded to", model_path)
"""
Spins up a Flask server that can do inference using the sentence transformers.

Definitely not the final product, just for demo purposes

How to use it (from the notebook context for example):
```python
import requests
from hansken.util import Vector

query_vector = Vector.from_base64(
    requests.get('http://localhost:9092/', params={'model': 'all-MiniLM-L6-v2', 'sentence': 'Test sentence'}).text
)
```
"""
from flask import Flask, request
from sentence_transformers import SentenceTransformer
from hansken.util import Vector

app = Flask(__name__)
models = {model_name: SentenceTransformer(model_name) 
          for model_name in ['all-MiniLM-L6-v2', 'clip-ViT-B-32']}


@app.route("/")
def inference():
    model = models[request.args.get('model')]
    sentence = request.args.get('sentence')
    return str(Vector.from_sequence(model.encode(str(sentence))))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9092)

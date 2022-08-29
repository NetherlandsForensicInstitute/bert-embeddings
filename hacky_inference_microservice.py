"""
Spins up a Flask server that can do inference using the sentence transformers.

Definitely not the final product, just for demo purposes
"""
from flask import Flask
from hansken.util import Vector

app = Flask(__name__)
models = {model_name: SentenceTransformer(model_name) 
          for model_name in ['all-MiniLM-L6-v2', 'clip-ViT-B-32']}

@app.route("/")
def inference():
    model = request.args.get('model')
    sentence = request.args.get('sentence')
    return str(Vector.from_sequence(model.encode(sentence)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9092)

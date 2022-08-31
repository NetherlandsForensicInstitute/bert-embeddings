# BERT embeddings

This repository contains some code that wraps the [`sentence_transformers` PyPI package](https://pypi.org/project/sentence-transformers/).
This is [a Hansken extraction plugin, read the docs for the SDK here](https://netherlandsforensicinstitute.github.io/hansken-extraction-plugin-sdk-documentation/latest/).
It can apply any of the available sentence transformers on the `chatMessage.message` field.

The plugin can be adapted to use different models, but it can also run on different fields of course; just change the matcher and the getter.

Note that it is recommended to always check a model's *model card* or README before actually using it.

The `.sb`-files are [Starboard Notebook](https://github.com/gzuidhof/starboard-notebook) files.
These files can be imported in the Code Notebooks that are included in the Expert UI of Hansken.
The notebooks are an example of how you can sort all chat messages in a case based on their similarity using [hansken.py](https://pypi.org/project/hansken).

## Building and running it
To run it, pull the latest copy to the place where Hansken is looking for plugins:

```bash
docker pull ghcr.io/netherlandsforensicinstitute/bert-embeddings:latest
```

Or clone (and modify) this repository and build your own copy using
```bash
git clone https://github.com/netherlandsforensicinstitute/bert-embeddings
cd bert-embeddings
docker build -t bert-embeddings .
```

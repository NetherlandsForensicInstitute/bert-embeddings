FROM python:3.8

# TODO See API breaking changes in 0.6.0
# TODO Unpin the SDK
RUN python -m pip install --no-cache hansken_extraction_plugin==0.5.0 sentence-transformers

LABEL maintainer="i.ellis@nfi.nl"
LABEL hansken.extraction.plugin.image="bert-embeddings"
LABEL hansken.extraction.plugin.name="BERTEmbeddings"
ENV SENTENCE_TRANSFORMERS_HOME="/tmp/"
COPY . /app
EXPOSE 8999
WORKDIR /app
RUN python bert_embeddings.py  # run the Python file once to cache the required models
ENTRYPOINT ["/usr/local/bin/serve_plugin"]
CMD ["bert_embeddings.py", "8999"]

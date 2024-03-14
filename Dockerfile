FROM python:3.10

RUN python -m pip install --no-cache hansken_extraction_plugin==0.7.2 sentence-transformers

LABEL maintainer="i.ellis@nfi.nl"
LABEL hansken.extraction.plugin.image="bert-embeddings"
LABEL hansken.extraction.plugin.name="BERTEmbeddings"
ENV SENTENCE_TRANSFORMERS_HOME="/tmp/"
COPY . /app
EXPOSE 8999
WORKDIR /app
RUN python bert_embeddings.py  # run the Python file once to cache the required models
RUN chmod -R 777 /tmp  # temporary, see why the cache dir can't be written to
ENTRYPOINT ["/usr/local/bin/serve_plugin", "-vvv"]
CMD ["bert_embeddings.py", "8999"]

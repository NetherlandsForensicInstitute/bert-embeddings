from hansken.util import Vector
from hansken_extraction_plugin.api.extraction_plugin import MetaExtractionPlugin
from hansken_extraction_plugin.api.plugin_info import Author, MaturityLevel, PluginInfo, PluginId, PluginResources
from hansken_extraction_plugin.api.tracelet import Tracelet
from hansken_extraction_plugin.runtime.extraction_plugin_runner import run_with_hanskenpy
from logbook import Logger
from sentence_transformers import SentenceTransformer

log = Logger(__name__)
MODEL_NAMES = ['all-MiniLM-L6-v2', 'clip-ViT-B-32']
models = [SentenceTransformer(model_name) for model_name in MODEL_NAMES]


def to_tracelet(embedding, model_name):
    return Tracelet('prediction', {
        'prediction.type': 'sentence-transformer',
        'prediction.modelName': model_name,
        'prediction.embedding': Vector.from_sequence(embedding)
    })


class BERTEmbeddings(MetaExtractionPlugin):

    def plugin_info(self):
        plugin_info = PluginInfo(
            id=PluginId(domain='nfi.nl', category='media', name='BERT'),
            version='2022.12.13',
            description='BERT embeddings for chatmessages',
            author=Author('Isadora Ellis', 'i.ellis@nfi.nl', 'NFI'),
            maturity=MaturityLevel.PROOF_OF_CONCEPT,
            webpage_url='https://git.eminjenv.nl/-/ide/project/hanskaton/extraction-plugins/bert-embeddings',
            matcher='type=chatMessage',
            license="Apache License 2.0",
            resources=PluginResources(maximum_cpu=1, maximum_memory=12000),
        )
        log.debug(f'returning plugin info: {plugin_info}')
        return plugin_info

    def process(self, trace):
        """

        :param trace: expected to be a chatMessage
        """

        log.info(f"processing trace {trace.get('name')}")
        # TODO Maybe use the text stream for e-mails (interesting if they are not plain text but HTML)
        # TODO Maybe add textMessage.message (mobile text message) and email via data stream
        chatmessage = trace.get('chatMessage.message', None)
        if chatmessage:
            for model, model_name in zip(models, MODEL_NAMES):
                embedding = model.encode(chatmessage, batch_size=1)
                log.info(str(embedding))
                trace.add_tracelet(to_tracelet(embedding, model_name))


if __name__ == "__main__":
    run_with_hanskenpy(BERTEmbeddings, endpoint='http://localhost:9091/gatekeeper/',
                       # the keystore REST endpoint when this script was exported, note that
                       # this can be overridden with --keystore
                       keystore='http://localhost:9090/keystore/',
                       # the project id of the project named "Semantic search",
                       project='326c693c-45bc-4648-b8e3-24abb4f43c1d')

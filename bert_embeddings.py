from hansken.util import Vector
from hansken_extraction_plugin.api.extraction_plugin import MetaExtractionPlugin
from hansken_extraction_plugin.api.plugin_info import Author, MaturityLevel, PluginInfo, PluginId, PluginResources
from hansken_extraction_plugin.api.tracelet import Tracelet
from hansken_extraction_plugin.runtime.extraction_plugin_runner import run_with_hanskenpy
from logbook import Logger
from sentence_transformers import SentenceTransformer

log = Logger(__name__)
MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_NAME)


def to_tracelet(embedding):
    return Tracelet('prediction', {
        'prediction.type': 'bert-embedding',
        'prediction.modelName': f'BERT+{MODEL_NAME}',
        'prediction.embedding': Vector.from_sequence(embedding)
    })


class BERTEmbeddings(MetaExtractionPlugin):

    def plugin_info(self):
        plugin_info = PluginInfo(
            self,
            id=PluginId(domain='nfi.nl', category='media', name='BERT'),
            version='2022.8.15',
            description='BERT embeddings for chatmessages',
            author=Author('Isadora Ellis', 'i.ellis@nfi.nl', 'NFI'),
            maturity=MaturityLevel.PROOF_OF_CONCEPT,
            webpage_url='https://git.eminjenv.nl/-/ide/project/hanskaton/extraction-plugins/bert-embeddings',
            matcher='type=chatMessage',
            license="Apache License 2.0",
            resources=PluginResources.builder().maximum_cpu(1).maximum_memory(2048).build(),
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
            embedding = model.encode(chatmessage, batch_size=1)
            log.info(str(embedding))
            trace.add_tracelet(to_tracelet(embedding))



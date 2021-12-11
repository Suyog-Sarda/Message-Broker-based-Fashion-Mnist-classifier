import importlib
import json


class ImageClassificationClient:
    _default_config = {
        "connector_class_module": "image_classification.client.connectors.kafka_connector",
        "connector_class": "KafkaConnector",
        "bootstrap_brokers": "localhost:9092"
    }

    def __init__(self, config_file=None):
        if config_file:
            with open(config_file) as json_file:
                config = json.load(json_file)
        else:
            config = ImageClassificationClient._default_config
        module = importlib.import_module(config["connector_class_module"])
        clazz = getattr(module, config["connector_class"])
        self._connector = clazz(config)

    def send_message(self, request, topic):
        self._connector.send_message(request, topic)

    def subscribe(self, topic_name, message_processor):
        return self._connector.subscribe(topic_name, message_processor)

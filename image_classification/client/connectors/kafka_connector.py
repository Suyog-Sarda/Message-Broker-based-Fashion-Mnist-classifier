from threading import Thread, Event

from kafka import KafkaProducer, KafkaConsumer

from image_classification.client.messages.image_classification_request import ImageClassificationRequest
from image_classification.client.messages.image_classification_response import ImageClassificationResponse
from image_classification.client.topics import REQUEST_TOPIC_NAME, RESPONSE_TOPIC_NAME


class Consumer(Thread):
    def __init__(self, bootstrap_brokers, topic, message_processor, **kwargs):
        super(Consumer, self).__init__()
        self.kwargs = kwargs
        self.topic = topic
        self.message_processor = message_processor
        self.stop_event = Event()
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_brokers,
            auto_offset_reset='earliest'
        )
        self.consumer.subscribe([self.topic])

    def run(self):
        while not self.stop_event.is_set():
            for message in self.consumer:
                if self.stop_event.is_set():
                    break
                message_payload = None
                # TODO: Need a better way to identify payload type.
                if message.topic == REQUEST_TOPIC_NAME:
                    message_payload = ImageClassificationRequest.from_bytes(message.value)
                elif message.topic == RESPONSE_TOPIC_NAME:
                    message_payload = ImageClassificationResponse.from_bytes(message.value)
                if message_payload:
                    self.message_processor.process_message(message_payload)
        self.consumer.close()

    def stop(self):
        self.stop_event.set()


class KafkaConnector:
    def __init__(self, config: dict):
        self.bootstrap_brokers = config.get("bootstrap_brokers", "localhost:9092")
        self._producer = None
        try:
            self._producer = KafkaProducer(bootstrap_servers=[self.bootstrap_brokers], api_version=(0, 10))
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
            raise ex

    def send_message(self, message, topic_name):
        key_bytes = message.key_bytes()
        value_bytes = message.to_bytes()
        self._producer.send(topic_name, key=key_bytes, value=value_bytes)
        self._producer.flush()
        print('Message published successfully.')

    def subscribe(self, topic_name, message_processor):
        return Consumer(self.bootstrap_brokers, topic_name, message_processor)

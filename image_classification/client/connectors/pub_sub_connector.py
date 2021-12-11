import uuid

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message

from image_classification.client.topics import REQUEST_TOPIC_NAME, RESPONSE_TOPIC_NAME
from image_classification.client.messages.image_classification_request import ImageClassificationRequest
from image_classification.client.messages.image_classification_response import ImageClassificationResponse


class PubSubConnector:
    def __init__(self, config: dict):
        self.project_id = config["project_id"]
        self.publisher = pubsub_v1.PublisherClient()

    def send_message(self, message, topic_name):
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        value_bytes = message.to_bytes()
        self.publisher.publish(topic_path, value_bytes).result()

    def subscribe(self, topic_name, message_processor):
        return Consumer(self.project_id, topic_name, message_processor)


class Consumer:
    def __init__(self, project_id, topic, message_processor):
        def callback(message: Message) -> None:
            message_payload = None
            if self.topic == REQUEST_TOPIC_NAME:
                message_payload = ImageClassificationRequest.from_bytes(message.data)
            elif self.topic == RESPONSE_TOPIC_NAME:
                message_payload = ImageClassificationResponse.from_bytes(message.data)
            if message_payload:
                self.message_processor.process_message(message_payload)
            message.ack()

        self.project_id = project_id
        self.subscription_id = str(uuid.uuid4())
        self.topic = topic
        self.message_processor = message_processor
        self.subscriber = pubsub_v1.SubscriberClient()
        sub_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)
        topic_path = self.subscriber.topic_path(self.project_id, self.topic)
        self.subscriber.create_subscription(request={"name": sub_path, "topic": topic_path})
        self.subs_future = self.subscriber.subscribe(sub_path, callback)

    def stop(self):
        self.subscriber.close()

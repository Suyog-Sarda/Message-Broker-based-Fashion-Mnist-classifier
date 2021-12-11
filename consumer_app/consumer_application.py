
from image_classification.client.image_classification_client import ImageClassificationClient
from image_classification.client.topics import RESPONSE_TOPIC_NAME


class ConsumerApp:
    def __init__(self):
        self.client = ImageClassificationClient()
        self.subscription = self.client.subscribe(RESPONSE_TOPIC_NAME, self)

    @staticmethod
    def process_message(response_message):
        print(response_message.results)

    def stop(self):
        self.subscription.stop()


if __name__ == '__main__':
    consumer = ConsumerApp()
    consumer.subscription.run()
    user_response = input('Do you want to stop this service? ')
    if user_response.lower() == 'yes':
        consumer.subscription.stop()
        consumer.stop()

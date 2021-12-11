import uuid

from image_classification.client.image_classification_client import ImageClassificationClient
from image_classification.client.messages.image_classification_request import ImageClassificationRequest
from image_classification.client.topics import REQUEST_TOPIC_NAME

if __name__ == '__main__':
    keep_running = True
    while keep_running:
        user_input = input('Do you want to predict on another batch of images? ')
        if user_input.lower() == 'yes':
            folder_path = input('Please enter the path of the folder containing images: ')
            request_id = str(uuid.uuid4())
            request = ImageClassificationRequest(request_id, folder_path)
            client = ImageClassificationClient()
            client.send_message(request, REQUEST_TOPIC_NAME)
        else:
            keep_running = False

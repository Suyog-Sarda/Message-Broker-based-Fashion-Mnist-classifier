from image_classification.client.image_classification_client import ImageClassificationClient
from image_classification.client.messages.image_classification_response import ImageClassificationResponse
from image_classification.client.topics import REQUEST_TOPIC_NAME, RESPONSE_TOPIC_NAME

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os


# load and prepare the image
def load_image(filename):
    # load the image
    img = load_img(filename, grayscale=True, target_size=(28, 28))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 1 channel
    img = img.reshape(1, 28, 28, 1)
    # prepare pixel data
    img = img.astype('float32')
    img = img / 255.0
    return img


class ModelRunner:
    def __init__(self):
        self.client = ImageClassificationClient()
        self.subscription = self.client.subscribe(REQUEST_TOPIC_NAME, self)

    def process_message(self, request_message):
        print(f"Received message: folder_path - {request_message.folder_path} request_id - {request_message.request_id}")
        try:
            model = load_model('D:/PycharmProjects/Vector_project/CNN/final_model.h5')
            results = dict()
            for img_name in os.listdir(request_message.folder_path):
                image = load_image(request_message.folder_path+'/'+img_name)
                result = model.predict(image)
                pred_class = int(np.argmax(result))
                results[img_name] = pred_class
            response = ImageClassificationResponse(request_message.request_id, results)
            self.client.send_message(response, RESPONSE_TOPIC_NAME)
        except Exception as ex:
            print(ex)

    def stop(self):
        self.subscription.stop()


if __name__ == '__main__':
    predictor = ModelRunner()
    predictor.subscription.run()
    user_response = input('Do you want to stop this service? ')
    if user_response.lower() == 'yes':
        predictor.stop()

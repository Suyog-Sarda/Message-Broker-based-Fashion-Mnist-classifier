Pre-requisites

Install the following:

1. Zooker
2. Kafka Python
3. Google cloud pubsub
4. Java 1.8
5. Python 3.9
6. Numpy
7. Matplotlib
8. Scikit Learn
9. Tensorflow
10. Keras

PLEASE NOTE: THE END TO END PIPELINE OF THE KAFKA BROKER IS TESTED AND WORKS PERFECTLY. GOOGLE PUB SUB IS NOT TESTED YET. YOU CAN GIVE A CONFIG JSON FILE PATH AS AN INPUT PARAMETER TO ImageClassificationClient IN LINE 14 OF client_app/classification_application.py

Launch the following processes:

1. Run Zookeeper : bin/zookeeper-server-start.sh config/zookeeper.properties
2. Run Kafka : bin/kafka-server-start.sh config/server.properties
3. Run client_app/classification_application.py --- Used for reading the images folder_path via command line for predicting the class each image belongs to and publishing it to the 'classification_request' topic
4.      --- Give the image folder path as input
5. Run image_classification/model/model_runner.py --- Used for subscribing to the 'classification_request' topic and predicting the class of each image in the folder and publishing the result to 'classification_response' topic
6. Run consumer_app/consumer_application.py --- Used for subscribing to the 'classification_response' topic and printing the results to the console
7.      --- The image classification predictions will be printed here


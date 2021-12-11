from numpy import mean, std
from matplotlib import pyplot
from sklearn.model_selection import KFold
from keras.datasets import fashion_mnist
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.optimizers import SGD


# load train and test dataset
def load_dataset():
    # load dataset
    (train_x, train_y), (test_x, test_y) = fashion_mnist.load_data()
    # reshape dataset to have a single channel
    train_x = train_x.reshape((train_x.shape[0], 28, 28, 1))
    test_x = test_x.reshape((test_x.shape[0], 28, 28, 1))
    # one hot encode target values
    train_y = to_categorical(train_y)
    test_y = to_categorical(test_y)
    return train_x, train_y, test_x, test_y


# scale pixels
def prep_pixels(train, test):
    # convert from integers to floats
    train_norm = train.astype('float32')
    test_norm = test.astype('float32')
    # normalize to range 0-1
    train_norm = train_norm / 255.0
    test_norm = test_norm / 255.0
    # return normalized images
    return train_norm, test_norm


# define cnn model
def define_model():
    model = Sequential()
    model.add(
        Conv2D(64, (3, 3), padding='same', activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(10, activation='softmax'))
    # compile model
    opt = SGD(learning_rate=0.01, momentum=0.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# evaluate a model using k-fold cross-validation
def evaluate_model(data_x, data_y, n_folds=5):
    scores, histories = list(), list()
    # prepare cross validation
    kfold = KFold(n_folds, shuffle=True, random_state=1)
    # enumerate splits
    for train_ix, test_ix in kfold.split(data_x):
        # define model
        model = define_model()
        # select rows for train and test
        train_x, train_y, test_x, test_y = data_x[train_ix], data_y[train_ix], data_x[test_ix], data_y[test_ix]
        # fit model
        history = model.fit(train_x, train_y, epochs=10, batch_size=32, validation_data=(test_x, test_y), verbose=0)
        # evaluate model
        _, acc = model.evaluate(test_x, test_y, verbose=0)
        print('> %.3f' % (acc * 100.0))
        # append scores
        scores.append(acc)
        histories.append(history)
    return scores, histories


# plot diagnostic learning curves
def summarize_diagnostics(histories):
    for i in range(len(histories)):
        # plot loss
        pyplot.subplot(211)
        pyplot.title('Cross Entropy Loss')
        pyplot.plot(histories[i].history['loss'], color='blue', label='train')
        pyplot.plot(histories[i].history['val_loss'], color='orange', label='test')
        # plot accuracy
        pyplot.subplot(212)
        pyplot.title('Classification Accuracy')
        pyplot.plot(histories[i].history['accuracy'], color='blue', label='train')
        pyplot.plot(histories[i].history['val_accuracy'], color='orange', label='test')
    pyplot.show()


# summarize model performance
def summarize_performance(scores):
    # print summary
    print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(scores) * 100, std(scores) * 100, len(scores)))
    # box and whisker plots of results
    pyplot.boxplot(scores)
    pyplot.show()


# run the test harness for evaluating a model
def run_test_harness():
    # load dataset
    train_x, train_y, test_x, test_y = load_dataset()
    # prepare pixel data
    train_x, test_x = prep_pixels(train_x, test_x)
    # evaluate model
    scores, histories = evaluate_model(train_x, train_y)
    # learning curves
    summarize_diagnostics(histories)
    # summarize estimated performance
    summarize_performance(scores)
    # define model
    model = define_model()
    # fit model
    model.fit(train_x, train_y, epochs=10, batch_size=32, verbose=0)
    # evaluate model on test dataset
    _, acc = model.evaluate(test_x, test_y, verbose=0)
    print('> %.3f' % (acc * 100.0))
    # save model
    model.save('final_model.h5')


if __name__ == '__main__':
    # entry point, run the test harness
    run_test_harness()

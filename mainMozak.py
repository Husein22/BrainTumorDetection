import cv2
import os
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import normalize, to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dropout, Flatten, Dense, Activation

class TumorDetector:
    def __init__(self, dataset_path, image_size=64):
        self.dataset_path = dataset_path
        self.image_size = image_size
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=(self.image_size, self.image_size, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(32, (3, 3), kernel_initializer='he_uniform'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(64, (3, 3), kernel_initializer='he_uniform'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2))
        model.add(Activation('softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def load_images(self, folder):
        images = []
        labels = []
        image_list = os.listdir(os.path.join(self.dataset_path, folder))

        for i, image_name in enumerate(image_list):
            if image_name.split('.')[1] == 'jpg':
                image_path = os.path.join(self.dataset_path, folder, image_name)
                image = cv2.imread(image_path)
                image = Image.fromarray(image, 'RGB')
                image = image.resize((self.image_size, self.image_size))
                images.append(np.array(image))
                labels.append(1 if folder == 'yes' else 0)

        return images, labels

    def load_dataset(self):
        no_tumor_images, no_tumor_labels = self.load_images('no')
        yes_tumor_images, yes_tumor_labels = self.load_images('yes')

        dataset = np.array(no_tumor_images + yes_tumor_images)
        labels = np.array(no_tumor_labels + yes_tumor_labels)

        return dataset, labels

    def preprocess_data(self, dataset, labels):
        normalized_dataset = normalize(dataset, axis=1)
        categorical_labels = to_categorical(labels, num_classes=2)

        return normalized_dataset, categorical_labels

    def train_model(self, x_train, y_train, batch_size=16, epochs=10, validation_data=None, shuffle=False):
        self.model.fit(x_train, y_train, batch_size=batch_size, verbose=1, epochs=epochs, validation_data=validation_data, shuffle=shuffle)

    def save_model(self, model_path):
        self.model.save(model_path)

if __name__ == "__main__":
    tumor_detector = TumorDetector(dataset_path="datasets/")
    dataset, labels = tumor_detector.load_dataset()
    normalized_dataset, categorical_labels = tumor_detector.preprocess_data(dataset, labels)

    x_train, x_test, y_train, y_test = train_test_split(normalized_dataset, categorical_labels, test_size=0.2, random_state=0)

    tumor_detector.train_model(x_train, y_train, epochs=10, validation_data=(x_train, y_train), shuffle=False)
    tumor_detector.save_model("TumorMozga10EpochsCategorical.h5")




import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense

class SimpleMLP:
    @staticmethod
    def build(shape, classes):
        return Sequential([
            Dense(32, activation='relu', input_shape=(shape,)),
            Dense(1, activation='sigmoid')   
        ])
        
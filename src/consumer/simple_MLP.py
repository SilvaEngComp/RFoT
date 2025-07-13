import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from sklearn.ensemble import AdaBoostClassifier


class SimpleMLP:
    @staticmethod
    def build(shape):
        return Sequential([
            Dense(32, activation='relu', input_shape=(shape,)),
            Dense(1, activation='sigmoid')   
        ])

class SimpleMLP2:
    @staticmethod
    def build(shape):
        return AdaBoostClassifier(n_estimators=100, algorithm="SAMME", random_state=0)

# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 12:55:35 2021

@author: silva
"""
import numpy as np

def activation(s,t=0.5):
    if s>t:
        return 1
    return 0

def calc_weight(w, train, b):
    for i in np.arange(w.shape[0]):
        b += w[i]*train[i]
    return b

def fit(train,t,epochs, eta):
    b=0
    train_cols = train.shape[1]-1
    w = np.zeros(train_cols)
    for i in range(epochs):
        for j in np.arange(train.shape[0]):    
            s = calc_weight(w,train[j,0:train_cols], b)
            y = activation(s,t)
            label = train[j,train_cols]
            if(y != label):
                w = w + eta*(label - y)*train[j,0:train_cols]
                b = b + eta*(label - y)
    return np.array([w,b])

def predict(test, model):
        y = calc_weight(model[0], test, model[1])
        return activation(y)
        

def createModelFactory(train):
	train, test = read_data()
	model = fit(train, 0.5, 100, 0.1)
	return model
	





























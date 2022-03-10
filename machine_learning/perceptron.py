from tensorflow.keras.optimizers import SGD
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from numpy.lib import shape_base


from keras.layers import Activation
from keras.layers import Dense

class SimpleMLP:
	
	def __init__():
		self.metrics = ['accuracy']
		self.optimizer = SGD(learning_rate, 
						decay= learning_rate / comms_round, 
						momentum=0.9
					   )  
		
	
    @staticmethod
    def build(shape, learning_rate= 0.1, comms_round = 100, loss ="categorical_crossentropy"):
		 
        model = Sequential([
            Dense(32, activation='relu', input_shape=(shape,)),
            Dense(372, activation='sigmoid')   
        ])
        

        return model
        
        
   
               
               
#initialize global model
shape = clients_batched['client_1']['data'].shape[0]
smlp_global = SimpleMLP()
global_model = smlp_global.build(shape, 10)


def test_model(X_test, Y_test,  model, comm_round):
    cce = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
    #logits = model.predict(X_test, batch_size=100)
    logits = model.predict(np.array([X_test]))
    Y_test = np.array(Y_test).reshape(1,-1)
    loss = cce(Y_test, logits)
    acc = accuracy_score(tf.argmax(logits, axis=1), tf.argmax(Y_test, axis=1))
    print('comm_round: {} | global_acc: {:.3%} | global_loss: {}'.format(comm_round, acc, loss))
    return acc, loss

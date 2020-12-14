#1. Load packages
import tensorflow as tf
import numpy as np
#2.Load dataset
fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
#3.Preprocess data
train_images = train_images / 255.0
test_images = test_images / 255.0
#4.Define and compile model
model = tf.keras.Sequential([
   tf.keras.layers.Flatten(input_shape=(28, 28)),
   tf.keras.layers.Dense(128, activation='relu'),
   tf.keras.layers.Dense(10),
   tf.keras.layers.Softmax()])
model.compile(optimizer='adam',
             loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
             metrics=['accuracy'])
#5.Train model
model.fit(train_images, train_labels, epochs=10)
#6.Evaluate accuracy
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest accuracy:', test_acc)
#7.Save model
model.save('my_model')
#8.Run predictions
predictions = model.predict(test_images)
print('\nPrediction:',predictions[0])

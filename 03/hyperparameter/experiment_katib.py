import argparse
import tensorflow as tf
import numpy as np

def main(params):
    cell_numbers = params.cells_number
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    train_images = train_images / 255.0
    test_images = test_images / 255.0
    model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(cell_numbers, activation='relu'),
    tf.keras.layers.Dense(10),
    tf.keras.layers.Softmax()])
    model.compile(optimizer='adam',
             loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
             metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=10)
    test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    print('accuracy:', test_acc)
    model.save('my_model')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='katib experiment')
    parser.add_argument('--cells_number', type=int, default=128)
    params = parser.parse_args()
    main(params)
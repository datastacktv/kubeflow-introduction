import tensorflow as tf
import numpy as np
import json
import os

def define_compile_model(model_path):
    model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10),
    tf.keras.layers.Softmax()])
    model.compile(optimizer='adam',
             loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
             metrics=['accuracy'])
    if not os.path.exists(os.path.dirname(model_path)):
        os.makedirs(os.path.dirname(model_path))
    with open(model_path, 'w') as f:
        f.write(model.to_json())
        
def main(params):
    define_compile_model(params.model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='define_compile_model')
    parser.add_argument('--model_path', type=str, default='None')
    params = parser.parse_args()
    main(params)


    
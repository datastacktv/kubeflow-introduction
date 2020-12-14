import tensorflow as tf
import numpy as np
import json
import os

def load_preprocess(train_images_data_path,train_labels_data_path,test_images_data_path,test_labels_data_path):
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    if not os.path.exists(os.path.dirname(train_images_data_path)):
        os.makedirs(os.path.dirname(train_images_data_path))
    if not os.path.exists(os.path.dirname(train_labels_data_path)):
        os.makedirs(os.path.dirname(train_labels_data_path))
    if not os.path.exists(os.path.dirname(test_images_data_path)):
        os.makedirs(os.path.dirname(test_images_data_path))
    if not os.path.exists(os.path.dirname(test_labels_data_path)):
        os.makedirs(os.path.dirname(test_labels_data_path))
   

    with open(train_images_data_path, 'w') as f:
        f.write(json.dumps(train_images.tolist()))

    with open(train_labels_data_path, 'w') as f:
        f.write(json.dumps(train_labels.tolist()))

     with open(test_images_data_path, 'w') as f:
        f.write(json.dumps(test_images.tolist()))

    with open(test_labels_data_path, 'w') as f:
        f.write(json.dumps(test_labels.tolist()))        


def main(params):
    load_preprocess(params.train_images_data_path,params.train_labels_data_path,params.test_images_data_path,params.test_labels_data_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='load_preprocess')
    parser.add_argument('--train_images_data_path', type=str, default='None')
    parser.add_argument('--train_labels_data_path', type=str, default='None')
    parser.add_argument('--test_images_data_path', type=str, default='None')
    parser.add_argument('--test_labels_data_path', type=str, default='None')
    params = parser.parse_args()
    main(params)
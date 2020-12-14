import tensorflow as tf
import argparse
import numpy as np
import json
import os

def train_model(model_path, train_images_data_path, train_labels_data_path, test_images_data_path, test_labels_data_path,trained_model_path):
    with open(train_images_data_path) as f:
        train_images_data_path_json = json.load(f)
        train_images = np.array(train_images_data_path_json)
    with open(train_labels_data_path) as f:
        train_labels_data_path_json = json.load(f)
        train_labels = np.array(train_labels_data_path_json)
     with open(test_images_data_path) as f:
        test_images_data_path_json = json.load(f)
        test_images = np.array(test_images_data_path_json)
    with open(test_labels_data_path) as f:
        test_labels_data_path_json = json.load(f)
        test_labels = np.array(test_labels_data_path_json)


    model_file = open(model_path, 'r')
    model_json = model_file.read()
    model_file.close()
    model = tf.keras.models.model_from_json(model_json)    

    model.fit(train_images, train_labels, epochs=10)
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    print('accuracy:', test_acc)

  
    if not os.path.exists(os.path.dirname(model_output_path)):
        os.makedirs(os.path.dirname(model_output_path))
    model.save(model_output_path, save_format='tf')



    if not os.path.exists(os.path.dirname(trained_model_path)):
        os.makedirs(os.path.dirname(trained_model_path))
    with open(model_path, 'w') as f:
        f.write(model.to_json())
        
def main(params):
    train_model(params.model_path,params.train_images_data_path,params.train_labels_data_path,params.test_images_data_path,params.test_labels_data_path,params.trained_model_path )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='train_model')
    parser.add_argument('--model_path', type=str, default='None')
    parser.add_argument('--train_images_data_path', type=str, default='None')
    parser.add_argument('--train_labels_data_path', type=str, default='None')
    parser.add_argument('--test_images_data_path', type=str, default='None')
    parser.add_argument('--test_labels_data_path', type=str, default='None')
    parser.add_argument('--trained_model_path', type=str, default='None')
    params = parser.parse_args()
    main(params)
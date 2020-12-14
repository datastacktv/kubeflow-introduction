import argparse
import kfp
import kfp.dsl as dsl
import datetime
import logging


# Components load
load_preprocess_data_component = kfp.components.load_component_from_file('load_preprocess_data/component.yaml')
define_compile_model_component = kfp.components.load_component_from_file('define_compile_model/component.yaml')
train_model_component = kfp.components.load_component_from_file('train_model/component.yaml')



# Operations definition


def load_preprocess_data_operation():
    return load_preprocess_data_component()

def define_compile_model_operation():
    return define_compile_model_component()


def train_model_operation(model_path, train_images_data_path, train_labels_data_path, test_images_data_path, test_labels_data_path):
    return train_model_component(model_path, train_images_data_path, train_labels_data_path, test_images_data_path, test_labels_data_path)




def main(params):
    @dsl.pipeline(
        name='kubeflos simple pipeline',
        description='Pipeline for training a fashion mnist classifier'
    )
    def simple_pipeline():
        now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        workspace_name = 'simple_pipeline' + now
        load_preprocess_data_task = load_preprocess_data_operation()
        define_compile_model_task = define_compile_model_operation()
        train_model_task = train_model_component(define_compile_model_task.outputs['model_path'],
                                                load_preprocess_data_task.outputs['train_images_data_path'],
                                                load_preprocess_data_task.outputs['train_labels_data_path'],
                                                load_preprocess_data_task.outputs['test_images_data_path'],
                                                load_preprocess_data_task.outputs['test_labels_data_path'])
        
    # Generate .zip file
    pipeline_func = simple_pipeline
    pipeline_filename = pipeline_func.__name__ + '.kf_pipeline_containers.zip'
    kfp.compiler.Compiler().compile(pipeline_func, pipeline_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Component-based simple build-train pipeline')
    params = parser.parse_args()
    main(params)
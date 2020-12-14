import argparse
import datetime
import logging
from kubernetes import client
from kfserving import KFServingClient
from kfserving import constants
from kfserving import V1alpha2EndpointSpec
from kfserving import V1alpha2PredictorSpec
from kfserving import V1alpha2TensorflowSpec
from kfserving import V1alpha2InferenceServiceSpec
from kfserving import V1alpha2InferenceService
from kubernetes.client import V1ResourceRequirements


def deploy_model(namespace,trained_model_path):
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting deploy model step ..')
    logging.info('Input data ..')
    logging.info('namespace:{}'.format(namespace))
    logging.info('trained_model_path:{}'.format(trained_model_path))

    logging.info('STEP: DEPLOY MODEL (1/2) Generating definition..')
    api_version = constants.KFSERVING_GROUP + '/' + constants.KFSERVING_VERSION
    now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    inference_service_name = 'simple-model'+now
    default_endpoint_spec = V1alpha2EndpointSpec(
        predictor=V1alpha2PredictorSpec(
        tensorflow=V1alpha2TensorflowSpec(
        storage_uri=trained_model_path,
        resources=V1ResourceRequirements(
        requests={'cpu': '100m', 'memory': '1Gi'},
        limits={'cpu': '100m', 'memory': '1Gi'}))))

    isvc = V1alpha2InferenceService(api_version=api_version,
                                    kind=constants.KFSERVING_KIND,
                                    metadata=client.V1ObjectMeta(
                                    name=inference_service_name,
                                    annotations=
                                            {
                                                'sidecar.istio.io/inject': 'false',
                                                'autoscaling.knative.dev/target': '1'
                                            },
                                    namespace=namespace),
                                    spec=V1alpha2InferenceServiceSpec(default=default_endpoint_spec))

#velascoluis: sidecar is disabled by https://github.com/knative/serving/issues/6829
#Note: make sure trained model path starts with file:// or gs://

    KFServing = KFServingClient()
    logging.info('STEP: DEPLOY MODEL (2/2) Creating inference service..')
    KFServing.create(isvc)
    logging.info('Inference service ' + inference_service_name + " created ...")
    KFServing.get(inference_service_name, namespace=namespace, watch=True, timeout_seconds=120)
    logging.info('Deploy model step finished')

def main(params):
    deploy_model(params.namespace, params.trained_model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy TF model KFServing')
    parser.add_argument('--namespace',          type=str, default='default')
    parser.add_argument('--trained_model_path', type=str, default='default')
    params = parser.parse_args()
    main(params)



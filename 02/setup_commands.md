# kubeflow v1.1 setup on Google Cloud command and notes

NOTE: This is not a executable script

* Enable APIs:

```bash
gcloud services enable \
  compute.googleapis.com \
  container.googleapis.com \
  iam.googleapis.com \
  servicemanagement.googleapis.com \
  cloudresourcemanager.googleapis.com \
  ml.googleapis.com \
  cloudbuild.googleapis.com
```

* Anthos Service Mesh Project initialization

```bash
curl --request POST \
  --header "Authorization: Bearer $(gcloud auth print-access-token)" \
  --data '' \
  https://meshconfig.googleapis.com/v1alpha1/projects/${PROJECT_ID}:initialize
  ```

* Install CLIs for mgmt cluster deployment

```bash
#kpt
sudo apt-get install google-cloud-sdk-kpt google-cloud-sdk google-cloud-sdk
```

```bash
#yq
sudo wget https://github.com/mikefarah/yq/releases/download/3.4.1/yq_linux_amd64 -O /usr/bin/yq &&    sudo chmod +x /usr/bin/yq
```

```bash
#kustomize
curl -s "https://raw.githubusercontent.com/\
kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash
sudo mv ./kustomize /usr/bin/kustomize
sudo chmod +x /usr/bin/kustomize
```

* Management cluster deploy

```bash
kpt pkg get https://github.com/kubeflow/gcp-blueprints.git/management@v1.1.0 ./
cd management
make get-pkg
##--Edit makefile
## Set values for:
#kpt cfg set ./instance name NAME
#kpt cfg set ./instance location LOCATION
#kpt cfg set ./instance gcloud.core.project PROJECT
#kpt cfg set ./upstream/management name NAME
#kpt cfg set ./upstream/management location LOCATION
#kpt cfg set ./upstream/management gcloud.core.project PROJECT
make set-values
make apply
#Install Cloud Config Connector
##
make create-ctxt
make apply-kcc
kpt cfg set ./instance managed-project ${PROJECT_ID}
anthoscli apply -f ./instance/managed-project/iam.yaml
```

* Install CLIs for kubeflow deployment
  
```bash
#kustomize 3.2
curl -LO https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv3.2.1/kustomize_kustomize.v3.2.1_linux_amd64
mv kustomize_kustomize.v3.2.1_linux_amd64 kustomize
chmod +x ./kustomize
sudo mv ./kustomize /usr/local/bin/kustomize
```

```bash
#istioctl
gcloud projects get-iam-policy ${PROJECT_ID} | grep -B 1 'roles/meshdataplane.serviceAgent'
curl -LO https://storage.googleapis.com/gke-release/asm/istio-1.4.10-asm.18-linux.tar.gz
curl -LO https://storage.googleapis.com/gke-release/asm/istio-1.4.10-asm.18-linux.tar.gz.1.sig
openssl dgst -verify - -signature istio-1.4.10-asm.18-linux.tar.gz.1.sig istio-1.4.10-asm.18-linux.tar.gz <<'EOF'
-----BEGIN PUBLIC KEY-----
....
-----END PUBLIC KEY-----
EOF
tar xzf istio-1.6.11-asm.1-linux-amd64.tar.gz
cd istio-1.6.11-asm.1
export PATH=$PWD/bin:$PATH
```

* Get and apply blueprints

```bash
kpt pkg get https://github.com/kubeflow/gcp-blueprints.git/kubeflow@v1.1.0 ./${KFDIR}
cd kf/kubeflow
make get-pkg
kubectl config use-context mgmt-cluster
kubectl create namespace ${PROJECT_ID}
kubectl config set-context --current --namespace ${PROJECT_ID}
##--Edit makefile
## Set values for:
#kpt cfg set ./instance mgmt-ctxt MGMT_NAME
#kpt cfg set ./upstream/manifests/gcp name NAME
#kpt cfg set ./upstream/manifests/gcp gcloud.core.project PROJECT
#kpt cfg set ./upstream/manifests/gcp gcloud.compute.zone ZONE
#kpt cfg set ./upstream/manifests/gcp location LOCATION
#kpt cfg set ./upstream/manifests/gcp log-firewalls false
#kpt cfg set ./upstream/manifests/stacks/gcp name NAME
#kpt cfg set ./upstream/manifests/stacks/gcp gcloud.core.project PROJECT
#kpt cfg set ./instance name NAME
#kpt cfg set ./instance location LOCATION
#kpt cfg set ./instance gcloud.core.project PROJECT
#kpt cfg set ./instance email EMAIL
#Export credentials
export CLIENT_ID=<Your CLIENT_ID>
export CLIENT_SECRET=<Your CLIENT_SECRET>
#Deploy
##
make apply
```

* Grant Web App user role

```bash
gcloud projects add-iam-policy-binding PROJECT --member=user:EMAIL --role=roles/iap.httpsResourceAccessor
```

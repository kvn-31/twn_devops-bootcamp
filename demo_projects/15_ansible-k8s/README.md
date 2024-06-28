# K8s
The goal of this project is to spin up a K8s cluster using terraform and configure the cluster using ansible. This also includes deploying an application to the cluster.

## Prerequisites
- for the kubernetes.core.k8s module we need the following:
  - python >= 3.9
  - kubernetes >= 24.2.0
  - PyYAML >= 3.11
  - jsonpatch
- to verify if something is available this command comes in handy:
  - `python3 -c "import PACKAGE`
- on Linux, the safest way is to use a venv:
```bash
python3 -m venv .venv #creates a virtual environment
source .venv/bin/activate #activates the virtual environment
```
  - the ansible command needs to be run from the venv

## Terraform
We are using the already existing terraform configuration from `terraform-eks`.

## Ansible
We are using the kubernetes.core.k8s module to deploy the application to the cluster.
It includes the creation of a simple nginx deployment and a service using `nginx-config.yaml` file.

Kubeconfig file is needed to connect to the cluster and is used by the k8s module. By default the module looks for the kubeconfig file in `~/.kube/config`. If the file is located elsewhere, the `K8s_AUTH_KUBECONFIG` environment variable can be set to the correct path.
`export K8s_AUTH_KUBECONFIG=/path/to/kubeconfig`

## Run the project
- `ansible-playbook deploy-to-k8s.yaml`
- `kubectl get pod -n my-app` to verify that the creation was successful
- `kubectl get svc -n my-app` to get the external IP of the service (might take some time)

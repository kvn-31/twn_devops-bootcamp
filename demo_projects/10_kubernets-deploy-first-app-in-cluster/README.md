# Kubernetes Demo Project - Deploy Application in Cluster

In this project, we create a simple Kubernetes cluster with a Deployment of mongo and mongo-express. They both have their own services.
The config (db url) is shared between mongo and mongo-express using a configMap and the db credentials are shared using a secret.

### Important Note
> The secrets are base64 encoded, but not encrypted. This is not a secure way to store secrets. In a real-world scenario, you would use a secret management tool like Vault, AWS Secrets Manager, or Azure Key Vault.
> No real cluster is built using this project. It is just a demo project to show how to deploy an application in a Kubernetes cluster, which is tested locally.

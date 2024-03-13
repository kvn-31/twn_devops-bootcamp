# Deploy to EKS from Jenkins

We can use Jenkins to deploy to EKS. The steps to configure are:
- install kubectl in the jenkins container
- install aws-iam-authenticator in the jenkins container (was installed in local machine automatically with eksctl)
- create kubeconfig to connect to eks cluster
- adjust Jenkinsfile to deploy to eks cluster

See [11_kubernetes_on_aws notes](..%2F..%2F..%2Fnotes%2F11_kubernetes_on_aws.md) for more details.

The github repo used for the actual application is [TWN - Java Maven App](https://github.com/kvn-31/twn_java-maven-app/tree/deploy-on-k8s)

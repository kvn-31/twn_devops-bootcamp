# Helm Chart Microservices

This demo project is again based on an  [existing microservice](https://github.com/GoogleCloudPlatform/microservices-demo) demo from Google.
For more details, see the README added to 10_kubernetes-microservices-demo.

In the previous example (`10_kubernetes-microservices-demo`), we deployed a microservices application using Kubernetes. We used a configuration file to describe the application and deployed it to the cluster. 
The config.yaml file was quite repetitive and long, which is avoided in this project because we will use Helm to deploy the same application.

As all the microservices shared a similar configuration, we created one deployment.yaml and one service.yaml that is used for all microservices.
Only redis needed its own configuration as the setup is different. It can be found in the redis folder.
As required by Helm we added a Chart.yaml which contains the metadata of the chart and a values.yaml file which contains the default values for the chart.

The values of the actual microservices can be found in `/values` folder.

This project was initialized running `helm create microservice`, which provided boilerplate that was removed and edited.

## Project structure and files
- `/charts` contains the microservices and redis charts
- `/values` contains the values for the microservices and redis
- `config.yaml` the "old" configuration file for the application, which is now replaced by the Helm chart
- `install.sh` script to install the Helm chart (simply just a collection of helm install commands)
- `uninstall.sh` script to uninstall the Helm chart
- `helmfile.yaml` the Helmfile to install the Helm chart

## How to deploy the application

### Prerequisites
connected to a Kubernetes cluster and Helm installed

There are two approaches to deploy the application:
1. Using the `install.sh` script
   - just runs multiple `helm install` commands
   - can be uninstalled using the `uninstall.sh` script
2. Using the `helmfile.yaml`
   - run `helmfile sync` to install the Helm chart
   - run `helmfile destroy` to uninstall the Helm chart
   - can be considered as the preferred way to deploy

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


## How to deploy the application

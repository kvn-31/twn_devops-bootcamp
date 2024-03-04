# ConfigMap and Secret Volume Types

In this quick exercise we will create a mosquitto deployment with a configmap and a secret volume type.

The file mosquitto-without-volumes.yaml is only used to create the mosquitto deployment without volumes and to inspect the container file system to see the actual paths of the mosquitto configuration files.

```bash
kubectl apply -f mosquitto-without-volumes.yaml
kubectl exec -it mosquitto-<pod-id> -- /bin/sh
```


## Using Config and Secret File

- if created: delete mosquitto without volumes
- first create configmap and secret
- then create mosquitto with volumes (see mosquito.yaml)

```bash
kubectl apply -f config-file.yaml
kubectl apply -f secret-file.yaml
```

We can now see the files created when we inspect the container file system.

```bash
kubectl exec -it mosquitto-<pod-id> -- /bin/sh
```

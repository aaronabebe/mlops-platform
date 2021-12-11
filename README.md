# mlops platform

Quick Links: 

- [Timetracking](docs/TIMETRACKING.md)
- [General Notes](docs/NOTES.md)

## todos

- [x] setup k3d + helm
- [x] setup clearml server
  - [x] fix memory issues with clearml elastic cluster -> deploy on remote server?
- [x] read docs plan project list
- [ ] check out clearml repo
- [ ] setup mnist pytorch
- [ ] find other ml example projects

## setup with docker compose

Due to the large memory constraints of running the clearml server in `k8s` I will also provide a little bit more lightweight version running with
`docker-compose`.

### prerequisites 

- docker-compose 

Follow the provided [tutorial](https://clear.ml/docs/latest/docs/deploying_clearml/clearml_server_linux_mac/) to set everything up. 

Start via:

```
docker-compose -f /opt/clearml/docker-compose.yml up -d
```

Follow the logs via: 

```
docker-compose -f /opt/clearml/docker-compose.yml logs -f
```



## setup with k8s/kind

### prerequisites 

- kind 
- kubectl
- helm


### setup notes

start the kind cluster

```sh
kind create cluster --config clearml-kind.yml
```

install clearml via helm

```sh
helm repo add allegroai https://allegroai.github.io/clearml-helm-charts
helm install clearml-server allegroai/clearml -n clearml --create-namespace
```

### kubectl commands

change current namespace
```sh
kubectl config set-context --current --namespace=default
```

important cluster getters

```sh
kubetl get events
kubetl get pods
kubectl get pvc
```



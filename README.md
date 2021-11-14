# mlops platform

## prerequisites 

- kind 
- kubectl
- helm


## setup notes

start the kind cluster

```sh
k3d cluster create --config clearml-kind.yml
```

install clearml via helm

```sh
helm repo add allegroai https://allegroai.github.io/clearml-helm-charts
helm install clearml-server allegroai/clearml -n clearml --create-namespace
```

## kubectl commands

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


## todos

- [x] setup k3d + helm
- [x ] setup clearml server
  - [x] fix memory issues with clearml elastic cluster -> deploy on remote server?
- [ ] plan pipeline + steps
- [ ]

## timetracking

- 14.11.21 | 6h | setup clearml-agent, setup k3d, helm, kubectl locally

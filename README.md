# mlops platform

## prerequisites 

- k3d 
- kubectl
- helm


## setup notes

start the k3d cluster

```sh
k3d cluster create mlops --k3s-node-label "app=clearml@server:0"
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
```


## todos

- [x] setup k3d + helm
- [ ] setup clearml server
  - [ ] fix memory issues with clearml elastic cluster -> deploy on remote server?
- [ ] plan pipeline + steps
- [ ]

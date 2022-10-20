# Fission Tutorial 

## Table of Contents

1. [Installation & Setup](#Installation&Setup)
2. [Usage](#Usage)

## Installation & Setup

Requirements:

1. Kubernetes version > 1.19
2. Kubectl
3. Helm v3

**Disclaimer: Only for local desktops. A separate process for cloud environments.**

#### Set namespace as *fission* & install program.

```bash
export FISSION_NAMESPACE="fission";
kubectl create namespace $FISSION_NAMESPACE;
kubectl create -k "github.com/fission/fission/crds/v1?ref=v1.17.0";
helm repo add fission-charts <https://fission.github.io/fission-charts/>;
helm repo update;
helm install --version v1.17.0 --namespace $FISSION_NAMESPACE fission \
  --set serviceType=NodePort,routerServiceType=NodePort \
  fission-charts/fission-all;
```

#### Install CLI:
i. macOS
```bash
curl -Lo fission <https://github.com/fission/fission/releases/download/v1.17.0/fission-v1.17.0-darwin-amd64> \\
    && chmod +x fission && sudo mv fission /usr/local/bin/
```
ii. Linux/WSL
```bash
curl -Lo fission <https://github.com/fission/fission/releases/download/v1.17.0/fission-v1.17.0-linux-amd64> \\
    && chmod +x fission && sudo mv fission /usr/local/bin/
```

## Usage
#### Create environment (Python)
You can change `name` to something else. `image` must match the language you are using
```bash
fission env create --spec --name python --image fission/python-env --builder fission/python-builder
```

#### Code
Clone the repo with example code
```bash 
git clone https://github.com/NauqGnesh/fission-tutorial.git
```

Your functions should be structured as such:
```bash
.
├── room/
│   ├── room.py
│   └── requirements.txt
└── lamp/
    ├── lamp.py 
    └── requirements.txt
```

#### Create functions
This will register a function to your fission namespace
* `--env` name of environment to execute function 
* `--name` name of function
* `--src` source code
* `--entrypoint` entrypoint of your code 

```bash
fission function create --spec --name room --env python --src "room/*" --entrypoint room.main
fission function create --spec --name lamp --env python --src "lamp/*" --entrypoint lamp.main
```

#### Trigger
This will create a trigger to invoke your fission functions 
* `--method` HTTP method
* `--url` route endpoint 
* `--function` name of function to be invoked 

```bash
fission route create --spec --method GET --url /lamp --function lamp
fission route create --spec --method GET --url /room --function room 
```

Addtionally, minikube doesn't support external load balancer, so we need to forward ports. Set `<local port>` to a free port on your machine. *Note: minikube uses 8080 by default*

```bash
export FISSION_ROUTER=$(minikube ip):$(kubectl -n fission get svc router -o jsonpath='{...nodePort}');
kubectl --namespace fission port-forward $(kubectl --namespace fission get pod -l svc=router -o name) <local port>:8888 &;
export FISSION_ROUTER=127.0.0.1:<local port>
```

#### Validate
```bash
fission spec validate
```

#### Deploy
Use `--watch` to deploy continuously
```bash
fission spec apply --wait 
```


### Test 
To invoke a function directly

``` bash
fission function test --name lamp
```

To invoke a function via trigger

``` bash
curl http://$FISSION_ROUTER/lamp
```



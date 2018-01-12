This is the Class Tools infrastructure specification and management tools.

- [Prerequisites](#prerequisites)
- [Build the notebook image](#build-the-notebook-image)
- [Setup JupyterHub on your Kubernetes cluster](#setup-jupyterhub-on-your-kubernetes-cluster)
- [Chart configuration](#chart-configuration)
- [Reference](#reference)

### Prerequisites

Make sure you have installed

* [Docker](https://www.docker.com/) >= *17.x.x*
* [Google Cloud SDK](https://cloud.google.com/sdk/)
* [kubectl](https://kubernetes.io/docs/user-guide/kubectl/)

### Build the notebook image

Specify the following environment variables:

* `DOCKER_REGISTRY` : the registry and repository to push the images, e.g. `me/my-docker-hub-repo`,
* `IMG_VERSION` : the suffix to append to each image. Each tag will be in the form `name-IMG_VERSION`. Defaults to *latest*.

To build and push the single-user Jupyter Notebook image to the docker repo specified above, run

```bash
make push-single-user
```

in the project's root directory.

You can also run

```bash
make build-single-user
```

to just build the docker image locally.


### Setup JupyterHub on your Kubernetes cluster

First, you need to install Helm. See [these instructions](https://github.com/kubernetes/helm/blob/master/docs/install.md)
for details on how to do this.

To initialize Helm, execute
```bash
kubectl --namespace kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller
```

**IMPORTANT**: Only execute the second command if the kubernetes cluster you are deploying to is RBAC-enabled.

Once the Helm initialization is done, install the JupyterHub helm repository to Helm, by running:
```bash
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update
```

### Chart configuration

Run

```bash
cp deployment/helm/config.yaml.example deployment/helm/config.yaml
```

and replace the placeholders inside the `config.yaml` file with their desirable values.

* `proxy.secretToken`: Quoting from [[1]](#reference):
> A 64-byte cryptographically secure randomly generated string used to secure communications between the hub and the configurable-http-proxy.
>
> This must be generated with `openssl rand -hex 32`.
>
> Changing this value will cause the proxy and hub pods to restart. It is good security practice to rotate these values over time. If this secret leaks, immediately change it to something else, or user data can be compromised

* `singleuser.image`: The docker image you built during the first phase of the setup process.
    * `singleuser.image.name`: The repository in which the image is hosted.
    * `singleuser.image.tag`: The tag of the target notebook image.

For more configuration options, see [[1]](#reference).

Once you have setup the `config.yaml` file, run
```bash
helm install jupyterhub/jupyterhub --version=v0.5 \
    --name=RELEASE-NAME --namespace=NAMESPACE-NAME \
    -f path/to/config.yaml [--set=rbac.enabled=false]
```

where:

* `--name` is a deployment identifier used by helm
* `--namespace` is the name of the namespace in which JupyterHub will be deployed. If it does not exist, it will
be created for you.

**NOTE**: If the cluster you are deploying to is not RBAC-enabled, then you need to also use the `--set` flag
in the above command.

After the above command executes, check the status of the deployment by running
```bash
kubectl get pods --namespace NAMESPACE-NAME
```

When both the proxy and the hub pods have a status of 'Running', you are good to go.

**NOTE**: You will also have to allow TCP traffic to the hub proxy's port on your cloud provider's firewall. Run
```bash
kubectl get services --namespace NAMESPACE-NAME
```

and look for the `proxy-public` service. Allow TCP traffic to the port which targets port 80 of the proxy. For instance,
say the output of the `get services` command were:
```
hub            ClusterIP      . . .   8081/TCP
proxy-api      ClusterIP      . . .   8001/TCP
proxy-http     ClusterIP      . . .   8000/TCP
proxy-public   LoadBalancer   . . .   80:31870/TCP,443:31182/TCP
```

We would have to allow traffic to `tcp:31870` on our firewall in order to be able to access the proxy.

### Reference

[1] [Helm Chart Configuration](https://zero-to-jupyterhub.readthedocs.io/en/latest/reference.html#id1)

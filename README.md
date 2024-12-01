# Local Development Environment

This is a modern Data Engineering stack.

## How to start

Follow this [guide](https://code.visualstudio.com/docs/devcontainers/containers#_installation) to install:

1. Docker Desktop
1. Visual Studio Code
1. Dev Containers extension

## Secrets

1. Create `.devcontainer/.env.secrets` if you want to pass secrets to containers.

## Services

> Local Development Environment starts multiple containers. If your computer is running slow, feel free to stop the ones that are not needed.

### JupyterLab

* [JupyterLab](http://localhost:8888) - Needs to be started manually: `jupyter-lab --notebook-dir=./code --IdentityProvider.token='' --no-browser`

### Spark

* [Spark Master UI](http://localhost:8081/)
* [Spark Worker UI](http://localhost:8091/)
* [Spark Application UI](http://localhost:4040/) - Available only when application runs. When port 4040 is used, drivers opens next port. Check logs.

### Trino

* [Trino UI](http://localhost:8082/ui/)

## Examples

Check `examples` folder for scrips and projects using this tech stack.

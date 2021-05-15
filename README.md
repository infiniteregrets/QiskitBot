# QiskitBot

A discord bot that allows you to execute Quantum Circuits, search the Qiskit Documentation, and search the Quantum Computing StackExchange. 

## Installation

Using docker-compose:

```
docker-compose up --build 
```
Manually from the Dockerfile
```
docker build -t qiskitbot . 
docker run --privileged -i -t qiskitbot 
```
On MacOs with deploy.sh
```
zsh deploy.sh
```

## Architecture of the sandbox (running untrusted code)
### Goal
Spawn a container per user, providing an isolated environment to run untrusted code. Save the state of the user using [CRIU](https://criu.org/Main_Page) (checkpoint and restore).
### Nested Containers
One of the main objectives of this project was to experiment with the idea of having containers inside of containers. Instead of mounting the unix socket and the spawning containers (the tradional way):
```
docker run -v /var/run/docker.sock:/var/run/docker.sock ...
```
I used podman inside of docker, which is a daemonless container engine used for developing, managing, and running OCI Containers. Podman is used with tools like Buildah and Skopeo, which not only makes managing images and containers easy but in my opinion much more powerful than docker!

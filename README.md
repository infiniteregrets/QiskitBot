# QiskitBot

A discord bot that allows you to execute Quantum Circuits, look up the Qiskit Documentation, and search the Quantum Computing StackExchange. 

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
## Disclaimer

Builds might fail on your machine. This is still under testing and there is a lot that needs to be fixed with the way the code is structured. Once everything is smooth, I will add docstrings and comments wherever neccessary (: 

## Architecture of the sandbox (running untrusted code)
### Goal
Spawn a container per user, providing an isolated environment to run untrusted code. Save the state of the user using [CRIU](https://criu.org/Main_Page) (checkpoint and restore).
### Nested Containers
One of the main objectives of this project was to experiment with the idea of having containers inside of containers. Instead of mounting the unix socket and the spawning containers (the tradional way):
```
docker run -v /var/run/docker.sock:/var/run/docker.sock ...
```
I used podman inside of docker, which is a daemonless container engine used for developing, managing, and running OCI Containers. Podman is used with tools like Buildah and Skopeo, which not only makes managing images and containers easy but in my opinion much more powerful than docker!

### Usage
```
<@Qiskit>asciicircuit \`\`\` <codeblock> \`\`\`
```
![](assets/asciicircuit.png)
```
<@Qiskit>mplcircuit \`\`\` <codeblock> \`\`\`
```
![](assets/circuit.png)
```
<@Qiskit>docs <searchitem> 
```
![](assets/docs.png)
```
<@Qiskit>mplplot  \`\`\` <codeblock> \`\`\`
```
![](assets/plot.png)
```
<@Qiskit>query <search criteria> \`\`\` <codeblock> \`\`\`
```
![](assets/stackexchange.png)

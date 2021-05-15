#!/bin/zsh

emulate -LR zsh

[ -f Dockerfile ] || { echo "No Dockerfile" ; exit 1; }

docker build -t qiskitbot . 
docker run --privileged -i -t qiskitbot /bin/bash

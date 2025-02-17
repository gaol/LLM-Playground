#!/bin/bash

echo -e "Trying to rebuild the docker image in `$(pwd)`"

docker build -t local_jupyter .

ps_id="`docker ps |grep local_jupyter| awk '{print $1}'`"

[[ ! -z "$ps_id" ]] && echo "Stopping local jupyter container ..." && docker stop $ps_id

# for daemon, use -d
echo -e "Now start the local_jupyter container with 8888 port exposed, stop the container will get removed."
docker run -p 8888:8888 --rm --name local_jupyter local_jupyter



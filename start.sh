#!/bin/bash

echo -e "Trying to rebuild the docker image in $(pwd)"

docker build -t local_jupyter .

[[ $? -ne 0 ]] && echo "Failed to build the docker image" && exit 1

ps_id="`docker ps |grep local_jupyter| awk '{print $1}'`"

[[ ! -z "$ps_id" ]] && echo "Stopping local jupyter container ..." && docker stop $ps_id

# for daemon, use -d
echo -e "Now start the local_jupyter container with 8888 port exposed, stop the container will get removed."

docker run -p 8888:8888 --rm \
    --name local_jupyter \
    -v "$(pwd)/notebooks":/home/lgao/llm/notebooks:rw \
    -v "$(pwd)/shares":/home/lgao/llm/shares:ro \
    -v "$(pwd)/models":/home/lgao/llm/models:ro \
    -v "$(pwd)/tools":/home/lgao/llm/tools:ro \
    local_jupyter


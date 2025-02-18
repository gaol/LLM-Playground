#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd ${SCRIPT_DIR}
[[ ! -e ".env" ]] && echo -e ".env file does not exist, create one." && touch .env
echo -e "Trying to rebuild the docker image in $(pwd)"
docker build -t local_jupyter .
[[ $? -ne 0 ]] && echo "Failed to build the docker image" && exit 1
popd

ps_id="`docker ps |grep local_jupyter| awk '{print $1}'`"

[[ ! -z "$ps_id" ]] && echo "Stopping local jupyter container ..." && docker stop $ps_id

# for daemon, use -d
echo -e "Now start the local_jupyter container with 8888 port exposed, stop the container will get removed."

docker run -p 8888:8888 --rm \
    --name local_jupyter \
    -v "${SCRIPT_DIR}/notebooks":/home/lgao/llm/notebooks:rw \
    -v "${SCRIPT_DIR}/shares":/home/lgao/llm/shares:ro \
    -v "${SCRIPT_DIR}/models":/home/lgao/llm/models:ro \
    -v "${SCRIPT_DIR}/tools":/home/lgao/llm/tools:ro \
    -v "${SCRIPT_DIR}/.env":/home/lgao/llm/.env:ro \
    local_jupyter

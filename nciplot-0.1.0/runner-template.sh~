CONTAINER_IMAGE="index.docker.io/mdehavensift/nciplot:latest"

. _util/container_exec.sh

echo ${data}
echo ${output}

container_exec ${CONTAINER_IMAGE} run-nciplot ${data} ${output}

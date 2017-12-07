CONTAINER_IMAGE="index.docker.io/sd2nciplot/nciplot:0.1.0"

. _util/container_exec.sh

echo ${data}
echo ${output}

container_exec ${CONTAINER_IMAGE} run-nciplot ${data} ${output}

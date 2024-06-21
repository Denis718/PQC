#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 {build|run}"
    exit 1
fi

source ./env

if [ "$1" == "build" ]; then
    docker build \
        --tag $OQS_OPENVPN_DOCKERIMAGE_CA \
        --target ca . 
fi

if [ "$1" == "run" ]; then
    docker run \
        --rm -d \
        --name $OQS_CA \
        -e OQSSIGALG=$OQS_SIGALG \
        -v ./ca:/config/openvpn \
        $OQS_OPENVPN_DOCKERIMAGE_CA \
        sh -c "cd /config/openvpn && ca_cacert.sh"


	echo "copy the 'ca' directory to the client"

fi


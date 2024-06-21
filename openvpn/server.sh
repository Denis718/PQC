#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 {build|run}"
    exit 1
fi

source ./env

if [ "$1" == "build" ]; then
    docker build \
        --tag $OQS_OPENVPN_DOCKERIMAGE_SERVER \
        --target server .
fi

if [ "$1" == "run" ]; then
    docker run \
        --rm -d \
        --name $OQS_SERVER \
        -e SERVERFQDN=$OQS_SERVER \
        --net bridge \
        -p 1194:1194/udp \
	    -p 80:80 \
        -v ./ca:/etc/openvpn \
        --cap-add=NET_ADMIN \
        $OQS_OPENVPN_DOCKERIMAGE_SERVER \
        serverstart.sh
fi

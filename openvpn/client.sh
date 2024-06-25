#!/bin/bash

if [ $# -ne 1 ] || ( [ "$1" != "build" ] && [ "$1" != "run" ] ); then
    echo "Usage: $0 {build|run}"
    exit 1
fi

source ./env

if [ "$1" == "build" ]; then
    docker build \
        --tag $OQS_OPENVPN_DOCKERIMAGE_CLIENT \
        --target client . 
fi

if [ "$1" == "run" ]; then
    docker run \
        --rm -d \
        --name $OQS_CLIENT \
        -e CLIENTFQDN=$OQS_CLIENT \
	    -e SERVERFQDN=$IP_OQS_SERVER \
        --net bridge \
        --mount src="$(pwd)/ca",target=/etc/openvpn,type=bind \
        --cap-add=NET_ADMIN \
        $OQS_OPENVPN_DOCKERIMAGE_CLIENT \
        clientstart.sh
fi


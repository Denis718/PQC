#!/bin/bash

# name of OQS signature algorithm to use for TLS auth key/certs
export OQS_SIGALG="p521_falcon1024"

# name of volume to contain all certs and configs
export OQS_DATA="ovpn-data-oqstest"

# name of docker network to use for testing
export OQS_NETWORK="oqsopenvpntestnet"

# DNS name of test server
export OQS_SERVER="oqsopenvpnserver"

# DNS name of test client
export OQS_CLIENT="oqsopenvpnclient"

# name of docker image to run
export OQS_OPENVPN_DOCKERIMAGE="oqs-openvpn"
export OQS_OPENVPN_DOCKERIMAGE_SERVER="oqs-openvpn-server"
export OQS_OPENVPN_DOCKERIMAGE_CLIENT="oqs-openvpn-client"



# salvar CA no cliente

docker run --name oqsopenvpnclient -e SERVERFQDN=oqsopenvpnserver -e CLIENTFQDN=oqsopenvpnclient --net bridge -d --cap-add=NET_ADMIN oqs-openvpn-client clientstart.sh




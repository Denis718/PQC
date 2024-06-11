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


docker volume create --name $OQS_DATA && docker network create --driver=bridge --subnet=172.18.1.0/24 $OQS_NETWORK


docker run -e OQSSIGALG=$OQS_SIGALG -v $OQS_DATA:/config/openvpn -d $OQS_OPENVPN_DOCKERIMAGE sh -c "cd /config/openvpn && ca_cacert.sh"


docker run --name $OQS_SERVER -e SERVERFQDN=$OQS_SERVER --net $OQS_NETWORK --ip 172.18.1.2 -v $OQS_DATA:/etc/openvpn -d --cap-add=NET_ADMIN $OQS_OPENVPN_DOCKERIMAGE_SERVER serverstart.sh
docker run --name $OQS_CLIENT -e SERVERFQDN=$OQS_SERVER -e CLIENTFQDN=$OQS_CLIENT --net $OQS_NETWORK --ip 172.18.1.3 -v $OQS_DATA:/etc/openvpn -d --cap-add=NET_ADMIN $OQS_OPENVPN_DOCKERIMAGE_CLIENT clientstart.sh


# Allow time to start up
sleep 3
# Check that initialization went OK for both server and client:
docker logs $OQS_SERVER | grep "Initialization Sequence Completed"
if [ $? -ne 0 ]; then
   echo "Error initializing server."
   RC=1
fi
docker logs $OQS_CLIENT | grep "Initialization Sequence Completed"
if [ $? -ne 0 ]; then
   echo "Error initializing client."
   RC=1
fi

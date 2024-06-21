#!/bin/bash

mkdir -p /dev/net
mknod /dev/net/tun c 10 200

# if env var not set, chose default certificate signature algorithm
if [ -z "$OQSSIGALG" ]; then
   OQSSIGALG="dilithium3"
fi

if [ -z "$SERVERFQDN" ]; then
    echo "SERVERFQDN env var not set. Exiting."
    exit 1
fi


# Location of config files
cd /etc/openvpn

openssl genpkey -algorithm $OQSSIGALG -out server_key.key && \
HOSTFQDN=$SERVERFQDN openssl req -new -key server_key.key -subj "/CN=$SERVERFQDN" -config /home/openvpn/openvpn-openssl.cnf -out server_cert.csr && \
HOSTFQDN=$SERVERFQDN openssl x509 -req -in server_cert.csr -CA ca_cert.crt -CAkey ca_key.key -CAcreateserial -out server_cert.crt -extensions usr_cert -extfile /home/openvpn/openvpn-openssl.cnf 


cp /home/openvpn/server.config server.config

# KEMs chosen will be taken from the system-wide openssl.cnf file
# overrule the colon-separated list by using the option --tls-groups

# if env var not set, chose default certificate signature algorithm
# if [ -z "$OQSIGALG" ]; then
#    OQSSIGALG="dilithium3"
# fi

if [ ! -f ca_cert.crt ]; then
    echo "CA file missing. Generating using $OQSSIGALG as signature algorithm..."
    exit 1
fi

service nginx start

if [ -z "$TLS_GROUPS" ]; then
    openvpn --config server.config 
else
    openvpn --config server.config --tls-groups $TLS_GROUPS
fi

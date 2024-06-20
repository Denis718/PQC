#!/bin/bash

mkdir -p /dev/net
mknod /dev/net/tun c 10 200

# if env var not set, chose default certificate signature algorithm
if [ -z "$OQSSIGALG" ]; then
   OQSSIGALG="dilithium3"
fi

if [ -z "$CLIENTFQDN" ]; then
    echo "CLIENTFQDN env var not set. Exiting."
    exit 1
fi

if [ -z "$SERVERFQDN" ]; then
    echo "SERVERFQDN env var not set. Exiting."
    exit 1
fi


# Location of config files:
cd /etc/openvpn

openssl genpkey -algorithm $OQSSIGALG -out client_key.key && \
HOSTFQDN=$CLIENTFQDN openssl req -new -key client_key.key -subj "/CN=$CLIENTFQDN" -config /home/openvpn/openvpn-openssl.cnf -out client_cert.csr && \
HOSTFQDN=$CLIENTFQDN openssl x509 -req -in client_cert.csr -CA ca_cert.crt -CAkey ca_key.key -out client_cert.crt -extensions usr_cert -extfile /home/openvpn/openvpn-openssl.cnf

sed -e "s/oqsopenvpnserver/$SERVERFQDN/g" /home/openvpn/client.config > client.config

# KEMs chosen will be taken from the system-wide openssl.cnf file
# overrule the colon-separated list by using the option --tls-groups

if [ ! -f ca_cert.crt ]; then
    echo "CA not found. Exiting."
    exit 1
fi

if [ -z "$TLS_GROUPS" ]; then
    openvpn --config client.config
else
    openvpn --config client.config --tls-groups $TLS_GROUPS
fi


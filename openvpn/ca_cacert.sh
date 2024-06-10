#!/bin/bash

# if env var not set, chose default certificate signature algorithm
if [ -z "$OQSSIGALG" ]; then
   OQSSIGALG="dilithium3"
fi

openssl genpkey -algorithm $OQSSIGALG -out ca_key.key 

openssl req -key ca_key.key -x509 -subj "/CN=oqsopenvpntest CA" -config /home/openvpn/openvpn-openssl.cnf -out ca_cert.crt
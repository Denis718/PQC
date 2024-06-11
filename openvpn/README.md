# OQS-OPENVPN 

### build container para gerar o certificado da CA 
```
docker build --tag oqs-openvpn --target ca .
```

### build container server oqs-openvpn 
```
docker build --tag oqs-openvpn-server --target server .
```

### build container cliente oqs-openvpn
```
docker build --tag oqs-openvpn-client --target client .
```

## RUN
```
init.sh
```

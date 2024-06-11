## Descrição

### oqs-httpd-reverse-proxy (OQS Apache HTTPd como *proxy* reverso)

O diretório [httpd-reverse-proxy](httpd-reverse-proxy/) contém uma cópia de [httpd](https://github.com/open-quantum-safe/oqs-demos/tree/main/httpd).

O arquivo [Dockerfile](httpd-reverse-proxy/Dockerfile) constrói o *container* oqs-httpd-reverse-proxy usando o OpenSSL(v3) com o [oqs-provider](https://github.com/open-quantum-safe/oqs-provider), o que possibilita a negociação de chaves quânticas seguras e sua utilização na autenticação confiável dentro do TLS 1.3. 

Os arquivos [httpd-ssl.conf](httpd-reverse-proxy/httpd-conf/httpd-ssl.conf) e [httpd.conf](httpd-reverse-proxy/httpd-conf/httpd.conf) foram alterados para o httpd, atuando como *proxy* reverso.

### json-server

O arquivo [Dockerfile](json-server/Dockerfile) constrói o json-server, um *container* Python, que usa o *framework* Flesk para criar as seguintes rotas:

- /register  - Registra um novo usuário no sistema.
- /login - Autenticação de algum usuário no sistema.
- /products - Lista uma série de produtos para usuários autenticados.

Para persistência dos dados no sistema, usamos um bando de dados, através de um *container* PostgreSQL, que foi inicializado com um conjunto de dados preliminares [db.json](json-server/db.json)

### json-server - oqs-htppd-reverse-proxy - oqs-curl

Subistituimos o *container* oqs-httpd em [httpd-wireshark-curl](../httpd-wireshark-curl/) pelo oqs-httpd-reverse-proxy. 

Sendo assim, temos o oqs-httpd-reverse-proxy entre o oqs-curl e o json-server.

O *container* Wireshark (oqs-wireshark) permite visualizar a troca de mensagens entre o json-server, oqs-httpd-reverse-proxy e o oqs-curl.


## Comandos para usar no oqs-curl 

Registra um novo usuário.
```
curl --cacert /cacert_curl/CA.crt --curves kyber768 https://oqs-httpd-reverse-proxy:4433/register -X POST -H "Content-type: application/json" --data '{"username": "user01", "password": "123"}'
```

Login de um usuário. 
```
TOKEN=$(curl --cacert /cacert_curl/CA.crt --curves kyber768 https://oqs-httpd-reverse-proxy:4433/login -X POST -H "Content-type: application/json" --data '{"username": "user01", "password": "123"}')
```

Lista produtos (apenas para usuários autenticados).
```
curl --cacert /cacert_curl/CA.crt --curves kyber768 https://oqs-httpd-reverse-proxy:4433/products -X GET -H "Authorization: Bearer $(echo $TOKEN)"
```

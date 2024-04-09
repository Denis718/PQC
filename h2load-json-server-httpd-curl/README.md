## Descrição

### oqs-h2load
O container oqs-h2load é uma ferramenta de benchmarking responsável por aferir os tempos de requisição para uma carga especificada conforme exemplo básico:
  ```
  h2load -n 1000 -c 10 https://oqs-httpd:4433/produtos --groups kyber768
  ```

-n : número de requisições
-c : requisições concorrentes

mais informações podem ser obtidas em: [h2load - HOW-TO](https://nghttp2.org/documentation/h2load-howto.html)
### oqs-httpd-reverse-proxy (OQS Apache HTTPd como *proxy* reverso)

O diretório [httpd-reverse-proxy](httpd-reverse-proxy/) contém uma copia de [httpd](https://github.com/open-quantum-safe/oqs-demos/tree/main/httpd).

O arquivo [Dockerfile](httpd-reverse-proxy/Dockerfile) constrói o *container* oqs-httpd-reverse-proxy usando o OpenSSL(v3) com o [oqs-provider](https://github.com/open-quantum-safe/oqs-provider), o que possibilita a negociação de chaves quânticas seguras e sua utilização na autenticação confiável dentro do TLS 1.3. 

Os arquivos [httpd-ssl.conf](httpd-reverse-proxy/httpd-conf/httpd-ssl.conf) e [httpd.conf](httpd-reverse-proxy/httpd-conf/httpd.conf) foram alterados para o httpd, atuar como *proxy* reverso.

### json-server

O arquivo [Dockerfile](json-server/Dockerfile) contrói o json-server, um *container* Node.js, que usa [db.json](json-server/db.json) como banco de dados.

### json-server - oqs-htppd-reverse-proxy - oqs-curl

Subistituimos o *container* oqs-httpd em [httpd-wireshark-curl](../httpd-wireshark-curl/) pelo oqs-httpd-reverse-proxy. 

Sendo assim, temos o oqs-httpd-reverse-proxy entre o oqs-curl e o json-server.

O *container* Wireshark (oqs-wireshark) permite visualizar a troca de mensagens entre o json-server, oqs-httpd-reverse-proxy e o oqs-curl.
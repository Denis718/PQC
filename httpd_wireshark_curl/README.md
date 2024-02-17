# Apache HTTPd OQS - Wireshark OQS - curl OQS

Pode ser necessário conceder permissões ao Docker para acessar o display X:
  ```
  xhost +local:$USER
  ```

Execute este comando para abrir a janela Wireshark em seu host:

  ```
  docker-compose up
  ```

Em seguida, continue usando o Wireshark normalmente, por exemplo, selecionando uma interface de rede para monitorar.

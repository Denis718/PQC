## Pelo fato do algoritmo Dilithium e Sphincs+ terem um número elevado de variantes, a alternativa para rodar todos os tempos do arquivo padrão PQCgenKAT_sign.c foi por meio da automatização com o arquivo test.sh

## Salve os arquivos desta pasta no diretório crypto_sign, localizado em Reference_Implementation
ex.:

    ├── Additional_Implementations
    ├── KAT
    ├── Reference_Implementation
    │   └── crypto_sign
    │       ├── PQCgenKAT_sign.c
    │       ├── PQCsignKAT.rsp
    │       ├── crypto_sign.rar
    │       ├── dilithium2
    │       ├── dilithium2-AES
    │       ├── dilithium2-AES-R
    │       ├── dilithium2-R
    │       ├── dilithium3
    │       ├── dilithium3-AES
    │       ├── dilithium3-AES-R
    │       ├── dilithium3-R
    │       ├── dilithium5
    │       ├── dilithium5-AES
    │       ├── dilithium5-AES-R
    │       ├── dilithium5-R
    │       └── test.sh
    └── Supporting_Documentation

## executar o comando : bash test.sh
após a execução será gerado o arquivo PQCsignKAT.rsp necessário para gerar o arquivo csv com o arquivo de notebook python "ResultsToCsv.ipynb"
# Exercicios: TLS, Certificados E HTTPS

## Objetivo

Entender como HTTPS usa certificados digitais para autenticar um servidor e cifrar a comunicacao, comparando HTTP simples, HTTPS com certificado nao confiavel e HTTPS validado por uma CA local.

## Preparacao

Siga o [README do laboratorio](README.md) ate conseguir acessar:

```text
http://localhost:18080/
https://localhost:18443/
```

## Exercicio 1: HTTP Sem TLS

Execute:

```bash
curl -v http://localhost:18080/
```

Responda:

1. Qual protocolo aparece na URL?
2. Existe handshake TLS?
3. O corpo da resposta veio em JSON?
4. O que uma pessoa na rede poderia observar em uma comunicacao HTTP sem TLS?

Resultado esperado:

- o aluno identifica que HTTP nao autentica o servidor com certificado;
- o aluno entende que HTTP nao cifra o conteudo da aplicacao.

## Exercicio 2: HTTPS Sem CA Confiavel

Execute:

```bash
curl -v https://localhost:18443/
```

Responda:

1. O comando funcionou ou falhou?
2. Qual erro de certificado apareceu?
3. O problema esta na criptografia ou na confianca da CA?
4. Por que o sistema operacional nao confia automaticamente na CA local do lab?

Resultado esperado:

- o aluno separa "conexao cifrada" de "identidade confiavel";
- o aluno entende que a cadeia de confianca precisa chegar a uma CA reconhecida pelo cliente.

## Exercicio 3: HTTPS Com CA Informada Manualmente

Execute:

```bash
curl --cacert certs/lab-ca.crt -v https://localhost:18443/
```

Responda:

1. O comando funcionou?
2. Qual arquivo foi usado para estabelecer confianca?
3. O que mudaria se o certificado do servidor tivesse sido assinado por outra CA?
4. Por que informar `--cacert` nao e a mesma coisa que instalar a CA no sistema operacional?

Resultado esperado:

- o aluno entende validacao manual de cadeia;
- o aluno entende que confianca depende da CA conhecida pelo cliente.

## Exercicio 4: Inspecao Do Certificado

Execute:

```bash
openssl x509 -in certs/localhost.crt -noout -subject -issuer -dates
```

Depois execute:

```bash
openssl x509 -in certs/localhost.crt -noout -text
```

Responda:

1. Qual e o `Subject` do certificado?
2. Qual e o `Issuer`?
3. Qual e a validade?
4. Onde aparece `DNS:localhost`?
5. Onde aparece `IP Address:127.0.0.1`?

Resultado esperado:

- o aluno localiza CN, issuer, validade e SAN;
- o aluno entende que navegadores modernos dependem de SAN para validar nomes.

## Exercicio 5: Handshake TLS

Execute:

```bash
openssl s_client -connect localhost:18443 -servername localhost -CAfile certs/lab-ca.crt
```

Responda:

1. O certificado foi verificado com sucesso?
2. Qual protocolo TLS foi negociado?
3. Qual cifra aparece na conexao?
4. Por que `-servername localhost` e relevante em servidores com SNI?

Resultado esperado:

- o aluno observa o handshake TLS;
- o aluno entende que SNI permite selecionar certificado por nome de servidor.

## Exercicio 6: Relacao Com Let's Encrypt

Responda:

1. Por que Let's Encrypt precisa validar controle de dominio?
2. Por que `localhost` nao e um bom alvo para certificado publico tradicional?
3. Qual desafio ACME usa um arquivo em `/.well-known/acme-challenge/`?
4. Qual desafio ACME usa registro TXT no DNS?
5. Em que situacao o DNS-01 costuma ser melhor que HTTP-01?

Resultado esperado:

- o aluno conecta o lab local com emissao publica real;
- o aluno entende que Let's Encrypt automatiza a validacao e emissao para dominios controlados.

## Consolidacao Individual

Preencha a tabela:

| Pergunta | Resposta |
| --- | --- |
| Porta HTTP usada no lab |  |
| Porta HTTPS usada no lab |  |
| Arquivo da CA local |  |
| Certificado do servidor |  |
| Chave privada do servidor |  |
| Principal diferenca entre HTTP e HTTPS |  |
| Motivo do erro em HTTPS sem `--cacert` |  |
| Desafio ACME mais comum para sites simples |  |

Depois escreva um paragrafo respondendo:

> Como a cadeia de confianca muda a forma como um cliente decide se deve confiar em um servidor HTTPS?

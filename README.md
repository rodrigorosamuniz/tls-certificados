# Lab: TLS, Certificados E HTTPS

Este laboratório mostra como HTTPS funciona na prática usando um ambiente local reproduzivel com Docker, Python e OpenSSL.

O objetivo nao e obter um certificado público real para `localhost`. O objetivo e entender os blocos fundamentais:

- diferenca entre HTTP e HTTPS;
- chave privada, certificado de servidor e CA;
- Subject Alternative Name (SAN);
- erro de confianca em certificados desconhecidos;
- validação manual com uma CA local;
- leitura de certificado e handshake com `openssl`;
- onde Let's Encrypt entra em um ambiente real.

## Arquivos

```text
lab_tls_certificados_https.ipynb
README.md
EXERCISES.md
docker-compose.yml
requirements.txt
app/server.py
scripts/generate_certs.py
scripts/inspect_cert.py
tests/
certs/.gitkeep
```

## Pré-requisitos

Para a trilha principal:

- Docker;
- Python 3.10 ou superior;
- OpenSSL;
- terminal com `curl`.

No macOS e Linux, `openssl` e `curl` normalmente ja existem. No Windows, use WSL ou Git Bash para uma experiencia mais parecida com os comandos abaixo.

## Opcao Recomendada: Rodar Localmente Com Docker

Entre na pasta do lab:

```bash
git clone https://github.com/rodrigorosamuniz/tls-certificados.git
cd tls-certificados
```

Gere a CA local e o certificado de servidor para `localhost`:

```bash
python3 scripts/generate_certs.py --output-dir certs
```

Suba os servidores:

```bash
docker compose up
```

O Compose sobe dois servicos:

- HTTP em `http://localhost:18080`;
- HTTPS em `https://localhost:18443`.

Observacao: internamente os containers usam as portas `8080` e `8443`; no seu computador, o Docker publica em `18080` e `18443` para reduzir conflitos com servicos locais.

Em outro terminal, teste HTTP:

```bash
curl -v http://localhost:18080/
```

Teste HTTPS sem confiar na CA local:

```bash
curl -v https://localhost:18443/
```

Esse comando deve falhar com erro de certificado, porque o sistema operacional nao conhece a CA local do lab.

Teste HTTPS informando a CA local:

```bash
curl --cacert certs/lab-ca.crt -v https://localhost:18443/
```

Esse comando deve funcionar, porque voce informou explicitamente qual CA deve ser usada para validar o certificado.

Quando terminar:

```bash
docker compose down
```

## Como Usar O Notebook

Abra o notebook:

```text
lab_tls_certificados_https.ipynb
```

Execute as células em ordem. O notebook guia o aluno por:

1. gerar certificados;
2. inspecionar campos do certificado;
3. subir os servidores com Docker;
4. testar HTTP e HTTPS;
5. comparar falha de confianca e validação com CA local;
6. analisar o handshake TLS com `openssl s_client`;
7. conectar o aprendizado com Let's Encrypt.

O notebook usa comandos de terminal. Em ambientes Jupyter locais, execute as células normalmente. No Colab, a parte conceitual funciona, mas Docker normalmente nao esta disponivel. Para Colab, use o notebook como roteiro de leitura e execute os comandos em uma maquina local ou VM.

## Onde Entra O Let's Encrypt

Let's Encrypt emite certificados publicamente confiaveis para nomes de dominio, usando o protocolo ACME. Em geral, o cliente ACME precisa provar controle do dominio por desafios como:

- HTTP-01: disponibilizar um token em `http://SEU_DOMINIO/.well-known/acme-challenge/...`, normalmente pela porta 80;
- DNS-01: publicar um registro TXT em `_acme-challenge.SEUDOMINIO`;
- TLS-ALPN-01: responder um desafio especifico na camada TLS.

Por isso, `localhost` e um subdominio aleatorio de tunel nao substituem automaticamente um dominio controlado. Para emissao real, use um dominio seu, DNS configurado e um servidor acessivel publicamente.

Este lab usa uma CA local para ensinar a mecanica de certificados sem depender de dominio, DNS, portas publicas ou creditos de servico.

## Extensao Opcional: Certbot Com Dominio Real

Use somente se voce tiver um dominio controlado e entender o impacto de expor um servico publicamente.

Exemplo conceitual com HTTP-01/webroot:

```bash
sudo certbot certonly --webroot \
  --webroot-path /var/www/html \
  -d exemplo.seudominio.com
```

Em aula, prefira explicar esse fluxo depois que os alunos entenderem a diferenca entre CA local, certificado de servidor, cadeia de confianca e validação de dominio.

## Testes Do Lab

Os scripts do lab possuem testes com `unittest`:

```bash
python3 -m unittest discover tests
```

## Cuidados Didáticos

Nao use chaves privadas reais, dominios corporativos, servidores de producao ou certificados validos da sua organizacao neste lab.

Os certificados gerados aqui sao didáticos e devem ficar apenas no ambiente local. A pasta `certs/` esta configurada para nao versionar arquivos sensíveis gerados durante a execução.

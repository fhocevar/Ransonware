# Python Malware Simulation Lab

**Laboratório Educacional de Cibersegurança — DIO**

Simulação controlada de ransomware utilizando Python, criptografia Fernet e Docker, com recuperação de arquivos por chave e validação de integridade SHA-256.

> **Aviso:** Este projeto possui finalidade exclusivamente educacional. O simulador trabalha com três arquivos fictícios, em um volume Docker dedicado, sem montar diretórios pessoais do computador. Não foi desenvolvido para criptografar arquivos reais, realizar extorsão ou comprometer sistemas.

---

## 1. Visão geral

Este projeto foi desenvolvido como parte de um desafio prático de cibersegurança da **Digital Innovation One (DIO)**.

O objetivo é compreender, por meio de uma simulação controlada, os princípios técnicos envolvidos em um ataque de ransomware e os mecanismos necessários para recuperar informações criptografadas.

O laboratório demonstra:

- Criação de arquivos fictícios.
- Geração de uma chave criptográfica aleatória.
- Criptografia simétrica utilizando Fernet.
- Armazenamento da chave em arquivo separado.
- Exibição de uma mensagem fictícia de ransomware.
- Recuperação mediante fornecimento manual da chave.
- Validação da integridade dos arquivos utilizando SHA-256.
- Isolamento do ambiente de execução com Docker.
- Aplicação de restrições de segurança no contêiner.

O projeto também prevê outros componentes educacionais, como simulação controlada de captura de teclas e estudos de mecanismos de defesa. Esses componentes devem ser documentados e validados separadamente.

### 1.1 Objetivos de aprendizagem

Ao concluir o laboratório de ransomware, espera-se compreender:

1. A diferença entre criptografia e descriptografia.
2. O papel de uma chave criptográfica.
3. O funcionamento básico da criptografia simétrica.
4. A importância da proteção e recuperação das chaves.
5. Como verificar a integridade de arquivos.
6. Como utilizar contêineres para executar experimentos de segurança.
7. Como aplicar o princípio do menor privilégio.
8. Por que backups, segregação de privilégios e estratégias de recuperação são importantes contra ransomware.

---

## 2. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Linguagem de programação do simulador |
| cryptography 50.0.2 | Implementação da criptografia Fernet |
| Fernet | Criptografia simétrica autenticada |
| SHA-256 | Verificação da integridade dos arquivos |
| Docker | Execução isolada |
| Docker Volume | Persistência dos arquivos fictícios e da chave |
| Linux / Zorin OS | Sistema operacional utilizado no desenvolvimento |
| Git | Versionamento do projeto |
| GitHub | Publicação e documentação |

### 2.1 Ambiente utilizado

O laboratório foi desenvolvido e executado em:

- Sistema operacional: Zorin OS 18.1 Core.
- Equipamento: Dell Inspiron 5547.
- Docker: 29.5.3.
- Imagem-base: `python:3.12-slim`.
- Imagem do laboratório: `dio-malware-lab:4.0`.
- Volume persistente: `dio-malware-lab-data`.
- Usuário de execução no contêiner: `labuser`.
- UID/GID: `10001:10001`.

A versão local do Python não precisa ser a mesma do contêiner para executar o laboratório pelo Docker.

---

## 3. Estrutura do projeto

O repositório está organizado para comportar os diferentes exercícios de cibersegurança.

```text
python-malware-simulation-lab/
├── ransomware/
│   ├── simulator.py
│   └── recovery_lab.py
│
├── keylogger/
│
├── defense/
│
├── tests/
│
├── docs/
│
├── sandbox/
│   └── samples/
│
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

### Descrição dos diretórios

| Diretório ou arquivo | Descrição |
|---|---|
| `ransomware/simulator.py` | Simulador principal de criptografia e recuperação |
| `ransomware/recovery_lab.py` | Arquivo auxiliar de experimentação, não utilizado no fluxo validado |
| `keylogger/` | Diretório reservado ao laboratório educacional de captura de teclas |
| `defense/` | Diretório destinado aos mecanismos de defesa e mitigação |
| `tests/` | Testes automatizados do projeto |
| `docs/` | Documentação complementar e evidências |
| `sandbox/samples/` | Área local destinada a exemplos e arquivos de teste |
| `Dockerfile` | Definição da imagem Docker |
| `requirements.txt` | Dependências Python do projeto |
| `.gitignore` | Exclusões do controle de versão |
| `README.md` | Documentação principal |

**Importante:** no fluxo Docker validado, os arquivos criptografados, recuperados e a chave não são armazenados diretamente nessas pastas do repositório. Eles ficam dentro do volume Docker dedicado.

O arquivo `recovery_lab.py` não é necessário para executar a simulação documentada neste README.

---

## 4. Arquitetura do laboratório

O laboratório utiliza uma imagem Docker e um volume persistente.

```text
                 ZORIN OS / LINUX
                         |
                         |
                    Docker Engine
                         |
                         v
             +-----------------------+
             | dio-malware-lab:4.0   |
             |                       |
             | Python 3.12           |
             | cryptography / Fernet |
             | simulator.py          |
             |                       |
             | Usuário: labuser      |
             | UID/GID: 10001        |
             +-----------+-----------+
                         |
                         |
                  Volume Docker
                         |
                         v
                  /lab-data/
                         |
          +--------------+--------------+
          |              |              |
       samples/       encrypted/     recovered/
          |              |              |
       Originais      Cópias          Arquivos
       fictícios      cifradas        recuperados
                         |
                    RANSOM_NOTE.txt

                  /lab-data/lab.key
                  Chave de recuperação
```

### 4.1 Separação entre host e contêiner

O sistema operacional hospedeiro é responsável por executar o Docker.

O código do simulador é executado dentro do contêiner.

Os dados do laboratório são armazenados em um volume Docker dedicado.

Os comandos utilizados não incluem montagem de diretórios pessoais, como `/home`, `Documents` ou `Downloads`.

Isso limita o escopo dos arquivos acessíveis pelo simulador.

### 4.2 Persistência

O contêiner é iniciado com `--rm`, sendo removido ao terminar a execução.

Entretanto, o volume `dio-malware-lab-data` permanece disponível.

Essa persistência é necessária porque a criptografia e a recuperação são realizadas em execuções separadas.

---

## 5. Requisitos

Antes de executar o projeto, é necessário ter:

- Linux com Docker instalado e operacional.
- Permissão para executar comandos Docker.
- Código-fonte do projeto disponível localmente.
- Acesso à imagem-base `python:3.12-slim` para a construção inicial.
- Espaço disponível para a imagem Docker e o pequeno volume de teste.

### 5.1 Verificar o Docker

```bash
docker --version
```

Verificar o funcionamento do Docker Engine:

```bash
docker info
```

### 5.2 Acessar o projeto

No ambiente utilizado durante o desenvolvimento:

```bash
cd ~/projetos/python-malware-simulation-lab
```

Verificar os arquivos:

```bash
ls -la
```

Verificar o Dockerfile:

```bash
cat Dockerfile
```

---

## 6. Dockerfile

A imagem utilizada no laboratório é definida por:

```dockerfile
FROM python:3.12-slim

RUN groupadd -g 10001 labgroup \
    && useradd -u 10001 -g labgroup -m labuser

WORKDIR /app

RUN pip install --no-cache-dir cryptography==50.0.2

COPY ransomware/ ./ransomware/

USER labuser

ENTRYPOINT ["python", "-m", "ransomware.simulator"]
```

### 6.1 Explicação

**Imagem-base**

```dockerfile
FROM python:3.12-slim
```

Utiliza uma imagem Python compacta.

**Usuário não privilegiado**

```dockerfile
RUN groupadd -g 10001 labgroup \
    && useradd -u 10001 -g labgroup -m labuser
```

Cria um usuário específico para a execução do laboratório.

**Dependência criptográfica**

```dockerfile
RUN pip install --no-cache-dir cryptography==50.0.2
```

Instala a biblioteca utilizada para gerar chaves e criptografar os arquivos fictícios.

**Código-fonte**

```dockerfile
COPY ransomware/ ./ransomware/
```

Copia o módulo do simulador para a imagem.

**Execução**

```dockerfile
USER labuser

ENTRYPOINT ["python", "-m", "ransomware.simulator"]
```

Define a execução como usuário não privilegiado e configura o simulador como ponto de entrada.

O comando informado após o nome da imagem é encaminhado ao simulador.

Por exemplo:

```text
encrypt
decrypt
```

---

## 7. Preparação do laboratório

Esta seção apresenta os comandos utilizados para preparar o ambiente.

### Passo 1 — Construir a imagem

Na raiz do projeto:

```bash
docker build -t dio-malware-lab:4.0 .
```

O Docker executará as etapas do Dockerfile.

Ao final, deverá indicar que a construção foi concluída.

Verificar a imagem:

```bash
docker images dio-malware-lab
```

**Observação:** reconstruir a imagem com a mesma tag atualiza a referência da imagem, mas não remove automaticamente o volume de dados.

### Passo 2 — Criar o volume persistente

```bash
docker volume create dio-malware-lab-data
```

Resultado esperado:

```text
dio-malware-lab-data
```

Verificar o volume:

```bash
docker volume ls
```

### Passo 3 — Configurar as permissões

O contêiner executa com UID/GID `10001:10001`.

Por padrão, o volume recém-criado pode pertencer ao usuário `root`, impedindo a escrita pelo usuário do laboratório.

Execute:

```bash
docker run --rm \
  --network none \
  --read-only \
  --user 0:0 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,volume-nocopy \
  --entrypoint /bin/sh \
  dio-malware-lab:4.0 \
  -c 'chown 10001:10001 /lab-data && chmod 700 /lab-data'
```

Esse comando ajusta as permissões do diretório raiz do volume.

Ele não executa a criptografia.

**Atenção:** o ajuste é feito em um contêiner temporário com usuário root. As execuções normais do simulador continuam utilizando o usuário não privilegiado `labuser`.

### Passo 4 — Validar as permissões

```bash
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,volume-nocopy \
  --entrypoint /bin/sh \
  dio-malware-lab:4.0 \
  -c 'id; ls -ldn /lab-data; test -w /lab-data && echo "GRAVACAO_OK" || echo "SEM_PERMISSAO"'
```

Resultado esperado:

```text
uid=10001(labuser) gid=10001(labgroup) groups=10001(labgroup)
drwx------ 2 10001 10001 ... /lab-data
GRAVACAO_OK
```

Se aparecer `GRAVACAO_OK`, o volume está preparado.

---

## 8. Executar a simulação de ransomware

O simulador possui duas operações principais:

| Operação | Função |
|---|---|
| `encrypt` | Cria os arquivos fictícios, gera uma chave e criptografa cópias |
| `decrypt` | Solicita a chave e recupera os arquivos |

### Passo 1 — Executar a criptografia

```bash
docker run --rm -it \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 64 \
  --memory 256m \
  --user 10001:10001 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,volume-nocopy \
  dio-malware-lab:4.0 encrypt
```

### 8.1 O que acontece

O programa:

1. Verifica a existência do volume `/lab-data`.
2. Prepara os diretórios necessários.
3. Cria os três arquivos fictícios.
4. Verifica o conteúdo esperado desses arquivos.
5. Gera uma nova chave Fernet.
6. Criptografa cópias dos arquivos.
7. Salva a chave em `lab.key`.
8. Grava uma mensagem fictícia de ransomware.
9. Exibe o resultado no terminal.

### 8.2 Arquivos utilizados

| Arquivo | Conteúdo |
|---|---|
| `documento.txt` | Documento fictício para teste de segurança |
| `financeiro.txt` | Dados financeiros simulados |
| `clientes.txt` | Nomes de usuários fictícios |

Nenhum desses arquivos contém dados reais.

### 8.3 Resultado obtido no laboratório

A execução validada produziu:

```text
[CRIADO] documento.txt
[CRIADO] financeiro.txt
[CRIADO] clientes.txt

[CRIPTOGRAFADO] documento.txt
[CRIPTOGRAFADO] financeiro.txt
[CRIPTOGRAFADO] clientes.txt

============================================
      SIMULAÇÃO DE RANSOMWARE - DIO
============================================

Seus arquivos fictícios foram criptografados.
Para recuperá-los, informe a chave de teste.
Nenhum pagamento é necessário.
Nenhum arquivo pessoal foi afetado.

[OK] Chave salva em /lab-data/lab.key
[INFO] A chave de recuperação não será exibida no terminal.
[SUCESSO] Simulação de criptografia concluída.
```

### 8.4 Arquivos produzidos

Após a criptografia, o volume contém uma estrutura semelhante a:

```text
/lab-data/
├── lab.key
│
├── samples/
│   ├── documento.txt
│   ├── financeiro.txt
│   └── clientes.txt
│
├── encrypted/
│   ├── documento.txt.encrypted
│   ├── financeiro.txt.encrypted
│   ├── clientes.txt.encrypted
│   └── RANSOM_NOTE.txt
│
└── recovered/
```

O simulador **preserva os arquivos originais fictícios** e criptografa cópias.

Essa decisão permite verificar posteriormente se a recuperação produziu dados idênticos aos originais.

---

## 9. Chave criptográfica

O simulador utiliza a biblioteca Fernet para gerar uma chave aleatória:

```python
key = Fernet.generate_key()
```

Essa chave é utilizada para criptografar os arquivos fictícios.

### 9.1 Armazenamento

A chave é salva em:

```text
/lab-data/lab.key
```

O arquivo é criado com permissões restritivas.

### 9.2 Por que a chave não aparece na criptografia?

A versão validada do simulador não exibe a chave durante a operação `encrypt`.

Isso permite separar duas atividades:

- A execução da criptografia.
- A consulta administrativa da chave para recuperação.

No laboratório, a chave permanece disponível ao responsável pelo exercício.

**Importante:** essa é uma simplificação educacional. O armazenamento da chave no mesmo volume dos dados não representa um mecanismo seguro de gerenciamento de chaves para produção.

---

## 10. Consultar a chave de recuperação

A consulta da chave é realizada explicitamente pelo responsável pelo laboratório.

Execute:

```bash
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --user 10001:10001 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,readonly \
  --entrypoint /bin/sh \
  dio-malware-lab:4.0 \
  -c 'cat /lab-data/lab.key; printf "\n"'
```

O comando lê o arquivo `lab.key` e apresenta seu conteúdo no terminal.

**Copie a chave exibida.**

Ela será utilizada na etapa de recuperação.

Não é necessário alterar o código, reconstruir a imagem ou recriar o volume para consultar a chave.

### Cuidados

- Não publique chaves reais em repositórios Git.
- Não utilize a chave fictícia deste laboratório para proteger dados pessoais.
- Não inclua `lab.key` em commits.
- Evite registrar chaves em capturas de tela ou evidências públicas.

---

## 11. Recuperar os arquivos criptografados

### Passo 1 — Iniciar a recuperação

Execute:

```bash
docker run --rm -it \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 64 \
  --memory 256m \
  --user 10001:10001 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,volume-nocopy \
  dio-malware-lab:4.0 decrypt
```

### Passo 2 — Informar a chave

O terminal apresentará:

```text
========== RECUPERAÇÃO - DIO ==========

Informe a chave gerada durante a criptografia.
A digitação ficará oculta no terminal.

Chave de recuperação (1/3):
```

Cole a chave obtida de `lab.key` e pressione Enter.

**A digitação é oculta.** Isso significa que os caracteres não aparecerão no terminal enquanto a chave é informada.

### Passo 3 — Validar a chave

O simulador verifica:

1. Se a chave possui um formato aceito pelo Fernet.
2. Se corresponde à chave armazenada no laboratório.
3. Se os arquivos criptografados podem ser descriptografados.
4. Se o conteúdo recuperado corresponde ao conteúdo original.

O simulador permite até três tentativas por execução.

### Passo 4 — Confirmar a recuperação

Na execução validada, a primeira tentativa apresentou:

```text
[ERRO] Formato de chave inválido.
```

Na segunda tentativa, a chave correta foi aceita:

```text
[OK] Chave correta!

[RECUPERADO] documento.txt - SHA-256 OK
[RECUPERADO] financeiro.txt - SHA-256 OK
[RECUPERADO] clientes.txt - SHA-256 OK

[SUCESSO] Todos os arquivos foram recuperados!
[OK] Arquivos salvos em /lab-data/recovered
```

**Resultado: recuperação concluída com sucesso.**

---

## 12. Verificação de integridade SHA-256

O laboratório utiliza SHA-256 para confirmar que os dados recuperados são idênticos aos originais.

A função utilizada é:

```python
import hashlib

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
```

O simulador calcula o hash do conteúdo recuperado e o compara com o hash do conteúdo original fictício.

A recuperação somente é considerada válida quando os valores coincidem.

### 12.1 Por que isso é importante?

Descriptografar um arquivo não é suficiente para garantir que a recuperação foi correta.

É necessário confirmar que:

- O conteúdo foi restaurado integralmente.
- Nenhum dado foi alterado durante o processo.
- O arquivo recuperado corresponde ao original esperado.

A comparação SHA-256 complementa a verificação criptográfica realizada pelo Fernet.

### 12.2 Conferência manual dos arquivos

Para listar os arquivos recuperados:

```bash
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --user 10001:10001 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,readonly \
  --entrypoint /bin/ls \
  dio-malware-lab:4.0 \
  -l /lab-data/recovered
```

Resultado observado:

```text
total 12
-rw------- 1 labuser labgroup 42 ... clientes.txt
-rw------- 1 labuser labgroup 45 ... documento.txt
-rw------- 1 labuser labgroup 46 ... financeiro.txt
```

Os três arquivos foram recuperados e permaneceram disponíveis no volume Docker.

---

## 13. Controles de segurança aplicados

O laboratório utiliza restrições adicionais na execução dos contêineres.

### 13.1 Rede desabilitada

```bash
--network none
```

O contêiner não recebe conectividade de rede externa.

### 13.2 Sistema de arquivos da imagem somente leitura

```bash
--read-only
```

Impede gravações no sistema de arquivos principal do contêiner.

O volume `/lab-data` continua gravável durante as operações de criptografia e recuperação.

### 13.3 Remoção de capacidades Linux

```bash
--cap-drop ALL
```

Remove capacidades adicionais do processo no contêiner.

### 13.4 Prevenção de elevação de privilégios

```bash
--security-opt no-new-privileges
```

Restringe mecanismos de aquisição de privilégios adicionais.

### 13.5 Limite de processos

```bash
--pids-limit 64
```

Limita a quantidade de processos disponíveis ao contêiner.

### 13.6 Limite de memória

```bash
--memory 256m
```

Limita a memória utilizada pelo contêiner.

### 13.7 Usuário não privilegiado

```bash
--user 10001:10001
```

Executa o simulador com o usuário `labuser`, em vez de root.

### 13.8 Ausência de bind mounts

O laboratório não utiliza montagens como:

```text
-v /home:/home
-v ~/Documents:/data
-v /:/host
```

Em vez disso, utiliza um volume Docker nomeado:

```text
dio-malware-lab-data
```

Essa escolha reduz o risco de acesso acidental a arquivos pessoais do sistema hospedeiro.

**Limitação:** Docker oferece isolamento de processos e sistemas de arquivos, mas não deve ser tratado como uma barreira absoluta contra software malicioso desconhecido. Este projeto utiliza apenas código educacional conhecido e arquivos fictícios.

---

## 14. Proteções implementadas no simulador

Além do isolamento Docker, o código aplica restrições sobre os arquivos processados.

### 14.1 Lista fixa de arquivos

O simulador trabalha exclusivamente com:

```text
documento.txt
financeiro.txt
clientes.txt
```

Não existe varredura automática do sistema de arquivos.

### 14.2 Diretório de trabalho fixo

```python
ROOT = Path("/lab-data")
```

O simulador utiliza diretórios específicos dentro do volume Docker.

### 14.3 Proteção contra links simbólicos

O código rejeita links simbólicos em caminhos relevantes e utiliza `O_NOFOLLOW` nas operações de leitura e escrita.

### 14.4 Limite de tamanho

Os arquivos processados possuem um limite de leitura de 4096 bytes.

### 14.5 Proteção contra sobrescrita

A criação de arquivos utiliza `O_EXCL`, impedindo a substituição silenciosa de arquivos existentes.

### 14.6 Preservação da chave

Se uma simulação já tiver criado `lab.key` ou arquivos criptografados, uma nova operação `encrypt` no mesmo volume será recusada.

Isso evita sobrescrever a chave de uma execução anterior.

### 14.7 Validação do conteúdo

O simulador compara os arquivos fictícios com os conteúdos esperados antes de executar a criptografia.

### 14.8 Recuperação sem sobrescrita

A operação `decrypt` também evita substituir arquivos recuperados que já existam.

---

## 15. Repetir o laboratório

O volume persiste entre execuções.

Por isso, **não execute `encrypt` repetidamente no mesmo volume** esperando gerar uma nova chave.

O simulador foi desenvolvido para preservar o estado de uma simulação já existente.

### 15.1 Repetir apenas a consulta

A chave pode ser consultada novamente pelo comando da seção 10.

### 15.2 Repetir apenas a recuperação

Se os arquivos já foram recuperados, uma nova execução de `decrypt` no mesmo volume encontrará arquivos existentes e poderá recusar a sobrescrita.

### 15.3 Criar uma nova simulação independente

A maneira mais segura de começar outra simulação sem apagar a anterior é utilizar um novo volume.

Por exemplo:

```bash
docker volume create dio-malware-lab-data-02
```

Preparar as permissões:

```bash
docker run --rm \
  --network none \
  --read-only \
  --user 0:0 \
  --mount type=volume,source=dio-malware-lab-data-02,target=/lab-data,volume-nocopy \
  --entrypoint /bin/sh \
  dio-malware-lab:4.0 \
  -c 'chown 10001:10001 /lab-data && chmod 700 /lab-data'
```

Depois, nos comandos de criptografia, consulta e recuperação, substituir:

```text
source=dio-malware-lab-data
```

por:

```text
source=dio-malware-lab-data-02
```

O novo volume terá seus próprios arquivos fictícios e sua própria chave.

**Não misture volumes entre as etapas.** A recuperação deve utilizar o mesmo volume empregado na criptografia.

---

## 16. Consultar o estado do laboratório

### 16.1 Listar imagens

```bash
docker images dio-malware-lab
```

### 16.2 Listar volumes

```bash
docker volume ls
```

### 16.3 Inspecionar o volume

```bash
docker volume inspect dio-malware-lab-data
```

### 16.4 Listar os arquivos do laboratório

```bash
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --user 10001:10001 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,readonly \
  --entrypoint /bin/ls \
  dio-malware-lab:4.0 \
  -la /lab-data
```

### 16.5 Listar os arquivos criptografados

```bash
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --user 10001:10001 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,readonly \
  --entrypoint /bin/ls \
  dio-malware-lab:4.0 \
  -l /lab-data/encrypted
```

### 16.6 Listar os arquivos recuperados

```bash
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --user 10001:10001 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,readonly \
  --entrypoint /bin/ls \
  dio-malware-lab:4.0 \
  -l /lab-data/recovered
```

---

## 17. Resolução de problemas

### Problema 1 — `Operation not permitted` no `chown`

Erro:

```text
chown: changing ownership of '/lab-data': Operation not permitted
```

**Causa observada no laboratório:**

O comando de configuração de permissões havia sido executado com:

```bash
--cap-drop ALL
```

Essa restrição removeu a capacidade necessária para alterar a propriedade do volume.

**Solução utilizada:**

Executar o ajuste inicial sem `--cap-drop ALL`, mantendo `--user 0:0`.

```bash
docker run --rm \
  --network none \
  --read-only \
  --user 0:0 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,volume-nocopy \
  --entrypoint /bin/sh \
  dio-malware-lab:4.0 \
  -c 'chown 10001:10001 /lab-data && chmod 700 /lab-data'
```

O ajuste foi concluído com sucesso.

### Problema 2 — `SEM_PERMISSAO`

Resultado:

```text
uid=10001(labuser) gid=10001(labgroup)
drwxr-xr-x 2 0 0 ... /lab-data
SEM_PERMISSAO
```

**Causa:**

O volume pertencia ao usuário root e não permitia escrita pelo usuário `labuser`.

**Solução:**

Executar a configuração de permissões descrita na seção 7.

Resultado confirmado:

```text
uid=10001(labuser) gid=10001(labgroup)
drwx------ 2 10001 10001 ... /lab-data
GRAVACAO_OK
```

### Problema 3 — Formato de chave inválido

Mensagem:

```text
[ERRO] Formato de chave inválido.
```

**Possíveis causas:**

- Chave copiada incorretamente.
- Caracteres ausentes.
- Caracteres adicionais.
- Conteúdo diferente de uma chave Fernet válida.

**Solução:**

Consultar novamente o arquivo `lab.key` e copiar apenas a chave, sem o prompt do terminal.

No teste realizado, a segunda tentativa foi aceita e a recuperação foi concluída.

### Problema 4 — Chave incorreta

Mensagem:

```text
[ERRO] Chave incorreta.
```

**Causa:**

A chave possui formato válido, mas não corresponde à chave armazenada no volume utilizado.

**Solução:**

Confirmar que o comando de consulta e o comando de recuperação utilizam o mesmo volume Docker.

### Problema 5 — Simulação já existente

Mensagem semelhante a:

```text
Já existe uma simulação neste volume.
A chave anterior foi preservada.
```

**Causa:**

O volume já contém uma simulação.

**Solução:**

Utilizar o estado existente ou criar um novo volume para uma nova execução.

Não apague a chave de uma simulação que ainda deseja recuperar.

### Problema 6 — Arquivo recuperado já existe

Mensagem semelhante a:

```text
Arquivo recuperado já existe
```

**Causa:**

O simulador impede sobrescrever resultados de uma recuperação anterior.

**Solução:**

Consultar os arquivos já recuperados ou iniciar uma nova simulação em outro volume.

### Problema 7 — Chave aparece junto ao prompt

O arquivo `lab.key` não contém necessariamente uma quebra de linha ao final.

Ao utilizar apenas `cat`, o prompt pode aparecer imediatamente após a chave.

Para melhorar a visualização:

```bash
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --user 10001:10001 \
  --mount type=volume,source=dio-malware-lab-data,target=/lab-data,readonly \
  --entrypoint /bin/sh \
  dio-malware-lab:4.0 \
  -c 'cat /lab-data/lab.key; printf "\n"'
```

---

## 18. Limpeza do ambiente

**Atenção:** a limpeza do volume apaga os arquivos fictícios, a chave de recuperação e os resultados da simulação.

### 18.1 Remover a imagem

```bash
docker rmi dio-malware-lab:4.0
```

A remoção da imagem não remove automaticamente o volume.

### 18.2 Remover o volume

Execute somente quando não precisar mais dos resultados:

```bash
docker volume rm dio-malware-lab-data
```

Isso remove os dados persistidos nesse volume, incluindo `lab.key`.

### 18.3 Verificar a limpeza

```bash
docker images dio-malware-lab
```

```bash
docker volume ls
```

**Recomendação:** evite comandos de limpeza global, como `docker system prune --volumes`, durante o desenvolvimento, pois podem afetar recursos de outros projetos.

---

## 19. Evidências da execução

O laboratório foi executado com sucesso em ambiente Linux, utilizando a imagem `dio-malware-lab:4.0`.

### 19.1 Preparação

| Verificação | Resultado |
|---|---|
| Construção da imagem Docker | Concluída |
| Criação do volume | Concluída |
| Configuração de permissões | Concluída |
| Validação de escrita | `GRAVACAO_OK` |

### 19.2 Criptografia

| Arquivo | Resultado |
|---|---|
| `documento.txt` | Criptografado |
| `financeiro.txt` | Criptografado |
| `clientes.txt` | Criptografado |
| `lab.key` | Gerado e armazenado |
| `RANSOM_NOTE.txt` | Gerado |

### 19.3 Recuperação

| Verificação | Resultado |
|---|---|
| Validação da chave | Aprovada na segunda tentativa |
| Recuperação de `documento.txt` | SHA-256 OK |
| Recuperação de `financeiro.txt` | SHA-256 OK |
| Recuperação de `clientes.txt` | SHA-256 OK |
| Existência dos três arquivos recuperados | Confirmada |

### 19.4 Resultado final

```text
[OK] Chave correta!

[RECUPERADO] documento.txt - SHA-256 OK
[RECUPERADO] financeiro.txt - SHA-256 OK
[RECUPERADO] clientes.txt - SHA-256 OK

[SUCESSO] Todos os arquivos foram recuperados!
[OK] Arquivos salvos em /lab-data/recovered
```

**Status do laboratório de ransomware: VALIDADO.**

---

## 20. Medidas de prevenção contra ransomware

O laboratório permite discutir controles defensivos utilizados em ambientes reais.

### 20.1 Backups

Manter cópias de segurança atualizadas, protegidas e testadas.

Priorizar estratégias com cópias offline ou imutáveis quando apropriado.

### 20.2 Princípio do menor privilégio

Usuários e aplicações devem possuir somente as permissões necessárias.

### 20.3 Segmentação de rede

Separar sistemas e serviços para limitar movimentação lateral em caso de comprometimento.

### 20.4 Atualizações de segurança

Aplicar correções em sistemas operacionais, bibliotecas, aplicações e serviços.

### 20.5 Proteção de endpoints

Utilizar mecanismos de detecção e resposta para identificar comportamentos suspeitos.

### 20.6 Monitoramento

Observar eventos como:

- Alterações anormais em grande quantidade de arquivos.
- Processos desconhecidos manipulando documentos.
- Tentativas de desabilitar ferramentas de proteção.
- Acessos inesperados a compartilhamentos.
- Atividades suspeitas envolvendo backups.

### 20.7 Plano de resposta a incidentes

Definir procedimentos para:

1. Identificação do incidente.
2. Contenção dos sistemas afetados.
3. Preservação de evidências.
4. Investigação.
5. Erradicação da ameaça.
6. Recuperação dos serviços.
7. Revisão das causas e controles preventivos.

---

## 21. Limitações do laboratório

Este projeto não implementa um ransomware real.

A simulação apresenta limitações intencionais:

- Processa somente três arquivos fictícios.
- Não procura arquivos no computador.
- Não acessa diretórios pessoais do hospedeiro.
- Não executa propagação pela rede.
- Não possui comunicação com servidores externos.
- Não implementa persistência maliciosa.
- Não utiliza mecanismos de ocultação.
- Não realiza exfiltração de dados.
- Não exige pagamento.
- Não destrói os arquivos originais.
- Mantém uma chave de recuperação disponível ao administrador do laboratório.

Essas limitações são deliberadas e compatíveis com a finalidade educacional.

---

## 22. Próximas etapas

O repositório prevê três frentes de estudo.

| Laboratório | Objetivo | Situação |
|---|---|---|
| Ransomware simulado | Criptografia, recuperação e integridade | Concluído e validado |
| Keylogger educacional | Estudo controlado de eventos de teclado | Pendente |
| Defesa e mitigação | Estudo de controles e detecção | Pendente |

Os laboratórios futuros deverão manter o mesmo princípio: execução controlada, dados fictícios e ausência de acesso indevido a informações pessoais.

---

## 23. Publicação no GitHub

Antes de publicar o projeto, verificar se não existem dados sensíveis ou arquivos desnecessários no repositório.

### 23.1 Verificar o estado do Git

```bash
git status
```

### 23.2 Verificar arquivos ignorados

O `.gitignore` deve excluir, quando aplicável:

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.env
*.key
lab.key
```

Os arquivos persistidos no volume Docker não fazem parte automaticamente do repositório Git.

### 23.3 Adicionar os arquivos do projeto

```bash
git add README.md Dockerfile ransomware/simulator.py .gitignore
```

### 23.4 Criar o commit

```bash
git commit -m "docs: document validated Docker ransomware simulation lab"
```

### 23.5 Publicar

Depois de confirmar que o repositório remoto está configurado e que não há arquivos sensíveis incluídos:

```bash
git push
```

O comando utiliza o remoto e o branch configurados no repositório local.

---

## 24. Conclusão

O laboratório demonstrou com sucesso o funcionamento de um ciclo controlado de criptografia e recuperação de arquivos.

A implementação utilizou Python, Fernet e Docker para criar um ambiente reproduzível, com dados fictícios, isolamento de rede, execução sem privilégios elevados e persistência controlada.

Durante a execução, foram identificados e corrigidos problemas de permissão no volume Docker, reforçando a importância da configuração adequada de usuários e privilégios em contêineres.

A simulação confirmou que:

- Os três arquivos fictícios foram criados.
- A chave criptográfica foi gerada e armazenada.
- As cópias dos arquivos foram criptografadas.
- A chave não foi revelada durante a criptografia.
- A recuperação exigiu o fornecimento manual da chave.
- Os três arquivos foram recuperados.
- A integridade dos conteúdos foi confirmada com SHA-256.

O exercício reforça a importância de compreender tanto o funcionamento da criptografia quanto os mecanismos de proteção, recuperação e resposta a incidentes.

**Resultado final: laboratório de ransomware educacional concluído e validado com sucesso.**

---

## 25. Referências

- [Digital Innovation One — DIO](https://www.dio.me/)
- [Python — Documentação oficial](https://docs.python.org/3/)
- [Cryptography — Fernet](https://cryptography.io/en/latest/fernet/)
- [Docker — Documentação oficial](https://docs.docker.com/)
- [NIST — Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CISA — StopRansomware](https://www.cisa.gov/stopransomware)

---

**Autor:** Fernando Augusto Hocevar  
**GitHub:** https://github.com/fhocevar  
**Projeto:** Python Malware Simulation Lab  
**Finalidade:** Educação, pesquisa e conscientização em cibersegurança.
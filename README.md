# Consulta de Veículos Sascar

Este projeto permite consultar informações de veículos através da API Sascar.

## Requisitos

- Python 3.6 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone este repositório ou baixe os arquivos do projeto

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências usando o arquivo requirements.txt:
```bash
pip install -r requirements.txt
```

## Configuração

Antes de executar o programa, você precisa ter as credenciais de acesso à API Sascar:
- Usuário
- Senha
- ID do Cliente (opcional)
- ID do Veículo (opcional)
- Placa do veículo (opcional)

## Uso

Execute o programa usando o comando:

```bash
python main.py --usuario SEU_USUARIO --senha SUA_SENHA [opções]
```

### Opções disponíveis:
- `--usuario`: Usuário da API (obrigatório)
- `--senha`: Senha da API (obrigatório)
- `--idCliente`: ID do cliente (opcional)
- `--idVeiculo`: ID do veículo (opcional)
- `--placa`: Placa do veículo (opcional)
- `--output`: Nome do arquivo de saída (padrão: veiculos.json)

### Exemplos:

Consulta básica:
```bash
python main.py --usuario seu_usuario --senha sua_senha
```

Consulta com placa específica:
```bash
python main.py --usuario seu_usuario --senha sua_senha --placa ABC1234
```

Consulta com ID do cliente:
```bash
python main.py --usuario seu_usuario --senha sua_senha --idCliente 12345
```

## Saída

O programa gera dois arquivos:
1. `veiculos.json`: Contém os dados em formato JSON
2. `veiculos.txt`: Contém os dados formatados em texto

## Observações

- O programa utiliza TLS 1.2 para comunicação segura com a API
- Os dados sensíveis (como senha) não são exibidos nos logs
- O resultado é limitado a 200 veículos por consulta 
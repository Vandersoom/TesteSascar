from zeep import Client
from zeep.transports import Transport
from requests import Session
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import json
import argparse

# Classe para forçar o uso de TLS 1.2
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1_2
        )

def main():
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Consulta de veículos via API Sascar')
    parser.add_argument('--usuario', required=True, help='Usuário da API')
    parser.add_argument('--senha', required=True, help='Senha da API')
    parser.add_argument('--idCliente', type=int, help='ID do cliente (opcional)')
    parser.add_argument('--idVeiculo', type=int, help='ID do veículo (opcional)')
    parser.add_argument('--placa', help='Placa do veículo (opcional)')
    parser.add_argument('--output', default='veiculos.json', help='Arquivo de saída (padrão: veiculos.json)')
    
    args = parser.parse_args()
    
    # URL do WSDL
    wsdl_url = 'https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl'
    
    # Configurar a sessão para usar TLS 1.2
    session = Session()
    session.mount('https://', TLSAdapter())
    transport = Transport(session=session)
    
    # Criar o cliente SOAP
    try:
        print("Conectando ao serviço SOAP...")
        client = Client(wsdl=wsdl_url, transport=transport)
        
        # Preparar os parâmetros para a chamada
        params = {
            'usuario': 'usuario aqui',
            'senha': 'senha aqui',
            'quantidade': 200
        }
        
        # Adicionar parâmetros opcionais se fornecidos
        if args.idCliente is not None:
            params['idCliente'] = args.idCliente
        
        if args.idVeiculo is not None:
            params['idVeiculo'] = args.idVeiculo
            
        if args.placa is not None:
            params['placa'] = args.placa
        
        # Imprimir parâmetros que serão usados (exceto a senha)
        print("\nParâmetros da consulta:")
        for key, value in params.items():
            if key != 'senha':
                print(f" - {key}: {value}")
        
        # Chamar o método
        print("\nChamando obterVeiculosJson...")
        result = client.service.obterVeiculosJson(**params)
        
        # Tentar fazer parse do resultado como JSON
        try:
            # O resultado pode vir diretamente como string JSON
            json_data = json.loads(result) if isinstance(result, str) else result
            print("\nResultado em formato JSON:")
            
            # Imprimir informações resumidas
            if isinstance(json_data, list):
                print(f"Total de veículos: {len(json_data)}")
                if len(json_data) > 0:
                    print("Amostra dos primeiros 2 veículos:")
                    for i, veiculo in enumerate(json_data[:2]):
                        print(f"Veículo {i+1}:")
                        print(json.dumps(veiculo, indent=2))
            else:
                print(json.dumps(json_data, indent=2))
        except (json.JSONDecodeError, TypeError):
            # Se não for um JSON válido, imprimir o resultado bruto
            print("\nResultado (não é um JSON válido):")
            print(result)
        
        # Salvar resultado completo em arquivos
        try:
            # Converter o resultado para um objeto Python
            if isinstance(result, str):
                # Primeiro, tenta fazer parse do resultado completo
                try:
                    json_data = json.loads(result)
                except json.JSONDecodeError:
                    # Se falhar, assume que é uma lista de strings JSON
                    json_data = [json.loads(item) for item in result.split(',')]
            else:
                json_data = result

            # Se ainda for uma lista de strings JSON, converte cada item
            if isinstance(json_data, list) and all(isinstance(item, str) for item in json_data):
                json_data = [json.loads(item) for item in json_data]

            # Salvar em JSON formatado
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"\nResultado completo salvo no arquivo '{args.output}'")

            # Salvar em TXT formatado
            txt_output = args.output.replace('.json', '.txt')
            with open(txt_output, 'w', encoding='utf-8') as f:
                for i, veiculo in enumerate(json_data, 1):
                    f.write(f"\n{'='*50}\n")
                    f.write(f"VEÍCULO {i}\n")
                    f.write(f"{'='*50}\n")
                    for key, value in veiculo.items():
                        f.write(f"{key}: {value}\n")
            print(f"Resultado formatado salvo no arquivo '{txt_output}'")
            
        except Exception as e:
            print("Erro ao salvar os arquivos:", str(e))
            print("Tipo do resultado:", type(result))
            if isinstance(result, str):
                print("Primeiros 100 caracteres do resultado:", result[:100])
        
    except Exception as e:
        print("Erro:", str(e))

if __name__ == "__main__":
    main()
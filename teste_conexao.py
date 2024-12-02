from mongo_connection import obter_dados

if __name__ == "__main__":
    # Teste de conexão
    origem_teste = "CVM"  # Substitua pela origem que deseja testar
    dados = obter_dados(origem_teste, limite=1)
    
    for doc in dados:
        print(doc)
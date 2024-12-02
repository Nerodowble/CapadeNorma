from mongo_connection import collection
import json
import os
from datetime import datetime

def obter_primeiro_ultimo_normativo(origem):
    """
    Função para obter o primeiro e último normativo de uma origem com base na data de emissão.
    :param origem: Nome da origem (string)
    :return: Um dicionário contendo as datas do primeiro e último normativo.
    """
    primeiro_normativo = collection.find({"origin": origem}).sort("issuance_date", 1).limit(1)
    ultimo_normativo = collection.find({"origin": origem}).sort("issuance_date", -1).limit(1)
    
    data_inicio = None
    data_fim = None

    for doc in primeiro_normativo:
        data_inicio = doc.get('issuance_date')

    for doc in ultimo_normativo:
        data_fim = doc.get('issuance_date')

    return {
        "base_de_dados_inicio": data_inicio.strftime('%Y-%m-%d') if isinstance(data_inicio, datetime) else data_inicio,
        "ultimo_normativo_atualizado": data_fim.strftime('%Y-%m-%d') if isinstance(data_fim, datetime) else data_fim
    }

def verificar_e_atualizar_resumos(arquivo_resumos="resumos.json"):
    """
    Verifica se as datas estão presentes em cada origem do arquivo de resumos e as atualiza, se necessário.
    """
    if not os.path.exists(arquivo_resumos):
        print(f"Arquivo {arquivo_resumos} não encontrado. Certifique-se de processar os resumos primeiro.")
        return

    try:
        with open(arquivo_resumos, 'r', encoding='utf-8') as f:
            resumos = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Erro ao carregar o arquivo JSON: {e}")
        print("Certifique-se de que o arquivo contém um JSON válido. Inicializando com uma lista vazia.")
        resumos = []

    origens = collection.distinct("origin")

    atualizou = False

    for origem in origens:
        resumo = next((item for item in resumos if item['origem'] == origem), None)

        if resumo:
            if 'base_de_dados_inicio' not in resumo or resumo['base_de_dados_inicio'] is None:
                resumo['base_de_dados_inicio'] = None
            if 'ultimo_normativo_atualizado' not in resumo or resumo['ultimo_normativo_atualizado'] is None:
                resumo['ultimo_normativo_atualizado'] = None

            if resumo['base_de_dados_inicio'] is None or resumo['ultimo_normativo_atualizado'] is None:
                print(f"Atualizando datas para a origem: {origem}")
                datas = obter_primeiro_ultimo_normativo(origem)
                resumo.update(datas)
                atualizou = True
            else:
                print(f"Origem {origem} já possui as datas atualizadas.")
        else:
            print(f"Origem {origem} não encontrada no arquivo de resumos. Pule esta ou processe novamente.")

    if atualizou:
        with open(arquivo_resumos, 'w', encoding='utf-8') as f:
            json.dump(resumos, f, ensure_ascii=False, indent=4)
        print("Arquivo de resumos atualizado com sucesso.")
    else:
        print("Nenhuma atualização necessária. Todas as origens já possuem as datas.")

if __name__ == "__main__":
    verificar_e_atualizar_resumos()

from mongo_connection import obter_dados, collection
from processar_dados import organizar_dados
from gerar_prompt import criar_prompt
from interagir_ia import gerar_resumo
from armazenar_resultados import exibir_resumo, salvar_resultados, origem_tem_resumo
from datetime import datetime

def obter_primeiro_ultimo_normativo(origem):
    """
    Função para obter o primeiro e último normativo de uma origem com base na data de emissão.
    :param origem: Nome da origem (string)
    :return: Um dicionário contendo as datas do primeiro e último normativo.
    """
    # Obtém o primeiro normativo com base em issuance_date
    primeiro_normativo = collection.find({"origin": origem}).sort("issuance_date", 1).limit(1)
    ultimo_normativo = collection.find({"origin": origem}).sort("issuance_date", -1).limit(1)
    
    # Extrair as datas
    data_inicio = None
    data_fim = None

    for doc in primeiro_normativo:
        data_inicio = doc.get('issuance_date')

    for doc in ultimo_normativo:
        data_fim = doc.get('issuance_date')

    # Converter datetime para string (YYYY-MM-DD)
    return {
        "base_de_dados_inicio": data_inicio.strftime('%Y-%m-%d') if isinstance(data_inicio, datetime) else data_inicio,
        "ultimo_normativo_atualizado": data_fim.strftime('%Y-%m-%d') if isinstance(data_fim, datetime) else data_fim
    }

def processar_todas_as_origens():
    """
    Função que automatiza o processo para todas as origens no banco de dados.
    Itera sobre cada origem, busca os dados, gera o resumo e exibe os resultados.
    """
    # Obtém uma lista de todas as origens distintas
    origens = collection.distinct("origin")

    for origem in origens:
        # Verificar se já existe um resumo para a origem
        if origem_tem_resumo(origem):
            print(f"Resumo já existente para {origem}. Pulando esta origem.")
            continue  # Pula essa origem e vai para a próxima
        
        # Busca dados relacionados à origem
        dados = obter_dados(origem)
        titulos, assuntos, tipos = organizar_dados(dados)
        
        # Obter datas de início e fim da base
        datas = obter_primeiro_ultimo_normativo(origem)
        
        # Criar o prompt para a IA
        prompt = criar_prompt(origem, titulos, assuntos, tipos)
        
        # Gerar o resumo usando a IA
        resumo = gerar_resumo(prompt)
        
        # Adicionar datas ao resumo
        resumo_completo = {
            "origem": origem,
            "resumo": resumo,
            "base_de_dados_inicio": datas.get("base_de_dados_inicio"),
            "ultimo_normativo_atualizado": datas.get("ultimo_normativo_atualizado")
        }
        
        # Exibir o resumo no terminal
        exibir_resumo(origem, resumo_completo)

        # Salvar os resultados em JSON e NDJSON
        salvar_resultados(origem, resumo_completo, json_file="resumos.json", ndjson_file="resumos.ndjson")

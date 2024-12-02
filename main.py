from processar_varias_origens import processar_todas_as_origens
from atualizar_datas import verificar_e_atualizar_resumos
import os
import json

def inicializar_arquivos(arquivo_resumos="resumos.json", arquivo_ndjson="resumos.ndjson"):
    """
    Inicializa os arquivos JSON e NDJSON se necessário.
    :param arquivo_resumos: Caminho do arquivo JSON com resumos.
    :param arquivo_ndjson: Caminho do arquivo NDJSON com resumos.
    """
    if not os.path.exists(arquivo_resumos):
        print(f"Arquivo {arquivo_resumos} não encontrado. Criando um novo arquivo vazio.")
        with open(arquivo_resumos, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    if os.path.exists(arquivo_ndjson):
        print(f"Carregando dados do arquivo {arquivo_ndjson} para verificar integridade.")
        with open(arquivo_ndjson, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        dados_ndjson = [json.loads(linha) for linha in linhas]

        # Atualizar o JSON com base no NDJSON
        with open(arquivo_resumos, 'r+', encoding='utf-8') as f:
            try:
                dados_json = json.load(f)
            except json.JSONDecodeError:
                dados_json = []

            origens_existentes = {item['origem'] for item in dados_json}
            for dado in dados_ndjson:
                if dado['origem'] not in origens_existentes:
                    dados_json.append(dado)

            f.seek(0)
            json.dump(dados_json, f, ensure_ascii=False, indent=4)
            f.truncate()

if __name__ == "__main__":
    # Inicializar os arquivos, se necessário
    inicializar_arquivos()

    # Etapa 1: Processar todas as origens e gerar resumos
    print("Processando todas as origens e gerando resumos...")
    processar_todas_as_origens()

    # Etapa 2: Atualizar as datas no arquivo de resumos
    print("Atualizando datas no arquivo de resumos...")
    verificar_e_atualizar_resumos()

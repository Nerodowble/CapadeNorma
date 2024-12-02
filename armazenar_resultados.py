import json
import ndjson
import os

def exibir_resumo(origem, resumo):
    """
    Função que exibe o resumo gerado para uma origem no terminal.
    :param origem: Nome da origem (string)
    :param resumo: Resumo gerado pela IA (string)
    """
    print(f"Origem: {origem}")
    print(f"Resumo: {resumo}")

def salvar_resultados(origem, resumo, json_file="resumos.json", ndjson_file="resumos.ndjson"):
    """
    Função que salva os resumos gerados em arquivos JSON e NDJSON.
    :param origem: Nome da origem (string)
    :param resumo: Resumo gerado pela IA (string)
    :param json_file: Nome do arquivo JSON onde os dados serão salvos (string)
    :param ndjson_file: Nome do arquivo NDJSON onde os dados serão salvos (string)
    """

    # Dados formatados para salvar
    resultado = {
        "origem": origem,
        "resumo": resumo
    }

    # Salvar no arquivo JSON
    if os.path.exists(json_file):
        # Carrega o arquivo existente e adiciona o novo resultado
        with open(json_file, 'r+', encoding='utf-8') as json_f:
            try:
                resumos_json = json.load(json_f)
            except json.JSONDecodeError:
                resumos_json = []
            resumos_json.append(resultado)
            # Reescreve o arquivo JSON com a lista atualizada
            json_f.seek(0)
            json.dump(resumos_json, json_f, ensure_ascii=False, indent=4)
            json_f.truncate()  # Remove qualquer dado restante no arquivo
    else:
        # Cria um novo arquivo JSON com o primeiro item
        with open(json_file, 'w', encoding='utf-8') as json_f:
            json.dump([resultado], json_f, ensure_ascii=False, indent=4)

    # Salvar no arquivo NDJSON
    with open(ndjson_file, 'a', encoding='utf-8') as ndjson_f:
        writer = ndjson.writer(ndjson_f)
        writer.writerow(resultado)

def origem_tem_resumo(origem, json_file="resumos.json", ndjson_file="resumos.ndjson"):
    """
    Função que verifica se uma origem já possui um resumo salvo em JSON ou NDJSON.
    :param origem: Nome da origem (string)
    :param json_file: Caminho do arquivo JSON com resumos (string)
    :param ndjson_file: Caminho do arquivo NDJSON com resumos (string)
    :return: True se a origem já tiver um resumo, False caso contrário
    """

    # Verificar no arquivo JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as json_f:
            resumos_json = json.load(json_f)
            # Verifica se a origem já existe no JSON
            if any(item['origem'] == origem for item in resumos_json):
                return True
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Arquivo não existe ou não pode ser decodificado

    # Verificar no arquivo NDJSON
    try:
        with open(ndjson_file, 'r', encoding='utf-8') as ndjson_f:
            resumos_ndjson = ndjson.reader(ndjson_f)
            # Verifica se a origem já existe no NDJSON
            if any(item['origem'] == origem for item in resumos_ndjson):
                return True
    except FileNotFoundError:
        pass  # Arquivo não existe, então a origem não tem resumo ainda

    # Se não encontrou em nenhum dos dois, a origem não tem resumo
    return False

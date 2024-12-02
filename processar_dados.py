def organizar_dados(dados):
    """
    Função que organiza os dados extraídos do banco para construir
    listas de títulos, assuntos e tipos de documentos normativos.
    :param dados: Dados extraídos do MongoDB
    :return: Listas organizadas de títulos, assuntos e tipos
    """
    titulos = [d['title'] for d in dados]
    assuntos = [d['subject'] for d in dados]
    tipos = list(set([d['norm_type'] for d in dados]))
    return titulos, assuntos, tipos

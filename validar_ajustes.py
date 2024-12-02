# Função para validar a qualidade dos resumos gerados e ajustar o prompt conforme necessário.
# Este código pode ser utilizado para monitorar e ajustar a qualidade do conteúdo.

def validar_resumo(origem, resumo):
    """
    Função que valida o resumo gerado para uma origem.
    :param origem: Nome da origem (string)
    :param resumo: Resumo gerado pela IA (string)
    :return: True se o resumo for válido, False se precisar de ajustes
    """
    # Aqui, você pode definir critérios de validação, como a presença de certas palavras-chave
    # ou a precisão das informações fornecidas no resumo.
    if len(resumo) < 50:
        print(f"Resumo muito curto para {origem}. Precisa de ajustes.")
        return False
    return True

def criar_prompt(origem, titulos, assuntos, tipos):
    """
    Função que constrói o prompt a ser enviado para a IA generativa,
    com base nas informações da origem, títulos, assuntos e tipos.
    Verifica a presença de siglas DOU, DOE, DOM e adiciona a base de publicação ao órgão emissor.
    :param origem: Nome da origem (string)
    :param titulos: Lista de títulos extraídos
    :param assuntos: Lista de assuntos extraídos
    :param tipos: Lista de tipos extraídos
    :return: Prompt formatado (string)
    """
    
    # Remove títulos duplicados
    titulos_unicos = list(set(titulos))  # Converte para set e volta para lista para eliminar duplicatas
    
    # Separar órgão regulador e a base de publicação
    partes_origem = origem.split("/")
    
    # Captura o órgão e a base, garantindo que não haja erro de mais de 2 elementos
    orgao = partes_origem[0]  # Primeira parte da origem é sempre o órgão
    base = partes_origem[1] if len(partes_origem) > 1 else ""  # A segunda parte, se existir, é a base de publicação

    # Ajustar o nome da base de publicação
    if base == "DOU":
        base_extenso = "Diário Oficial da União"
    elif base == "DOE":
        base_extenso = "Diário Oficial do Estado"
    elif base == "DOM":
        base_extenso = "Diário Oficial Municipal"
    else:
        base_extenso = ""

    # Adicionar a base de publicação ao órgão emissor no resumo
    if base_extenso:
        orgao_extenso = f"{orgao} em referência da base {base_extenso}"
    else:
        orgao_extenso = orgao

    # **NOVO PROMPT PARA INTERPRETAÇÃO DE SIGLA**
    prompt = f"""
    **Interpretação de Sigla**

    **Sigla:** {orgao}

    **Contexto:** 
    - **Categoria Geral:** Governo
    - **Palavras-Chave Contextuais:** {', '.join(assuntos[:3])}

    **Tarefa:**
    Interprete a sigla **{orgao}** com base no contexto fornecido. Forneça a **EXPANSÃO DA SIGLA** mais provável, juntamente com uma **BREVE DESCRIÇÃO** (máximo 2 frases) sobre o que a sigla representa.

    **Requisitos de Resposta:**
    1. **Precisão:** Priorize a precisão da expansão da sigla.
    2. **Conciso:** Mantenha a descrição breve e focada.
    3. **Minimizar Alucinação:** Evite inferências não suportadas pelo contexto.

    **Formato de Resposta:**
    - **Sigla:** {orgao}
    - **Expansão da Sigla:** [AGUARDE_RESPOSTA_IA]
    - **Breve Descrição:** [AGUARDE_RESPOSTA_IA]
    """
    return prompt




def interpretar_sigla(titulo):
    # **FUNÇÃO DESATIVADA, AGORA USANDO O NOVO PROMPT PARA IA**
    pass
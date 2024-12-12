import requests
import json
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Função para chamar a API do Google Gemini e gerar o resumo da origem
def gerar_resumo(prompt, model_name="gemini-1.5-flash"):
    """
    Função que envia o prompt para a API do Google Gemini e retorna o resumo gerado.
    :param prompt: Texto do prompt a ser enviado para a IA (string)
    :param model_name: Nome do modelo a ser usado (string)
    :return: Resumo gerado pela IA (string)
    """
    # API Key carregada do .env
    api_key = os.getenv("GEMINI_API_KEY")
    
    # URL da API para o modelo específico
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    # Cabeçalhos da requisição
    headers = {
        "Content-Type": "application/json"
    }
    
    # Corpo da requisição com o prompt (descrição da origem)
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    # Fazer a requisição POST à API
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        response_data = response.json()
        # Extrair o conteúdo gerado
        content = response_data['candidates'][0]['content']['parts'][0]['text']
        return content
    else:
        return f"Erro: {response.status_code} - {response.text}"

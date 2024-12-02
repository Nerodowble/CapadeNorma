from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Conexão ao MongoDB utilizando URI no .env
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Acessa a base e coleção corretas
db = client['legalbot_platform']
collection = db['norm']

def obter_dados(origem, limite=100):
    """
    Função que busca os dados de normativos para uma origem específica.
    :param origem: Nome da origem (string)
    :param limite: Número máximo de documentos a serem retornados
    :return: Dados de normativos da origem
    """
    return collection.find({"origin": origem}).limit(limite)

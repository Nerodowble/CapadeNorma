Capa de Normas - Projeto com IA Generativa
Índice
Visão Geral do Projeto
Estrutura do Projeto
Instalação e Configuração
Funcionamento do Programa
Arquitetura do Código
Detalhamento das Funções
Fluxo de Execução
Formatos de Saída
Considerações Finais
Visão Geral do Projeto
O projeto Capa de Normas tem como objetivo gerar resumos automáticos para documentos regulatórios, utilizando IA Generativa (LLM) para interpretar e criar resumos detalhados de normas emitidas por órgãos reguladores. A principal funcionalidade do programa é criar uma "capa de origem" para cada origem de norma no banco de dados, incluindo:

Resumo da origem.
Tipos de documentos emitidos.
Funções regulatórias do órgão.
Datas de início e último normativo atualizado.
O projeto utiliza o Google Gemini para receber dados como origem, títulos, assuntos e tipos de normas, gerando resumos estruturados.

Estrutura do Projeto

CapaDeNormas/
│
├── main.py                      # Arquivo principal para iniciar o processo completo
├── gerar_prompt.py               # Função para criar o prompt para a IA
├── interagir_ia.py               # Função para interagir com a IA generativa
├── processar_varias_origens.py   # Função que processa todas as origens
├── atualizar_datas.py            # Atualiza ou adiciona datas aos resumos gerados
├── armazenar_resultados.py       # Função para armazenar e verificar os resultados
├── mongo_connection.py           # Função para conectar e buscar dados do MongoDB
├── processar_dados.py            # Função para processar os dados extraídos
├── .env                          # Arquivo com as variáveis de ambiente (chave API)
├── resumos.json                  # Arquivo JSON com os resumos gerados
├── resumos.ndjson                # Arquivo NDJSON com os resumos gerados
├── requirements.txt              # Arquivo com as dependências do projeto
└── README.md                     # Arquivo README com a documentação do projeto
Instalação e Configuração
Passos para Instalação
Clone o repositório do projeto:


git clone https://github.com/seuusuario/CapaDeNormas.git
cd CapaDeNormas
Crie e ative um ambiente virtual Python:


python -m venv meu_ambiente
source meu_ambiente/bin/activate  # Linux ou Mac
meu_ambiente\Scripts\activate     # Windows
Instale as dependências:


pip install -r requirements.txt
Configure as variáveis de ambiente:

Crie um arquivo .env na raiz do projeto:
plaintext

GEMINI_API_KEY=<sua-chave-de-api>
MONGO_URI=<sua-uri-de-conexao>
Funcionamento do Programa
O programa funciona em dois estágios principais:

Processamento de Resumos:

Busca todas as origens no banco de dados MongoDB.
Gera resumos utilizando a IA Generativa (Google Gemini).
Salva os resumos nos arquivos resumos.json e resumos.ndjson.
Atualização de Datas:

Verifica se cada origem tem as datas de início e último normativo atualizado.
Se as datas não estiverem presentes, elas são calculadas e adicionadas.
Arquitetura do Código
Arquivo: main.py
Arquivo principal que integra todo o fluxo:
Processa as origens e gera resumos.
Atualiza as datas dos resumos.
Arquivo: atualizar_datas.py
Pode ser chamado de forma independente ou pelo main.py.
Atualiza as datas para cada origem no arquivo resumos.json.
Arquivo: processar_varias_origens.py
Processa todas as origens e gera resumos para aquelas que ainda não possuem.
Fluxo de Execução
Conexão ao Banco:

Conecta ao MongoDB para buscar as origens.
Processamento de Resumos:

Para cada origem:
Verifica se o resumo já existe.
Caso não exista, gera o resumo e salva.
Atualização de Datas:

Verifica e adiciona as datas de início e fim para cada origem no arquivo resumos.json.
Salvar e Exibir Resultados:

O resumo gerado é exibido no terminal e salvo nos formatos JSON e NDJSON.
Formatos de Saída
JSON (resumos.json)
Contém uma lista de objetos JSON com as informações das origens e resumos gerados.
Exemplo:

json

[
    {
        "origem": "BACEN",
        "resumo": "Resumo detalhado da origem BACEN...",
        "base_de_dados_inicio": "2020-01-01",
        "ultimo_normativo_atualizado": "2024-12-01"
    }
]
NDJSON (resumos.ndjson)
Contém um documento JSON por linha.
Exemplo:

plaintext

{"origem": "BACEN", "resumo": "Resumo detalhado da origem BACEN...", "base_de_dados_inicio": "2020-01-01", "ultimo_normativo_atualizado": "2024-12-01"}
Considerações Finais
Este projeto automatiza a criação de resumos e organiza informações regulatórias, permitindo maior agilidade na análise de documentos. Com a integração entre IA Generativa e MongoDB, o sistema oferece eficiência e precisão ao gerar insights detalhados de cada órgão regulador.
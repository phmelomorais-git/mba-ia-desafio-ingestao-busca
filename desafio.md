# Desafio Técnico – Ingestão e Busca Semântica com LangChain e PostgreSQL

## 🎯 Objetivo
Você deve entregar um software capaz de:

### Ingestão
- Ler um arquivo PDF.
- Dividir o conteúdo em *chunks* de 1000 caracteres com *overlap* de 150.
- Gerar embeddings para cada chunk.
- Armazenar os vetores em um banco PostgreSQL com extensão **pgVector**.

### Busca
- Permitir que o usuário faça perguntas via CLI.
- Responder **somente** com base no conteúdo do PDF.

#### Exemplo no CLI
Faça sua pergunta:
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?

RESPOSTA: O faturamento foi de 10 milhões de reais.


#### Perguntas fora do contexto
PERGUNTA: Quantos clientes temos em 2024?

RESPOSTA: Não tenho informações necessárias para responder sua pergunta.


---

## 🛠 Tecnologias obrigatórias
- **Linguagem:** Python  
- **Framework:** LangChain  
- **Banco:** PostgreSQL + pgVector  
- **Execução do banco:** Docker & Docker Compose  

### Pacotes recomendados
- Split: `RecursiveCharacterTextSplitter`
- Embeddings OpenAI: `OpenAIEmbeddings`
- Embeddings Gemini: `GoogleGenerativeAIEmbeddings`
- PDF Loader: `PyPDFLoader`
- Ingestão: `PGVector`
- Busca: `similarity_search_with_score(query, k=10)`

---

## 🔑 Configuração de APIs

### OpenAI
- Criar API Key
- Embeddings: `text-embedding-3-small`
- LLM: `gpt-5-nano`

### Gemini
- Criar API Key
- Embeddings: `models/embedding-001`
- LLM: `gemini-2.5-flash-lite`

---

## 📌 Requisitos detalhados

### 1. Ingestão do PDF
- Dividir PDF em chunks de 1000 caracteres com overlap de 150.
- Gerar embeddings.
- Salvar no PostgreSQL com pgVector.

### 2. Consulta via CLI
Passos ao receber uma pergunta:

1. Vetorizar a pergunta.  
2. Buscar os 10 resultados mais relevantes (k=10).  
3. Montar o prompt.  
4. Chamar a LLM.  
5. Retornar a resposta.

#### Prompt obrigatório
CONTEXTO: {resultados concatenados do banco de dados}

REGRAS:

Responda somente com base no CONTEXTO.

Se a informação não estiver explicitamente no CONTEXTO, responda:
"Não tenho informações necessárias para responder sua pergunta."

Nunca invente ou use conhecimento externo.

Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO: {pergunta do usuário}

RESPONDA A "PERGUNTA DO USUÁRIO"


---

## 📁 Estrutura obrigatória do projeto

├── docker-compose.yml

├── requirements.txt

├── .env.example

├── src/

│   ├── ingest.py

│   ├── search.py

│   ├── chat.py

├── document.pdf

└── README.md



---

## 📚 Repositórios úteis
- Curso de nivelamento com LangChain  
- Template básico com estrutura do projeto  

---

## 🐍 VirtualEnv
python3 -m venv venv
source venv/bin/activate



---

## ▶️ Ordem de execução

### 1. Subir o banco
docker compose up -d


### 2. Executar ingestão
python src/ingest.py



### 3. Rodar o chat
python src/chat.py



---

## 📦 Entregável
Repositório público no GitHub contendo:
- Código-fonte completo
- README com instruções claras de execução

---

© Full Cycle 2015 - 2026 — Todos os direitos reservados.

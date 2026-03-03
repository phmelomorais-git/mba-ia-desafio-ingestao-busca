# MBA IA - Desafio Ingestão e Busca

> Instruções rápidas para configurar o ambiente, instalar dependências e executar o script de ingestão de PDF.

**Requisitos**
- Python 3.11+ (testado em 3.13)
- [requirements.txt](requirements.txt) contém as dependências do projeto

**Setup (recomendado: virtualenv)**

Windows (PowerShell):
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

Windows (CMD):
```cmd
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Variáveis de ambiente**
- Crie um arquivo `.env` na raiz do projeto com a variável `PDF_PATH` apontando para o PDF que será usado.

Exemplo `.env`:
```
PDF_PATH=./data/meu_documento.pdf
```

No PowerShell você também pode executar anonimamente (sem `.env`):
```powershell
$env:PDF_PATH = 'C:\caminho\para\meu.pdf'
py src/ingest.py
```

**Executar ingestão**

Com a virtualenv ativada e `PDF_PATH` definido:
```bash
py src/ingest.py
# ou
python src/ingest.py
```

O script principal de ingestão é [src/ingest.py](src/ingest.py).

**Observações**
- Durante a instalação pode aparecer um aviso informando que scripts foram instalados em um diretório de usuário que não está no `PATH` (ex.: `...\LocalCache\local-packages\Python313\Scripts`). Isso é normal em instalações por usuário; adicionar esse diretório ao `PATH` torna utilitários instalados (como `openai` CLI) acessíveis globalmente.
- O instalador também pode sugerir atualizar o `pip`. Recomendo rodar `py -m pip install --upgrade pip` se quiser.

Se quiser, eu crio um `.env.example` e executo um teste rápido (se você fornecer um PDF de exemplo).
# Desafio MBA Engenharia de Software com IA - Full Cycle

Descreva abaixo como executar a sua solução.



py -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
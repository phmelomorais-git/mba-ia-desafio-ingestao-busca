import os
from pathlib import Path
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*args, **kwargs):
        # dotenv not installed in environment; noop so script can still run
        return False
try:
    from langchain_community.document_loaders import PyPDFLoader
except ModuleNotFoundError as e:
    raise RuntimeError(
        "Missing dependency 'langchain-community'. Run 'pip install -r requirements.txt'"
    ) from e

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ModuleNotFoundError as e:
    raise RuntimeError(
        "Missing dependency 'langchain-text-splitters'. Run 'pip install -r requirements.txt'"
    ) from e

try:
    from langchain_openai import OpenAIEmbeddings
except ModuleNotFoundError as e:
    raise RuntimeError(
        "Missing dependency 'langchain-openai'. Run 'pip install -r requirements.txt'"
    ) from e

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ModuleNotFoundError as e:
    raise RuntimeError(
        "Missing dependency 'langchain-google-genai'. Run 'pip install -r requirements.txt'"
    ) from e

try:
    from langchain_core.documents import Document
except ModuleNotFoundError as e:
    raise RuntimeError(
        "Missing dependency 'langchain-core'. Run 'pip install -r requirements.txt'"
    ) from e

try:
    from langchain_postgres import PGVector
except ModuleNotFoundError as e:
    raise RuntimeError(
        "Missing dependency 'langchain-postgres'. Run 'pip install -r requirements.txt'"
    ) from e

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")


def ingest_pdf():
    # Expect the Google and database related variables present in your .env
    for k in ("GOOGLE_API_KEY", "PG_VECTOR_COLLECTION_NAME", "DATABASE_URL", "PDF_PATH"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    pdf_path = os.path.expanduser(PDF_PATH)
    pdf_path = os.path.abspath(pdf_path)

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    if not docs:
        print("No documents were loaded from the PDF.")
        return []

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    print(f"Loaded {len(docs)} document(s) and produced {len(chunks)} chunks.")
    if not chunks:
        raise SystemExit(0)

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in chunks
    ]    

    ids = [f"doc-{i}" for i in range(len(enriched))]

    # Initialize embeddings: prefer OpenAI if available, otherwise try Google GenAI.
    google_model = os.getenv("GOOGLE_EMBEDDING_MODEL")

    # If no model is configured, default to the Gemini embeddings model
    # recommended in the Gemini docs.
    if not google_model:
        google_model = "gemini-embedding-001"
    else:
        # Sanitize legacy/ambiguous model names (e.g. 'embedding-001')
        if "embedding-001" in google_model and "gemini" not in google_model:
            google_model = "gemini-embedding-001"

    print(f"Using Google embedding model: {google_model}")

    # Prefer OpenAI embeddings when an OpenAI API key is available.
    if os.getenv("OPENAI_API_KEY"):
        embeddings = OpenAIEmbeddings()
    elif os.getenv("GOOGLE_API_KEY"):
        # Rely on the langchain-google-genai implementation.
        embeddings = GoogleGenerativeAIEmbeddings(model=google_model)
    else:
        raise RuntimeError(
            "No supported embeddings provider configured. Set OPENAI_API_KEY or GOOGLE_API_KEY and ensure the corresponding langchain integration is installed."
        )

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)

    return chunks


if __name__ == "__main__":
    ingest_pdf()

from ingestion.loader import load_pdf
from ingestion.splitter import split_documents
from embeddings.embedding_model import get_embedding
from database.mongodb import get_collection
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = "data/Generative AI with LangChain.pdf"

def ingest():
    collection = get_collection()

    docs = load_pdf(PDF_PATH)
    chunks = split_documents(docs)

    documents = [
        {
            "text": chunk.page_content,
            "embedding": get_embedding(chunk.page_content)
        }
        for chunk in chunks
    ]

    collection.insert_many(documents)
    print(f"✅ Inserted {len(documents)} chunks")

if __name__ == "__main__":
    ingest()
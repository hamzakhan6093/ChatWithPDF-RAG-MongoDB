from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2"
)

def get_embedding(text: str, input_type="document"):
    if input_type == "document":
        return embeddings.embed_documents([text])[0]
    return embeddings.embed_query(text)

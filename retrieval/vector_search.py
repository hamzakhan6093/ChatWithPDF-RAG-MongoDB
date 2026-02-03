from embeddings.embedding_model import get_embedding

def search_similar_docs(collection, query, k=5):
    query_embedding = get_embedding(query, input_type="query")

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 384,
                "limit": k
            }
        },
        {
            "$project": {
                "_id": 0,
                "text": 1
            }
        }
    ]

    results = collection.aggregate(pipeline)
    return [doc["text"] for doc in results]

from pymongo.operations import SearchIndexModel
import time

def create_vector_index(collection, index_name="vector_index"):
    model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "numDimensions": 384,
                    "path": "embedding",
                    "similarity": "cosine"
                }
            ]
        },
        name=index_name,
        type="vectorSearch"
    )

    collection.create_search_index(model=model)

    while True:
        indices = list(collection.list_search_indexes(index_name))
        if indices and indices[0].get("queryable"):
            break
        time.sleep(5)

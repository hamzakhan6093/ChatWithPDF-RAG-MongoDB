from langchain_community.llms import Ollama
import os



def get_llm():
    return Ollama(
        model=os.getenv("OLLAMA_MODEL_NAME", "OLLAMA_MODEL_NAME"),
        base_url=os.getenv("OLLAMA_BASE_URL", "OLLAMA_BASE_URL"),
        temperature=0.1,
        num_predict=300
    )

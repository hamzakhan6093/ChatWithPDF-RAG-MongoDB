from langchain_community.document_loaders import PyPDFLoader
    
def load_pdf(pdf_path: str):
    """
    Load a PDF file and return LangChain Document objects
    """
    loader = PyPDFLoader(pdf_path)
    return loader.load()
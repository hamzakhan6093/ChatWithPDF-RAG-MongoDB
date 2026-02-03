import streamlit as st

# ===== Ingestion Imports =====
from ingestion.loader import load_pdf
from ingestion.splitter import split_documents

# ===== RAG Imports =====
from database.mongodb import get_collection
from retrieval.vector_search import search_similar_docs
from llm.ollama_llm import get_llm
from prompts.system_prompt import build_prompt
from embeddings.embedding_model import get_embedding

from dotenv import load_dotenv
load_dotenv()

def run_app():
    st.set_page_config(
        page_title="PDF Chat Assistant",
        page_icon="📚",
        layout="centered"
    )

    # Modern chat interface styling
    st.markdown("""
        <style>
        /* Main app styling */
        .stApp {
            background-color: white;
            
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Header styling */
        .chat-header {
            background: linear-gradient(135deg, #2e73ff 0%, #2d6ae3 100%);
            padding: 28px 24px;
            border-radius: 20px 20px 0 0;
            color: white;
            text-align: left;
            margin-bottom: 0;
            box-shadow: 0 4px 12px rgba(45, 106, 227, 0.15);
        }
        
        .chat-header h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 6px;
            color: white;
        }
        
        .chat-header p {
            font-size: 15px;
            color: white;
            margin: 0;
            font-weight: 400;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            background-color: yellow;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }
        
        /* Chat container - CHANGED TO WHITE */
        .chat-container {
            background: white;  /* Changed from black to white */
            border-radius: 0 0 20px 20px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
            padding: 0;
            min-height: 20px;  /* Increased from 20px */
            display: flex;
            flex-direction: column;
        }
        
        /* Message styling */
        [data-testid="stChatMessage"] {
            margin: 8px 16px;
            max-width: 75%;
            animation: fadeIn 0.3s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* User message (right side) */
        [data-testid="stChatMessage"][aria-label*="user"] {
            margin-left: auto;
            background: linear-gradient(135deg, #2e73ff 0%, #2d6ae3 100%);
            color: white;  /* Changed from black to white */
            border-radius: 18px 18px 4px 18px;
            padding: 14px 18px;
            box-shadow: 0 2px 8px rgba(45, 106, 227, 0.2);
        }
        
        /* Bot message (left side) */
        [data-testid="stChatMessage"][aria-label*="assistant"] {
            margin-right: auto;
            background: linear-gradient(135deg, #f0f7ff 0%, #e8f2ff 100%);
            color: #1e293b;  /* Dark color for readability */
            border: 1px solid #e2e8f0;
            border-radius: 18px 18px 18px 4px;
            padding: 14px 18px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }
        
        /* Message name labels */
        .message-name {
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 6px;
            display: block;
            color: #64748b;  /* Gray color for names */
        }
        
        [data-testid="stChatMessage"][aria-label*="user"] .message-name {
            color: rgba(255, 255, 255, 0.9);  /* Light color for user name */
        }
        
        [data-testid="stChatMessage"][aria-label*="assistant"] .message-name {
            color: #475569;  /* Dark gray for assistant name */
        }
        
        /* Chat input styling */
        .stChatInputContainer {
            background: white;  /* Changed from black to white */
            padding: 16px;
            border-top: 1px solid #e2e8f0;
            border-radius: 0 0 20px 20px;
        }
        
        .stChatInputContainer input {
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            padding: 14px 20px;
            font-size: 15px;
            transition: all 0.2s;
            background: white;  /* Ensure input background is white */
            color: #1e293b;  /* Ensure input text is dark */
        }
        
        .stChatInputContainer input:focus {
            border-color: #2e73ff;
            box-shadow: 0 0 0 3px rgba(46, 115, 255, 0.1);
        }
        
        /* Hide default avatars */
        .stChatMessageAvatar {
            display: none;
        }
        
        /* Scrollbar styling */
        .main .block-container {
            max-width: 800px;
            padding: 0;
        }
        
        /* Welcome message */
        .welcome-container {
            text-align: center;
            padding: 40px 20px;
            color: #64748b;  /* Gray color */
        }
        
        .welcome-container h3 {
            color: #1e293b;  /* Dark color */
            margin-bottom: 12px;
        }
        
        /* Make sure all text in chat is visible */
        .chat-container, .chat-container * {
            color: #1e293b !important;
        }
        </style>
        
        <div class="chat-header">
            <h1>Support Bot</h1>
            <p><span class="status-indicator"></span>Chatbot • Ready to assist with your PDF documents</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm your PDF assistant. Upload and process your PDF documents, then ask me anything about their content."
        })

    # Setup RAG components
    collection = get_collection()
    llm = get_llm()

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Display chat messages
    if len(st.session_state.messages) == 1:  # Only welcome message
        st.markdown("""
            <div class="welcome-container">
                <h3>📚 PDF Chat Assistant</h3>
                <p>Ask questions about your uploaded PDF documents</p>
            </div>
        """, unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        name = "You" if message["role"] == "user" else "Assistant"
        with st.chat_message(message["role"], avatar=None):
            st.markdown(f'<span class="message-name">{name}</span>', unsafe_allow_html=True)
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your question about the PDF..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        name = "You"
        with st.chat_message("user", avatar=None):
            st.markdown(f'<span class="message-name">{name}</span>', unsafe_allow_html=True)
            st.markdown(prompt)

        # Generate RAG response
        with st.spinner("Analyzing documents..."):
            try:
                # Search for relevant documents
                docs = search_similar_docs(collection, prompt)
                context = " ".join(docs)
                
                # Build prompt and get response
                rag_prompt = build_prompt(context, prompt)
                response = llm.invoke(rag_prompt)
                
            except Exception as e:
                response = f"I encountered an error while processing your request: {str(e)}"

        # Display assistant response
        name = "Assistant"
        with st.chat_message("assistant", avatar=None):
            st.markdown(f'<span class="message-name">{name}</span>', unsafe_allow_html=True)
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown('</div>', unsafe_allow_html=True)


def main():
    run_app()


if __name__ == "__main__":
    main()
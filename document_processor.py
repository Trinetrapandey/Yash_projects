import tempfile
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_pinecone import Pinecone as PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import streamlit as st
import time

from config import Config

class DocumentProcessor:
    """Handles PDF processing and vector store operations"""
    
    def __init__(self):
        self.pc = None
        self.embeddings = None
        self.llm = None
        
    def initialize_components(self):
        """Initialize Pinecone and Azure OpenAI components"""
        Config.validate_environment()
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        
        # Initialize embeddings
        self.embeddings = AzureOpenAIEmbeddings(
            deployment="text-embedding-3-small",
            model="text-embedding-3-small",
            openai_api_type="azure",
            openai_api_key=Config.AZURE_OPENAI_KEY,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            openai_api_version="2023-05-15",
            chunk_size=2048
        )
        
        # Initialize LLM
        self.llm = AzureChatOpenAI(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            api_key=Config.AZURE_OPENAI_KEY,
            api_version="2024-02-01",
            deployment_name=Config.DEPLOYMENT_NAME,
        )
        
        return self.pc, self.embeddings, self.llm
    
    def process_pdf(self, uploaded_file, index_name):
        """Process uploaded PDF and create vector store"""
        # Save uploaded file to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name

        try:
            # Read PDF with enhanced status
            with st.status("📖 **Reading PDF Document...**", expanded=True) as status:
                reader = PdfReader(pdf_path)
                pages = [p.extract_text() or "" for p in reader.pages]
                text = "\n".join(pages)

                if not text.strip():
                    raise ValueError("No text could be extracted from the PDF file.")
                
                status.update(label=f"✅ **PDF Read Successfully - {len(pages)} pages**", state="complete")

            # Split text into chunks
            with st.status("🔪 **Splitting Text into Chunks...**", expanded=True) as status:
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=Config.CHUNK_SIZE,
                    chunk_overlap=Config.CHUNK_OVERLAP,
                    length_function=len
                )
                texts = text_splitter.split_text(text)
                status.update(label=f"✅ **Created {len(texts)} Text Chunks**", state="complete")

            # Test embedding
            with st.status("🧠 **Testing Embeddings...**", expanded=True) as status:
                vector = self.embeddings.embed_query(texts[0])
                status.update(label=f"✅ **Vector Dimension: {len(vector)}**", state="complete")

            # Create or connect to Pinecone index
            with st.status("🗄️ **Setting Up Vector Database...**", expanded=True) as status:
                if index_name not in self.pc.list_indexes().names():
                    self.pc.create_index(
                        name=index_name,
                        dimension=Config.EMBEDDING_DIMENSION,  
                        metric="cosine",
                        spec=ServerlessSpec(
                            cloud="aws",
                            region="us-east-1"
                        )
                    )
                    # Wait for index to be ready
                    while not self.pc.describe_index(index_name).status['ready']:
                        time.sleep(1)
                    status.update(label=f"✅ **Created New Index: {index_name}**", state="complete")
                else:
                    status.update(label=f"✅ **Using Existing Index: {index_name}**", state="complete")

            # Create documents from text chunks
            with st.status("📄 **Creating Document Vectors...**", expanded=True) as status:
                chunks = text_splitter.create_documents([text])
                status.update(label=f"✅ **Prepared {len(chunks)} Documents**", state="complete")

            # Upload documents to Pinecone
            with st.status("🚀 **Uploading to Knowledge Base...**", expanded=True) as status:
                vectorstore = PineconeVectorStore.from_documents(
                    documents=chunks,
                    index_name=index_name,
                    embedding=self.embeddings
                )
                status.update(label="✅ **Knowledge Base Ready!**", state="complete")
            
            return vectorstore
        
        finally:
            # Clean up temporary file
            os.unlink(pdf_path)
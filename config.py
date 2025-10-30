import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for environment variables and settings"""
    
    # Retrieve environment variables
    PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
    AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    DEPLOYMENT_NAME = os.environ.get("DEPLOYMENT_NAME")
    
    # Default settings
    DEFAULT_INDEX_NAME = "intellidoc-index"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 20
    EMBEDDING_DIMENSION = 1536
    
    @classmethod
    def validate_environment(cls):
        """Validate that all required environment variables are set"""
        missing_vars = []
        if not cls.PINECONE_API_KEY:
            missing_vars.append("PINECONE_API_KEY")
        if not cls.AZURE_OPENAI_KEY:
            missing_vars.append("AZURE_OPENAI_KEY")
        if not cls.AZURE_OPENAI_ENDPOINT:
            missing_vars.append("AZURE_OPENAI_ENDPOINT")
        
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")
        
        return True
import pinecone
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from config import PINECONE_API_KEY, PINECONE_ENVIRONMENT

class KnowledgeBase:
    def __init__(self):
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
        self.embeddings = OpenAIEmbeddings()
        
        # Initialize Pinecone index
        if "ai-sdr-knowledge" not in pinecone.list_indexes():
            pinecone.create_index("ai-sdr-knowledge", dimension=1536)
        
        self.vector_store = Pinecone.from_existing_index("ai-sdr-knowledge", self.embeddings)
    
    def add_knowledge(self, documents):
        """Add documents to knowledge base"""
        self.vector_store.add_documents(documents)
    
    def search_knowledge(self, query, k=5):
        """Search knowledge base for relevant information"""
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
    
    def get_sales_insights(self, prospect_data):
        """Get relevant sales insights for a prospect"""
        query = f"sales strategies for {prospect_data.get('industry')} companies with {prospect_data.get('company_size')} employees"
        insights = self.search_knowledge(query, k=3)
        return insights

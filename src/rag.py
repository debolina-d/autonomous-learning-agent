"""RAG Manager - Handles vector storage and semantic retrieval"""
import chromadb
from chromadb.utils import embedding_functions
import uuid

class RAGManager:
    """Manages ChromaDB vector store for semantic search and retrieval"""
    
    def __init__(self, collection_name="learning_knowledge_base"):
        """Initialize vector store with persistent storage"""
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Initialize sentence transformer for embeddings
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create or get collection with sanitized name
        clean_name = "".join(c if c.isalnum() else "_" for c in collection_name)
        self.collection = self.client.get_or_create_collection(
            name=clean_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, text_list):
        """Add text documents to vector database"""
        if not text_list:
            return

        # Generate unique IDs and add to collection
        ids = [str(uuid.uuid4()) for _ in text_list]
        self.collection.add(documents=text_list, ids=ids)

    def retrieve(self, query, n_results=3):
        """Perform semantic search and return top n results"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return "\n\n".join(results['documents'][0]) if results['documents'] else ""

    def clear_collection(self):
        """Clear collection data for fresh content"""
        try:
            collection_name = self.collection.name
            self.client.delete_collection(collection_name)
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.embedding_fn
            )
        except Exception as e:
            print(f"Warning: Could not clear collection: {e}")
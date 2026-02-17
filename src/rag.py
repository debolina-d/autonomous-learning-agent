import chromadb
from chromadb.utils import embedding_functions
import uuid
import os

class RAGManager:
    def __init__(self, collection_name="learning_knowledge_base"):
        """
        Initializes the Vector Store.
        Using a PersistentClient ensures data is saved to disk (./chroma_db folder).
        """
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Uses a embedding model (all-MiniLM-L6-v2)
        # This converts text into number lists (vectors)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create or get the collection (think of it as a table in SQL)
        # We sanitize the name to ensure it follows ChromaDB naming rules
        clean_name = "".join(c if c.isalnum() else "_" for c in collection_name)
        self.collection = self.client.get_or_create_collection(
            name=clean_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, text_list):
        """
        Adds text snippets to the vector database.
        """
        if not text_list:
            return

        # Generate unique IDs for each chunk
        ids = [str(uuid.uuid4()) for _ in text_list]
        
        # Add to collection (Embeddings are generated automatically here)
        self.collection.add(
            documents=text_list,
            ids=ids
        )

    def retrieve(self, query, n_results=3):
        """
        Semantic Search: Finds the top 'n' snippets most similar to the query.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Results return a list of lists, we flatten it
        return "\n\n".join(results['documents'][0]) if results['documents'] else ""

    def clear_collection(self):
        """Optional: Clears data to start fresh for a new topic"""
        try:
            collection_name = self.collection.name
            self.client.delete_collection(collection_name)
            # Recreate the collection after deletion
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.embedding_fn
            )
        except Exception as e:
            print(f"Warning: Could not clear collection: {e}")
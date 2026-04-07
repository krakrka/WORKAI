import chromadb
from chromadb.utils import embedding_functions
import os

class WorkAIMemory:
    def __init__(self, persist_directory="./chroma_db"):
        # Initialisation du client persistant (stocké sur disque)
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Utilisation d'un modèle d'embedding Open Source par défaut
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Création ou récupération de la collection principale
        self.collection = self.client.get_or_create_collection(
            name="workai_knowledge",
            embedding_function=self.embedding_fn
        )

    def store_knowledge(self, doc_id, text, metadata=None):
        """Sauvegarde un fragment d'information ou de code."""
        self.collection.add(
            documents=[text],
            metadatas=[metadata] if metadata else [{"source": "system"}],
            ids=[doc_id]
        )
        return f"Document {doc_id} mémorisé."

    def query_knowledge(self, query_text, n_results=3):
        """Recherche les informations les plus pertinentes."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results['documents']

# Instance partagée pour le projet
memory_manager = WorkAIMemory()
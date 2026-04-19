import os
import chromadb
from chromadb.config import Settings

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError:
    GoogleGenerativeAIEmbeddings = None

class KBLoader:
    def __init__(self, docs_dir: str = "docs", persist_dir: str = ".chroma_db_gemini"):
        self.docs_dir = docs_dir
        self.persist_dir = persist_dir
        self.collection_name = "course_materials"
        
        from langchain_community.embeddings import HuggingFaceEmbeddings
        self.embeddings_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_dir)
    
    def get_collection(self):
        # Safer get_or_create logic
        return self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
            
    def load_and_ingest(self):
        collection = self.get_collection()
        
        # Check if already ingested
        if collection.count() > 0:
            print(f"ChromaDB already contains {collection.count()} documents. Skipping ingestion.")
            return

        if not os.path.exists(self.docs_dir):
            print(f"Warning: {self.docs_dir} directory not found.")
            return

        documents = []
        ids = []
        metadatas = []
        
        print("Ingesting documents into ChromaDB...")
        for i, filename in enumerate(os.listdir(self.docs_dir)):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.docs_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                documents.append(content)
                ids.append(f"doc_{i}")
                metadatas.append({"source": filename, "topic": filename.replace(".txt", "").replace("_", " ")})
                
        if documents:
            # Generate embeddings and add to collection
            embeddings = self.embeddings_model.embed_documents(documents)
            collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Successfully ingested {len(documents)} documents.")
        else:
            print("No text documents found to ingest.")

    def retrieve(self, query: str, top_k: int = 3) -> list:
        """Retrieves top_k relevant documents for the query."""
        collection = self.get_collection()
        if collection.count() == 0:
            return []
            
        query_embedding = self.embeddings_model.embed_query(query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        retrieved_docs = []
        if results and results.get("documents") and len(results["documents"]) > 0:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            for doc, meta in zip(docs, metas):
                retrieved_docs.append(f"[Topic: {meta.get('topic', 'Unknown')}]\n{doc}")
                
        return retrieved_docs

if __name__ == "__main__":
    loader = KBLoader()
    loader.load_and_ingest()

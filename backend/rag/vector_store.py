"""
AI Travel Guardian+ — FAISS Vector Store
Build, save, load, and search FAISS vector indices.
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import faiss


class FAISSVectorStore:
    """FAISS-based vector store for similarity search."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents: List[str] = []

    def add_documents(self, texts: List[str], embeddings: np.ndarray):
        """Add documents and their embeddings to the index."""
        self.index.add(embeddings.astype("float32"))
        self.documents.extend(texts)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """Search for top-k most similar documents."""
        if self.index.ntotal == 0:
            return []
        
        k = min(k, self.index.ntotal)
        query = query_embedding.reshape(1, -1).astype("float32")
        distances, indices = self.index.search(query, k)

        results = []
        for j, i in enumerate(indices[0]):
            if 0 <= i < len(self.documents):
                results.append({
                    "text": self.documents[i],
                    "distance": float(distances[0][j]),
                    "index": int(i),
                })
        return results

    def save(self, path: str):
        """Save FAISS index and documents to disk."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(p) + ".faiss")
        with open(str(p) + "_docs.json", "w", encoding="utf-8") as f:
            json.dump(self.documents, f)

    def load(self, path: str) -> bool:
        """Load FAISS index and documents from disk. Returns True if successful."""
        faiss_path = str(path) + ".faiss"
        docs_path = str(path) + "_docs.json"
        if Path(faiss_path).exists() and Path(docs_path).exists():
            self.index = faiss.read_index(faiss_path)
            with open(docs_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
            return True
        return False

    @property
    def count(self) -> int:
        return self.index.ntotal

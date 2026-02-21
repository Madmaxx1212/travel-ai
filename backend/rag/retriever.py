"""
AI Travel Guardian+ — RAG Retriever
Query FAISS indices to retrieve relevant context for LLM prompts.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional

from rag.embedder import DataEmbedder
from rag.vector_store import FAISSVectorStore


class RAGRetriever:
    """Retrieval-Augmented Generation retriever using FAISS indices."""

    def __init__(self):
        self.embedder = DataEmbedder()
        self.flight_store = FAISSVectorStore()
        self.hotel_store = FAISSVectorStore()
        self.city_store = FAISSVectorStore()
        self._initialized = False

    def initialize(self, flights: list = None, hotels: list = None, city_data: dict = None,
                   faiss_flights_path: str = None, faiss_hotels_path: str = None,
                   faiss_city_path: str = None):
        """Initialize stores from data or load from disk."""
        # Try loading from disk first
        loaded_all = True

        if faiss_flights_path and self.flight_store.load(faiss_flights_path):
            pass
        elif flights:
            texts, embeddings = self.embedder.embed_flights(flights)
            self.flight_store.add_documents(texts, embeddings)
            if faiss_flights_path:
                self.flight_store.save(faiss_flights_path)
        else:
            loaded_all = False

        if faiss_hotels_path and self.hotel_store.load(faiss_hotels_path):
            pass
        elif hotels:
            texts, embeddings = self.embedder.embed_hotels(hotels)
            self.hotel_store.add_documents(texts, embeddings)
            if faiss_hotels_path:
                self.hotel_store.save(faiss_hotels_path)
        else:
            loaded_all = False

        if faiss_city_path and self.city_store.load(faiss_city_path):
            pass
        elif city_data:
            texts, embeddings = self.embedder.embed_city_knowledge(city_data)
            self.city_store.add_documents(texts, embeddings)
            if faiss_city_path:
                self.city_store.save(faiss_city_path)
        else:
            loaded_all = False

        self._initialized = True
        return loaded_all

    def retrieve_flights(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant flight information for a query."""
        if self.flight_store.count == 0:
            return []
        embedding = self.embedder.embed_query(query)
        results = self.flight_store.search(embedding, k=k)
        return [r["text"] for r in results]

    def retrieve_hotels(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant hotel information for a query."""
        if self.hotel_store.count == 0:
            return []
        embedding = self.embedder.embed_query(query)
        results = self.hotel_store.search(embedding, k=k)
        return [r["text"] for r in results]

    def retrieve_city_info(self, query: str, k: int = 8) -> List[str]:
        """Retrieve relevant city knowledge for a query."""
        if self.city_store.count == 0:
            return []
        embedding = self.embedder.embed_query(query)
        results = self.city_store.search(embedding, k=k)
        return [r["text"] for r in results]

    def retrieve_context(self, query: str, include_flights: bool = True,
                         include_hotels: bool = True, include_city: bool = True,
                         k: int = 5) -> str:
        """Retrieve combined context from all stores as a formatted string."""
        context_parts = []

        if include_flights:
            flight_results = self.retrieve_flights(query, k=k)
            if flight_results:
                context_parts.append("**Flight Information:**\n" + "\n".join(f"- {r}" for r in flight_results))

        if include_hotels:
            hotel_results = self.retrieve_hotels(query, k=k)
            if hotel_results:
                context_parts.append("**Hotel Information:**\n" + "\n".join(f"- {r}" for r in hotel_results))

        if include_city:
            city_results = self.retrieve_city_info(query, k=k)
            if city_results:
                context_parts.append("**City Knowledge:**\n" + "\n".join(f"- {r}" for r in city_results))

        return "\n\n".join(context_parts) if context_parts else "No relevant context available."

    @property
    def is_initialized(self) -> bool:
        return self._initialized

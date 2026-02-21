"""
AI Travel Guardian+ — Data Embedder
Uses sentence-transformers to embed flights, hotels, and city knowledge for RAG.
"""

import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer


class DataEmbedder:
    """Embed text data using sentence-transformers for FAISS indexing."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_flights(self, flights: list) -> Tuple[List[str], np.ndarray]:
        """Convert flights to text documents and embed them."""
        texts = []
        for f in flights:
            text = (
                f"Flight {f.get('flight_number', 'N/A')} by {f.get('airline', 'N/A')} "
                f"from {f.get('source', 'N/A')} to {f.get('destination', 'N/A')}. "
                f"Departs {f.get('departure_time', 'N/A')}, arrives {f.get('arrival_time', 'N/A')}. "
                f"Duration: {f.get('duration_mins', 'N/A')} mins. "
                f"Price: ₹{f.get('price', 'N/A')}. "
                f"Historical on-time rate: {(f.get('historical_ontime_rate', 0.85)) * 100:.0f}%. "
                f"Airline: {f.get('airline', 'N/A')}. Stops: {f.get('stops', 0)}."
            )
            texts.append(text)

        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return texts, embeddings

    def embed_hotels(self, hotels: list) -> Tuple[List[str], np.ndarray]:
        """Convert hotels to text documents and embed them."""
        texts = []
        for h in hotels:
            text = (
                f"Hotel {h.get('name', 'N/A')} in {h.get('city', 'N/A')}. "
                f"Budget tier: {h.get('budget_tier', 'N/A')}. "
                f"Price: ₹{h.get('price_per_night', 'N/A')} per night. "
                f"Rating: {h.get('rating', 'N/A')}/5. "
                f"Distance from centre: {h.get('distance_centre_km', 'N/A')} km. "
                f"Address: {h.get('address', 'N/A')}."
            )
            texts.append(text)

        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return texts, embeddings

    def embed_city_knowledge(self, city_data: dict) -> Tuple[List[str], np.ndarray]:
        """Chunk city knowledge into paragraphs and embed."""
        chunks = []
        for city, info in city_data.items():
            # Attractions
            for attr in info.get("top_attractions", []):
                chunk = (
                    f"{city} attraction: {attr['name']}. {attr['description']}. "
                    f"Cost: {attr['cost']}. Best time: {attr['best_time']}. "
                    f"Duration: {attr['duration_mins']} minutes."
                )
                chunks.append(chunk)

            # Food spots
            for food in info.get("food_spots", []):
                chunk = (
                    f"{city} food: {food['name']} in {food['area']}. "
                    f"Cuisine: {food['cuisine']}. Price: {food['price_range']}. "
                    f"Specialty: {food['specialty']}."
                )
                chunks.append(chunk)

            # Tips
            for tip in info.get("tips", []):
                chunks.append(f"{city} travel tip: {tip}")

            # Transport
            transport = info.get("transport", {})
            for mode, desc in transport.items():
                chunks.append(f"{city} transport ({mode}): {desc}")

        embeddings = self.model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)
        return chunks, embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query string."""
        return self.model.encode([query], convert_to_numpy=True)[0]

"""
AI Travel Guardian+ — Airline Sentiment Analyser
VADER-based sentiment analysis on airline reviews with aggregate scoring.
"""

from typing import Dict, Optional
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class AirlineSentimentAnalyser:
    """Analyse airline review sentiment using VADER."""

    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self._cache: Dict[str, float] = {}

    def analyse_vader(self, text: str) -> dict:
        """Run VADER sentiment on a single text."""
        scores = self.vader.polarity_scores(text)
        compound = scores["compound"]
        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        return {"compound": compound, "pos": scores["pos"], "neu": scores["neu"],
                "neg": scores["neg"], "sentiment": sentiment}

    def analyse_reviews_for_airline(self, airline: str, db_session) -> dict:
        """Aggregate sentiment scores for all reviews of an airline."""
        from database.models import AirlineReview
        reviews = db_session.query(AirlineReview).filter(
            AirlineReview.airline == airline
        ).all()

        if not reviews:
            return {"airline": airline, "total_reviews": 0, "overall_sentiment": 0.0,
                    "aspect_scores": {}, "sentiment_label": "neutral", "service_quality_score": 0.5}

        compounds = []
        aspect_totals = {"punctuality": [], "staff": [], "comfort": [], "value": [], "food": []}

        for review in reviews:
            result = self.analyse_vader(review.review_text)
            compounds.append(result["compound"])
            if review.punctuality_score is not None:
                aspect_totals["punctuality"].append(review.punctuality_score)
            if review.staff_score is not None:
                aspect_totals["staff"].append(review.staff_score)
            if review.comfort_score is not None:
                aspect_totals["comfort"].append(review.comfort_score)
            if review.value_score is not None:
                aspect_totals["value"].append(review.value_score)
            if review.food_score is not None:
                aspect_totals["food"].append(review.food_score)

        avg_compound = sum(compounds) / len(compounds)
        aspect_scores = {k: (sum(v) / len(v) if v else 0.5) for k, v in aspect_totals.items()}

        if avg_compound >= 0.05:
            label = "positive"
        elif avg_compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"

        # Map compound (-1 to 1) to quality score (0 to 1)
        quality_score = round((avg_compound + 1) / 2, 4)

        return {
            "airline": airline,
            "total_reviews": len(reviews),
            "overall_sentiment": round(avg_compound, 4),
            "aspect_scores": {k: round(v, 4) for k, v in aspect_scores.items()},
            "sentiment_label": label,
            "service_quality_score": quality_score,
        }

    def get_airline_quality_score(self, airline: str, db_session) -> float:
        """Return a single 0-1 quality score for use in CCS. Cached."""
        if airline in self._cache:
            return self._cache[airline]
        result = self.analyse_reviews_for_airline(airline, db_session)
        score = result["service_quality_score"]
        self._cache[airline] = score
        return score

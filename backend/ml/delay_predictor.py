"""
AI Travel Guardian+ — Flight Delay Predictor
XGBoost model that predicts flight delay probability using 13 engineered features.
Uses SHAP TreeExplainer for model interpretability.
"""

import os
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import xgboost as xgb
import shap

from utils.helpers import is_indian_holiday


# Feature names used by the model
FEATURE_NAMES = [
    "hour_of_day", "day_of_week", "month", "is_weekend", "is_holiday",
    "historical_delay_rate", "congestion_index", "duration_mins", "stops",
    "price_normalised", "airline_encoded", "source_encoded", "destination_encoded"
]

# Human-readable labels for SHAP explanations
FEATURE_LABELS = {
    "hour_of_day": "Departure Time",
    "day_of_week": "Day of Week",
    "month": "Month",
    "is_weekend": "Weekend Travel",
    "is_holiday": "Holiday Period",
    "historical_delay_rate": "Historical Delay Rate",
    "congestion_index": "Airport Congestion",
    "duration_mins": "Flight Duration",
    "stops": "Number of Stops",
    "price_normalised": "Price Level",
    "airline_encoded": "Airline",
    "source_encoded": "Departure Airport",
    "destination_encoded": "Arrival Airport",
}

MODELS_DIR = Path(__file__).resolve().parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


class FlightDelayPredictor:
    """XGBoost-based flight delay prediction with SHAP explanations."""

    def __init__(self, model_path: str = None, encoder_path: str = None):
        self.model_path = Path(model_path) if model_path else MODELS_DIR / "xgboost_delay_model.pkl"
        self.encoder_path = Path(encoder_path) if encoder_path else MODELS_DIR / "label_encoders.pkl"
        self.model: Optional[xgb.XGBClassifier] = None
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.explainer: Optional[shap.TreeExplainer] = None

        if self.model_path.exists() and self.encoder_path.exists():
            self._load_model()

    def _load_model(self):
        """Load saved model and encoders from disk."""
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)
        with open(self.encoder_path, "rb") as f:
            self.label_encoders = pickle.load(f)
        self.explainer = shap.TreeExplainer(self.model)

    def _save_model(self):
        """Save model and encoders to disk."""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
        with open(self.encoder_path, "wb") as f:
            pickle.dump(self.label_encoders, f)

    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer features from raw flight data."""
        features = pd.DataFrame()

        # Time features
        features["hour_of_day"] = df["departure_time"].apply(
            lambda t: int(str(t).split(":")[0]) if pd.notna(t) else 12
        )
        features["day_of_week"] = df["day_of_week"].fillna(3).astype(int)
        features["month"] = df["month"].fillna(6).astype(int)
        features["is_weekend"] = features["day_of_week"].apply(lambda d: 1 if d >= 5 else 0)
        features["is_holiday"] = df.apply(
            lambda row: 1 if is_indian_holiday(
                int(row.get("month", 6)),
                15  # Approximate mid-month
            ) else 0, axis=1
        )

        # Numeric features
        features["historical_delay_rate"] = df["historical_delay_rate"].fillna(0.15).astype(float)
        features["congestion_index"] = df["congestion_index"].fillna(0.5).astype(float)
        features["duration_mins"] = df["duration_mins"].fillna(120).astype(int)
        features["stops"] = df["stops"].fillna(0).astype(int)

        # Normalised price (by route max)
        if "price" in df.columns:
            route_key = df.get("source", "X").astype(str) + "_" + df.get("destination", "Y").astype(str)
            max_prices = df.groupby(route_key)["price"].transform("max")
            max_prices = max_prices.replace(0, 1)
            features["price_normalised"] = (df["price"] / max_prices).fillna(0.5)
        else:
            features["price_normalised"] = 0.5

        # Encode categorical features
        for col in ["airline", "source", "destination"]:
            encoded_col = f"{col}_encoded"
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    features[encoded_col] = self.label_encoders[col].fit_transform(
                        df[col].fillna("Unknown").astype(str)
                    )
                else:
                    le = self.label_encoders[col]
                    vals = df[col].fillna("Unknown").astype(str)
                    # Handle unseen labels
                    known = set(le.classes_)
                    vals_safe = vals.apply(lambda x: x if x in known else le.classes_[0])
                    features[encoded_col] = le.transform(vals_safe)
            else:
                features[encoded_col] = 0

        return features[FEATURE_NAMES]

    def _generate_target(self, df: pd.DataFrame) -> pd.Series:
        """Generate binary delay target from historical delay rate."""
        # Simulate delay labels based on historical rates + noise
        np.random.seed(42)
        delay_rates = df["historical_delay_rate"].fillna(0.15).astype(float)
        random_vals = np.random.random(len(df))
        return (random_vals < delay_rates).astype(int)

    def train(self, df: pd.DataFrame) -> dict:
        """Train XGBoost model on flight data."""
        print("[INFO] Preparing features for training...")
        X = self._prepare_features(df)
        y = self._generate_target(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"[INFO] Training set: {len(X_train)} | Test set: {len(X_test)}")
        print(f"[INFO] Positive rate: {y.mean():.2%}")

        self.model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            min_child_weight=3,
            gamma=0.1,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
            eval_metric="logloss",
            use_label_encoder=False,
        )

        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False,
        )

        # Evaluate
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "f1": round(f1_score(y_test, y_pred), 4),
            "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
        }

        print(f"[OK] Model trained -- Accuracy: {metrics['accuracy']}, F1: {metrics['f1']}, AUC: {metrics['roc_auc']}")

        # Initialize SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)

        # Save
        self._save_model()
        print(f"[OK] Model saved to {self.model_path}")

        return metrics

    def predict(self, flight_features: dict) -> dict:
        """Predict delay probability for a single flight with SHAP explanation."""
        if self.model is None:
            raise RuntimeError("Model not loaded. Train or load a model first.")

        df = pd.DataFrame([flight_features])
        X = self._prepare_features(df)

        # Prediction
        delay_prob = float(self.model.predict_proba(X)[0][1])
        delay_risk_score = round(delay_prob * 100, 1)

        # Risk level
        if delay_prob < 0.15:
            risk_level = "low"
        elif delay_prob < 0.30:
            risk_level = "medium"
        elif delay_prob < 0.50:
            risk_level = "high"
        else:
            risk_level = "very_high"

        # SHAP explanation
        shap_top3 = []
        if self.explainer is not None:
            try:
                shap_values = self.explainer.shap_values(X)
                if isinstance(shap_values, list):
                    sv = shap_values[1][0]  # Class 1 (delay)
                else:
                    sv = shap_values[0]

                feature_impacts = list(zip(FEATURE_NAMES, sv, X.iloc[0].values))
                feature_impacts.sort(key=lambda x: abs(x[1]), reverse=True)

                for feat, shap_val, feat_val in feature_impacts[:3]:
                    shap_top3.append({
                        "feature": FEATURE_LABELS.get(feat, feat),
                        "value": round(float(feat_val), 4),
                        "impact": round(float(abs(shap_val)), 4),
                        "direction": "increases delay risk" if shap_val > 0 else "decreases delay risk",
                    })
            except Exception:
                shap_top3 = [{"feature": "Analysis", "value": 0, "impact": 0, "direction": "unavailable"}]

        return {
            "delay_probability": round(delay_prob, 4),
            "delay_risk_score": delay_risk_score,
            "risk_level": risk_level,
            "shap_top3": shap_top3,
        }

    def predict_batch(self, flights: List[dict]) -> List[dict]:
        """Run predictions for multiple flights."""
        results = []
        for flight in flights:
            prediction = self.predict(flight)
            enriched = {**flight, **prediction}
            results.append(enriched)
        return results

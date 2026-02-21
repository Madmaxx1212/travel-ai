"""
AI Travel Guardian+ — Model Training Script
Standalone script that trains the XGBoost delay prediction model on seed data.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from ml.delay_predictor import FlightDelayPredictor


def main():
    print("=" * 60)
    print("  AI Travel Guardian+ — XGBoost Model Training")
    print("=" * 60)

    data_dir = Path(__file__).resolve().parent.parent.parent / "data"
    csv_path = data_dir / "sample_flights.csv"

    if not csv_path.exists():
        print(f"[ERROR] Flight data not found at {csv_path}")
        print("   Run database/seed_data.py first to generate sample data.")
        sys.exit(1)

    print(f"[INFO] Loading data from {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"[INFO] Loaded {len(df)} flight records")

    predictor = FlightDelayPredictor()
    metrics = predictor.train(df)

    print("\n" + "=" * 60)
    print("  Training Results")
    print("=" * 60)
    print(f"  Accuracy : {metrics['accuracy']}")
    print(f"  F1 Score : {metrics['f1']}")
    print(f"  ROC AUC  : {metrics['roc_auc']}")
    print("=" * 60)

    # Quick test prediction
    test_flight = {
        "departure_time": "08:30", "day_of_week": 2, "month": 3,
        "historical_delay_rate": 0.12, "congestion_index": 0.55,
        "duration_mins": 135, "stops": 0, "price": 5500,
        "airline": "Vistara", "source": "BOM", "destination": "DEL",
    }
    result = predictor.predict(test_flight)
    print(f"\n[TEST] Test Prediction (BOM->DEL, Vistara, 08:30):")
    print(f"   Delay Probability: {result['delay_probability']:.2%}")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Top Factor: {result['shap_top3'][0]['feature'] if result['shap_top3'] else 'N/A'}")
    print("\n[OK] Training complete!")


if __name__ == "__main__":
    main()

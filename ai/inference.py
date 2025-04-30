import joblib
import pandas as pd
from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

MODEL_PATH = Path(__file__).parent / "models"
KNN_MODEL_PATH = MODEL_PATH / "knn.pkl"
DT_MODEL_PATH = MODEL_PATH / "decision_tree.pkl"

FRAUD_PROBABILITY_THRESHOLD = 0.5

knn_model: KNeighborsClassifier = joblib.load(KNN_MODEL_PATH)
decision_tree_model: DecisionTreeClassifier = joblib.load(DT_MODEL_PATH)

CATEGORIES = [
    "entertainment",
    "food_dining",
    "gas_transport",
    "grocery_net",
    "grocery_pos",
    "health_fitness",
    "home",
    "kids_pets",
    "misc_net",
    "misc_pos",
    "personal_care",
    "shopping_net",
    "shopping_pos",
    "travel",
]


def prepare_input(amount, category, hour):
    """Prepare the input data for prediction."""
    data = {"amt": [float(amount)], "hour": [int(hour)]}

    for cat in CATEGORIES:
        data[f"category_{cat}"] = [1 if cat == category else 0]

    return pd.DataFrame(data)


def predict_fraud(amount, category, hour, model_type="knn"):
    """Predict if a transaction is fraudulent."""
    if category not in CATEGORIES:
        raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}")

    if not (0 <= hour <= 23):
        raise ValueError("Hour must be between 0 and 23")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    input_data = prepare_input(amount, category, hour)

    model = knn_model if model_type.lower() == "knn" else decision_tree_model

    probability = model.predict_proba(input_data)[0][1]
    prediction = probability >= FRAUD_PROBABILITY_THRESHOLD

    return {"prediction": bool(prediction), "probability": float(probability), "model_used": model_type.lower()}

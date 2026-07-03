import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")


class SimpleCGPAModel:
    """Fallback model used when model.pkl is not available."""
    def predict(self, features):
        results = []
        for row in features:
            attendance, avg_marks, lowest, highest, consistency, _ = row
            score = avg_marks * 0.06 + attendance * 0.02 + consistency * 0.01
            results.append(max(0, min(10, score)))
        return results


def load_model():
    try:
        with open(MODEL_PATH, "rb") as file:
            return pickle.load(file)
    except Exception:
        return SimpleCGPAModel()


model = load_model()


def predict_score(features):
    predicted_score = float(model.predict(features)[0])
    return min(predicted_score, 10)

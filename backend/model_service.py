import joblib
import pandas as pd


FEATURE_META = {}


def load_model_package(model_path):
    return joblib.load(model_path)


def extract_model(loaded):
    if isinstance(loaded, dict):
        print("MODEL DICTIONARY KEYS:", loaded.keys())

        for key in ["pipeline", "model", "best_model", "classifier", "random_forest"]:
            if key in loaded and hasattr(loaded[key], "predict"):
                return loaded[key]

        for value in loaded.values():
            if hasattr(value, "predict"):
                return value

        raise ValueError("No valid model with predict() found inside model file.")

    return loaded


def get_feature_names(model_path=None):
    if not model_path:
        return []

    loaded = load_model_package(model_path)

    if isinstance(loaded, dict):
        for key in ["feature_names", "features", "columns"]:
            if key in loaded:
                return list(loaded[key])

    model = extract_model(loaded)

    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)

    return []


def normalize_prediction(prediction):
    pred = str(prediction).strip().lower()

    label_map = {
        "0": "Normal",
        "1": "High Risk",
        "2": "Anomaly",

        "normal": "Normal",
        "high risk": "High Risk",
        "high_risk": "High Risk",
        "risk": "High Risk",
        "danger": "High Risk",
        "critical": "High Risk",

        "anomaly": "Anomaly",
        "anomalous": "Anomaly",
        "abnormal": "Anomaly",
        "outlier": "Anomaly",
    }

    return label_map.get(pred, str(prediction))


def build_input_frame(data, features):
    if features:
        row = []

        for feature in features:
            value = data.get(feature, 0)

            try:
                value = float(value)
            except ValueError:
                value = 0

            row.append(value)

        return pd.DataFrame([row], columns=features)

    return pd.DataFrame([data])


def predict(data, model_path):
    loaded = load_model_package(model_path)
    model = extract_model(loaded)

    features = get_feature_names(model_path)
    frame = build_input_frame(data, features)

    raw_prediction = model.predict(frame)[0]
    final_prediction = normalize_prediction(raw_prediction)

    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(model.predict_proba(frame).max())

    return {
        "prediction": final_prediction,
        "raw_prediction": str(raw_prediction),
        "confidence": confidence
    }, 200
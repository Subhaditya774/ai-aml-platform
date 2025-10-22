import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def generate_and_train(n=2000, out_model="app/models/aml_model.pkl", out_enc="app/models/country_encoder.pkl"):
    np.random.seed(42)
    data = pd.DataFrame({
        "amount": np.random.randint(10, 80000, n),
        "counterparty_country": np.random.choice(["US","UK","KY","CN","IN","SG","KY","AE"], n),
        "is_international": np.random.choice([0,1], n),
    })
    # label heuristic: suspicious if large+intl or KY country or very frequent pattern (simple)
    data["label"] = ((data["amount"] > 25000) & (data["is_international"] == 1)) | (data["counterparty_country"] == "KY")
    data["label"] = data["label"].astype(int)

    le = LabelEncoder()
    data["country_enc"] = le.fit_transform(data["counterparty_country"])

    X = data[["amount","country_enc","is_international"]]
    y = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(out_model), exist_ok=True)
    joblib.dump(model, out_model)
    joblib.dump(le, out_enc)

    print("Model trained. Train acc:", model.score(X_train,y_train), "Test acc:", model.score(X_test,y_test))

if __name__ == "__main__":
    generate_and_train()

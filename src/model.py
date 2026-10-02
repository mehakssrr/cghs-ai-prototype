import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier
from src.config import NOSHOW_MODEL_PATH

def train_noshow_model(df: pd.DataFrame):
    X = df.drop(columns=["no_show"])
    y = df["no_show"]
    
    # Encode gender
    X = X.copy()
    X["gender_male"] = (X["Gender"] == "M").astype(int)
    X = X.drop(columns=["Gender"])
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42
    )
    model.fit(X_train, y_train)
    
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"Test AUC: {auc:.3f}")
    
    NOSHOW_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, NOSHOW_MODEL_PATH)
    print(f"Model saved to {NOSHOW_MODEL_PATH}")
    return model

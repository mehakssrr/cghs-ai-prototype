
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

PROJECT_DIR = "/content/drive/MyDrive/cghs-ai-prototype"

DATA_PATH = os.path.join(PROJECT_DIR, "data", "appointments_no_show.csv")
df = pd.read_csv(DATA_PATH)

df = df.rename(columns=str.lower)
if 'no_show' not in df.columns:
    if 'no_show' in [c.lower() for c in df.columns]:
        rename_map = {c: c.lower() for c in df.columns}
        df = df.rename(columns=rename_map)

if df['no_show'].dtype == object:
    df['no_show'] = df['no_show'].map({'Yes': 1, 'No': 0, 'yes': 1, 'no': 0})

feature_cols = ['age']
# Add more if available, e.g. sms_received, neighbourhood, etc.

X = df[feature_cols].fillna(0)
y = df['no_show']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("Classification report:")
print(classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_proba))

MODEL_PATH = os.path.join(PROJECT_DIR, "ml_models", "noshow_model.pkl")
joblib.dump(model, MODEL_PATH)

preprocess_info = {
    "feature_cols": feature_cols
}
PREPROCESS_PATH = os.path.join(PROJECT_DIR, "ml_models", "preprocess_noshow.pkl")
joblib.dump(preprocess_info, PREPROCESS_PATH)

print("Model saved to:", MODEL_PATH)
print("Preprocess info saved to:", PREPROCESS_PATH)

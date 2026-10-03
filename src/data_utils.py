import pandas as pd
from src.config import DATA_DIR

def load_appointments_raw() -> pd.DataFrame:
    path = DATA_DIR / "raw" / "appointments_no_show.csv"
    df = pd.read_csv(path)
    return df

def clean_appointments(df: pd.DataFrame) -> pd.DataFrame:
    # Example cleaning; adapt column names to your dataset
    df = df.copy()
    
    # Target variable: 1 = no-show, 0 = showed up
    if "No_show" in df.columns:
        df["no_show"] = (df["No_show"] == "Yes").astype(int)
    elif "no_show" in df.columns:
        df["no_show"] = df["no_show"].astype(int)
    
    # Age sanity
    df = df[(df["Age"] >= 0) & (df["Age"] <= 100)]
    
    # Simple features
    df["is_senior"] = (df["Age"] >= 60).astype(int)
    
    # Keep only needed columns
    keep_cols = [c for c in df.columns if c in [
        "Age", "Gender", "is_senior", "no_show"
    ]]
    return df[keep_cols]

def save_processed(df: pd.DataFrame) -> None:
    path = DATA_DIR / "processed" / "appointments_clean.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

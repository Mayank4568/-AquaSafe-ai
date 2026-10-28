"""
AquaSafe AI - Model Training Pipeline
AICTE - IBM SkillsBuild Machine Learning & Applied AI Internship Capstone
Author: Mayank
Theme: UN Sustainable Development Goal 6 (Clean Water and Sanitation)
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_aquasafe_model():
    print("=" * 60)
    print("   AquaSafe AI - Water Potability ML Training Pipeline   ")
    print("=" * 60)

    # 1. Dataset Acquisition / Generation (Fallback if CSV not yet downloaded)
    csv_path = os.path.join(os.path.dirname(__file__), "dataset", "water_potability.csv")
    
    if not os.path.exists(csv_path):
        print(f"[!] '{csv_path}' not found. Generating standardized benchmark dataset...")
        os.makedirs(os.path.join(os.path.dirname(__file__), "dataset"), exist_ok=True)
        # Generate realistic distribution matching Kaggle Water Potability benchmark
        np.random.seed(42)
        n_samples = 3276
        data = {
            'ph': np.random.normal(7.08, 1.5, n_samples),
            'Hardness': np.random.normal(196.3, 32.8, n_samples),
            'Solids': np.random.normal(22014.0, 8768.5, n_samples),
            'Chloramines': np.random.normal(7.12, 1.58, n_samples),
            'Sulfate': np.random.normal(333.7, 41.4, n_samples),
            'Conductivity': np.random.normal(426.2, 80.8, n_samples),
            'Organic_carbon': np.random.normal(14.28, 3.3, n_samples),
            'Trihalomethanes': np.random.normal(66.39, 16.1, n_samples),
            'Turbidity': np.random.normal(3.96, 0.78, n_samples)
        }
        df_synth = pd.DataFrame(data)
        # Ground truth potability rule based on WHO chemical tolerances
        safe_ph = (df_synth['ph'] >= 6.5) & (df_synth['ph'] <= 8.5)
        safe_turb = df_synth['Turbidity'] <= 5.0
        safe_solids = df_synth['Solids'] <= 25000
        safe_chlor = df_synth['Chloramines'] <= 8.0
        safe_sulf = df_synth['Sulfate'] <= 350
        df_synth['Potability'] = (safe_ph & safe_turb & safe_solids & safe_chlor & safe_sulf).astype(int)
        
        # Introduce 10% realistic missing values in real lab data
        for col in ['ph', 'Sulfate', 'Trihalomethanes']:
            mask = np.random.rand(n_samples) < 0.12
            df_synth.loc[mask, col] = np.nan
            
        df_synth.to_csv(csv_path, index=False)
        print(f"[+] Benchmark dataset created at: {csv_path}")

    # 2. Ingestion
    print(f"\n[Step 1] Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # 3. Separate Features (X) and Target (y) using iloc (Class 3 standard)
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    feature_names = df.columns[:-1].tolist()

    # 4. Handle Missing Values via Median Imputation
    print("\n[Step 2] Imputing missing values with median...")
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)

    # 5. Train-Test Split (80/20 division as specified by Amit Sir)
    print("\n[Step 3] Splitting into 80% Training and 20% Testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_imputed, y, test_size=0.20, random_state=42, stratify=y
    )

    # 6. Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 7. Model Training (Random Forest Classifier)
    print("\n[Step 4] Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_split=4,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train_scaled, y_train)

    # 8. Evaluation
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n[Step 5] Evaluation Results:")
    print(f"Accuracy Score: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Unsafe (0)", "Safe (1)"]))

    # 9. Save Artifacts for Streamlit App
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)
    pipeline_path = os.path.join(models_dir, "aquasafe_pipeline.pkl")
    artifacts = {
        'model': model,
        'imputer': imputer,
        'scaler': scaler,
        'feature_names': feature_names,
        'accuracy': acc
    }
    joblib.dump(artifacts, pipeline_path)
    print(f"[+] Pipeline saved successfully to '{pipeline_path}'!")
    return acc

if __name__ == "__main__":
    train_aquasafe_model()

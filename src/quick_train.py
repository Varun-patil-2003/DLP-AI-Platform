"""
Quick Training Script - Uses only Random Forest (faster)
Skips SVM to avoid long training times
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import DATASET_PATH, RANDOM_FOREST_MODEL
from custom_preprocessing import CustomDataPreprocessor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
from imblearn.over_sampling import SMOTE

def train_quick_model():
    """Quick training with Random Forest only"""
    print("\n" + "=" * 80)
    print(" " * 15 + "QUICK TRAINING - RANDOM FOREST ONLY")
    print("=" * 80)
    
    # Preprocessing
    print("\n[1/3] Preprocessing data...")
    preprocessor = CustomDataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.preprocess_pipeline(DATASET_PATH)
    preprocessor.save_preprocessor()
    
    # Apply SMOTE
    print("\n[2/3] Training Random Forest model...")
    print("Applying SMOTE for class balance...")
    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    
    # Train Random Forest
    print("Training Random Forest (this takes ~2 minutes)...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    rf_model.fit(X_train_balanced, y_train_balanced)
    print("[OK] Training completed!")
    
    # Evaluate
    print("\n[3/3] Evaluating model...")
    y_pred = rf_model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("\nRandom Forest Performance:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  TN: {cm[0,0]:5d}  FP: {cm[0,1]:5d}")
    print(f"  FN: {cm[1,0]:5d}  TP: {cm[1,1]:5d}")
    
    # Save model
    print("\nSaving model...")
    joblib.dump(rf_model, RANDOM_FOREST_MODEL)
    print(f"[OK] Model saved to: {RANDOM_FOREST_MODEL}")
    
    # Create dummy SVM for app compatibility
    from config import SVM_MODEL
    joblib.dump(rf_model, SVM_MODEL)  # Use RF as placeholder
    print(f"[OK] Placeholder SVM saved for compatibility")
    
    # Generate report
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("QUICK TRAINING REPORT - RANDOM FOREST")
    report_lines.append("=" * 80)
    report_lines.append(f"\nDataset: {DATASET_PATH.name}")
    report_lines.append(f"Training Samples: {len(X_train)}")
    report_lines.append(f"Test Samples: {len(X_test)}")
    report_lines.append(f"Features: {len(preprocessor.feature_names)}")
    report_lines.append("\nModel Performance:")
    report_lines.append(f"  Accuracy:  {accuracy:.4f}")
    report_lines.append(f"  Precision: {precision:.4f}")
    report_lines.append(f"  Recall:    {recall:.4f}")
    report_lines.append(f"  F1-Score:  {f1:.4f}")
    report_lines.append("\n" + "=" * 80)
    report_lines.append("TRAINING COMPLETED - Ready to launch web app!")
    report_lines.append("=" * 80)
    
    report_path = Path(__file__).parent.parent / 'training_report.txt'
    with open(report_path, 'w') as f:
        f.write("\n".join(report_lines))
    
    print("\n" + "=" * 80)
    print("[OK] TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nNext step: Launch web app")
    print("  python app/app.py")
    print("\nOr double-click: run_webapp.bat")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    train_quick_model()

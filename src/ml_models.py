"""
Machine Learning Models Module
Implements Random Forest and SVM for data leakage detection
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
from imblearn.over_sampling import SMOTE
import joblib
from pathlib import Path
import sys
import time

sys.path.append(str(Path(__file__).parent.parent))
from config import RF_PARAMS, SVM_PARAMS, RANDOM_FOREST_MODEL, SVM_MODEL


class MLModelTrainer:
    """Train and evaluate machine learning models"""
    
    def __init__(self):
        self.rf_model = None
        self.svm_model = None
        self.feature_importance = None
        
    def handle_class_imbalance(self, X_train, y_train):
        """Handle class imbalance using SMOTE"""
        print("\nHandling class imbalance with SMOTE...")
        print(f"Original class distribution:")
        print(pd.Series(y_train).value_counts())
        
        smote = SMOTE(random_state=RF_PARAMS['random_state'])
        X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
        
        print(f"\nAfter SMOTE:")
        print(pd.Series(y_resampled).value_counts())
        
        return X_resampled, y_resampled
    
    def train_random_forest(self, X_train, y_train, use_smote=True):
        """Train Random Forest model"""
        print("\n" + "=" * 70)
        print("TRAINING RANDOM FOREST MODEL")
        print("=" * 70)
        
        # Handle class imbalance
        if use_smote:
            X_train, y_train = self.handle_class_imbalance(X_train, y_train)
        
        # Train model
        print("\nTraining Random Forest...")
        print(f"Parameters: {RF_PARAMS}")
        
        start_time = time.time()
        self.rf_model = RandomForestClassifier(**RF_PARAMS)
        self.rf_model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        print(f"[OK] Training completed in {training_time:.2f} seconds")
        
        # Feature importance
        if hasattr(X_train, 'columns'):
            self.feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': self.rf_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\nTop 10 Most Important Features:")
            print(self.feature_importance.head(10))
        
        return self.rf_model
    
    def train_svm(self, X_train, y_train, use_smote=True):
        """Train SVM model"""
        print("\n" + "=" * 70)
        print("TRAINING SVM MODEL")
        print("=" * 70)
        
        # Handle class imbalance
        if use_smote:
            X_train, y_train = self.handle_class_imbalance(X_train, y_train)
        
        # Train model
        print("\nTraining SVM...")
        print(f"Parameters: {SVM_PARAMS}")
        
        start_time = time.time()
        self.svm_model = SVC(**SVM_PARAMS, probability=True)
        self.svm_model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        print(f"[OK] Training completed in {training_time:.2f} seconds")
        
        return self.svm_model
    
    def evaluate_model(self, model, X_test, y_test, model_name="Model"):
        """Evaluate model performance"""
        print("\n" + "=" * 70)
        print(f"EVALUATING {model_name.upper()}")
        print("=" * 70)
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"\n{model_name} Performance Metrics:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        
        if y_pred_proba is not None:
            auc = roc_auc_score(y_test, y_pred_proba)
            print(f"  ROC-AUC:   {auc:.4f}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\nConfusion Matrix:")
        print(f"  TN: {cm[0][0]:5d}  FP: {cm[0][1]:5d}")
        print(f"  FN: {cm[1][0]:5d}  TP: {cm[1][1]:5d}")
        
        # Classification Report
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Normal', 'Leakage']))
        
        # Calculate false positive rate
        fpr = cm[0][1] / (cm[0][0] + cm[0][1]) if (cm[0][0] + cm[0][1]) > 0 else 0
        print(f"\nFalse Positive Rate: {fpr:.4f}")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'auc': auc if y_pred_proba is not None else None,
            'confusion_matrix': cm,
            'false_positive_rate': fpr
        }
    
    def save_models(self):
        """Save trained models"""
        print("\n" + "=" * 70)
        print("SAVING MODELS")
        print("=" * 70)
        
        if self.rf_model is not None:
            joblib.dump(self.rf_model, RANDOM_FOREST_MODEL)
            print(f"[OK] Random Forest model saved to: {RANDOM_FOREST_MODEL}")
        
        if self.svm_model is not None:
            joblib.dump(self.svm_model, SVM_MODEL)
            print(f"[OK] SVM model saved to: {SVM_MODEL}")
        
        if self.feature_importance is not None:
            importance_path = RANDOM_FOREST_MODEL.parent / 'feature_importance.csv'
            self.feature_importance.to_csv(importance_path, index=False)
            print(f"[OK] Feature importance saved to: {importance_path}")
    
    @staticmethod
    def load_model(model_path):
        """Load a trained model"""
        model = joblib.load(model_path)
        print(f"[OK] Model loaded from: {model_path}")
        return model
    
    def compare_models(self, rf_metrics, svm_metrics):
        """Compare performance of models"""
        print("\n" + "=" * 70)
        print("MODEL COMPARISON")
        print("=" * 70)
        
        comparison_df = pd.DataFrame({
            'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC', 'FPR'],
            'Random Forest': [
                rf_metrics['accuracy'],
                rf_metrics['precision'],
                rf_metrics['recall'],
                rf_metrics['f1_score'],
                rf_metrics['auc'],
                rf_metrics['false_positive_rate']
            ],
            'SVM': [
                svm_metrics['accuracy'],
                svm_metrics['precision'],
                svm_metrics['recall'],
                svm_metrics['f1_score'],
                svm_metrics['auc'],
                svm_metrics['false_positive_rate']
            ]
        })
        
        print("\n", comparison_df.to_string(index=False))
        
        # Determine best model
        if rf_metrics['f1_score'] > svm_metrics['f1_score']:
            print("\n[OK] Best Model: Random Forest")
        else:
            print("\n[OK] Best Model: SVM")
        
        return comparison_df


def main():
    """Test ML models"""
    from config import DATASET_PATH
    from preprocessing import DataPreprocessor
    from feature_engineering import FeatureEngineer
    
    print("=" * 70)
    print("TRAINING MACHINE LEARNING MODELS")
    print("=" * 70)
    
    # Load data
    print("\nLoading dataset...")
    df = pd.read_csv(DATASET_PATH)
    
    # Feature engineering
    engineer = FeatureEngineer()
    df = engineer.engineer_features(df)
    
    # Preprocessing
    preprocessor = DataPreprocessor()
    df_processed = preprocessor.preprocess(df, fit=True)
    X_train, X_test, y_train, y_test = preprocessor.prepare_train_test_split(df_processed)
    
    # Train models
    trainer = MLModelTrainer()
    
    # Random Forest
    trainer.train_random_forest(X_train, y_train)
    rf_metrics = trainer.evaluate_model(trainer.rf_model, X_test, y_test, "Random Forest")
    
    # SVM
    trainer.train_svm(X_train, y_train)
    svm_metrics = trainer.evaluate_model(trainer.svm_model, X_test, y_test, "SVM")
    
    # Compare models
    trainer.compare_models(rf_metrics, svm_metrics)
    
    # Save models
    trainer.save_models()
    preprocessor.save_preprocessor()
    
    print("\n" + "=" * 70)
    print("[OK] Model training completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()

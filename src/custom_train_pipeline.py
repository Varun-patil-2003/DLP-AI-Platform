"""
Custom Training Pipeline for Data_Leakage_Detection.csv
Complete workflow from data loading to model training
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import DATASET_PATH
from custom_preprocessing import CustomDataPreprocessor
from ml_models import MLModelTrainer

def main():
    """Main training pipeline"""
    print("\n" + "=" * 80)
    print(" " * 10 + "AI-DRIVEN DATA LEAKAGE DETECTION")
    print(" " * 15 + "CUSTOM TRAINING PIPELINE")
    print("=" * 80)
    print(f"\nDataset: {DATASET_PATH.name}")
    print(f"Location: {DATASET_PATH}")
    print("=" * 80)
    
    try:
        # Step 1: Preprocessing
        print("\n" + "=" * 80)
        print("STEP 1: DATA PREPROCESSING")
        print("=" * 80)
        
        preprocessor = CustomDataPreprocessor()
        X_train, X_test, y_train, y_test = preprocessor.preprocess_pipeline(DATASET_PATH)
        
        # Save preprocessor
        preprocessor.save_preprocessor()
        
        # Step 2: Train ML Models
        print("\n" + "=" * 80)
        print("STEP 2: TRAINING MACHINE LEARNING MODELS")
        print("=" * 80)
        
        ml_trainer = MLModelTrainer()
        
        # Train Random Forest
        print("\n>>> Training Random Forest Model...")
        ml_trainer.train_random_forest(X_train, y_train, use_smote=True)
        rf_metrics = ml_trainer.evaluate_model(
            ml_trainer.rf_model, X_test, y_test, "Random Forest"
        )
        
        # Train SVM
        print("\n>>> Training SVM Model...")
        ml_trainer.train_svm(X_train, y_train, use_smote=True)
        svm_metrics = ml_trainer.evaluate_model(
            ml_trainer.svm_model, X_test, y_test, "SVM"
        )
        
        # Compare models
        print("\n>>> Comparing Models...")
        comparison = ml_trainer.compare_models(rf_metrics, svm_metrics)
        
        # Save models
        ml_trainer.save_models()
        
        # Step 3: Generate Report
        print("\n" + "=" * 80)
        print("STEP 3: GENERATING TRAINING REPORT")
        print("=" * 80)
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("AI-DRIVEN DATA LEAKAGE DETECTION - TRAINING REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        report_lines.append(f"Dataset: {DATASET_PATH.name}")
        report_lines.append(f"Training Samples: {len(X_train)}")
        report_lines.append(f"Test Samples: {len(X_test)}")
        report_lines.append(f"Features: {len(preprocessor.feature_names)}")
        report_lines.append("")
        report_lines.append("FEATURE LIST:")
        for i, feature in enumerate(preprocessor.feature_names, 1):
            report_lines.append(f"  {i:2d}. {feature}")
        report_lines.append("")
        report_lines.append("MODEL PERFORMANCE:")
        report_lines.append("-" * 80)
        report_lines.append(f"{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        report_lines.append("-" * 80)
        report_lines.append(
            f"{'Random Forest':<20} "
            f"{rf_metrics['accuracy']:<12.4f} "
            f"{rf_metrics['precision']:<12.4f} "
            f"{rf_metrics['recall']:<12.4f} "
            f"{rf_metrics['f1_score']:<12.4f}"
        )
        report_lines.append(
            f"{'SVM':<20} "
            f"{svm_metrics['accuracy']:<12.4f} "
            f"{svm_metrics['precision']:<12.4f} "
            f"{svm_metrics['recall']:<12.4f} "
            f"{svm_metrics['f1_score']:<12.4f}"
        )
        report_lines.append("")
        
        # Best model
        best_model = "Random Forest" if rf_metrics['f1_score'] > svm_metrics['f1_score'] else "SVM"
        best_f1 = max(rf_metrics['f1_score'], svm_metrics['f1_score'])
        report_lines.append(f"BEST MODEL: {best_model} (F1-Score: {best_f1:.4f})")
        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("TRAINING COMPLETED SUCCESSFULLY!")
        report_lines.append("=" * 80)
        
        # Print and save report
        report_text = "\n".join(report_lines)
        print("\n" + report_text)
        
        report_path = Path(__file__).parent.parent / 'training_report.txt'
        with open(report_path, 'w') as f:
            f.write(report_text)
        
        print(f"\n[OK] Report saved to: {report_path}")
        
        # Final Summary
        print("\n" + "=" * 80)
        print(" " * 25 + "TRAINING COMPLETE!")
        print("=" * 80)
        print("\nGenerated Files:")
        print(f"  [OK] models/random_forest_model.pkl")
        print(f"  [OK] models/svm_model.pkl")
        print(f"  [OK] models/scaler.pkl")
        print(f"  [OK] models/feature_importance.csv")
        print(f"  [OK] training_report.txt")
        print("\nNext Steps:")
        print(f"  1. Review training_report.txt")
        print(f"  2. Launch web app: python app/app.py")
        print(f"  3. Test predictions at http://localhost:5000")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n" + "=" * 80)
        print("[ERROR] ERROR OCCURRED")
        print("=" * 80)
        print(f"Error: {str(e)}")
        print("\nDebug Information:")
        import traceback
        traceback.print_exc()
        print("=" * 80)
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

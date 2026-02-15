"""
Complete Training Pipeline
Orchestrates the entire model training workflow
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import warnings
warnings.filterwarnings('ignore')

sys.path.append(str(Path(__file__).parent.parent))
from config import DATASET_PATH
from data_generator import DataLeakageDatasetGenerator
from preprocessing import DataPreprocessor
from feature_engineering import FeatureEngineer
from ml_models import MLModelTrainer
from dl_models import DLModelTrainer


class TrainingPipeline:
    """Complete training pipeline for all models"""
    
    def __init__(self):
        self.df = None
        self.df_processed = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.results = {}
        
    def step1_generate_dataset(self, n_samples=10000, leakage_ratio=0.15):
        """Step 1: Generate synthetic dataset"""
        print("\n" + "=" * 70)
        print("STEP 1: GENERATING DATASET")
        print("=" * 70)
        
        generator = DataLeakageDatasetGenerator(
            n_samples=n_samples,
            leakage_ratio=leakage_ratio
        )
        self.df = generator.generate_dataset()
        generator.save_dataset(self.df)
        
        return self.df
    
    def step2_feature_engineering(self):
        """Step 2: Engineer features"""
        print("\n" + "=" * 70)
        print("STEP 2: FEATURE ENGINEERING")
        print("=" * 70)
        
        engineer = FeatureEngineer()
        self.df = engineer.engineer_features(self.df)
        
        return self.df
    
    def step3_preprocessing(self):
        """Step 3: Preprocess data"""
        print("\n" + "=" * 70)
        print("STEP 3: DATA PREPROCESSING")
        print("=" * 70)
        
        self.preprocessor = DataPreprocessor()
        self.df_processed = self.preprocessor.preprocess(self.df, fit=True)
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = \
            self.preprocessor.prepare_train_test_split(self.df_processed)
        
        # Save preprocessor
        self.preprocessor.save_preprocessor()
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def step4_train_ml_models(self):
        """Step 4: Train ML models"""
        print("\n" + "=" * 70)
        print("STEP 4: TRAINING MACHINE LEARNING MODELS")
        print("=" * 70)
        
        ml_trainer = MLModelTrainer()
        
        # Train Random Forest
        ml_trainer.train_random_forest(self.X_train, self.y_train)
        rf_metrics = ml_trainer.evaluate_model(
            ml_trainer.rf_model, self.X_test, self.y_test, "Random Forest"
        )
        self.results['random_forest'] = rf_metrics
        
        # Train SVM
        ml_trainer.train_svm(self.X_train, self.y_train)
        svm_metrics = ml_trainer.evaluate_model(
            ml_trainer.svm_model, self.X_test, self.y_test, "SVM"
        )
        self.results['svm'] = svm_metrics
        
        # Compare models
        comparison = ml_trainer.compare_models(rf_metrics, svm_metrics)
        
        # Save models
        ml_trainer.save_models()
        
        return rf_metrics, svm_metrics
    
    def step5_train_dl_models(self):
        """Step 5: Train DL models"""
        print("\n" + "=" * 70)
        print("STEP 5: TRAINING DEEP LEARNING MODELS")
        print("=" * 70)
        
        dl_trainer = DLModelTrainer()
        
        # Train LSTM
        print("\n>>> Training LSTM Model...")
        dl_trainer.train_lstm(self.X_train, self.y_train)
        lstm_metrics = dl_trainer.evaluate_lstm(self.X_test, self.y_test)
        self.results['lstm'] = lstm_metrics
        
        # Train Autoencoder
        print("\n>>> Training Autoencoder...")
        dl_trainer.train_autoencoder(self.X_train)
        autoencoder_metrics = dl_trainer.detect_anomalies_autoencoder(
            self.X_test, self.y_test
        )
        self.results['autoencoder'] = autoencoder_metrics
        
        # Save models
        dl_trainer.save_models()
        
        return lstm_metrics, autoencoder_metrics
    
    def step6_generate_report(self):
        """Step 6: Generate comprehensive report"""
        print("\n" + "=" * 70)
        print("STEP 6: GENERATING FINAL REPORT")
        print("=" * 70)
        
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("AI-DRIVEN DATA LEAKAGE DETECTION - TRAINING REPORT")
        report_lines.append("=" * 70)
        report_lines.append("")
        
        report_lines.append("DATASET INFORMATION")
        report_lines.append("-" * 70)
        report_lines.append(f"Total Samples: {len(self.df)}")
        report_lines.append(f"Training Samples: {len(self.X_train)}")
        report_lines.append(f"Test Samples: {len(self.X_test)}")
        report_lines.append(f"Number of Features: {self.X_train.shape[1]}")
        report_lines.append(f"Class Distribution: {dict(self.df['is_leakage'].value_counts())}")
        report_lines.append("")
        
        report_lines.append("MODEL PERFORMANCE SUMMARY")
        report_lines.append("-" * 70)
        
        # Create comparison table
        models = ['random_forest', 'svm', 'lstm', 'autoencoder']
        metrics_names = ['accuracy', 'precision', 'recall', 'f1_score']
        
        report_lines.append(f"{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        report_lines.append("-" * 70)
        
        for model in models:
            if model in self.results:
                metrics = self.results[model]
                report_lines.append(
                    f"{model.replace('_', ' ').title():<20} "
                    f"{metrics['accuracy']:<12.4f} "
                    f"{metrics['precision']:<12.4f} "
                    f"{metrics['recall']:<12.4f} "
                    f"{metrics['f1_score']:<12.4f}"
                )
        
        report_lines.append("")
        
        # Best model
        best_model = max(self.results.items(), key=lambda x: x[1]['f1_score'])
        report_lines.append(f"BEST MODEL: {best_model[0].replace('_', ' ').title()}")
        report_lines.append(f"Best F1-Score: {best_model[1]['f1_score']:.4f}")
        report_lines.append("")
        
        report_lines.append("=" * 70)
        report_lines.append("TRAINING COMPLETED SUCCESSFULLY!")
        report_lines.append("=" * 70)
        
        # Print report
        report_text = "\n".join(report_lines)
        print("\n" + report_text)
        
        # Save report
        report_path = Path(__file__).parent.parent / 'training_report.txt'
        with open(report_path, 'w') as f:
            f.write(report_text)
        
        print(f"\n✓ Report saved to: {report_path}")
    
    def run_complete_pipeline(self):
        """Run the complete training pipeline"""
        print("\n" + "=" * 80)
        print(" " * 15 + "AI-DRIVEN DATA LEAKAGE DETECTION")
        print(" " * 20 + "COMPLETE TRAINING PIPELINE")
        print("=" * 80)
        
        try:
            # Check if dataset exists
            if not DATASET_PATH.exists():
                self.step1_generate_dataset()
            else:
                print(f"\nLoading existing dataset from: {DATASET_PATH}")
                self.df = pd.read_csv(DATASET_PATH)
                print(f"✓ Dataset loaded: {self.df.shape}")
            
            # Feature Engineering
            self.step2_feature_engineering()
            
            # Preprocessing
            self.step3_preprocessing()
            
            # Train ML Models
            self.step4_train_ml_models()
            
            # Train DL Models
            self.step5_train_dl_models()
            
            # Generate Report
            self.step6_generate_report()
            
            print("\n" + "=" * 80)
            print(" " * 25 + "PIPELINE COMPLETED!")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n❌ Error in pipeline: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Main function"""
    pipeline = TrainingPipeline()
    pipeline.run_complete_pipeline()


if __name__ == "__main__":
    main()

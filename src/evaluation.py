"""
Model Evaluation and Visualization Module
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve,
    confusion_matrix, classification_report
)
import joblib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import MODELS_DIR, DATASET_PATH


class ModelEvaluator:
    """Evaluate and visualize model performance"""
    
    def __init__(self):
        self.results_dir = MODELS_DIR.parent / 'results'
        self.results_dir.mkdir(exist_ok=True)
        
    def plot_confusion_matrix(self, cm, model_name, save=True):
        """Plot confusion matrix heatmap"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Normal', 'Leakage'],
                   yticklabels=['Normal', 'Leakage'])
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if save:
            path = self.results_dir / f'{model_name}_confusion_matrix.png'
            plt.savefig(path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {path}")
        
        plt.close()
    
    def plot_roc_curve(self, y_test, y_pred_proba, model_name, save=True):
        """Plot ROC curve"""
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.4f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {model_name}')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        
        if save:
            path = self.results_dir / f'{model_name}_roc_curve.png'
            plt.savefig(path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {path}")
        
        plt.close()
    
    def plot_precision_recall_curve(self, y_test, y_pred_proba, model_name, save=True):
        """Plot Precision-Recall curve"""
        precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='blue', lw=2)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Precision-Recall Curve - {model_name}')
        plt.grid(alpha=0.3)
        
        if save:
            path = self.results_dir / f'{model_name}_pr_curve.png'
            plt.savefig(path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {path}")
        
        plt.close()
    
    def plot_feature_importance(self, feature_importance_df, top_n=20, save=True):
        """Plot feature importance"""
        plt.figure(figsize=(10, 8))
        
        top_features = feature_importance_df.head(top_n)
        sns.barplot(x='importance', y='feature', data=top_features, palette='viridis')
        plt.title(f'Top {top_n} Most Important Features')
        plt.xlabel('Importance Score')
        plt.ylabel('Feature')
        plt.tight_layout()
        
        if save:
            path = self.results_dir / 'feature_importance.png'
            plt.savefig(path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {path}")
        
        plt.close()
    
    def plot_model_comparison(self, results_dict, save=True):
        """Plot model comparison"""
        models = list(results_dict.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        
        data = {metric: [results_dict[model][metric] for model in models] 
                for metric in metrics}
        
        df = pd.DataFrame(data, index=[m.replace('_', ' ').title() for m in models])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        df.plot(kind='bar', ax=ax, width=0.8)
        plt.title('Model Performance Comparison')
        plt.xlabel('Models')
        plt.ylabel('Score')
        plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        plt.ylim([0, 1.0])
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save:
            path = self.results_dir / 'model_comparison.png'
            plt.savefig(path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {path}")
        
        plt.close()
    
    def plot_training_history(self, history, model_name, save=True):
        """Plot training history for deep learning models"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Loss
        axes[0].plot(history.history['loss'], label='Training Loss')
        if 'val_loss' in history.history:
            axes[0].plot(history.history['val_loss'], label='Validation Loss')
        axes[0].set_title(f'{model_name} - Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Accuracy
        if 'accuracy' in history.history:
            axes[1].plot(history.history['accuracy'], label='Training Accuracy')
            if 'val_accuracy' in history.history:
                axes[1].plot(history.history['val_accuracy'], label='Validation Accuracy')
            axes[1].set_title(f'{model_name} - Accuracy')
            axes[1].set_xlabel('Epoch')
            axes[1].set_ylabel('Accuracy')
            axes[1].legend()
            axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            path = self.results_dir / f'{model_name}_training_history.png'
            plt.savefig(path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {path}")
        
        plt.close()
    
    def generate_evaluation_report(self, y_test, y_pred, y_pred_proba, model_name):
        """Generate comprehensive evaluation report"""
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append(f"EVALUATION REPORT: {model_name.upper()}")
        report_lines.append("=" * 70)
        report_lines.append("")
        
        # Classification Report
        report_lines.append("CLASSIFICATION REPORT")
        report_lines.append("-" * 70)
        report_lines.append(classification_report(y_test, y_pred, 
                                                  target_names=['Normal', 'Leakage']))
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        report_lines.append("\nCONFUSION MATRIX")
        report_lines.append("-" * 70)
        report_lines.append(f"True Negatives:  {cm[0][0]}")
        report_lines.append(f"False Positives: {cm[0][1]}")
        report_lines.append(f"False Negatives: {cm[1][0]}")
        report_lines.append(f"True Positives:  {cm[1][1]}")
        
        # Additional Metrics
        fpr = cm[0][1] / (cm[0][0] + cm[0][1]) if (cm[0][0] + cm[0][1]) > 0 else 0
        fnr = cm[1][0] / (cm[1][0] + cm[1][1]) if (cm[1][0] + cm[1][1]) > 0 else 0
        
        report_lines.append("\nADDITIONAL METRICS")
        report_lines.append("-" * 70)
        report_lines.append(f"False Positive Rate: {fpr:.4f}")
        report_lines.append(f"False Negative Rate: {fnr:.4f}")
        
        report_lines.append("")
        report_lines.append("=" * 70)
        
        report_text = "\n".join(report_lines)
        
        # Save report
        report_path = self.results_dir / f'{model_name}_evaluation_report.txt'
        with open(report_path, 'w') as f:
            f.write(report_text)
        
        print(f"✓ Evaluation report saved: {report_path}")
        
        return report_text


def main():
    """Test evaluation module"""
    print("=" * 70)
    print("MODEL EVALUATION MODULE")
    print("=" * 70)
    
    evaluator = ModelEvaluator()
    
    # Load feature importance if exists
    importance_path = MODELS_DIR / 'feature_importance.csv'
    if importance_path.exists():
        print("\nGenerating feature importance plot...")
        feature_importance = pd.read_csv(importance_path)
        evaluator.plot_feature_importance(feature_importance)
    
    print("\n✓ Evaluation module ready")


if __name__ == "__main__":
    main()

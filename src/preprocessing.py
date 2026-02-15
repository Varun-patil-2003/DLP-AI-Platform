"""
Data Preprocessing Module
Handles data cleaning, encoding, and normalization
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import RANDOM_STATE, TEST_SIZE, SCALER_PATH


class DataPreprocessor:
    """Preprocess data for machine learning models"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.categorical_columns = []
        self.numerical_columns = []
        self.feature_names = []
        
    def identify_column_types(self, df):
        """Identify categorical and numerical columns"""
        # Exclude target and ID columns
        exclude_cols = ['is_leakage', 'user_id', 'session_id']
        
        self.categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        self.categorical_columns = [col for col in self.categorical_columns if col not in exclude_cols]
        
        self.numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.numerical_columns = [col for col in self.numerical_columns if col not in exclude_cols]
        
        print(f"Categorical columns ({len(self.categorical_columns)}): {self.categorical_columns}")
        print(f"Numerical columns ({len(self.numerical_columns)}): {self.numerical_columns}")
        
    def encode_categorical_features(self, df, fit=True):
        """Encode categorical features using Label Encoding"""
        df_encoded = df.copy()
        
        for col in self.categorical_columns:
            if fit:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
            else:
                if col in self.label_encoders:
                    # Handle unseen categories
                    le = self.label_encoders[col]
                    df_encoded[col] = df[col].apply(
                        lambda x: le.transform([str(x)])[0] if str(x) in le.classes_ else -1
                    )
                    
        return df_encoded
    
    def scale_numerical_features(self, df, fit=True):
        """Scale numerical features"""
        df_scaled = df.copy()
        
        if len(self.numerical_columns) > 0:
            if fit:
                df_scaled[self.numerical_columns] = self.scaler.fit_transform(
                    df[self.numerical_columns]
                )
            else:
                df_scaled[self.numerical_columns] = self.scaler.transform(
                    df[self.numerical_columns]
                )
        
        return df_scaled
    
    def handle_missing_values(self, df):
        """Handle missing values"""
        # Fill numerical columns with median
        for col in self.numerical_columns:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        # Fill categorical columns with mode
        for col in self.categorical_columns:
            if df[col].isnull().any():
                df[col].fillna(df[col].mode()[0], inplace=True)
        
        return df
    
    def preprocess(self, df, fit=True):
        """Complete preprocessing pipeline"""
        print("\n" + "=" * 70)
        print("PREPROCESSING DATA")
        print("=" * 70)
        
        # Make a copy
        df_processed = df.copy()
        
        # Identify column types
        if fit:
            self.identify_column_types(df_processed)
        
        # Handle missing values
        print("\nHandling missing values...")
        df_processed = self.handle_missing_values(df_processed)
        
        # Encode categorical features
        print("Encoding categorical features...")
        df_processed = self.encode_categorical_features(df_processed, fit=fit)
        
        # Scale numerical features
        print("Scaling numerical features...")
        df_processed = self.scale_numerical_features(df_processed, fit=fit)
        
        # Store feature names
        if fit:
            self.feature_names = [col for col in df_processed.columns 
                                 if col not in ['is_leakage', 'user_id', 'session_id']]
        
        print(f"\n✓ Preprocessing completed")
        print(f"✓ Total features: {len(self.feature_names)}")
        
        return df_processed
    
    def prepare_train_test_split(self, df, target_col='is_leakage'):
        """Prepare train and test sets"""
        print("\n" + "=" * 70)
        print("PREPARING TRAIN-TEST SPLIT")
        print("=" * 70)
        
        # Separate features and target
        X = df[self.feature_names]
        y = df[target_col]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=TEST_SIZE, 
            random_state=RANDOM_STATE,
            stratify=y
        )
        
        print(f"Training set size: {X_train.shape}")
        print(f"Test set size: {X_test.shape}")
        print(f"\nClass distribution in training set:")
        print(y_train.value_counts(normalize=True))
        
        return X_train, X_test, y_train, y_test
    
    def save_preprocessor(self, path=None):
        """Save preprocessor objects"""
        if path is None:
            path = SCALER_PATH
        
        preprocessor_data = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'categorical_columns': self.categorical_columns,
            'numerical_columns': self.numerical_columns,
            'feature_names': self.feature_names
        }
        
        joblib.dump(preprocessor_data, path)
        print(f"\n✓ Preprocessor saved to: {path}")
    
    @staticmethod
    def load_preprocessor(path=None):
        """Load preprocessor objects"""
        if path is None:
            path = SCALER_PATH
        
        preprocessor_data = joblib.load(path)
        
        preprocessor = DataPreprocessor()
        preprocessor.scaler = preprocessor_data['scaler']
        preprocessor.label_encoders = preprocessor_data['label_encoders']
        preprocessor.categorical_columns = preprocessor_data['categorical_columns']
        preprocessor.numerical_columns = preprocessor_data['numerical_columns']
        preprocessor.feature_names = preprocessor_data['feature_names']
        
        print(f"✓ Preprocessor loaded from: {path}")
        return preprocessor


def main():
    """Test preprocessing module"""
    from config import DATASET_PATH
    
    print("=" * 70)
    print("TESTING DATA PREPROCESSING MODULE")
    print("=" * 70)
    
    # Load data
    print("\nLoading dataset...")
    df = pd.read_csv(DATASET_PATH)
    print(f"✓ Dataset loaded: {df.shape}")
    
    # Create preprocessor
    preprocessor = DataPreprocessor()
    
    # Preprocess data
    df_processed = preprocessor.preprocess(df, fit=True)
    
    # Prepare train-test split
    X_train, X_test, y_train, y_test = preprocessor.prepare_train_test_split(df_processed)
    
    # Save preprocessor
    preprocessor.save_preprocessor()
    
    print("\n" + "=" * 70)
    print("✓ Preprocessing test completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()

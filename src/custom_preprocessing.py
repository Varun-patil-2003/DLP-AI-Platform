"""
Custom Preprocessing for Data_Leakage_Detection.csv
Handles the actual dataset structure with 15 columns
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import joblib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import RANDOM_STATE, TEST_SIZE, SCALER_PATH


class CustomDataPreprocessor:
    """Preprocess Data_Leakage_Detection.csv dataset"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.numerical_imputer = SimpleImputer(strategy='median')
        self.categorical_imputer = SimpleImputer(strategy='most_frequent')
        self.feature_names = []
        
    def load_and_clean_data(self, filepath):
        """Load and perform initial cleaning"""
        print("\n" + "=" * 70)
        print("LOADING DATASET")
        print("=" * 70)
        
        df = pd.read_csv(filepath)
        print(f"[OK] Dataset loaded: {df.shape}")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        
        # Display column info
        print(f"\nColumns:")
        for i, col in enumerate(df.columns, 1):
            missing = df[col].isnull().sum()
            dtype = str(df[col].dtype)
            print(f"  {i:2d}. {col:30s} - {dtype:8s} ({missing:5d} missing)")
        
        # Check target variable
        print(f"\nTarget Variable (Abnormality) Distribution:")
        print(df['Abnormality'].value_counts())
        print(f"Percentage:")
        print((df['Abnormality'].value_counts(normalize=True) * 100).round(2))
        
        return df
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        print("\n" + "=" * 70)
        print("HANDLING MISSING VALUES")
        print("=" * 70)
        
        df_clean = df.copy()
        
        # Identify column types
        numerical_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        numerical_cols = [col for col in numerical_cols if col not in ['id', 'Abnormality']]
        
        categorical_cols = df_clean.select_dtypes(include=['object']).columns.tolist()
        
        # Impute numerical columns
        if numerical_cols:
            print(f"\nImputing {len(numerical_cols)} numerical columns...")
            df_clean[numerical_cols] = self.numerical_imputer.fit_transform(df_clean[numerical_cols])
            print("[OK] Numerical imputation completed")
        
        # Impute categorical columns
        if categorical_cols:
            print(f"\nImputing {len(categorical_cols)} categorical columns...")
            for col in categorical_cols:
                if df_clean[col].isnull().any():
                    mode_value = df_clean[col].mode()
                    if len(mode_value) > 0:
                        df_clean[col].fillna(mode_value[0], inplace=True)
                    else:
                        df_clean[col].fillna('unknown', inplace=True)
            print("[OK] Categorical imputation completed")
        
        print(f"\n[OK] Missing values handled successfully")
        print(f"  Remaining missing values: {df_clean.isnull().sum().sum()}")
        
        return df_clean
    
    def engineer_features(self, df):
        """Create additional features from existing data"""
        print("\n" + "=" * 70)
        print("FEATURE ENGINEERING")
        print("=" * 70)
        
        df_eng = df.copy()
        
        # Parse date if present
        if 'date' in df_eng.columns and not df_eng['date'].isnull().all():
            try:
                df_eng['date_parsed'] = pd.to_datetime(df_eng['date'], errors='coerce')
                df_eng['hour'] = df_eng['date_parsed'].dt.hour
                df_eng['day_of_week'] = df_eng['date_parsed'].dt.dayofweek
                df_eng['is_weekend'] = (df_eng['day_of_week'] >= 5).astype(int)
                df_eng['is_business_hours'] = ((df_eng['hour'] >= 9) & (df_eng['hour'] <= 17)).astype(int)
                
                # Drop parsed date column
                df_eng.drop(['date_parsed'], axis=1, inplace=True)
                print("[OK] Temporal features extracted from date")
            except Exception as e:
                print(f"[WARN] Could not parse dates: {e}")
        
        # Authentication risk score
        auth_cols = ['Through_pwd', 'Through_pin', 'Through_MFA']
        available_auth = [col for col in auth_cols if col in df_eng.columns]
        if available_auth:
            df_eng['auth_method_count'] = df_eng[available_auth].sum(axis=1)
            print("[OK] Authentication features aggregated")
        
        # Data access risk score
        access_cols = ['Data Modification', 'Confidential Data Access', 'Confidential File Transfer']
        available_access = [col for col in access_cols if col in df_eng.columns]
        if available_access:
            df_eng['data_access_score'] = df_eng[available_access].sum(axis=1)
            print("[OK] Data access risk score created")
        
        print(f"\n[OK] Feature engineering completed")
        print(f"  Total features now: {len(df_eng.columns)}")
        
        return df_eng
    
    def encode_categorical_features(self, df, fit=True):
        """Encode categorical features"""
        print("\n" + "=" * 70)
        print("ENCODING CATEGORICAL FEATURES")
        print("=" * 70)
        
        df_encoded = df.copy()
        
        # Identify categorical columns (excluding id and target)
        categorical_cols = df_encoded.select_dtypes(include=['object']).columns.tolist()
        categorical_cols = [col for col in categorical_cols if col not in ['id', 'date']]
        
        print(f"Encoding {len(categorical_cols)} categorical columns...")
        
        for col in categorical_cols:
            if fit:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                self.label_encoders[col] = le
                print(f"  [OK] {col}: {len(le.classes_)} unique values")
            else:
                if col in self.label_encoders:
                    le = self.label_encoders[col]
                    df_encoded[col] = df_encoded[col].apply(
                        lambda x: le.transform([str(x)])[0] if str(x) in le.classes_ else -1
                    )
        
        print("[OK] Encoding completed")
        return df_encoded
    
    def scale_features(self, df, fit=True):
        """Scale numerical features"""
        print("\n" + "=" * 70)
        print("SCALING FEATURES")
        print("=" * 70)
        
        df_scaled = df.copy()
        
        # Identify numerical columns (excluding id and target)
        numerical_cols = df_scaled.select_dtypes(include=[np.number]).columns.tolist()
        numerical_cols = [col for col in numerical_cols if col not in ['id', 'Abnormality']]
        
        if numerical_cols:
            print(f"Scaling {len(numerical_cols)} numerical features...")
            if fit:
                df_scaled[numerical_cols] = self.scaler.fit_transform(df_scaled[numerical_cols])
            else:
                df_scaled[numerical_cols] = self.scaler.transform(df_scaled[numerical_cols])
            print("[OK] Scaling completed")
        
        return df_scaled
    
    def prepare_features_target(self, df):
        """Separate features and target"""
        # Drop non-feature columns
        drop_cols = ['id', 'date', 'Abnormality']
        drop_cols = [col for col in drop_cols if col in df.columns]
        
        X = df.drop(columns=drop_cols)
        y = df['Abnormality']
        
        self.feature_names = X.columns.tolist()
        
        print(f"\n[OK] Features prepared")
        print(f"  Feature count: {len(self.feature_names)}")
        print(f"  Sample size: {len(X)}")
        
        return X, y
    
    def preprocess_pipeline(self, filepath):
        """Complete preprocessing pipeline"""
        print("\n" + "=" * 80)
        print(" " * 20 + "DATA PREPROCESSING PIPELINE")
        print("=" * 80)
        
        # Load data
        df = self.load_and_clean_data(filepath)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Feature engineering
        df = self.engineer_features(df)
        
        # Encode categorical
        df = self.encode_categorical_features(df, fit=True)
        
        # Scale features
        df = self.scale_features(df, fit=True)
        
        # Prepare X, y
        X, y = self.prepare_features_target(df)
        
        # Train-test split
        print("\n" + "=" * 70)
        print("TRAIN-TEST SPLIT")
        print("=" * 70)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=y
        )
        
        print(f"Training set: {X_train.shape}")
        print(f"Test set: {X_test.shape}")
        print(f"\nClass distribution in training set:")
        print(y_train.value_counts())
        print(f"\nClass distribution in test set:")
        print(y_test.value_counts())
        
        print("\n" + "=" * 80)
        print("[OK] PREPROCESSING COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
        return X_train, X_test, y_train, y_test
    
    def save_preprocessor(self, path=None):
        """Save preprocessor objects"""
        if path is None:
            path = SCALER_PATH
        
        preprocessor_data = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'numerical_imputer': self.numerical_imputer,
            'categorical_imputer': self.categorical_imputer,
            'feature_names': self.feature_names
        }
        
        joblib.dump(preprocessor_data, path)
        print(f"\n[OK] Preprocessor saved to: {path}")
    
    @staticmethod
    def load_preprocessor(path=None):
        """Load preprocessor objects"""
        if path is None:
            path = SCALER_PATH
        
        preprocessor_data = joblib.load(path)
        
        preprocessor = CustomDataPreprocessor()
        preprocessor.scaler = preprocessor_data['scaler']
        preprocessor.label_encoders = preprocessor_data['label_encoders']
        preprocessor.numerical_imputer = preprocessor_data['numerical_imputer']
        preprocessor.categorical_imputer = preprocessor_data['categorical_imputer']
        preprocessor.feature_names = preprocessor_data['feature_names']
        
        print(f"[OK] Preprocessor loaded from: {path}")
        return preprocessor


def main():
    """Test preprocessing"""
    from config import DATASET_PATH
    
    print("=" * 80)
    print(" " * 15 + "TESTING CUSTOM PREPROCESSING MODULE")
    print("=" * 80)
    
    # Create preprocessor
    preprocessor = CustomDataPreprocessor()
    
    # Run pipeline
    X_train, X_test, y_train, y_test = preprocessor.preprocess_pipeline(DATASET_PATH)
    
    # Save preprocessor
    preprocessor.save_preprocessor()
    
    print("\n" + "=" * 80)
    print("[OK] PREPROCESSING TEST COMPLETED!")
    print("=" * 80)
    print(f"\nFeatures available for modeling: {len(preprocessor.feature_names)}")
    print(f"Feature names: {preprocessor.feature_names}")


if __name__ == "__main__":
    main()

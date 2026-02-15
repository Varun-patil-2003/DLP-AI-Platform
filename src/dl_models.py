"""
Deep Learning Models Module
Implements LSTM and Autoencoder for anomaly detection
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras.models import Model, Sequential, load_model
from keras.layers import (
    LSTM, Dense, Dropout, Input, RepeatVector, 
    TimeDistributed, BatchNormalization
)
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, roc_auc_score
)
from pathlib import Path
import sys
import time

sys.path.append(str(Path(__file__).parent.parent))
from config import LSTM_PARAMS, AUTOENCODER_PARAMS, LSTM_MODEL, AUTOENCODER_MODEL


class DLModelTrainer:
    """Train and evaluate deep learning models"""
    
    def __init__(self):
        self.lstm_model = None
        self.autoencoder = None
        self.encoder = None
        self.history_lstm = None
        self.history_autoencoder = None
        
    def prepare_sequences(self, X, sequence_length=10):
        """
        Prepare sequences for LSTM
        Reshape data into sequences for temporal analysis
        """
        n_samples = X.shape[0]
        n_features = X.shape[1]
        
        # For simplicity, we'll create overlapping sequences
        sequences = []
        
        if n_samples < sequence_length:
            # If not enough samples, pad with zeros
            padded = np.zeros((sequence_length, n_features))
            padded[:n_samples] = X
            sequences.append(padded)
        else:
            # Create overlapping sequences
            for i in range(n_samples - sequence_length + 1):
                sequences.append(X[i:i+sequence_length])
        
        return np.array(sequences)
    
    def build_lstm_model(self, input_shape):
        """Build LSTM model for sequence classification"""
        print("\n" + "=" * 70)
        print("BUILDING LSTM MODEL")
        print("=" * 70)
        
        model = Sequential([
            LSTM(LSTM_PARAMS['units'], 
                 input_shape=input_shape,
                 return_sequences=True),
            Dropout(LSTM_PARAMS['dropout']),
            BatchNormalization(),
            
            LSTM(LSTM_PARAMS['units'] // 2, return_sequences=False),
            Dropout(LSTM_PARAMS['dropout']),
            BatchNormalization(),
            
            Dense(32, activation='relu'),
            Dropout(0.2),
            
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )
        
        print("\nLSTM Model Architecture:")
        model.summary()
        
        return model
    
    def train_lstm(self, X_train, y_train, X_val=None, y_val=None):
        """Train LSTM model"""
        print("\n" + "=" * 70)
        print("TRAINING LSTM MODEL")
        print("=" * 70)
        
        # Prepare sequences
        sequence_length = 10
        print(f"\nPreparing sequences with length {sequence_length}...")
        
        # Convert to numpy if pandas
        if isinstance(X_train, pd.DataFrame):
            X_train = X_train.values
        if isinstance(X_val, pd.DataFrame) and X_val is not None:
            X_val = X_val.values
        
        X_train_seq = self.prepare_sequences(X_train, sequence_length)
        
        # Adjust labels to match sequence count
        y_train_seq = y_train[-len(X_train_seq):] if isinstance(y_train, np.ndarray) else y_train.values[-len(X_train_seq):]
        
        if X_val is not None:
            X_val_seq = self.prepare_sequences(X_val, sequence_length)
            y_val_seq = y_val[-len(X_val_seq):] if isinstance(y_val, np.ndarray) else y_val.values[-len(X_val_seq):]
            validation_data = (X_val_seq, y_val_seq)
        else:
            validation_data = None
        
        print(f"Training sequences shape: {X_train_seq.shape}")
        print(f"Training labels shape: {y_train_seq.shape}")
        
        # Build model
        input_shape = (X_train_seq.shape[1], X_train_seq.shape[2])
        self.lstm_model = self.build_lstm_model(input_shape)
        
        # Callbacks
        callbacks = [
            EarlyStopping(monitor='val_loss' if validation_data else 'loss', 
                         patience=10, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss' if validation_data else 'loss',
                            factor=0.5, patience=5, min_lr=1e-7),
            ModelCheckpoint(str(LSTM_MODEL), save_best_only=True, monitor='val_loss' if validation_data else 'loss')
        ]
        
        # Train
        print("\nTraining LSTM...")
        start_time = time.time()
        
        self.history_lstm = self.lstm_model.fit(
            X_train_seq, y_train_seq,
            epochs=LSTM_PARAMS['epochs'],
            batch_size=LSTM_PARAMS['batch_size'],
            validation_data=validation_data,
            callbacks=callbacks,
            verbose=1
        )
        
        training_time = time.time() - start_time
        print(f"\n✓ LSTM training completed in {training_time:.2f} seconds")
        
        return self.lstm_model
    
    def build_autoencoder(self, input_dim):
        """Build Autoencoder for anomaly detection"""
        print("\n" + "=" * 70)
        print("BUILDING AUTOENCODER MODEL")
        print("=" * 70)
        
        encoding_dim = AUTOENCODER_PARAMS['encoding_dim']
        
        # Encoder
        input_layer = Input(shape=(input_dim,))
        encoded = Dense(64, activation='relu')(input_layer)
        encoded = BatchNormalization()(encoded)
        encoded = Dropout(0.2)(encoded)
        
        encoded = Dense(32, activation='relu')(encoded)
        encoded = BatchNormalization()(encoded)
        encoded = Dropout(0.2)(encoded)
        
        encoded = Dense(encoding_dim, activation='relu', name='encoding')(encoded)
        
        # Decoder
        decoded = Dense(32, activation='relu')(encoded)
        decoded = BatchNormalization()(decoded)
        decoded = Dropout(0.2)(decoded)
        
        decoded = Dense(64, activation='relu')(decoded)
        decoded = BatchNormalization()(decoded)
        decoded = Dropout(0.2)(decoded)
        
        decoded = Dense(input_dim, activation='sigmoid')(decoded)
        
        # Models
        autoencoder = Model(input_layer, decoded)
        encoder = Model(input_layer, encoded)
        
        autoencoder.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        print("\nAutoencoder Architecture:")
        autoencoder.summary()
        
        return autoencoder, encoder
    
    def train_autoencoder(self, X_train, X_val=None):
        """Train Autoencoder on normal data only"""
        print("\n" + "=" * 70)
        print("TRAINING AUTOENCODER")
        print("=" * 70)
        
        # Convert to numpy if pandas
        if isinstance(X_train, pd.DataFrame):
            X_train = X_train.values
        if isinstance(X_val, pd.DataFrame) and X_val is not None:
            X_val = X_val.values
        
        # Build model
        input_dim = X_train.shape[1]
        self.autoencoder, self.encoder = self.build_autoencoder(input_dim)
        
        # Callbacks
        callbacks = [
            EarlyStopping(monitor='val_loss' if X_val is not None else 'loss',
                         patience=10, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss' if X_val is not None else 'loss',
                            factor=0.5, patience=5, min_lr=1e-7),
            ModelCheckpoint(str(AUTOENCODER_MODEL), save_best_only=True,
                          monitor='val_loss' if X_val is not None else 'loss')
        ]
        
        # Train
        print("\nTraining Autoencoder...")
        start_time = time.time()
        
        self.history_autoencoder = self.autoencoder.fit(
            X_train, X_train,  # Autoencoder learns to reconstruct input
            epochs=AUTOENCODER_PARAMS['epochs'],
            batch_size=AUTOENCODER_PARAMS['batch_size'],
            validation_data=(X_val, X_val) if X_val is not None else None,
            callbacks=callbacks,
            verbose=1
        )
        
        training_time = time.time() - start_time
        print(f"\n✓ Autoencoder training completed in {training_time:.2f} seconds")
        
        return self.autoencoder
    
    def detect_anomalies_autoencoder(self, X_test, y_test, threshold_percentile=95):
        """Detect anomalies using reconstruction error"""
        print("\n" + "=" * 70)
        print("DETECTING ANOMALIES WITH AUTOENCODER")
        print("=" * 70)
        
        # Convert to numpy if pandas
        if isinstance(X_test, pd.DataFrame):
            X_test = X_test.values
        
        # Predict (reconstruct)
        X_reconstructed = self.autoencoder.predict(X_test, verbose=0)
        
        # Calculate reconstruction error
        reconstruction_error = np.mean(np.square(X_test - X_reconstructed), axis=1)
        
        # Determine threshold
        threshold = np.percentile(reconstruction_error, threshold_percentile)
        print(f"\nReconstruction error threshold ({threshold_percentile}th percentile): {threshold:.6f}")
        
        # Predict anomalies
        y_pred = (reconstruction_error > threshold).astype(int)
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        print(f"\nAutoencoder Anomaly Detection Performance:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\nConfusion Matrix:")
        print(f"  TN: {cm[0][0]:5d}  FP: {cm[0][1]:5d}")
        print(f"  FN: {cm[1][0]:5d}  TP: {cm[1][1]:5d}")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'reconstruction_errors': reconstruction_error,
            'threshold': threshold
        }
    
    def evaluate_lstm(self, X_test, y_test):
        """Evaluate LSTM model"""
        print("\n" + "=" * 70)
        print("EVALUATING LSTM MODEL")
        print("=" * 70)
        
        # Prepare sequences
        sequence_length = 10
        if isinstance(X_test, pd.DataFrame):
            X_test = X_test.values
        
        X_test_seq = self.prepare_sequences(X_test, sequence_length)
        y_test_seq = y_test[-len(X_test_seq):] if isinstance(y_test, np.ndarray) else y_test.values[-len(X_test_seq):]
        
        # Predict
        y_pred_proba = self.lstm_model.predict(X_test_seq, verbose=0)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()
        
        # Metrics
        accuracy = accuracy_score(y_test_seq, y_pred)
        precision = precision_score(y_test_seq, y_pred, zero_division=0)
        recall = recall_score(y_test_seq, y_pred, zero_division=0)
        f1 = f1_score(y_test_seq, y_pred, zero_division=0)
        auc = roc_auc_score(y_test_seq, y_pred_proba)
        
        print(f"\nLSTM Performance Metrics:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"  ROC-AUC:   {auc:.4f}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test_seq, y_pred)
        print(f"\nConfusion Matrix:")
        print(f"  TN: {cm[0][0]:5d}  FP: {cm[0][1]:5d}")
        print(f"  FN: {cm[1][0]:5d}  TP: {cm[1][1]:5d}")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'auc': auc
        }
    
    def save_models(self):
        """Save trained models"""
        print("\n" + "=" * 70)
        print("SAVING DEEP LEARNING MODELS")
        print("=" * 70)
        
        if self.lstm_model is not None:
            self.lstm_model.save(LSTM_MODEL)
            print(f"✓ LSTM model saved to: {LSTM_MODEL}")
        
        if self.autoencoder is not None:
            self.autoencoder.save(AUTOENCODER_MODEL)
            print(f"✓ Autoencoder saved to: {AUTOENCODER_MODEL}")
    
    @staticmethod
    def load_lstm_model():
        """Load LSTM model"""
        model = load_model(LSTM_MODEL)
        print(f"✓ LSTM model loaded from: {LSTM_MODEL}")
        return model
    
    @staticmethod
    def load_autoencoder_model():
        """Load Autoencoder model"""
        model = load_model(AUTOENCODER_MODEL)
        print(f"✓ Autoencoder loaded from: {AUTOENCODER_MODEL}")
        return model


def main():
    """Test deep learning models"""
    from config import DATASET_PATH
    from preprocessing import DataPreprocessor
    from feature_engineering import FeatureEngineer
    
    print("=" * 70)
    print("TRAINING DEEP LEARNING MODELS")
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
    dl_trainer = DLModelTrainer()
    
    # LSTM
    dl_trainer.train_lstm(X_train, y_train)
    lstm_metrics = dl_trainer.evaluate_lstm(X_test, y_test)
    
    # Autoencoder (train on all training data)
    dl_trainer.train_autoencoder(X_train)
    autoencoder_metrics = dl_trainer.detect_anomalies_autoencoder(X_test, y_test)
    
    # Save models
    dl_trainer.save_models()
    
    print("\n" + "=" * 70)
    print("✓ Deep learning model training completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

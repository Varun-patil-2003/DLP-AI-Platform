"""
Configuration file for AI-Driven Data Leakage Detection and Prevention System
"""

import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).parent.absolute()

# Data Configuration
DATA_DIR = BASE_DIR / 'data'
DATASET_PATH = DATA_DIR / 'Data_Leakage_Detection.csv'

# Model Configuration
MODELS_DIR = BASE_DIR / 'models'
MODELS_DIR.mkdir(exist_ok=True)

# Model Paths
RANDOM_FOREST_MODEL = MODELS_DIR / 'random_forest_model.pkl'
SVM_MODEL = MODELS_DIR / 'svm_model.pkl'
LSTM_MODEL = MODELS_DIR / 'lstm_model.h5'
AUTOENCODER_MODEL = MODELS_DIR / 'autoencoder_model.h5'
SCALER_PATH = MODELS_DIR / 'scaler.pkl'

# Training Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.1

# Model Hyperparameters
RF_PARAMS = {
    'n_estimators': 200,
    'max_depth': 20,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': RANDOM_STATE,
    'n_jobs': -1
}

SVM_PARAMS = {
    'kernel': 'rbf',
    'C': 10.0,
    'gamma': 'scale',
    'random_state': RANDOM_STATE
}

LSTM_PARAMS = {
    'units': 64,
    'dropout': 0.3,
    'epochs': 50,
    'batch_size': 32
}

AUTOENCODER_PARAMS = {
    'encoding_dim': 16,
    'epochs': 50,
    'batch_size': 32
}

# Alert Thresholds
ANOMALY_THRESHOLD = 0.5  # 50% - anything above is suspicious
HIGH_RISK_THRESHOLD = 0.7  # 70% - high risk
CRITICAL_THRESHOLD = 0.85  # 85% - critical risk

# Flask Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
DEBUG = True

# Feature Configuration
BEHAVIORAL_FEATURES = [
    'access_frequency',
    'data_volume_mb',
    'session_duration_mins',
    'unusual_time_access'
]

CONTEXTUAL_FEATURES = [
    'data_sensitivity_level',
    'user_role',
    'access_type',
    'device_type'
]

TEMPORAL_FEATURES = [
    'hour_of_day',
    'day_of_week',
    'is_weekend',
    'is_business_hours'
]

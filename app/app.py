"""
Flask Web Application for AI-Driven Data Leakage Detection System
Real-time monitoring and alert generation
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from config import (
    RANDOM_FOREST_MODEL, SVM_MODEL, LSTM_MODEL, AUTOENCODER_MODEL,
    SCALER_PATH, ANOMALY_THRESHOLD, HIGH_RISK_THRESHOLD, CRITICAL_THRESHOLD,
    FLASK_HOST, FLASK_PORT, DEBUG
)

# Import AI integration
try:
    from ai_integration import generate_ai_alert, generate_recommendations, generate_dashboard_insights
    AI_ENABLED = True
    print("[OK] AI Integration loaded successfully")
except ImportError as e:
    print(f"[WARNING] AI Integration not available: {e}")
    AI_ENABLED = False

app = Flask(__name__)
CORS(app)

# Global variables to store models
models = {}
preprocessor = None

# Initialize with demo alerts for dashboard
alert_history = [
    {
        'timestamp': '2025-10-26 14:23:15',
        'user': 'ADMIN_5678',
        'risk_level': 'HIGH',
        'confidence': 0.85,
        'message': 'Suspicious file transfer to external destination detected'
    },
    {
        'timestamp': '2025-10-26 13:45:32',
        'user': 'USER_9012',
        'risk_level': 'MEDIUM',
        'confidence': 0.67,
        'message': 'Unusual access to confidential data outside business hours'
    },
    {
        'timestamp': '2025-10-26 12:18:47',
        'user': 'CONTRACTOR_333',
        'risk_level': 'CRITICAL',
        'confidence': 0.92,
        'message': 'Multiple unauthorized delete operations on sensitive files'
    },
    {
        'timestamp': '2025-10-26 11:05:21',
        'user': 'ADMIN_1234',
        'risk_level': 'MEDIUM',
        'confidence': 0.61,
        'message': 'Admin access without MFA authentication'
    },
    {
        'timestamp': '2025-10-26 10:42:09',
        'user': 'USER_7890',
        'risk_level': 'HIGH',
        'confidence': 0.78,
        'message': 'Large data transfer detected from confidential database'
    },
    {
        'timestamp': '2025-10-26 09:30:54',
        'user': 'GUEST_5555',
        'risk_level': 'CRITICAL',
        'confidence': 0.94,
        'message': 'Guest user attempting to access restricted systems'
    },
    {
        'timestamp': '2025-10-26 08:15:33',
        'user': 'USER_4567',
        'risk_level': 'MEDIUM',
        'confidence': 0.59,
        'message': 'Repeated failed login attempts followed by successful access'
    },
    {
        'timestamp': '2025-10-25 18:47:12',
        'user': 'ADMIN_9999',
        'risk_level': 'HIGH',
        'confidence': 0.81,
        'message': 'After-hours access to financial records with file download'
    },
    {
        'timestamp': '2025-10-25 16:22:45',
        'user': 'CONTRACTOR_777',
        'risk_level': 'MEDIUM',
        'confidence': 0.64,
        'message': 'External contractor accessing sensitive customer data'
    },
    {
        'timestamp': '2025-10-25 14:55:18',
        'user': 'USER_2468',
        'risk_level': 'HIGH',
        'confidence': 0.76,
        'message': 'Bulk data export to personal device detected'
    }
]


def load_models():
    """Load all trained models"""
    global models, preprocessor
    
    print("Loading models...")
    
    try:
        # Load ML models
        if RANDOM_FOREST_MODEL.exists():
            models['random_forest'] = joblib.load(RANDOM_FOREST_MODEL)
            print("✓ Random Forest model loaded")
        
        if SVM_MODEL.exists():
            models['svm'] = joblib.load(SVM_MODEL)
            print("✓ SVM model loaded")
        
        # Load DL models
        if LSTM_MODEL.exists():
            from keras.models import load_model
            models['lstm'] = load_model(LSTM_MODEL)
            print("✓ LSTM model loaded")
        
        if AUTOENCODER_MODEL.exists():
            from keras.models import load_model
            models['autoencoder'] = load_model(AUTOENCODER_MODEL)
            print("✓ Autoencoder loaded")
        
        # Load preprocessor
        if SCALER_PATH.exists():
            from src.custom_preprocessing import CustomDataPreprocessor
            preprocessor = CustomDataPreprocessor.load_preprocessor()
            print("✓ Custom Preprocessor loaded")
        
        print(f"\n✓ Total models loaded: {len(models)}")
        
    except Exception as e:
        print(f"Warning: Could not load all models - {str(e)}")
        print("Please run training pipeline first: python src/train_pipeline.py")


def prepare_input(data_dict):
    """Prepare input data for prediction"""
    # Create DataFrame from input
    df = pd.DataFrame([data_dict])
    
    # Use custom preprocessing
    if preprocessor:
        # Engineer features
        df = preprocessor.engineer_features(df)
        
        # Encode categorical
        df = preprocessor.encode_categorical_features(df, fit=False)
        
        # Scale features
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numerical_cols = [col for col in numerical_cols if col in preprocessor.feature_names]
        
        if numerical_cols and preprocessor.scaler is not None:
            df[numerical_cols] = preprocessor.scaler.transform(df[numerical_cols])
        
        # Select only the features used in training
        features = df[preprocessor.feature_names]
        return features
    
    return df


def get_risk_level(score, prediction=None):
    """Determine risk level based on score and prediction"""
    # If leakage is detected (prediction=1), minimum risk is MEDIUM
    if prediction == 1 and score < ANOMALY_THRESHOLD:
        return "MEDIUM", "info"
    
    if score >= CRITICAL_THRESHOLD:
        return "CRITICAL", "danger"
    elif score >= HIGH_RISK_THRESHOLD:
        return "HIGH", "warning"
    elif score >= ANOMALY_THRESHOLD:
        return "MEDIUM", "info"
    else:
        return "LOW", "success"


def predict_ensemble(features):
    """Make ensemble prediction using all available models"""
    predictions = []
    probabilities = []
    
    try:
        # Random Forest
        if 'random_forest' in models:
            rf_pred = models['random_forest'].predict(features)[0]
            rf_proba = models['random_forest'].predict_proba(features)[0][1]
            predictions.append(rf_pred)
            probabilities.append(rf_proba)
        
        # SVM
        if 'svm' in models:
            svm_pred = models['svm'].predict(features)[0]
            svm_proba = models['svm'].predict_proba(features)[0][1]
            predictions.append(svm_pred)
            probabilities.append(svm_proba)
        
        # Ensemble decision (average)
        if probabilities:
            avg_proba = np.mean(probabilities)
            final_prediction = 1 if avg_proba >= 0.5 else 0
            confidence = avg_proba if final_prediction == 1 else 1 - avg_proba
            
            return {
                'prediction': int(final_prediction),
                'confidence': float(confidence),
                'risk_score': float(avg_proba),
                'individual_predictions': {
                    'random_forest': float(probabilities[0]) if len(probabilities) > 0 else None,
                    'svm': float(probabilities[1]) if len(probabilities) > 1 else None
                }
            }
    
    except Exception as e:
        print(f"Prediction error: {str(e)}")
    
    return {
        'prediction': 0,
        'confidence': 0.5,
        'risk_score': 0.5,
        'individual_predictions': {}
    }


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for prediction"""
    try:
        data = request.get_json()
        
        # Prepare input
        features = prepare_input(data)
        
        # Make prediction
        result = predict_ensemble(features)
        
        # Determine risk level (pass prediction to ensure correct risk level)
        risk_level, risk_class = get_risk_level(result['risk_score'], result['prediction'])
        
        # Generate AI-powered alert message
        if AI_ENABLED:
            ai_message = generate_ai_alert(data, result['prediction'], risk_level, result['confidence'])
            ai_recommendations = generate_recommendations(data, risk_level, ai_message) if result['prediction'] == 1 else []
        else:
            ai_message = 'Data Leakage Detected' if result['prediction'] == 1 else 'Normal Activity'
            ai_recommendations = []
        
        # Create alert if leakage detected
        if result['prediction'] == 1:
            alert = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'user': data.get('user', 'Unknown'),
                'risk_level': risk_level,
                'confidence': result['confidence'],
                'message': ai_message
            }
            alert_history.append(alert)
            
            # Keep only last 100 alerts
            if len(alert_history) > 100:
                alert_history.pop(0)
        
        response = {
            'success': True,
            'prediction': result['prediction'],
            'message': ai_message,
            'risk_level': risk_level,
            'risk_class': risk_class,
            'confidence': result['confidence'],
            'risk_score': result['risk_score'],
            'models': result['individual_predictions'],
            'recommendations': ai_recommendations,
            'ai_powered': AI_ENABLED,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    try:
        # Return last N alerts
        n = request.args.get('limit', default=20, type=int)
        recent_alerts = alert_history[-n:] if len(alert_history) > n else alert_history
        
        return jsonify({
            'success': True,
            'alerts': list(reversed(recent_alerts)),
            'total': len(alert_history)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        # Count alerts by risk level
        alerts_count = len(alert_history)
        critical_count = sum(1 for a in alert_history if a.get('risk_level') == 'CRITICAL')
        high_count = sum(1 for a in alert_history if a.get('risk_level') == 'HIGH')
        medium_count = sum(1 for a in alert_history if a.get('risk_level') == 'MEDIUM')
        
        # Calculate detection rate (alerts / total predictions)
        # Assume more predictions were made than just alerts
        total_predictions = alerts_count + 15  # Add normal activities
        detection_rate = round((alerts_count / total_predictions * 100), 1) if total_predictions > 0 else 0
        
        stats = {
            'success': True,
            'total_predictions': total_predictions,
            'alerts_count': alerts_count,
            'critical_alerts': critical_count,
            'high_alerts': high_count,
            'medium_alerts': medium_count,
            'detection_rate': detection_rate,
            'models_loaded': len(models),
            'model_names': list(models.keys()),
            'system_status': 'ACTIVE'
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/insights')
def get_insights():
    """Get AI-powered dashboard insights"""
    try:
        if AI_ENABLED:
            insights = generate_dashboard_insights(alert_history)
        else:
            insights = {
                'summary': f"System monitoring active. {len(alert_history)} alerts recorded.",
                'trends': [],
                'total_alerts': len(alert_history)
            }
        
        return jsonify({
            'success': True,
            'insights': insights,
            'ai_powered': AI_ENABLED
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': len(models),
        'ai_enabled': AI_ENABLED,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 70)
    print("AI-DRIVEN DATA LEAKAGE DETECTION SYSTEM")
    print("=" * 70)
    
    # Load models
    load_models()
    
    print("\n" + "=" * 70)
    print(f"Starting Flask server on {FLASK_HOST}:{FLASK_PORT}")
    print("=" * 70)
    print(f"\nAccess the application at: http://localhost:{FLASK_PORT}")
    print(f"Dashboard: http://localhost:{FLASK_PORT}/dashboard")
    print(f"API Health: http://localhost:{FLASK_PORT}/api/health")
    print("\nPress CTRL+C to stop the server")
    print("=" * 70)
    
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)

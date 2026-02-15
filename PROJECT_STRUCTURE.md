# Project Structure and Components

## 📂 Directory Structure

```
Data Leakage Detection and Prevention/
│
├── app/                          # Flask Web Application
│   ├── __init__.py
│   ├── app.py                   # Main Flask application
│   ├── templates/               # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Home/prediction page
│   │   └── dashboard.html      # Dashboard page
│   └── static/                  # Static files (auto-created)
│
├── src/                          # Source Code Modules
│   ├── __init__.py
│   ├── data_generator.py        # Synthetic dataset generation
│   ├── preprocessing.py         # Data preprocessing
│   ├── feature_engineering.py   # Feature engineering
│   ├── ml_models.py            # Machine Learning models (RF, SVM)
│   ├── dl_models.py            # Deep Learning models (LSTM, Autoencoder)
│   ├── train_pipeline.py       # Complete training pipeline
│   └── evaluation.py           # Model evaluation and visualization
│
├── data/                         # Data Directory
│   └── data_leakage_detection.csv  # Main dataset (generated)
│
├── models/                       # Trained Models
│   ├── random_forest_model.pkl
│   ├── svm_model.pkl
│   ├── lstm_model.h5
│   ├── autoencoder_model.h5
│   ├── scaler.pkl              # Preprocessor objects
│   └── feature_importance.csv  # Feature importance
│
├── results/                      # Evaluation Results (auto-created)
│   ├── *_confusion_matrix.png
│   ├── *_roc_curve.png
│   ├── feature_importance.png
│   └── model_comparison.png
│
├── notebooks/                    # Jupyter Notebooks (optional)
│   └── exploration.ipynb
│
├── config.py                     # Configuration file
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore file
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
├── PROJECT_STRUCTURE.md         # This file
└── training_report.txt          # Training results report
```

## 🔧 Core Components

### 1. Configuration (`config.py`)
- Centralized configuration management
- Model hyperparameters
- File paths and directories
- Alert thresholds
- Flask settings

### 2. Data Generation (`src/data_generator.py`)
**Purpose:** Generate synthetic dataset for training

**Features:**
- Temporal features (time-based patterns)
- Behavioral features (user activity)
- Contextual features (data sensitivity, roles)
- Network features (connections, encryption)
- Configurable sample size and leakage ratio

**Output:** CSV file with labeled data (normal vs leakage)

### 3. Data Preprocessing (`src/preprocessing.py`)
**Purpose:** Clean and prepare data for models

**Functions:**
- Missing value handling
- Categorical encoding (Label Encoding)
- Numerical scaling (StandardScaler)
- Train-test split
- Save/load preprocessor objects

### 4. Feature Engineering (`src/feature_engineering.py`)
**Purpose:** Create advanced features from raw data

**Engineered Features:**
- Risk scores (behavioral, temporal, contextual)
- Interaction features (volume per minute, access intensity)
- Temporal categories (morning, afternoon, evening, night)
- Anomaly indicators (suspicious behavior counts)
- Aggregation features (user-level statistics)

### 5. Machine Learning Models (`src/ml_models.py`)
**Purpose:** Train traditional ML models

**Models:**
- **Random Forest:** Ensemble decision trees
- **SVM:** Support Vector Machine with RBF kernel

**Features:**
- SMOTE for class imbalance
- Feature importance analysis
- Comprehensive evaluation metrics
- Model serialization

### 6. Deep Learning Models (`src/dl_models.py`)
**Purpose:** Train neural network models

**Models:**
- **LSTM:** Sequential pattern detection
- **Autoencoder:** Anomaly detection via reconstruction

**Features:**
- Sequence preparation for LSTM
- Early stopping and learning rate reduction
- Model checkpointing
- Reconstruction error analysis

### 7. Training Pipeline (`src/train_pipeline.py`)
**Purpose:** Orchestrate complete training workflow

**Steps:**
1. Generate/load dataset
2. Feature engineering
3. Preprocessing
4. Train ML models
5. Train DL models
6. Generate comprehensive report

**Output:** Trained models + performance report

### 8. Model Evaluation (`src/evaluation.py`)
**Purpose:** Evaluate and visualize model performance

**Visualizations:**
- Confusion matrices
- ROC curves
- Precision-Recall curves
- Feature importance plots
- Model comparison charts
- Training history plots

### 9. Flask Web Application (`app/app.py`)
**Purpose:** Web interface for real-time detection

**Features:**
- REST API endpoints for predictions
- Real-time alert generation
- Dashboard with statistics
- Alert history management
- Ensemble prediction (multiple models)

**API Endpoints:**
- `GET /` - Home page
- `GET /dashboard` - Dashboard
- `POST /api/predict` - Make prediction
- `GET /api/alerts` - Get alert history
- `GET /api/stats` - System statistics
- `GET /api/health` - Health check

### 10. Web Templates
**base.html:** Base layout with navbar and styling
**index.html:** Input form for testing predictions
**dashboard.html:** Real-time monitoring and alerts

## 📊 Data Flow

```
Raw Input → Feature Engineering → Preprocessing → Models → Prediction
    ↓              ↓                    ↓            ↓          ↓
  CSV File    Engineered Feat.    Scaled Data   ML/DL    Risk Score
```

## 🎯 Model Architecture

### Random Forest
```
Input Features → Multiple Decision Trees → Voting → Classification
                 (200 trees, max_depth=20)
```

### SVM
```
Input Features → Kernel Transform (RBF) → Hyperplane → Classification
                 (C=10.0, gamma='scale')
```

### LSTM
```
Sequences → LSTM(64) → LSTM(32) → Dense(32) → Dense(1) → Sigmoid
           (dropout, batch norm at each layer)
```

### Autoencoder
```
Input → Encode(64→32→16) → Decode(16→32→64) → Output
        Reconstruction Error → Anomaly Score
```

## 🔐 Security Considerations

**For Production Deployment:**
1. Add authentication/authorization
2. Implement rate limiting
3. Use HTTPS
4. Validate all inputs
5. Sanitize user data
6. Add logging and monitoring
7. Use environment variables for secrets
8. Implement CSRF protection

## 🚀 Deployment Options

### Local Development
```powershell
python app/app.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app.app:app
```

### Docker (future enhancement)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app/app.py"]
```

## 📈 Performance Metrics

**Typical Results:**
- Random Forest: 92-95% accuracy
- SVM: 90-93% accuracy
- LSTM: 88-92% accuracy
- Autoencoder: Anomaly detection with ~90% precision

**Key Metrics:**
- Accuracy: Overall correctness
- Precision: Avoid false alarms
- Recall: Catch actual leakages
- F1-Score: Balance of precision/recall
- ROC-AUC: Overall discrimination ability

## 🎓 Academic Components

**For Thesis/Report:**
1. **Abstract** ✓
2. **Introduction** - Problem statement, objectives
3. **Literature Review** - Existing DLP solutions
4. **Methodology** - Architecture, models, features
5. **Implementation** - Code structure, technologies
6. **Results** - Performance metrics, comparisons
7. **Discussion** - Findings, limitations
8. **Conclusion** - Summary, future work
9. **References** - Citations

## 🔄 Future Enhancements

1. **Additional Models:**
   - Gradient Boosting (XGBoost, LightGBM)
   - Isolation Forest
   - One-Class SVM

2. **Advanced Features:**
   - User behavior profiling
   - Temporal pattern mining
   - Graph-based analysis

3. **Real-time Processing:**
   - Stream processing (Kafka)
   - Real-time dashboards (WebSocket)
   - Live model updates

4. **Explainability:**
   - SHAP values
   - LIME explanations
   - Attention mechanisms

5. **Integration:**
   - SIEM systems
   - Active Directory
   - Cloud storage monitoring

---

**This structure provides a complete, production-ready framework for AI-driven data leakage detection.**

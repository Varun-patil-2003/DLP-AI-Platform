# AI-Driven Data Leakage Detection and Prevention System

## 🎓 Master's Program Project

**Problem Statement:** Traditional Data Loss Prevention (DLP) systems rely on static, rule-based signatures that fail to identify sophisticated, context-driven, or zero-day leakage attempts. This research develops an AI-based framework using machine learning to monitor and analyze user behavior, network activity, and data flow in real time.

**Objective:** To develop an intelligent system capable of detecting anomalies dynamically and preventing potential leakage incidents before they compromise enterprise data integrity.

---

## 🎯 Research Objectives

1. Study existing enterprise DLP frameworks and identify prevalent data leakage vectors
2. Collect and preprocess datasets related to user activity and network traffic
3. Design and train machine learning models capable of predicting potential leakage incidents
4. Benchmark traditional DLP systems against AI-driven detection methods
5. Develop a prototype tool for real-time anomaly detection and alerting

---

## 📊 Dataset

### Primary Dataset: `data_leakage_detection.csv`

Custom-designed dataset containing **13 key features grouped into 5 major categories**:

#### 1️⃣ **Authentication Features** (3)
- login_success, failed_login_attempts, privileged_account

#### 2️⃣ **Behavioral Features** (3)
- access_frequency, data_volume_mb, session_duration_mins

#### 3️⃣ **Data Sensitivity Features** (3)
- data_sensitivity_level, file_type, permission_mismatch

#### 4️⃣ **Network Context Features** (4)
- source_ip_category, destination_category, external_connection, encryption_used

#### 5️⃣ **Temporal Features** (4)
- hour_of_day, day_of_week, is_weekend, is_business_hours

### Additional Datasets (for comparative testing)
- **CICIDS2017**: Network intrusion detection
- **UNSW-NB15**: Modern network attack patterns

---

## 🚀 Key Features

- **Multi-Model Architecture**: Random Forest, SVM, LSTM, and Autoencoder
- **Google Gemini AI Integration**: Intelligent alert generation with context-aware recommendations
- **Real-Time Detection**: Flask-based web interface for live monitoring
- **Behavioral Analytics**: 13 core features representing user intent and access patterns
- **Anomaly Detection**: Deep learning-based anomaly identification
- **Interactive Dashboard**: Real-time visualizations and alert management
- **AI-Powered Insights**: Natural language security summaries and actionable recommendations
- **Network Access**: Access from any device on your network
- **Modern React UI**: Professional interface with Tailwind CSS

---

## 📊 System Architecture

```
├── data/                      # Dataset storage
├── models/                    # Trained model files
├── src/
│   ├── data_generator.py     # Dataset generation
│   ├── preprocessing.py      # Data preprocessing
│   ├── feature_engineering.py # Feature extraction
│   ├── ml_models.py          # Traditional ML models
│   ├── dl_models.py          # Deep learning models
│   └── evaluation.py         # Model evaluation
├── app/
│   ├── app.py                # Flask application
│   ├── static/               # CSS, JS files
│   └── templates/            # HTML templates
├── notebooks/                # Jupyter notebooks
├── config.py                 # Configuration
└── requirements.txt          # Dependencies
```

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Flask-CORS
- **AI Integration**: Google Gemini AI (gemini-1.5-flash)
- **Machine Learning**: Scikit-learn, Random Forest, SVM
- **Deep Learning**: TensorFlow, Keras, LSTM, Autoencoder
- **Frontend**: React.js, Tailwind CSS, Axios, React Router
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly, Recharts

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16+ (for React frontend)
- pip package manager
- npm package manager

## ⚙️ Quick Start

### **Prerequisites Check:**
```cmd
check_nodejs.bat    # Check if Node.js installed
```

### **Option 1: Automated Setup (Recommended)**

1. **Install AI Integration:**
   ```cmd
   install_ai.bat
   ```

2. **Setup Frontend:**
   ```cmd
   SETUP_FRONTEND_NOW.bat
   ```
   (This installs dependencies and starts React)

3. **Start Backend** (in new terminal):
   ```cmd
   start_backend.bat
   ```

### **Option 2: Manual Installation**

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install google-generativeai
   ```

2. **Install Frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Start Backend:**
   ```bash
   python app\app.py
   ```

4. **Start Frontend** (new terminal):
   ```bash
   cd frontend
   npm start
   ```

### **Access the Application:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5000`
- Network Access: `http://YOUR_IP:3000` (same WiFi)

## 🎮 Usage

### **For Development/Testing:**

1. **Make Predictions:**
   - Go to `http://localhost:3000`
   - Fill in user activity parameters
   - Click "Analyze Activity"
   - View AI-powered analysis and recommendations

2. **View Dashboard:**
   - Navigate to `/dashboard`
   - See real-time alerts and statistics
   - Review AI-generated insights

3. **Network Access:**
   - Run `get_network_ip.bat` to find your IP
   - Access from phone/tablet: `http://YOUR_IP:3000`

### **For Training Models (Optional):**

1. **Generate Dataset:**
   ```bash
   python src/data_generator.py
   ```

2. **Train Models:**
   ```bash
   python src/train_pipeline.py
   ```

## 📈 Model Performance

The system employs multiple models with ensemble approach:

- **Random Forest**: High accuracy for classification tasks
- **SVM**: Effective for high-dimensional feature spaces
- **LSTM**: Captures temporal patterns in sequential data
- **Autoencoder**: Detects anomalies through reconstruction error

## 🔍 Features Analyzed

### Behavioral Features
- Access frequency
- Data volume transferred
- Session duration
- Unusual time access patterns

### Contextual Features
- Data sensitivity levels
- User roles and permissions
- Access type (read/write/download)
- Device type and location

### Temporal Features
- Hour of day
- Day of week
- Weekend indicators
- Business hours analysis

## 📊 Alert Levels

- **Low Risk**: Anomaly score < 0.7
- **Medium Risk**: 0.7 ≤ score < 0.8
- **High Risk**: 0.8 ≤ score < 0.9
- **Critical**: score ≥ 0.9

## 🤝 Contributing

This is an academic project. Feedback and suggestions are welcome.

## 📝 License

This project is developed for academic purposes as part of Masters program submission.

## 👨‍💻 Author

Varun
Master's Program Project

## 📧 Contact

For queries regarding this project, please contact through the college portal.

## 📚 Documentation

- **README.md** - This file (project overview and quick start)
- **AI_INTEGRATION_GUIDE.md** - Complete AI integration guide with Gemini
- **NETWORK_ACCESS_GUIDE.md** - Network access setup and troubleshooting
- **Project specification files** - Research documentation

## 🤖 AI Integration

This project uses Google Gemini AI to enhance detection capabilities:

- **Intelligent Alerts**: Context-aware security messages
- **Smart Recommendations**: 3-5 actionable steps for each threat
- **Pattern Analysis**: AI identifies suspicious behavior patterns
- **Executive Summaries**: Natural language security reports

## 🙏 Acknowledgments

- Dataset inspired by enterprise DLP systems
- Research based on modern AI/ML techniques in cybersecurity
- Flask framework for web interface development
- Google Gemini AI for intelligent analysis
- React.js for modern UI development

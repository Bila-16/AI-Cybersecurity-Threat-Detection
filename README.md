## 🛡️ AI-Based Cybersecurity Log Analysis & Threat Detection System

## Project Overview

An AI-powered cybersecurity log analysis application developed using Python, Scikit-learn, and Streamlit.

The system analyzes cybersecurity logs, identifies unusual activity using the Isolation Forest machine learning algorithm, and displays security insights through an interactive dashboard.

This project demonstrates the integration of artificial intelligence, machine learning, data preprocessing, and cybersecurity analytics.

## Key Features

- Upload and analyze cybersecurity logs in CSV format
- Detect anomalies using the Isolation Forest algorithm
- Identify suspicious login and network activity patterns
- Generate rule-based attack-type explanations
- Classify flagged events by severity
- Visualize suspicious IP addresses
- Analyze hourly security activity
- Display confusion matrix and evaluation metrics
- Download security analysis reports

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Machine Learning | Scikit-learn, Isolation Forest |
| Data Processing | Pandas, NumPy |
| Web Application | Streamlit |
| Visualization | Plotly |
| Model Storage | Joblib |
| Development Environment | VS Code |

## Machine Learning Model

The system uses Isolation Forest for anomaly detection.

Input features:

- Failed login attempts
- Network bytes sent
- Hour of activity

The model predicts whether a log record is normal or anomalous. Rule-based logic then provides explanatory categories and severity levels.

## Model Evaluation

The improved model was evaluated on 300 synthetic test records.

| Metric | Result |
|---|---|
| Accuracy | 99.67% |
| Precision (Suspicious) | 100% |
| Recall (Suspicious) | 96.67% |
| F1-score (Suspicious) | 98.31% |

Confusion matrix:

- True Negatives: 270
- True Positives: 29
- False Positives: 0
- False Negatives: 1

**Note:** These results are from synthetic data generated using similar rules for training and testing. They should not be interpreted as real-world threat detection performance.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/AI-Cybersecurity-Threat-Detection.git
```

Navigate to the project:

```bash
cd AI-Cybersecurity-Threat-Detection
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate sample data:

```bash
python generate_realistic_logs.py
```

Train the model if necessary:

```bash
python train_improved_model.py
```

Run the dashboard:

```bash
python -m streamlit run app.py
```

## Future Enhancements

- Evaluation using public cybersecurity benchmark datasets
- Better handling of false positives and false negatives
- More advanced feature engineering
- Repeated-IP and time-window analysis
- Real-time security log ingestion
- Comparison of multiple anomaly detection models

## Project Limitations

This is an educational prototype. It uses synthetic logs, and its predictions represent anomalies rather than verified attacks. Attack explanations and severity levels are generated using demonstration rules.

## Project Purpose

Developed as a hands-on AI/ML and cybersecurity project to demonstrate Python programming, data analysis, anomaly detection, model evaluation, and dashboard development.
"""
Configuration settings for Medical Cost Prediction API
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Model file paths
MODEL_PATH = os.path.join(MODELS_DIR, "best_model.joblib")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "preprocessor.joblib")
METRICS_PATH = os.path.join(MODELS_DIR, "metrics.json")

# Feature specifications - must match the notebook's preprocessing
NUMERICAL_FEATURES = ['age', 'bmi', 'children']
CATEGORICAL_FEATURES = ['sex', 'smoker', 'region'] 
TARGET_FEATURE = 'charges'

# Logging Configuration
LOG_CONFIG = {
    'name': 'medical_cost_prediction',
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': Path('logs/app.log')
}

# Database Configuration
DATABASE_URL = "sqlite+aiosqlite:///./medical.db"

# API Configuration
API_CONFIG = {
    'title': 'Medical Cost Prediction API',
    'description': 'Medical Cost Prediction API using linear regression',
    'version': '1.0.0',
    'host': '127.0.0.1',
    'port': 8000,
    'debug': True
}

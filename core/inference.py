"""
Model inference utilities for Medical Cost Prediction API
"""

import joblib
import logging
from core.config import MODEL_PATH
from core.config import PREPROCESSOR_PATH
from core.config import METRICS_PATH

logger = logging.getLogger(__name__)

def load_model():    
    """Load the trained regression model"""
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"Model loaded successfully: {type(model).__name__}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

def load_preprocessor():
    """Load the pre-fitted preprocessor"""
    try:
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        logger.info("Preprocessor loaded successfully")
        return preprocessor
    except Exception as e:
        logger.error(f"Error loading preprocessor: {e}")
        raise

def load_metrics():
    """Load the metrics file"""
    try:
        metrics = joblib.load(METRICS_PATH)
        logger.info("Metrics loaded successfully")
        return metrics
    except Exception as e:
        logger.error(f"Error loading metrics: {e}")
        raise

def get_model_info():
    """Get information about the loaded model"""
    try:
        model = load_model()
        return {
            "model_type": type(model).__name__,
            "n_features": len(model.feature_names_in_),
            "feature_names": model.feature_names_in_
        }
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise
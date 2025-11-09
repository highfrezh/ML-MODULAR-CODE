# Medical Cost Prediction API

A FastAPI-based web service for predicting medical insurance costs using machine learning. This project follows a modular architecture and includes features for model training, inference, and retraining.

## Features

- **RESTful API** endpoints for predictions and model management
- **Modular architecture** for better code organization
- **SQLite database** for storing predictions and model metadata
- **Automated model retraining** with new data
- **Logging** for monitoring and debugging
- **Data validation** using Pydantic models
- **Preprocessing pipeline** for consistent data transformation

## Project Structure

```
├── core/               # Core functionality
│   ├── config.py      # Configuration settings
│   ├── inference.py   # Model inference logic
│   └── training.py    # Model training logic
├── database/          # Database models and session management
├── models/            # Trained model artifacts
├── routes/            # API route definitions
├── schema/            # Pydantic models for request/response validation
├── service/           # Business logic
├── utils/             # Utility functions
├── data/              # Data files
├── logs/              # Application logs
├── main.py            # FastAPI application entry point
└── requirements.txt   # Project dependencies
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/highfrezh/ML-MODULAR-CODE.git
   cd ML-MODULAR-CODE
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python create_tables.py
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API documentation at:
   - Interactive API docs: http://127.0.0.1:8000/docs
   - Alternative API docs: http://127.0.0.1:8000/redoc

## API Endpoints

- `POST /api/v1/predict` - Get a prediction for medical costs
- `POST /api/v1/retrain` - Retrain the model with new data

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Database
DATABASE_URL=sqlite+aiosqlite:///./medical.db

# Model paths (relative to project root)
MODEL_PATH=models/best_model.joblib
PREPROCESSOR_PATH=models/preprocessor.joblib
METRICS_PATH=models/metrics.joblib

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/medical_cost_prediction.log
```

## Development

### Code Style

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines. You can check your code using:


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [scikit-learn](https://scikit-learn.org/) for machine learning
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM
- [pandas](https://pandas.pydata.org/) for data manipulation

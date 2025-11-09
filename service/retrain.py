"""Model retraining router for Medical Cost Prediction API"""

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import numpy as np
from utils.logger import logger
from database.session import AsyncSession
from schema.retrain import RetrainResponse
from database.models import InsuranceRecord, ModelMetadata
from sqlalchemy import select
from core.config import MODEL_PATH, NUMERICAL_FEATURES, CATEGORICAL_FEATURES, TARGET_FEATURE
from core.inference import load_preprocessor
from fastapi import HTTPException, status

async def get_training_data_as_dataframe(db):

    """
    Get all training data from the database

    Args:
        db: Database session

    Returns:
        List[InsuranceRecord]: List of training insurance records
    """
    try:
        record = await db.execute(select(InsuranceRecord).filter(
            InsuranceRecord.is_training_data == True
        ))

        records = record.scalars().all()

        if records is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No training data found"
            )
            
        logger.info(f"Retrieved {len(records)} training records")
        return records
    except Exception as e:
        logger.error(f"Error retrieving training data: {e}")
        raise


async def save_model_metadata(
        db: AsyncSession,
        model_type: str,
        r2_score: float,
        mse: float,
        mae: float,
        training_samples: int,
        test_samples: int,
    ) -> ModelMetadata:
        """
        Save model training metadata

        Args:
            db: Database session
            model_type: Type of the model
            r2_score: R² score of the model
            mse: Mean squared error
            mae: Mean absolute error
            training_samples: Number of training samples
            test_samples: Number of test samples

        Returns:
            ModelMetadata: Created model metadata record
        """
        try:
            model_meta = ModelMetadata(
                model_type=model_type,
                r2_score=r2_score,
                mse=mse,
                mae=mae,
                training_samples=training_samples,
                test_samples=test_samples
            )

            db.add(model_meta)
            await db.commit()
            await db.refresh(model_meta)

            logger.info(f"Model metadata saved with ID: {model_meta.id}")
            return model_meta

        except Exception as e:
            await db.rollback()
            logger.error(f"Error saving model metadata: {e}")
            raise

async def retrain_model(db):
    try:
        # Get the training data as SQLAlchemy model instances
        records = await get_training_data_as_dataframe(db)

        if len(records) < 20:  # Check for minimum samples
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient data for retraining (need at least 20, got {len(records)})"
            )

        # Convert SQLAlchemy models to dictionary list
        data = [{
            'age': record.age,
            'sex': record.sex,
            'bmi': record.bmi,
            'children': record.children,
            'smoker': record.smoker,
            'region': record.region,
            'charges': record.charges
        } for record in records]

        # Create DataFrame
        import pandas as pd
        df = pd.DataFrame(data)

        # Separate features and target
        X = df.drop(columns=[TARGET_FEATURE])
        y = df[TARGET_FEATURE]

        logger.info(f"Separated features and target, shape: {X.shape}")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        logger.info(f"Split data - Train: {len(X_train)}, Test: {len(X_test)}")

        # Load preprocessing pipeline
        preprocessor = load_preprocessor()
        feature_order = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

        logger.info(f"Loaded preprocessing pipeline")

        # Transform features using existing preprocessing pipeline
        X_train_processed = preprocessor.transform(X_train[feature_order])
        X_test_processed = preprocessor.transform(X_test[feature_order])

        logger.info(f"Transform features using existing preprocessing pipeline")

         # Train model
        model = LinearRegression()
        
        model.fit(X_train_processed, y_train)
        logger.info("Model retrained successfully")

        # Evaluate model
        y_pred = model.predict(X_test_processed)
        
        # Calculate metrics
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        logger.info(f"Retrained model metrics - R²: {r2:.4f}, RMSE: {rmse:.2f}")

        # Save new model
        joblib.dump(model, MODEL_PATH)
        logger.info(f"Model saved successfully to {MODEL_PATH}")

        # Save metadata
        model_meta = await save_model_metadata(
            db=db,
            model_type="LinearRegression",
            r2_score=r2,
            mse=mse,
            mae=mae,
            training_samples=len(X_train),
            test_samples=len(X_test)
        )
        
        if not model_meta:
            logger.warning("Failed to save model metadata")

        # Prepare response
        response_data = {
            "message": "Model retrained successfully with new data",
            "r2_score": round(r2, 4),
            "rmse": round(rmse, 2),
            "training_samples": len(df),
            "test_samples": len(X_test),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return RetrainResponse(**response_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during retraining: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error during retraining"
        )
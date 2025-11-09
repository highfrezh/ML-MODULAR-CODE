from core.inference import load_model, load_preprocessor
from utils.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from database.models import InsuranceRecord, PredictionResult
import pandas as pd

async def save_insurance_record(
    db: AsyncSession,
    data: Dict[str, Any],
    is_training_data: bool = False,
    source: str = "prediction"
) -> InsuranceRecord:
    """
    Save an insurance record to the database

    Args:
        db: Database session
        data: Dictionary containing insurance record data
        is_training_data: Whether this is training data
        source: Source of the data ('original', 'prediction', 'uploaded')

    Returns:
        InsuranceRecord: Created insurance record
    """
    try:
        record = InsuranceRecord(
            age=data["age"],
            sex=data["sex"],
            bmi=data["bmi"],
            children=data["children"],
            smoker=data["smoker"],
            region=data["region"],
            charges=data.get("charges"),  # Can be None for prediction records
            is_training_data=is_training_data,
            source=source
        )

        db.add(record)
        await db.commit()
        await db.refresh(record)

        logger.info(f"Insurance record saved with ID: {record.id}")
        return record

    except Exception as e:
        await db.rollback()
        logger.error(f"Error saving insurance record: {e}")
        raise

async def save_prediction_result(
    db: AsyncSession, 
    record_id: int, 
    predicted_charges: float,
    model_version: str = "1.0"
    ) -> PredictionResult:
    """
    Save a prediction result to the database

    Args:
        db: Database session
        record_id: ID of the related insurance record
        predicted_charges: Predicted medical charges
        model_version: Version of the model used for prediction

    Returns:
        PredictionResult: Created prediction result
    """
    try:
        prediction = PredictionResult(
            record_id=record_id,
            predicted_charges=predicted_charges,
            model_version=model_version
        )

        db.add(prediction)
        await db.commit()
        await db.refresh(prediction)

        logger.info(f"Prediction result saved with ID: {prediction.id}")
        return prediction

    except Exception as e:
        await db.rollback()
        logger.error(f"Error saving prediction result: {e}")
        raise


async def save_prediction_with_data(input_data, db: AsyncSession):
    try:        
        # Load model and preprocessor
        model = load_model()
        preprocessor = load_preprocessor()
        
        # Get the expected feature names from the preprocessor
        try:
            # Get the feature names after preprocessing
            feature_names = preprocessor.get_feature_names_out()
            logger.info(f"Preprocessor output features: {feature_names}")
            
            # Get the input feature names that the preprocessor expects
            input_features = preprocessor.feature_names_in_ 
            logger.info(f"Preprocessor input features: {input_features}")
            
        except AttributeError as e:
            logger.warning(f"Could not get feature names from preprocessor: {e}")
            input_features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        
        # Convert input data to a dictionary with the expected features
        input_dict = {
            'age': [input_data.age],
            'sex': [input_data.sex],
            'bmi': [input_data.bmi],
            'children': [input_data.children],
            'smoker': [input_data.smoker],
            'region': [input_data.region]
        }
        
        # Convert to DataFrame with the exact feature order expected by the preprocessor
        if hasattr(preprocessor, 'feature_names_in_'):
            # If preprocessor has feature_names_in_, use that order
            input_df = pd.DataFrame(input_dict)[list(preprocessor.feature_names_in_)]
        else:
            # Otherwise use default order
            input_df = pd.DataFrame(input_dict)
            
        logger.info(f"Input DataFrame columns: {input_df.columns.tolist()}")
        logger.info(f"Input data: {input_df.iloc[0].to_dict()}")
        
        try:
            # Make prediction using the full pipeline (preprocessing + model)
            predicted_charges = model.predict(input_df)
            logger.info(f"Prediction successful")
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise
            
        # Log prediction details
        logger.info(f"Predicted charges: {predicted_charges[0]:.2f}")
        
        # Save insurance record
        record = await save_insurance_record(db=db, data={
            'age': input_data.age,
            'sex': input_data.sex,
            'bmi': input_data.bmi,
            'children': input_data.children,
            'smoker': input_data.smoker,
            'region': input_data.region,
            'charges': predicted_charges[0]
        }, is_training_data=input_data.is_training_data)

        # Save prediction result
        await save_prediction_result(db=db, record_id=record.id, predicted_charges=predicted_charges[0])
        
        return predicted_charges[0]
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise


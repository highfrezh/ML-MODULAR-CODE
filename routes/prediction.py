"""
Prediction router for Medical Cost Prediction API
"""

from fastapi import APIRouter, HTTPException, status
from schema.prediction import InsuranceInput, PredictionResponse
from  utils.logger import logger
from service.prediction import save_prediction_with_data
from database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

router = APIRouter(prefix="/api/v1", tags=["Prediction"])



@router.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(input_data: InsuranceInput, db: AsyncSession = Depends(get_db)):
    """
    Predict medical insurance cost based on beneficiary features
    
    This endpoint accepts beneficiary features and returns a predicted
    medical insurance cost.
    """
    try:
        logger.info("Prediction request received")
        
        # Make prediction
        predicted_charges = await save_prediction_with_data(input_data, db)           

        # Prepare and return response
        return PredictionResponse(
            predicted_charges=predicted_charges,
            status="success"
        )

    except ValueError as e:
        logger.error(f"Validation error in prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Input validation error: {str(e)}"
        )
    
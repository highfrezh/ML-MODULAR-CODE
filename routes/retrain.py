"""Model retraining router for Medical Cost Prediction API"""

from fastapi import APIRouter, HTTPException, status
from schema.retrain import RetrainResponse
from utils.logger import logger
from service.retrain import retrain_model
from database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

router = APIRouter(prefix="/api/v1", tags=["Retrain"])

@router.post("/retrain", response_model=RetrainResponse)
async def retrain_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Retrain the medical cost prediction model with all the data stored in database.
    Uses a LinearRegression by default.
    """
    try:
        logger.info("Retraining request received.")

        return await retrain_model(db)
    except Exception as e:
        logger.error(f"Unexpected error during retraining: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error during retraining"
        )
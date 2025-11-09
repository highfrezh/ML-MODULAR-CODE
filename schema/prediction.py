from pydantic import BaseModel

class InsuranceInput(BaseModel):
    age: int 
    sex: str 
    bmi: float 
    children: int 
    smoker: str 
    region: str
    is_training_data: bool = False

class PredictionResponse(BaseModel):
    """
    Response model for prediction endpoint
    """
    predicted_charges: float
    status: str = "success"
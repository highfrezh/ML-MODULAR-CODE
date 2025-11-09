from pydantic import BaseModel

class RetrainResponse(BaseModel):
    """
    Response model for retraining endpoint
    """
    message: str        
    r2_score: float     
    rmse: float         
    training_samples: int 
    test_samples: int   
    timestamp: str      

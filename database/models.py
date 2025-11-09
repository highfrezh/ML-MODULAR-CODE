"""
SQLAlchemy database models for Medical Cost Prediction
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):   
    pass

class InsuranceRecord(Base):
    """
    Model for storing insurance records
    """
    __tablename__ = "insurance_records"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)  # 'male' or 'female'
    bmi = Column(Float, nullable=False)
    children = Column(Integer, nullable=False)
    smoker = Column(String(3), nullable=False)  # 'yes' or 'no'
    region = Column(String(20), nullable=False)  # 'southwest', 'southeast', 'northwest', 'northeast'
    charges = Column(Float, nullable=True)  # Nullable for prediction records
    is_training_data = Column(Boolean, default=True)
    source = Column(String(20), default="original")  # 'original', 'prediction', 'uploaded'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship with predictions
    predictions = relationship("PredictionResult", back_populates="insurance_record")


class PredictionResult(Base):
    """
    Model for storing prediction results
    """
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("insurance_records.id"), nullable=False)
    predicted_charges = Column(Float, nullable=False)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship with insurance record
    insurance_record = relationship("InsuranceRecord", back_populates="predictions")


class ModelMetadata(Base):
    """
    Model for storing model training metadata
    """
    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True, index=True)
    model_type = Column(String(50), nullable=False)  
    r2_score = Column(Float, nullable=False)
    mse = Column(Float, nullable=False)
    mae = Column(Float, nullable=False)
    training_samples = Column(Integer, nullable=False)
    test_samples = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

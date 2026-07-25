from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import joblib
import numpy as np
import pandas as pd
import os

# Define all 54 African countries (case-insensitive matching)
AFRICAN_COUNTRIES = {
    "algeria", "angola", "benin", "botswana", "burkina faso", "burundi",
    "cameroon", "cape verde", "central african republic", "chad", "comoros", "congo",
    "democratic republic of the congo", "djibouti", "egypt", "equatorial guinea",
    "eritrea", "eswatini", "ethiopia", "gabon", "gambia", "ghana", "guinea",
    "guinea-bissau", "ivory coast", "kenya", "lesotho", "liberia", "libya",
    "madagascar", "malawi", "mali", "mauritania", "mauritius", "morocco",
    "mozambique", "namibia", "niger", "nigeria", "rwanda", "sao tome and principe",
    "senegal", "seychelles", "sierra leone", "somalia", "south africa", "south sudan",
    "sudan", "tanzania", "togo", "tunisia", "uganda", "zambia", "zimbabwe"
}

app = FastAPI(
    title="AgriSmart Africa Crop Yield API",
    description="An API to predict crop yields based on African climate, country, and farming inputs.",
    version="1.0.0"
)

ALLOWED_ORIGINS = [
    "https://linear-regression-model1.onrender.com",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  
    allow_credentials=True,        
    allow_methods=["*"],  
    allow_headers=["*"],            
)

# Load the trained model, scaler, AND the model columns
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    model = joblib.load(os.path.join(BASE_DIR, 'best_model.pkl'))
    scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.pkl'))
    # NEW: Load the columns to align the one-hot encoding
    model_columns = joblib.load(os.path.join(BASE_DIR, 'model_columns.pkl')) 
except Exception as e:
    print(f"Warning: Files not found. {e}")

# Pydantic Model now includes the Country string!
class FarmData(BaseModel):
    country: str = Field(..., description="Name of the African country (e.g., 'Rwanda', 'Kenya')")
    average_rain_fall_mm_per_year: float = Field(..., ge=50.0, le=3500.0)
    avg_temp: float = Field(..., ge=1.0, le=40.0)
    pesticides_tonnes: float = Field(..., ge=0.0, le=400000.0)
    
    @validator('country')
    def validate_african_country(cls, v):
        """Validate that the country is in Africa (case-insensitive)"""
        country_lower = v.lower().strip()
        if country_lower not in AFRICAN_COUNTRIES:
            allowed_countries = ", ".join(sorted(AFRICAN_COUNTRIES)).title()
            raise ValueError(
                f"'{v}' is not an African country. This API is restricted to African nations only. "
                f"Allowed countries: {allowed_countries}"
            )
        return country_lower

@app.get("/health")
def health_check():
    """Check API health and model status"""
    try:
        model_features = len(model_columns) if 'model_columns' in globals() else 0
        return {
            "status": "healthy",
            "model_loaded": True,
            "expected_features": model_features,
            "model_columns_sample": list(model_columns)[:10] if 'model_columns' in globals() else []
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "model_loaded": False,
            "error": str(e)
        }

@app.post("/predict")
def predict_yield(data: FarmData):
    try:
        # 1. Put the user's input into a dictionary
        input_dict = {
            'average_rain_fall_mm_per_year': data.average_rain_fall_mm_per_year,
            'avg_temp': data.avg_temp,
            'pesticides_tonnes': data.pesticides_tonnes,
            'Area': data.country
        }
        
        # 2. Convert to a Pandas DataFrame
        df_input = pd.DataFrame([input_dict])
        
        # 3. One-Hot Encode the country string
        df_encoded = pd.get_dummies(df_input, columns=['Area'])
        
        # 4. Align the new dataframe with the exact columns the model was trained on
        # This adds all the other African countries as '0' (False)
        df_encoded = df_encoded.reindex(columns=model_columns, fill_value=0)
        
        # DEBUG: Show what features are being used
        print(f"Input country: {data.country}")
        print(f"Features sent to model: {df_encoded.columns.tolist()}")
        print(f"Feature values: {df_encoded.values[0]}")
        
        # 5. Scale and Predict
        scaled_features = scaler.transform(df_encoded)
        prediction = model.predict(scaled_features)
        
        return {
            "predicted_yield_hg_ha": round(float(prediction[0]), 2),
            "country": data.country,
            "rainfall_mm": data.average_rain_fall_mm_per_year,
            "temperature_c": data.avg_temp,
            "pesticides_tonnes": data.pesticides_tonnes
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/retrain")
def trigger_retraining(background_tasks: BackgroundTasks):
    def retrain_model_task():
        pass
    background_tasks.add_task(retrain_model_task)
    return {"message": "Model retraining triggered."}
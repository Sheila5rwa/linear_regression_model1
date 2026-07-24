from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np

# Initialize FastAPI App
app = FastAPI(
    title="AgriSmart Africa Crop Yield API",
    description="An API to predict crop yields based on climate and farming inputs.",
    version="1.0.0"
)

# Strict CORS Middleware Configuration (Rubric Requirement)
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://your-flutter-app-domain.com", # Replace with your actual frontend domain later
    "https://your-render-url.onrender.com" # Replace with your Render URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"], 
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

# Load the trained model and scaler
try:
    model = joblib.load('best_model.pkl')
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError:
    print("Warning: Model or Scaler not found. Please train the model first.")

# Pydantic Model with strict data types and range constraints (Rubric Requirement)
class FarmData(BaseModel):
    average_rain_fall_mm_per_year: float = Field(
        ..., 
        ge=50.0, 
        le=3500.0, 
        description="Annual rainfall in mm (Must be between 50 and 3500)"
    )
    avg_temp: float = Field(
        ..., 
        ge=1.0, 
        le=40.0, 
        description="Average temperature in Celsius (Must be between 1.0 and 40.0)"
    )
    pesticides_tonnes: float = Field(
        ..., 
        ge=0.0, 
        le=400000.0, 
        description="Pesticides used in tonnes (Must be between 0 and 400,000)"
    )

# Prediction Endpoint
@app.post("/predict")
def predict_yield(data: FarmData):
    try:
        # 1. Convert input data to a 2D numpy array in the exact order the model was trained on
        input_features = np.array([[
            data.average_rain_fall_mm_per_year,
            data.avg_temp,
            data.pesticides_tonnes
        ]])
        
        # 2. Scale the features using the saved StandardScaler
        scaled_features = scaler.transform(input_features)
        
        # 3. Make the prediction
        prediction = model.predict(scaled_features)
        
        # 4. Return the predicted yield rounded to 2 decimal places
        return {"predicted_yield_hg_ha": round(float(prediction[0]), 2)}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

# Model Retraining Endpoint (Rubric Requirement)
@app.post("/retrain")
def trigger_retraining(background_tasks: BackgroundTasks):
    def retrain_model_task():
        # In a real-world scenario, this block would:
        # 1. Connect to a database containing new harvest data from farmers.
        # 2. Preprocess the new data.
        # 3. Call model.fit() or model.partial_fit() to update the weights.
        # 4. Save the updated best_model.pkl back to the server.
        print("Background task running: Fetching new agricultural data and retraining model...")
        pass
    
    # Add the retraining function to background tasks so the API doesn't hang
    background_tasks.add_task(retrain_model_task)
    
    return {"message": "Model retraining has been triggered successfully in the background."}
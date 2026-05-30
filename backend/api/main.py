from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.model.predict import predict_future

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================

@app.get("/")
def root():

    return {
        "message": "RainLiveCast API running"
    }

# =========================

@app.get("/predict")
def predict():

    result = predict_future()

    return result
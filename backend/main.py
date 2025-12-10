"""
Autonomous Predictive Maintenance System - FastAPI Backend
Master Agent orchestrating multiple Worker AI agents for predictive maintenance,
customer engagement, service scheduling, and manufacturing quality improvement.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(
    title="Predictive Maintenance AI System",
    description="Agentic AI for automotive predictive maintenance with Master-Worker orchestration",
    version="1.0.0"
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Predictive Maintenance AI System",
        "status": "operational",
        "agents": {
            "master": "active",
            "workers": ["data_analysis", "diagnosis", "customer_engagement", 
                       "scheduling", "feedback", "manufacturing_insights"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

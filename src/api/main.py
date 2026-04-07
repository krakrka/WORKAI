from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="WorkAI Backend API", version="0.1.0")

# Modèle pour une requête de tâche
class TaskRequest(BaseModel):
    prompt: str
    context_id: Optional[str] = "default"

# Modèle pour la réponse
class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

@app.get("/")
async def root():
    return {"status": "online", "service": "WorkAI Core"}

@app.post("/task/submit", response_model=TaskResponse)
async def submit_task(request: TaskRequest):
    # Ici, l'API appellera l'Orchestrateur (ceo_agent) plus tard
    print(f"Requête reçue : {request.prompt}")
    return {
        "task_id": "temp-123",
        "status": "received",
        "message": "La tâche a été transmise au CEO Agent."
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Cirkl Graphiti Memory API")

# CORS pour N8N
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pour l'instant, on stocke en mémoire (Neo4j sera ajouté après)
connections_memory = {}
episodes_memory = []

class CirklConnection(BaseModel):
    user_id: str
    connection_name: str
    role: Optional[str] = None
    company: Optional[str] = None
    location: str
    meeting_context: str
    authenticity_score: float
    conversation: str
    timestamp: Optional[str] = None

@app.post("/api/connection/add")
async def add_connection(connection: CirklConnection):
    """Ajoute une nouvelle connexion"""
    try:
        connection_id = f"{connection.user_id}_{datetime.now().timestamp()}"
        
        connection_data = {
            "id": connection_id,
            "user_id": connection.user_id,
            "connection_name": connection.connection_name,
            "role": connection.role,
            "company": connection.company,
            "location": connection.location,
            "authenticity_score": connection.authenticity_score,
            "timestamp": connection.timestamp or datetime.now().isoformat()
        }
        
        if connection.user_id not in connections_memory:
            connections_memory[connection.user_id] = []
        
        connections_memory[connection.user_id].append(connection_data)
        
        return {
            "status": "success",
            "message": f"Connexion avec {connection.connection_name} ajoutée",
            "connection_id": connection_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Cirkl Graphiti Memory",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
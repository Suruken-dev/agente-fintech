import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.rag import ask_question

# Definir el modelo de la solicitud
class QuestionRequest(BaseModel):
    question: str

# Definir el modelo de la respuesta
class SourceResponse(BaseModel):
    filename: str
    category: str
    page: str
    content_preview: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceResponse]

# Inicializar la app FastAPI
app = FastAPI(
    title="Agente Fintech - API",
    description="API para consultar documentos internos de FinBank Digital",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Agente Fintech funcionando. Usa POST /ask para hacer preguntas.",
        "docs": "/docs"
    }

@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):
    try:
        result = ask_question(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Para ejecutar el servidor directamente (opcional)
if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
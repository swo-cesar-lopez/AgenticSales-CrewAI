from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from datetime import datetime
import warnings

# Importar la clase CrewAiAgents
from crew_ai_agents.crew import CrewAiAgents

# Ignorar ciertas advertencias
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI(title="API de CrewAI Agents")

# Modelos de entrada para cada endpoint
class TrainRequest(BaseModel):
    n_iterations: int
    filename: str

class ReplayRequest(BaseModel):
    task_id: str

class TestRequest(BaseModel):
    n_iterations: int
    openai_model_name: str

# Nuevo modelo para el endpoint run
class RunRequest(BaseModel):
    topic: str = Field(default="AI LLMs", description="Tema sobre el que trabajarán los agentes")
    current_year: str = Field(default=None, description="Año actual para contextualizar la investigación")

@app.post("/run")
async def run_endpoint(request: RunRequest = Body(...)):
    """
    Ejecuta la función 'run' que inicia el crew con los inputs proporcionados.
    """
    # Si no se proporciona el año, usar el año actual
    if request.current_year is None:
        request.current_year = str(datetime.now().year)
    
    inputs = {
        'topic': request.topic,
        'current_year': request.current_year
    }
    
    try:
        # Ejecutar el crew y capturar el resultado
        result = CrewAiAgents().crew().kickoff(inputs=inputs)
        
        # Devolver tanto el mensaje de éxito como el resultado
        return {
            "message": "Crew run executed successfully",
            "result": result,
            "topic": request.topic
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while running the crew: {e}")

@app.post("/train")
async def train_endpoint(request: TrainRequest):
    """
    Entrena el crew por un número de iteraciones, usando un archivo dado.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        CrewAiAgents().crew().train(
            n_iterations=request.n_iterations,
            filename=request.filename,
            inputs=inputs
        )
        return {"message": "Crew training executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while training the crew: {e}")

@app.post("/replay")
async def replay_endpoint(request: ReplayRequest):
    """
    Reproduce la ejecución del crew a partir de un task_id específico.
    """
    try:
        CrewAiAgents().crew().replay(task_id=request.task_id)
        return {"message": "Crew replay executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while replaying the crew: {e}")

@app.post("/test")
async def test_endpoint(request: TestRequest):
    """
    Ejecuta un test del crew con un número de iteraciones y un modelo de OpenAI especificado.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        CrewAiAgents().crew().test(
            n_iterations=request.n_iterations,
            openai_model_name=request.openai_model_name,
            inputs=inputs
        )
        return {"message": "Crew test executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while testing the crew: {e}")
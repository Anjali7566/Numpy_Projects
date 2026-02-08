import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from engine import PhysicsEngine

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
engine = PhysicsEngine()

class Control(BaseModel):
    G: float
    dt: float

@app.get("/")
def root():
    return {"status": "N-Body Backend Running"}

@app.post("/control")
def update_control(c: Control):
    engine.G = c.G
    engine.dt = c.dt
    return {"ok": True}

@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    while True:
        pos, vel = engine.step()
        await ws.send_json({
            "positions": pos.tolist(),
            "velocities": vel.tolist()
        })
        await asyncio.sleep(1 / 60)

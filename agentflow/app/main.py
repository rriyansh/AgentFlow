from fastapi import FastAPI
from app.graph import build_graph

app = FastAPI()
graph = build_graph()


@app.get("/")
def read_root():
    return {"status": "ok"}

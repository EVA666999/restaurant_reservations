import os
import sys

from fastapi import FastAPI

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import uvicorn
from routers import reservations, tables

app = FastAPI()

app.include_router(tables.router)
app.include_router(reservations.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

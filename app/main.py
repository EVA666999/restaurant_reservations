from fastapi import FastAPI
from routers import tables, reservations
import uvicorn

app = FastAPI()

app.include_router(tables.router)
app.include_router(reservations.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
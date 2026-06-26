from fastapi import FastAPI, Depends, HTTPException
from app.api import search, documents
from app.db import init_db

app = FastAPI(title="Mini Search Engine")

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(search.router, prefix="/search")
app.include_router(documents.router, prefix="/documents")

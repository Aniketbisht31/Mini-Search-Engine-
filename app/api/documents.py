from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models import documents

router = APIRouter()

class DocumentCreate(BaseModel):
    title: str
    body: str

@router.post("/")
async def create_document(payload: DocumentCreate, session: AsyncSession = Depends(get_session)):
    stmt = insert(documents).values(title=payload.title, body=payload.body).returning(documents.c.id)
    result = await session.execute(stmt)
    await session.commit()
    document_id = result.scalar_one()
    return {"id": document_id}

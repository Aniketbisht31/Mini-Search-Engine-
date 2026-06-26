from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session

router = APIRouter()

@router.get("/")
async def query(q: str = Query(..., min_length=1), session: AsyncSession = Depends(get_session)):
    query_text = text(
        "SELECT id, title, body, ts_rank_cd(content_vector, plainto_tsquery('english', :q)) AS rank "
        "FROM documents WHERE content_vector @@ plainto_tsquery('english', :q) "
        "ORDER BY rank DESC LIMIT 20"
    )
    result = await session.execute(query_text, {"q": q})
    rows = result.all()
    return [dict(id=row.id, title=row.title, body=row.body, rank=row.rank) for row in rows]

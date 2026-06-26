import os
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://search_user:search_pass@localhost/search_db")
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS unaccent;"))

        await conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                content_vector tsvector
            );
            """
        ))

        await conn.execute(text(
            """
            CREATE INDEX IF NOT EXISTS documents_content_idx ON documents USING GIN(content_vector);
            """
        ))

        await conn.execute(text(
            """
            CREATE FUNCTION documents_trigger() RETURNS trigger AS $$
            begin
              new.content_vector := to_tsvector('english', coalesce(new.title,'') || ' ' || coalesce(new.body,''));
              return new;
            end
            $$ LANGUAGE plpgsql;
            """
        ))

        await conn.execute(text(
            """
            CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
            ON documents FOR EACH ROW EXECUTE PROCEDURE documents_trigger();
            """
        ))

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

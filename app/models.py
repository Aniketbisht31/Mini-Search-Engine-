from sqlalchemy import Table, Column, Integer, Text
from sqlalchemy.orm import registry

mapper_registry = registry()

documents = Table(
    "documents",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("title", Text, nullable=False),
    Column("body", Text, nullable=False),
)

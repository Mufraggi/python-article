from sqlmodel import create_engine, SQLModel

from src.schemas.task import Task


def migrate():
    sqlite_url = "sqlite:///tasks.db"
    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)

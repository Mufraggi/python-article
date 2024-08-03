import uuid
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, UUID
from typing import NewType

TaskId = NewType('TaskId', uuid.UUID)


class Task(SQLModel, table=True):
    id: TaskId = Field(sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4))
    title: str
    description: Optional[str] = None
    is_completed: bool = False



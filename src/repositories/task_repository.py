from typing import Type

from sqlmodel import Session

from src.repositories.abs_crud import AbstractCRUD
from src.schemas.task import Task, TaskId


class TaskRepository(AbstractCRUD[Task, TaskId]):
    def __init__(self, session: Session):
        self.__session = session

    def get_session(self) -> Session:
        return self.__session

    def model(self) -> Type[Task]:
        return Task

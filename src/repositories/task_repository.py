from typing import Type, Protocol

from sqlmodel import Session, select

from src.repositories.abs_crud import AbstractCRUD
from src.schemas.task import Task, TaskId


class ITaskRepository(Protocol):
    def get_session(self) -> Session:
        pass

    def model(self) -> Type[Task]:
        pass

    def list_tasks_id(self) -> list[TaskId]:
        pass

    def create(self, obj: Task) -> Task:
        pass

    def get_by_id(self, id: TaskId) -> Task | None:
        pass

    def update(self, obj: Task) -> Task:
        pass

    def delete(self, id: TaskId) -> None:
        pass

    def list(self, skip: int = 0, limit: int = 100) -> list[Task]:
        pass


class TaskRepository(AbstractCRUD[Task, TaskId]):
    def __init__(self, session: Session):
        self.__session = session

    def get_session(self) -> Session:
        return self.__session

    def model(self) -> Type[Task]:
        return Task

    def list_tasks_id(self) -> list[TaskId]:
        session = self.get_session()
        statement = select(self.model().id)
        results = session.exec(statement)
        return [TaskId(uuid) for uuid in results]


def create_task_repository(session: Session) -> ITaskRepository:
    return TaskRepository(session)

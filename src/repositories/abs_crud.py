from sqlmodel import SQLModel, Session, select
from typing import TypeVar, Generic, Type
from abc import ABC, abstractmethod

T = TypeVar('T', bound=SQLModel)
ID = TypeVar('ID')


class AbstractCRUD(ABC, Generic[T, ID]):
    @abstractmethod
    def model(self) -> Type[T]:
        pass

    @abstractmethod
    def get_session(self) -> Session:
        pass

    def create(self, obj: T) -> T:
        session = self.get_session()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def get_by_id(self, id: ID) -> T | None:
        session = self.get_session()
        return session.get(self.model(), id)

    def update(self, obj: T) -> T:
        session = self.get_session()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, id: ID) -> None:
        session = self.get_session()
        obj = session.get(self.model(), id)
        if obj:
            session.delete(obj)
            session.commit()

    def list(self, skip: int = 0, limit: int = 100) -> list[T]:
        session = self.get_session()
        statement = select(self.model()).offset(skip).limit(limit)
        results = session.exec(statement)
        return list(results)

import pytest
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine
from src.repositories.task_repository import TaskRepository, create_task_repository
from src.schemas.task import Task, TaskId


@pytest.fixture(scope="function")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="function")
def session(engine):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def task_repository(session):
    return create_task_repository(session)


def test_create_task(task_repository):
    task = Task(title="Test Task", description="Test Description")
    created_task = task_repository.create(task)
    assert created_task.id is not None
    assert created_task.title == "Test Task"
    assert created_task.description == "Test Description"
    assert not created_task.is_completed


def test_get_task_by_id(task_repository):
    task = Task(title="Test Task")
    created_task = task_repository.create(task)
    retrieved_task = task_repository.get_by_id(created_task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Test Task"


def test_update_task(task_repository):
    task = Task(title="Test Task")
    created_task = task_repository.create(task)
    created_task.title = "Updated Task"
    updated_task = task_repository.update(created_task)
    assert updated_task.title == "Updated Task"


def test_delete_task(task_repository):
    task = Task(title="Test Task")
    created_task = task_repository.create(task)
    task_repository.delete(created_task.id)
    retrieved_task = task_repository.get_by_id(created_task.id)
    assert retrieved_task is None


def test_list_tasks(task_repository):
    task_repository.create(Task(title="Task 1"))
    task_repository.create(Task(title="Task 2"))
    task_repository.create(Task(title="Task 3"))
    tasks = task_repository.list()
    assert len(tasks) == 3
    assert all(isinstance(task, Task) for task in tasks)


def test_model_method(task_repository):
    assert task_repository.model() == Task


def test_get_session_method(task_repository, session):
    assert task_repository.get_session() == session


def test_get_non_existent_task(task_repository):
    non_existent_id = TaskId(uuid4())
    retrieved_task = task_repository.get_by_id(non_existent_id)
    assert retrieved_task is None

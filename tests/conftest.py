import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.product_management.models import Base


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()

    yield session

    session.close()
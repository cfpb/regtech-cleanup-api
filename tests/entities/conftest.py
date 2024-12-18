import pytest
from sbl_filing_api.entities.models.dao import Base as Filing_Base
from regtech_user_fi_management.entities.models.dao import Base as Institution_Base
from test_dao import Base as Test_Base
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="function", autouse=True)
def setup_filing_db(request: pytest.FixtureRequest, engine: Engine):
    Filing_Base.metadata.create_all(bind=engine)

    def teardown():
        Filing_Base.metadata.drop_all(bind=engine)

    request.addfinalizer(teardown)


@pytest.fixture(scope="function", autouse=True)
def setup_institution_db(request: pytest.FixtureRequest, engine: Engine):
    Institution_Base.metadata.create_all(bind=engine)

    def teardown():
        Institution_Base.metadata.drop_all(bind=engine)

    request.addfinalizer(teardown)


@pytest.fixture(scope="function", autouse=True)
def setup_test_db(request: pytest.FixtureRequest, engine: Engine):
    Test_Base.metadata.create_all(bind=engine)

    def teardown():
        Test_Base.metadata.drop_all(bind=engine)

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def transaction_session(session_generator: scoped_session):
    with session_generator() as session:
        return session


@pytest.fixture(scope="function")
def query_session(session_generator: scoped_session):
    with session_generator() as session:
        return session


@pytest.fixture(scope="function")
def session_generator(engine: Engine):
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

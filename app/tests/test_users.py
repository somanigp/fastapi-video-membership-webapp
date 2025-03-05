import pytest
from app import db
from app.users.models import User

# NOTE A fixture in pytest is a function that sets up preconditions needed for a test and ensures proper cleanup afterward. It helps with test preparation by providing reusable components such as database connections, test data, and configurations.
@pytest.fixture(scope='module')  # The fixture runs once per module. The same session is used for all tests in the module.
def setup():
    # setup : The code before yield prepares resources (e.g., database session, test data, mock object. The part before yield runs first, setting up the database session.
    session = db.get_session()
    yield session  # yield session provides the session to the test functions.
    # teardown : After all tests using this fixture complete, the code after yield runs.
    q = User.objects.filter(email='test@test.com')
    if q.count() != 0:
        q.delete()  # NOTE Delete a user
    session.shutdown()

def test_create_user(setup):
    User.create_user(email='test@test.com', password='abc123')

def test_duplicate_user(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@test.com', password='abc123dafd')

def test_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@test', password='abc123dafd')

def test_valid_password(setup):
    q = User.objects.filter(email='test@test.com')
    assert q.count() == 1
    user_obj = q.first()
    assert user_obj.verify_password('abc123') == True
    assert user_obj.verify_password('abc1234') == False

# def test_assert():
#     assert True is True


# def test_equal():
#     assert 1 == 1

# def test_equal():
#     assert 1 != 1

# def test_invalid_assert():
#     with pytest.raises(AssertionError):
#         assert True is not True

# import pytest

# @pytest.fixture
# def sample_data():
#     data = {"user": "test_user", "email": "test@example.com"}
#     yield data  # Provided to test functions
#     print("Teardown: Cleaning up data")  # Runs after test execution


# def test_example(sample_data):
#     assert sample_data["user"] == "test_user"

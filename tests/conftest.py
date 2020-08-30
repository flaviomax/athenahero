import pytest


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""

    def urlopen_mock(self, method, url, *args, **kwargs):
        raise RuntimeError(f"The test was about to {method} {self.scheme}://{self.host}{url}")

    monkeypatch.setattr("urllib3.connectionpool.HTTPConnectionPool.urlopen", urlopen_mock)


# Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
BCRYPT_LOG_ROUNDS = 4

# Enable the TESTING flag to disable the error catching during request handling
# so that you get better error reports when performing test requests against the application.
TESTING = True
ENV = "development"

# Disable CSRF tokens in the Forms (only valid for testing purposes!)
WTF_CSRF_ENABLED = False

# DATABASE
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/athenahero_test"
SQLALCHEMY_TRACK_MODIFICATIONS = False

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

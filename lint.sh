isort athenahero tests
black --line-length 120 --target-version py36 athenahero tests
pydocstyle athenahero/ --convention=numpy
mypy athenahero
flake8 setup.py athenahero tests
pylint -j 0 athenahero
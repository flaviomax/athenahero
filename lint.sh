isort -m 3 --tc athenahero tests
black --line-length 120 --target-version py36 athenahero tests
# find . -name '*.py' -exec autopep8 --max-line-length 120 --in-place '{}' \;
# pydocstyle athenahero/ --convention=numpy
# mypy athenahero
flake8 --max-line-length=120 athenahero tests
# pylint -j 0 athenahero
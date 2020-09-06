start: database-setup
	gunicorn -b 0.0.0.0:5000 -w 5 --preload wsgi:app

start-dev: database-setup
	FLASK_ENV=development flask run --host 0.0.0.0 --no-reload

database-setup:
	FLASK_APP=athenahero flask db upgrade

.PHONY: test
test:
	pytest -v

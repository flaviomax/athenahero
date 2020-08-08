start: database-setup
	gunicorn -b localhost:5000 wsgi:app

start-dev: database-setup
	FLASK_APP=athenahero FLASK_ENV=development flask run

database-setup:
	FLASK_APP=athenahero flask db upgrade

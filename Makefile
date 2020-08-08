start:
	gunicorn -b localhost:5000 wsgi:app

start-dev:
	FLASK_APP=athenahero FLASK_ENV=development flask run

# flask new migration: 
	# FLASK_APP=athenahero flask db migrate -m "mensgaem"
	#  ele olha o estado atual do banco e cria as migrações sozinho!!

start: database-setup
	gunicorn -b localhost:5000 wsgi:app

start-dev: database-setup
	FLASK_APP=athenahero FLASK_ENV=development flask run

database-setup:
	FLASK_APP=athenahero flask db upgrade

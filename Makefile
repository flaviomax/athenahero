# flask new migration: 
	# FLASK_APP=athenahero flask db migrate -m "mensgaem"
	#  ele olha o estado atual do banco e cria as migrações sozinho!!
	# FLASK_APP=athenahero flask db upgrade roda as migracoes

start: database-setup
	gunicorn -b localhost:5000 -w 5 --preload wsgi:app

start-dev: database-setup
	FLASK_ENV=development flask run --no-reload

database-setup:
	FLASK_APP=athenahero flask db upgrade

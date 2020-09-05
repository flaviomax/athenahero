# flask new migration: 
	# FLASK_APP=athenahero flask db migrate -m "mensgaem"
	#  ele olha o estado atual do banco e cria as migrações sozinho!!
	# FLASK_APP=athenahero flask db upgrade roda as migracoes
	# se precisar ser manual, usar `revision` ao inves de `migrate`

start: database-setup
	gunicorn -b 0.0.0.0:5000 -w 5 --preload wsgi:app

start-dev: database-setup
	FLASK_ENV=development flask run --host 0.0.0.0 --no-reload

database-setup:
	FLASK_APP=athenahero flask db upgrade

.PHONY: test
test:
	pytest -v

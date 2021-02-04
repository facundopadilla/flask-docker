start-off-cache:
	docker-compose up -d --no-build --force-recreate
full-start:
	docker-compose up -d
start-test:
	docker-compose up -d --no-build --force-recreate flask_app db
stop:
	docker-compose down -v
start-debug:
	export FLASK_APP=run_debug.py
	export FLASK_DEBUG=1
	python run.py
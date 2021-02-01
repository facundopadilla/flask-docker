start-off-cache:
	docker-compose up -d --no-build --force-recreate
full-start:
	docker-compose up -d
stop:
	docker-compose down -v
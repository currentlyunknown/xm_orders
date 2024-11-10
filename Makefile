.ONESHELL:

COMPOSE := docker compose

EXEC_ORDERS := $(COMPOSE) exec orders
EXEC_ORDERS_DB := $(COMPOSE) exec orders-db

docker_build:
	$(COMPOSE) build

docker_bash: docker_up_d
	$(EXEC_ORDERS) bash

docker_bash_db: docker_up_d
	$(EXEC_ORDERS_DB) bash

docker_up:
	$(COMPOSE) up

docker_up_d:
	$(COMPOSE) up -d

docker_down_containers_only:
	$(COMPOSE) down

docker_down:
	$(COMPOSE) down -v

docker_nuke:
	docker system prune -a && docker volume prune

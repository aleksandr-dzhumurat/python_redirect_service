CURRENT_DIR = $(shell pwd)
PROJECT_NAME = tinyurl
PORT = 8080
include .env
export

prepare-dirs:
	mkdir -p ${CURRENT_DIR}/data || true && \
	mkdir -p ${CURRENT_DIR}/data/pg_data || true

build-network:
	docker network create service_network -d bridge || true

build:
	docker build -t ${PROJECT_NAME}:dev .

build-postgres:
	docker build -f postgres/Dockerfile -t ${PROJECT_NAME}_postgres:dev ./postgres

run-postgres:
	docker run -it --rm \
	--network service_network \
	-v "${CURRENT_DIR}/data/pg_data:/var/lib/postgresql/data" \
	-p 5432:5432 \
	-e POSTGRES_HOST_AUTH_METHOD="trust" \
	--name postgres_container \
	${PROJECT_NAME}_postgres:dev


stop-postgres:
	docker rm -f ${PROJECT_NAME}_postgres || true

stop:
	docker rm -f ${PROJECT_NAME}_container || true

run: stop build-network prepare-dirs
	docker run -it --rm \
	    --env-file ${CURRENT_DIR}/.env \
	    -p ${FASTAPI_PORT}:${FASTAPI_PORT} \
	    -v "${CURRENT_DIR}/src:/srv/src" \
	    -v "${CURRENT_DIR}/data:/srv/data" \
		--network service_network \
	    --name ${PROJECT_NAME}_container \
	    ${PROJECT_NAME}:dev

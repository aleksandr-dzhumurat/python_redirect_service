CURRENT_DIR = $(shell pwd)
PROJECT_NAME = tinyurl
PORT = 8080
include .env
export

prepare-dirs:
	mkdir -p ${CURRENT_DIR}/data || true

build-network:
	docker network create service_network -d bridge || true

build:
	docker build -t ${PROJECT_NAME}:dev .

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

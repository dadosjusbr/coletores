#!make
include .env

create-volume:
	docker volume create --driver local \
	--opt type=none \
	--opt device=${DATA_VOLUME_PATH} \
	--opt o=bind \
	--name=dadosjusbr

build-executor:
	docker build -t executor -f executor/Dockerfile .

file-server:
	docker run -d \
   	 	-v dadosjusbr:/web \
    	-p 8080:8080 \
    	halverneus/static-file-server:latest

run-executor:
	make create-volume
	docker run \
	-v dadosjusbr:/output \
	-v /var/run/docker.sock:/var/run/docker.sock \
	--privileged \
	--env-file ./executor/.env \
	executor
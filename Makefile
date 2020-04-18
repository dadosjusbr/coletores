# Create a output folder inside workdir path and create a docker volume with this path.
create-volume:
	mkdir -p $(shell pwd)/output
	docker volume create --driver local \
	--opt type=none \
	--opt device=$(shell pwd)/output \
	--opt o=bind \
	--name=dadosjusbr

# Build executor image
build-executor:
	docker build -t executor -f executor/Dockerfile .

# Create a static server containing dadosjusbr docker volume files.
file-server:
	docker run -d \
   	 	-v dadosjusbr:/web \
    	-p 8090:8080 \
    	halverneus/static-file-server:latest

# Run executor after builded image.
run-executor:
	make create-volume
	docker run \
	--rm \
	-v dadosjusbr:/output \
	-v /var/run/docker.sock:/var/run/docker.sock \
	--privileged \
	--env-file ./executor/.env \
	executor
VERSION=v1
DOCKERUSER=97052212345

#
# You should probably update the docker.io user if you update this
#

build:
	docker build -f Dockerfile-logs -t logs  .

#
# The following make rule labels the current docker image with the version
# number specified above and also the "latest" tag. It then pushes it to
# hub.docker.io
#
push:
	docker tag logs  $(DOCKERUSER)/bigdata-logs:$(VERSION)
	docker push $(DOCKERUSER)/bigdata-logs:$(VERSION)
	docker tag logs  $(DOCKERUSER)/bigdata-logs:latest
	docker push $(DOCKERUSER)/bigdata-logs:latest
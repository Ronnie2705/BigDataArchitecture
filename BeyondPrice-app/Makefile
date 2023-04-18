VERSION=v1
DOCKERUSER=bhawneet1034

#
# You should probably update the docker.io user if you update this
#

build:
	docker build -f Dockerfile-angular -t angular  .

#
# The following make rule labels the current docker image with the version
# number specified above and also the "latest" tag. It then pushes it to
# hub.docker.io
#
push:
	docker tag angular  $(DOCKERUSER)/bigdata-angular:$(VERSION)
	docker push $(DOCKERUSER)/bigdata-angular:$(VERSION)
	docker tag angular  $(DOCKERUSER)/bigdata-angular:latest
	docker push $(DOCKERUSER)/bigdata-angular:latest
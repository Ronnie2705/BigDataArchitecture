VERSION=v1
DOCKERUSER=bhawneet1034

build:
	docker build -f Dockerfile-rest -t bigdata-rest .

push:
	docker tag bigdata-rest $(DOCKERUSER)/bigdata-rest:$(VERSION)
	docker push $(DOCKERUSER)/bigdata-rest:$(VERSION)
	docker tag bigdata-rest $(DOCKERUSER)/bigdata-rest:latest
	docker push $(DOCKERUSER)/bigdata-rest:latest

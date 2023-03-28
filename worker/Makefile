VERSION=v1
DOCKERUSER=97052212345

build:
	docker build -f Dockerfile -t bigdata-worker .

push:
	docker tag bigdata-worker $(DOCKERUSER)/bigdata-worker:$(VERSION)
	docker push $(DOCKERUSER)/bigdata-worker:$(VERSION)
	docker tag bigdata-worker $(DOCKERUSER)/bigdata-worker:latest
	docker push $(DOCKERUSER)/bigdata-worker:latest


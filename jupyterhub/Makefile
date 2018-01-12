SHELL = /bin/bash
DOCKER_PATH=docker/
IMG_VERSION?=latest

.PHONY: build-image push-image build-single-user push-single-user check-env

check-env:
ifndef DOCKER_REGISTRY
	$(error DOCKER_REGISTRY not set)
endif

build-image: check-env
	docker build -f ${DOCKER_PATH}/${IMAGE}/Dockerfile ${ARG} -t $(DOCKER_REGISTRY):$(IMAGE)-$(IMG_VERSION) .

push-image: check-env build-image
	docker push $(DOCKER_REGISTRY):$(IMAGE)-$(IMG_VERSION)

build-single-user:
	make IMAGE="single-user" build-image

push-single-user: build-single-user
	make IMAGE="single-user" push-image

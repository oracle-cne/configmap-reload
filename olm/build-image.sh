#!/usr/bin/env bash -x
export GOPATH=$(go env GOPATH)

name="configmap-reload"
version="{{{ .major }}}.{{{ .minor }}}.{{{ .patch }}}"
registry="container-registry.oracle.com/olcne"
docker_tag=${registry}/${name}:v${version}

docker build --pull \
    --build-arg https_proxy=${https_proxy} \
    -t ${docker_tag} -f ./olm/builds/Dockerfile .

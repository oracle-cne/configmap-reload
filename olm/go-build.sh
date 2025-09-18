#!/usr/bin/env bash

mkdir -p bin
version="0.15.0"

ldflags="
        -s -w -extldflags '-static'
        -X main.version=v${version}"

go build --installsuffix cgo -trimpath=false -v -o ./bin/configmap-reload \
	-ldflags "${ldflags}" configmap-reload.go

#!/usr/bin/env bash

set -euo pipefail

log() {
    echo "go-build.sh: $*"
}

mkdir -p bin
version="0.15.0"
build_host="${HOST:-$(hostname)}"
build_user="${USER:-$(id -un)}@${build_host}"
go_source="${GOPATH_SRC:-$(pwd)}"

ldflags="
        -s -w -extldflags '-static'
        -extldflags=-L/usr/lib64
        -X main.version=v${version}"

log "starting configmap-reload build"
log "git_revision=$(git rev-parse HEAD)"
log "build_user=${build_user}"
log "go_version=$(go version)"
log "compiling Go binary from ${go_source}"
go build --installsuffix cgo -trimpath=false -v -o ./bin/configmap-reload \
    -ldflags "${ldflags}" "${go_source}"

log "verifying configmap-reload binary"
./bin/configmap-reload -h

log "completed configmap-reload build"

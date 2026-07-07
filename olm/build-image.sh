#!/usr/bin/env bash

set -euo pipefail

name="configmap-reload"
version="0.15.0"
registry="container-registry.oracle.com/olcne"
docker_tag=${registry}/${name}:v${version}
golang_version="${GOLANG_VERSION:-${1:-}}"

log() {
    echo "build-image.sh: $*"
}

set -x

if [[ -z "${golang_version}" ]]; then
    echo "build-image.sh: unable to determine Go version; set GOLANG_VERSION or pass it as the first argument" >&2
    exit 1
fi

build_args=(
    --pull
    --build-arg "GOLANG_VERSION=${golang_version}"
    -t "${docker_tag}"
    -f ./olm/builds/Dockerfile
    .
)

mount_yum_config() {
    local yum_repo_config_file="${YUM_REPO_CONFIG_FILE:-}"

    if [[ -z "${yum_repo_config_file}" ]]; then
        log "YUM_REPO_CONFIG_FILE is not set; using base image repository configuration"
        return
    elif [[ "${yum_repo_config_file}" != /* ]]; then
        yum_repo_config_file="$(pwd)/${yum_repo_config_file}"
    fi

    log "checking yum repo config file ${yum_repo_config_file}"
    if [[ ! -s "${yum_repo_config_file}" ]]; then
        echo "build-image.sh: yum repo config file ${yum_repo_config_file} is missing or empty" >&2
        exit 1
    fi

    log "mounting yum repo config file ${yum_repo_config_file}"
    build_args=(
        --volume "${yum_repo_config_file}:/etc/yum.repos.d/extra.repo:ro"
        "${build_args[@]}"
    )
}

mount_yum_config

log "building ${docker_tag}"
podman build "${build_args[@]}"

log "saving ${docker_tag} to ${name}.tar"
podman save "${docker_tag}" > "${name}.tar"

log "completed image build"

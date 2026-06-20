FROM container-registry.oracle.com/os/oraclelinux:8 AS builder

ARG GOLANG_VERSION

ENV GOPATH=/workspace/go CGO_ENABLED=0 GOTOOLCHAIN=local
ENV GOPATH_SRC=$GOPATH/src/github.com/oracle-cne/configmap-reload
WORKDIR $GOPATH_SRC

RUN dnf module disable -y go-toolset:ol8 \
    dnf install --enablerepo=ol8_codeready_builder -y gcc git glibc-devel golang-${GOLANG_VERSION} hostname && \
    dnf clean all && \
    rm -rf /var/cache/yum/* && \
    go version

COPY . $GOPATH_SRC

RUN git config --global --add safe.directory $(pwd) && \
    bash olm/go-build.sh

# -----------------------------------------------------------------------------

FROM container-registry.oracle.com/os/oraclelinux:8-slim

RUN microdnf update -y && \
    microdnf clean all && \
    rm -rf /var/cache/yum/*

COPY LICENSE.txt THIRD_PARTY_LICENSES.txt /licenses/
COPY olm/SECURITY.md /licenses/ORACLE_SECURITY.md

COPY --from=builder /workspace/go/src/github.com/oracle-cne/configmap-reload/bin/configmap-reload /usr/bin/configmap-reload

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

USER 65534

ENTRYPOINT  [ "/usr/bin/configmap-reload"]

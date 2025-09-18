FROM container-registry.oracle.com/os/oraclelinux:8 as builder

WORKDIR $GOPATH/src/github.com/oracle-cne/configmap-reload

RUN dnf install which git glibc-devel -y && \
    dnf install golang -y && \
    dnf clean all && \
    rm -rf /var/cache/yum/*

COPY . $GOPATH/src/github.com/oracle-cne/configmap-reload

RUN sh olm/go-build.sh

# -----------------------------------------------------------------------------

FROM container-registry.oracle.com/os/oraclelinux:8-slim

RUN microdnf update -y && \
    microdnf clean all && \
    rm -rf /var/cache/yum/*

COPY LICENSE SECURITY.md THIRD_PARTY_LICENSES.txt /licenses/
COPY olm/SECURITY.md /licenses/ORACLE_SECURITY.md

COPY --from=builder $GOPATH/src/github.com/oracle-cne/configmap-reload/bin/configmap-reload /usr/bin/configmap-reload

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

ENTRYPOINT  [ "/usr/bin/configmap-reload"]

FROM container-registry.oracle.com/os/oraclelinux:8
COPY rpms /tmp/
RUN dnf install -y /tmp/*.rpm &&\
    dnf clean all &&\
    rm -rf /var/cache/yum/* /tmp/*.rpm

FROM container-registry.oracle.com/os/oraclelinux:8-slim

COPY --from=0 /usr/share/licenses/configmap-reload /usr/share/licenses/configmap-reload
COPY --from=0 /usr/bin/configmap-reload /usr/bin/configmap-reload
RUN microdnf clean all &&\
    rm -rf /var/cache/yum/* &&\
    test -d /LICENSES || ln -s /usr/share/licenses /LICENSES

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

ENTRYPOINT  [ "/usr/bin/configmap-reload"]

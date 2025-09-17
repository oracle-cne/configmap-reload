{{{$version := printf "%s.%s.%s" .major .minor .patch }}}
%global debug_package   %{nil}
%{!?registry: %global registry container-registry.oracle.com/olcne}
%global _name	configmap-reload
%global _buildhost build-ol%{?oraclelinux}-%{?_arch}.oracle.com

Name:		%{_name}-container-image
Version:        {{{$version}}}
Release:        1%{?dist}
Summary:	Simple binary to trigger a reload when a Kubernetes ConfigMap is updated.
License:        Apache 2.0
Url:            https://github.com/jimmidyson/configmap-reload
Source:         %{name}-%{version}.tar.bz2
Vendor:         Oracle America

%description
configmap-reload is a simple binary to trigger a reload when Kubernetes ConfigMaps are updated. It watches mounted volume dirs and notifies the target process that the config map has been changed. It currently only supports sending an HTTP request, but in future it is expected to support sending OS (e.g. SIGHUP) once Kubernetes supports pod PID namespaces.

%prep
%setup -q -n %{name}-%{version}

%build
%global docker_tag %{registry}/%{_name}:v%{version}

%__rm -f .dockerignore
yum clean all && \
yumdownloader --destdir=${PWD}/rpms %{_name}-%{version}-%{release}.%{_build_arch}

docker build --pull \
    --build-arg https_proxy=${https_proxy} \
    -t %{docker_tag} -f ./olm/builds/Dockerfile .
docker save -o %{_name}.tar %{docker_tag}

%install
%__install -D -m 644 %{_name}.tar %{buildroot}/usr/local/share/olcne/%{_name}.tar

%files
%license LICENSE.txt
/usr/local/share/olcne/%{_name}.tar

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Added Oracle Specific Build Files.



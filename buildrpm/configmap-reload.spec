
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global _name	configmap-reload
%global package_name	    github.com/jimmidyson/%{_name}
%global golang_version 1.16
%global _buildhost build-ol%{?oraclelinux}-%{?_arch}.oracle.com

Name:           %{_name}
Version:        0.15.0
Release:        1%{?dist}
Summary:	Simple binary to trigger a reload when a Kubernetes ConfigMap is updated.
License:        Apache 2.0
Url:            https://github.com/jimmidyson/configmap-reload
Source:         %{name}-%{version}.tar.bz2
Vendor:         Oracle America
BuildRequires:  golang >= %{golang_version}

%description
configmap-reload is a simple binary to trigger a reload when Kubernetes ConfigMaps are updated. It watches mounted volume dirs and notifies the target process that the config map has been changed. It currently only supports sending an HTTP request, but in future it is expected to support sending OS (e.g. SIGHUP) once Kubernetes supports pod PID namespaces.

%prep
%setup -q -n %{name}-%{version}

%build
export GOPATH=$(go env GOPATH)
GOPATH_SRC=$GOPATH/src/%{package_name}
%__mkdir_p $GOPATH_SRC
%__rm -r $GOPATH_SRC
%__ln_s $PWD $GOPATH_SRC

pushd $GOPATH_SRC
cd ${GOPATH_SRC}
make out/configmap-reload

%install
install -d -m 755 %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir}/ %{_builddir}/%{name}-%{version}/out/configmap-reload

%files
%{_bindir}/configmap-reload
%license LICENSE.txt THIRD_PARTY_LICENSES.txt
%doc README.md

%clean
rm -fr %{buildroot}
rm -fr %{_builddir}/%{name}-%{version}

%changelog
* Thu Sep 18 2025 Olcne-Builder Jenkins <olcne-builder_us@oracle.com> - 0.15.0-1
- Added Oracle Specific Build Files.


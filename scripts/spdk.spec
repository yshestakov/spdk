# Copyright (c) 2018, Mellanox Technologies. All rights reserved.

%if "%{?_version:1}" == ""
	# %define scm_version %(echo "$(./scripts/get_ver.sh)" )
	%define scm_version 18.10
	%define unmangled_version %{scm_version}
%else
	%define scm_version %{_version}
	%define unmangled_version %{_version}
%endif
%if "%{?_rev:1}" == ""
	%define scm_rev 1
%else
	%define scm_rev %{_rev}
%endif

%if "%{?_sha1:1}" == ""
	%define _sha1 ""
%endif
%if "%{?_branch:1}" == ""
	%define _branch ""
%endif

Name:		spdk
Version:	%{scm_version}
Release:	%{scm_rev}%{?dist}
Summary:	Storage Performance Development Kit
Packager: 	yuriis@mellanox.com

Group: 		System Environment/Daemons
License: 	BSD and LGPLv2 and GPLv2
URL: 		http://www.spdk.io
Source0:	spdk-%{version}.tar.gz
Source1:	spdk-dpdk-%{version}.tar.gz
Source2:	spdk-intel-ipsec-mb-%{version}.tar.gz

ExclusiveArch: i686 x86_64 aarch64
%ifarch aarch64
%global machine armv8a
%global target arm64-%{machine}-linuxapp-gcc
%global _config arm64-%{machine}-linuxapp-gcc
%else
%global machine default
%global target %{_arch}-%{machine}-linuxapp-gcc
%global _config %{_arch}-native-linuxapp-gcc
%endif

# DPDK dependencies
BuildRequires: kernel-devel
BuildRequires: kernel-headers
# not present @ CentOS-7.4 w/o EPEL:
# - BuildRequires: libpcap-devel, python-sphinx, inkscape
# - BuildRequires: texlive-collection-latexextra
BuildRequires: doxygen
BuildRequires:graphviz
BuildRequires: numactl-devel

# SPDK build dependencies
BuildRequires:	git make gcc gcc-c++
BuildRequires:	CUnit-devel, libaio-devel, openssl-devel, libuuid-devel 
BuildRequires:	libiscsi-devel
BuildRequires:  python-pep8, lcov, clang-analyzer
# Additional dependencies for SPDK CLI 
BuildRequires:	python-configshell
# Additional dependencies for NVMe over Fabrics
BuildRequires:	libibverbs-devel, librdmacm-devel
# Additional dependencies for building docs
# not present @ CentOS-7.4 w/o EPEL:
# - mscgen 
# - astyle-devel
%ifarch x86_64
# Additional dependencies for building pmem based backends
# BuildRequires:	libpmemblk-devel
%endif

# SPDK runtime dependencies
Requires:	libibverbs >= 41mlnx1-OFED.4.4
Requires:	librdmacm  >= 41mlnx1-OFED.4.2
# Requires:	libibverbs >= 20.0-3.el7
# Requires:	librdmacm  >= 20.0-3.el7
Requires:	python, sg3_utils
# Requires:	avahi
Requires:   libhugetlbfs-utils

%description
The Storage Performance Development Kit (SPDK) provides a set of tools and
libraries for writing high performance, scalable, user-mode storage
applications.

%prep
%setup -q
tar zxf %{SOURCE1}
tar zxf %{SOURCE2}
# test -e ./dpdk/config/common_linuxapp

%build
./configure --with-rdma --without-pmdk \
	--disable-coverage --disable-debug \
	--prefix=/usr
# SPDK make
make %{?_smp_mflags}

# make docs?

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sbindir}
install -p -m 755 app/nvmf_tgt/nvmf_tgt %{buildroot}/%{_sbindir}
install -p -m 755 app/spdk_tgt/spdk_tgt %{buildroot}/%{_sbindir}
install -p -m 755 app/vhost/vhost %{buildroot}/%{_sbindir}
install -p -m 755 app/iscsi_tgt/iscsi_tgt %{buildroot}/%{_sbindir}
install -p -m 755 app/iscsi_top/iscsi_top %{buildroot}/%{_bindir}
install -p -m 755 app/trace/spdk_trace %{buildroot}/%{_bindir}
install -p -m 755 examples/nvme/perf/perf %{buildroot}/%{_bindir}/nvme-perf
install -p -m 755 contrib/setup_nvmf_tgt.py %{buildroot}/%{_sbindir}
install -p -m 755 contrib/setup_hugepages.sh %{buildroot}/%{_sbindir}
if [ -e contrib/nvmf_tgt.service ] ; then
  mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
  install -p -m 644 contrib/nvmf_tgt.service %{buildroot}%{_sysconfdir}/systemd/system
fi
if [ -e contrib/nvmf_tgt-default ] ; then
  mkdir -p %{buildroot}%{_sysconfdir}/default
  install -p -m 644 contrib/nvmf_tgt-default %{buildroot}%{_sysconfdir}/default/nvmf_tgt
fi
if [ -e contrib/nvmf_tgt.conf.example ] ; then
  mkdir -p %{buildroot}%{_sysconfdir}/spdk
  install -p -m 644 contrib/nvmf_tgt.conf.example %{buildroot}%{_sysconfdir}/spdk/nvmf_tgt.conf
fi
# Install SPDK rpc services
mkdir -p %{buildroot}/%{_libdir}/python2.7/site-packages/rpc/
install -p -m 644 scripts/rpc/* %{buildroot}/%{_libdir}/python2.7/site-packages/rpc/
install -p -m 755 scripts/rpc.py %{buildroot}/%{_bindir}/spdk_rpc.py
#mkdir -p %{buildroot}/%{_sysconfdir}/avahi/services/
#install -p -m 644 contrib/avahi-spdk.service %{buildroot}/%{_sysconfdir}/avahi/services/spdk.service

%files
%{_sbindir}/*
%{_bindir}/*
%{_sysconfdir}/systemd/system/nvmf_tgt.service
# %{_sysconfdir}/avahi/services/spdk.service
%{_libdir}/python2.7/site-packages/rpc/
%config(noreplace) %{_sysconfdir}/default/nvmf_tgt
%config(noreplace) %{_sysconfdir}/spdk/*
%doc README.md LICENSE

%post
case "$1" in
1) # install
	systemctl daemon-reload
#	systemctl restart avahi-daemon || true
	;;
2) # upgrade
	systemctl daemon-reload
#	systemctl restart avahi-daemon || true
	;;
esac

%changelog
* Fri Nov 16 2018 Yuriy Shestakov <yuriis@mellanox.com>
- build in a Docker image with upstream rdma-core libs
- packaged v18.10

* Wed May 16 2018 Yuriy Shestakov <yuriis@mellanox.com>
- Initial packaging

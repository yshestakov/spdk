# Copyright (c) 2018-2020, Mellanox Technologies. All rights reserved.

%define scm_version 20.01
%define unmangled_version %{scm_version}
%if "%{?_rev:1}" == ""
%define scm_rev 1
%else
%define scm_rev %{_rev}
%endif
Epoch: 0

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
Source3:	spdk-isa-l-%{version}.tar.gz
Source4:	spdk-ocf-%{version}.tar.gz

%define package_version %{epoch}:%{version}-%{release}
%define install_datadir %{buildroot}/%{_datadir}/%{name}
%define install_sbindir %{buildroot}/%{_sbindir}
%define install_bindir %{buildroot}/%{_bindir}
%define install_docdir %{buildroot}/%{_docdir}/%{name}

# It is somewhat hard to get SPDK RPC working with python 2.7
# Distros that don't support python3 will use python2
%if "%{dist}" == ".el7" || "%{dist}" == ".el7.centos" || "%{dist}" == ".el7.centos.a"
# So, let's switch to Python36 from IUS repo - https://github.com/iusrepo/python36
  %define use_python python3.6
  %define python_ver 3.6
%else
  # on Fedora 28+ we have python3 == 3.7
  %define use_python python3
  %define python_ver 3.7
%endif

ExclusiveArch: x86_64 aarch64
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
BuildRequires: graphviz
BuildRequires: numactl-devel
BuildRequires: libiscsi-devel

# SPDK build dependencies
BuildRequires:	git make gcc gcc-c++
BuildRequires:	CUnit-devel, libaio-devel, openssl-devel, libuuid-devel 
BuildRequires:	libiscsi-devel
BuildRequires:  lcov, clang-analyzer
# Additional dependencies for SPDK CLI 
BuildRequires:	python3-pep8 python3-configshell
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

# Build python36 from IUS repo and install on CentOS/7
# -- https://github.com/iusrepo/python36/blob/master/python36.spec
Requires: python36

# SPDK runtime dependencies
#Requires:	libibverbs >= 41mlnx1-OFED.4.4
#Requires:	librdmacm  >= 41mlnx1-OFED.4.2
#Requires:	libibverbs >= 23.0-1.el7
#Requires:	librdmacm  >= 23.0-1.el7
Requires:	libibverbs
Requires:	librdmacm 
Requires:	sg3_utils
# Requires:	avahi
Requires:   libhugetlbfs-utils
%if "%{use_python}" == "python36"
  Requires: %{name}%{?_isa} = %{package_version} python36 
%else
  Requires: %{name}%{?_isa} = %{package_version} python3 python3-configshell python3-pexpect
%endif

%description
The Storage Performance Development Kit (SPDK) provides a set of tools and
libraries for writing high performance, scalable, user-mode storage
applications.

%global debug_package %{nil}

%prep
%setup -q
tar zxf %{SOURCE1}
tar zxf %{SOURCE2}
tar zxf %{SOURCE3}
tar zxf %{SOURCE4}
# test -e ./dpdk/config/common_linuxapp

%build
sed -i 's#CONFIG_PREFIX="/usr/local"#CONFIG_PREFIX="/usr"#' CONFIG
./configure \
	--prefix=/usr \
	--disable-coverage \
         --enable-debug \
	--disable-tests \
	--without-crypto \
	--without-fio \
	--with-vhost \
	--without-pmdk \
	--without-vpp \
	--without-rbd \
	--with-rdma \
	--without-vtune 
	# --with-iscsi-initiator
	#--with-shared 
# SPDK make
make %{?_smp_mflags}

# make docs?

%install
mkdir -p %{install_bindir}
mkdir -p %{install_sbindir}
install -p -m 755 app/nvmf_tgt/nvmf_tgt %{install_sbindir}
install -p -m 755 app/spdk_tgt/spdk_tgt %{install_sbindir}
install -p -m 755 app/vhost/vhost %{install_sbindir}
install -p -m 755 app/iscsi_tgt/iscsi_tgt %{install_sbindir}
install -p -m 755 app/iscsi_top/iscsi_top %{install_bindir}
install -p -m 755 app/trace/spdk_trace %{install_bindir}
install -p -m 755 app/spdk_lspci/spdk_lspci %{install_bindir}
install -p -m 755 app/trace_record/spdk_trace_record %{install_bindir}
install -p -m 755 examples/nvme/perf/perf %{install_sbindir}/nvme-perf
install -p -m 755 examples/nvme/identify/identify %{install_sbindir}/nvme-identify
install -p -m 755 examples/nvme/nvme_manage/nvme_manage %{install_sbindir}/
install -p -m 755 examples/blob/cli/blobcli %{install_sbindir}/
install -p -m 755 contrib/setup_nvmf_tgt.py %{install_sbindir}
install -p -m 755 contrib/setup_vhost.py %{install_sbindir}
install -p -m 755 contrib/vhost_add_config.sh %{install_sbindir}
install -p -m 755 contrib/setup_hugepages.sh %{install_sbindir}
systemd_dir=${RPM_BUILD_ROOT}%{_prefix}/lib/systemd/system
mkdir -p ${systemd_dir}
mkdir -p %{buildroot}%{_sysconfdir}/default
mkdir -p %{buildroot}%{_sysconfdir}/spdk
mkdir -p %{install_datadir}
install -p -m 644 include/spdk/pci_ids.h %{install_datadir}
install -p -m 644 scripts/common.sh %{install_datadir}
install -p -m 755 scripts/setup.sh %{install_datadir}
# install -p -m 755 contrib/arp_fixup.sh %{install_sbindir}

for fn in nvmf_tgt vhost spdk_tgt ; do
  if [ -e contrib/$fn.service ] ; then
    install -p -m 644 contrib/$fn.service ${systemd_dir}
  fi
  if [ -e contrib/$fn-default ] ; then
    install -p -m 644 contrib/$fn-default %{buildroot}%{_sysconfdir}/default/$fn
  fi
  if [ -e contrib/$fn.conf.example ] ; then
    install -p -m 644 contrib/$fn.conf.example %{buildroot}%{_sysconfdir}/spdk/
  fi
done
# Install SPDK rpc services
if [ -e %{_libdir}/python%{python_ver} ] ; then
    mkdir -p %{buildroot}/%{_libdir}/python%{python_ver}/site-packages/rpc/
    install -p -m 644 scripts/rpc/* %{buildroot}/%{_libdir}/python%{python_ver}/site-packages/rpc/
fi
install -p -m 755 scripts/rpc.py %{install_bindir}/spdk_rpc.py
sed -i -e 's!/usr/bin/env python3$!/usr/bin/python'%{python_ver}'!' %{install_bindir}/spdk_rpc.py

%files
%{_sbindir}/*
%{_bindir}/*
%{_prefix}/lib/systemd/system/*.service
%{_libdir}/*
%{_datadir}/*
%config(noreplace) %{_sysconfdir}/default/*
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
* Tue Jan 28 2020 Yuriy Shestakov <yuriis@mellanox.com>
- ported to v20.01 pre-release

* Wed Aug  7 2019 Yuriy Shestakov <yuriis@mellanox.com>
- ported to v19.07 release

* Mon Jul 15 2019 Yuriy Shestakov <yuriis@mellanox.com>
- ported to v19.04.1 release

* Thu May  2 2019 Yuriy Shestakov <yuriis@mellanox.com>
- ported to v19.04 release

* Thu Apr 11 2019 Yuriy Shestakov <yuriis@mellanox.com>
- added vhost config/service definition
- packaged v19.04-pre

* Fri Nov 16 2018 Yuriy Shestakov <yuriis@mellanox.com>
- build in a Docker image with upstream rdma-core libs
- packaged v18.10

* Wed May 16 2018 Yuriy Shestakov <yuriis@mellanox.com>
- Initial packaging

%define sblim_testsuite_version 1.2.4
%define provider_dir %{_libdir}/cmpi
%define tog_pegasus_version 2:2.6.1-1

Name:           sblim-gather
Version:        2.2.1
Release:        2%{?dist}
Summary:        SBLIM Gatherer

Group:          Applications/System
License:        CPL
URL:            http://sourceforge.net/projects/sblim/
Source0:        http://downloads.sourceforge.net/project/sblim/%{name}/%{version}/%{name}-%{version}.tar.bz2
Source1:        gather-config.h.prepend
Source2:        gather-config.h
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: sblim-cmpi-devel
BuildRequires: sblim-cmpi-base-devel
BuildRequires: tog-pegasus-devel >= %{tog_pegasus_version}
BuildRequires: libsysfs-devel
BuildRequires: libvirt-devel
Requires:      tog-pegasus >= %{tog_pegasus_version}

%description
Standards Based Linux Instrumentation for Manageability
Performance Data Gatherer Base.
This package contains the agents and control programs for gathering
and providing performance data.

%package        provider
Summary:        SBLIM Gatherer Provider
Group:          Applications/System
BuildRequires:  tog-pegasus-devel >= %{tog_pegasus_version}
Requires:       %{name} = %{version}-%{release}
Requires:       sblim-cmpi-base
Requires:       tog-pegasus

%description    provider
The CIM (Common Information Model) Providers for the
SBLIM (Standards Based Linux Instrumentation for Manageability)
Gatherer.

%package        devel
Summary:        SBLIM Gatherer Development Support
Group:          Development/Libraries
BuildRequires:  tog-pegasus-devel >= %{tog_pegasus_version}
Requires:       %{name} = %{version}-%{release}
Requires:       tog-pegasus

%description    devel
This package is needed to develop new plugins for the
SBLIM (Standards Based Linux Instrumentation for Manageability)
Gatherer.

%package        test
Summary:        SBLIM Gatherer Testcase Files
Group:          Applications/System
BuildRequires:  tog-pegasus-devel >= %{tog_pegasus_version}
Requires:       %{name}-provider = %{version}-%{release}
Requires:       sblim-testsuite
Requires:       tog-pegasus

%description    test
Gatherer Testcase Files for the
SBLIM (Standards Based Linux Instrumentation for Manageability)
Testsuite

%prep
%setup -q

%build
%ifarch s390 s390x ppc ppc64
export CFLAGS="$RPM_OPT_FLAGS -fsigned-char -fno-strict-aliasing"
%else
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
export CXXFLAGS="$CFLAGS"
%configure TESTSUITEDIR=%{_datadir}/sblim-testsuite \
        CIMSERVER=pegasus \
        PROVIDERDIR=%{provider_dir}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*a
rm -f $RPM_BUILD_ROOT/%{provider_dir}/*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/gather/*plug/*a

# Install a redirection so that the arch-specific autoconf stuff continues to
# work but doesn't create multilib conflicts.
cat %{SOURCE1} \
        $RPM_BUILD_ROOT/%{_includedir}/gather/gather-config.h > \
        $RPM_BUILD_ROOT/%{_includedir}/gather/gather-config-%{_arch}.h
chmod 644 $RPM_BUILD_ROOT/%{_includedir}/gather/gather-config.h
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/%{_includedir}/gather/

# shared libraries
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/cmpi" > $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%config(noreplace) %{_sysconfdir}/init.d/gatherer
%docdir %{_datadir}/doc/%{name}-%{version}
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/doc/%{name}-%{version}
%{_localstatedir}/run/gather
%{_libdir}/lib[^O]*.so.*
%dir %{_libdir}/gather
%{_libdir}/gather/mplug
%{_libdir}/gather/rplug

%files provider
%defattr(-,root,root,-)
%{_libdir}/gather/cplug
%{_libdir}/libOSBase_MetricUtil.so
%{_libdir}/cmpi
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib[^O]*.so
%{_includedir}/gather

%files test
%defattr(-,root,root,-)
%{_datadir}/sblim-testsuite/cim/Linux*
%{_datadir}/sblim-testsuite/system/linux/Linux*
%{_datadir}/sblim-testsuite/system/linux/gather-systemname.sh
%{_datadir}/sblim-testsuite/test-gather.sh

%define GATHER_SCHEMA %{_datadir}/%{name}/Linux_Metric.mof %{_datadir}/%{name}/Linux_IPProtocolEndpointMetric.mof %{_datadir}/%{name}/Linux_LocalFileSystemMetric.mof %{_datadir}/${name}/Linux_NetworkPortMetric.mof %{_datadir}/%{name}/Linux_OperatingSystemMetric.mof %{_datadir}/%{name}/Linux_ProcessorMetric.mof %{_datadir}/%{name}/Linux_UnixProcessMetric.mof %{_datadir}/%{name}/Linux_XenMetric.mof %{_datadir}/%{name}/Linux_zECKDMetric.mof %{_datadir}/%{name}/Linux_zCECMetric.mof %{_datadir}/%{name}/Linux_zLPARMetric.mof %{_datadir}/%{name}/Linux_zCHMetric.mof
%define GATHER_REGISTRATION %{_datadir}/%{name}/Linux_IPProtocolEndpointMetric.registration %{_datadir}/%{name}/Linux_LocalFileSystemMetric.registration %{_datadir}/%{name}/Linux_Metric.registration %{_datadir}/%{name}/Linux_NetworkPortMetric.registration %{_datadir}/%{name}/Linux_OperatingSystemMetric.registration %{_datadir}/%{name}/Linux_ProcessorMetric.registration %{_datadir}/%{name}/Linux_UnixProcessMetric.registration %{_datadir}/%{name}/Linux_XenMetric.registration %{_datadir}/%{name}/Linux_zECKDMetric.registration %{_datadir}/%{name}/Linux_zCECMetric.registration %{_datadir}/%{name}/Linux_zLPARMetric.registration %{_datadir}/%{name}/Linux_zCHMetric.registration

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%pre provider
if [ $1 -gt 1 ]
then
  %{_datadir}/%{name}/provider-register.sh -t pegasus -d \
        -r %{GATHER_REGISTRATION} -m %{GATHER_SCHEMA} > /dev/null 2>&1 || :;
  # don't let registration failure when server not running fail upgrade!
fi

%post provider
/sbin/ldconfig
if [ $1 -ge 1 ]
then
  %{_datadir}/%{name}/provider-register.sh -t pegasus \
        -r %{GATHER_REGISTRATION} -m %{GATHER_SCHEMA} > /dev/null 2>&1 || :;
  # don't let registration failure when server not running fail install!
fi

%preun provider
# Deregister only if not upgrading 
if [ $1 -eq 0 ]
then
  %{_datadir}/%{name}/provider-register.sh -t pegasus -d \
        -r %{GATHER_REGISTRATION} -m %{GATHER_SCHEMA} > /dev/null 2>&1 || :;
  # don't let registration failure when server not running fail erase!
fi

%postun provider -p /sbin/ldconfig

%changelog
* Mon Jun 21 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.1-2
- Add -fno-strict-aliasing

* Mon Jun  7 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.1-1
- Update to sblim-gather-2.2.1

* Tue Oct 13 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.9-1
- Initial support

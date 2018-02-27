#
# spec file for package lrbd
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/


Summary: lrbd
Name: lrbd
Version: 1.6
Release: 0
License: LGPL-2.1+ 
Group: System Environment/Base
Distribution: SUSE
URL: http://bugs.opensuse.org
Source0: lrbd-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
Requires: python-netifaces
Requires: python-rados
Requires: python-rbd
Requires: ceph-common
Requires: targetcli-rbd
Summary: Configures iSCSI access to Ceph rbd images

%description
This utility creates, modifies and retrieves a centralized, configuration from 
Ceph for configuring iSCSI access on a host.

%prep


%build
%__tar xvzf %{SOURCE0}
%__rm -f lrbd/man/*.gz
%__gzip lrbd/man/lrbd.*

%install
%define _samples %{buildroot}%{_docdir}/%{name}/samples
mkdir -p %{buildroot}/var/adm/fillup-templates
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_docdir}/%{name}/samples
mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_sbindir}

cd lrbd
install -m 555 lrbd %{buildroot}%{_sbindir}
install -m 644 man/lrbd.conf.5.gz %{buildroot}%{_mandir}/man5
install -m 644 man/lrbd.8.gz %{buildroot}%{_mandir}/man8

install -m 644 sysconfig/lrbd %{buildroot}/var/adm/fillup-templates/sysconfig.lrbd
install -m 644 systemd/lrbd.service %{buildroot}%{_unitdir}
ln -sf %{_sbindir}/service %{buildroot}%_sbindir/rclrbd
install -m 644 README.migration %{buildroot}%{_docdir}/%{name}
install -m 644 LICENSE %{buildroot}%{_docdir}/%{name}

install -m 644 samples/acls+discovery.json  %{_samples}
install -m 644 samples/acls+discovery+mutual.json  %{_samples}
install -m 644 samples/acls.json  %{_samples}
install -m 644 samples/acls+mutual+discovery.json  %{_samples}
install -m 644 samples/acls+mutual+discovery+mutual.json  %{_samples}
install -m 644 samples/acls+mutual.json  %{_samples}
install -m 644 samples/complete.json  %{_samples}
install -m 644 samples/no_authentication+explicit.json  %{_samples}
install -m 644 samples/no_authentication.json  %{_samples}
install -m 644 samples/plain.json  %{_samples}
install -m 644 samples/simple.json  %{_samples}
install -m 644 samples/tpg+discovery.json  %{_samples}
install -m 644 samples/tpg+discovery+mutual.json  %{_samples}
install -m 644 samples/tpg.json  %{_samples}
install -m 644 samples/tpg+mutual+discovery.json  %{_samples}
install -m 644 samples/tpg+mutual+discovery+mutual.json  %{_samples}
install -m 644 samples/tpg+mutual.json  %{_samples}
install -m 644 samples/2gateways+2images+no_authentication.json %{_samples}
install -m 644 samples/2gateways+2portals+2images+isolated+no_authentication.json %{_samples}
install -m 644 samples/2gateways+2portals+2images+no_authentication.json %{_samples}
install -m 644 samples/2gateways+2portals+no_authentication.json %{_samples}
install -m 644 samples/2gateways+no_authentication.json %{_samples}
install -m 644 samples/2plain+3gateways+2portals+2images+isolated+no_authentication.json %{_samples}
install -m 644 samples/3gateways+2portals+2images+isolated+no_authentication.json %{_samples}
install -m 644 samples/3gateways+no_authentication.json %{_samples}
install -m 644 samples/plain+2gateways+2portals+2images+isolated+combined.json %{_samples}
install -m 644 samples/2gateways+tpg+identified.json %{_samples}
install -m 644 samples/3gateways+tpg+identified.json %{_samples}
install -m 644 samples/3gateways+80targets+no_authentication.json %{_samples}
install -m 644 samples/tpg+identified+mutual+discovery+mutual.json %{_samples}
install -m 644 samples/tpg+identified.json %{_samples}
install -m 644 samples/2gateways+2images+2targets+no_authentication.json %{_samples}
install -m 644 samples/2gateways+2images+assigned_lun+no_authentication.json %{_samples}
install -m 644 samples/plain+uuid.json %{_samples}
install -m 644 samples/plain+wwn_generate.json %{_samples}
install -m 644 samples/nonstandard_port+no_authentication.json %{_samples}
install -m 644 samples/plain+attributes.json %{_samples}
install -m 644 samples/plain+rbd_name.json %{_samples}
install -m 644 samples/plain+retries.json %{_samples}
install -m 644 samples/README.NEW %{_samples}


%pre
if [ "$1" == "2" ]
then
  # Upgrade from 1.0
  grep -q wwn_generate %{_sbindir}/lrbd
  if [ $? -ne 0 ]
  then
    cat > %{_localstatedir}/lib/misc/lrbd.disabled <<EOF
Please migrate your existing configuration:
lrbd -m 1.0 > /tmp/lrbd.conf-migrated
lrbd -f /tmp/lrbd.conf-migrated
rm -f %{_localstatedir}/lib/misc/lrbd.disabled

See %{_docdir}/%{name}/README.migration for details.
EOF
  fi
fi
%service_add_pre lrbd.service 

%post
%service_add_post lrbd.service 
%fillup_and_insserv



%preun
%service_del_preun lrbd.service 

%postun
export DISABLE_RESTART_ON_UPDATE=yes
%service_del_postun lrbd.service 

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
/var/adm/fillup-templates/sysconfig.lrbd
%{_sbindir}/lrbd
%{_sbindir}/rclrbd
%{_mandir}/man5/lrbd.conf.5.gz
%{_mandir}/man8/lrbd.8.gz
%{_unitdir}/lrbd.service
%dir %attr(-, root, root) %{_docdir}/%{name}
%dir %attr(-, root, root) %{_docdir}/%{name}/samples
%{_docdir}/%{name}/README.migration
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/samples/*

%changelog

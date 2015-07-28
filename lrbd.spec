Summary: lrbd
Name: lrbd
Version: 0.9.0
Release: 0
License: LGPL-2.1+ 
Distribution: SUSE
URL: https://github.com/swiftgist/lrbd
Source0: lrbd-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
Summary: Configures iSCSI access to Ceph rbd images

%description
This utility creates, modifies and retrieves the configuration from Ceph for 
applying targetcli commands to a host.  

%prep


%build
tar xvzf %{SOURCE0}
rm -f lrbd/man/*.gz
%__gzip lrbd/man/lrbd.*

%install
%define _samples %{buildroot}/%{_docdir}/%{name}/samples
mkdir -p %{buildroot}/var/adm/fillup-templates
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/%{_docdir}/%{name}/samples
mkdir -p %{buildroot}/usr/share/man/man8
mkdir -p %{buildroot}/usr/sbin

cd lrbd
install -m 555 lrbd %{buildroot}/usr/sbin
install -m 644 man/lrbd.8.gz %{buildroot}/%{_mandir}/man8

install -m 644 sysconfig/lrbd %{buildroot}/var/adm/fillup-templates/sysconfig.lrbd
install -m 644 systemd/lrbd.service %{buildroot}/usr/lib/systemd/system
ln -sf %_sbindir/service %{buildroot}%_sbindir/rclrbd

install -m 644 samples/acls+discovery.json  %{_samples}
install -m 644 samples/acls+discovery+mutual.json  %{_samples}
install -m 644 samples/acls.json  %{_samples}
install -m 644 samples/acls+mutual+discovery.json  %{_samples}
install -m 644 samples/acls+mutual+discovery+mutual.json  %{_samples}
install -m 644 samples/acls+mutual.json  %{_samples}
install -m 644 samples/complete.json  %{_samples}
install -m 644 samples/no_authentication+explicit.json  %{_samples}
install -m 644 samples/no_authentication.json  %{_samples}
install -m 644 samples/tpg+discovery.json  %{_samples}
install -m 644 samples/tpg+discovery+mutual.json  %{_samples}
install -m 644 samples/tpg.json  %{_samples}
install -m 644 samples/tpg+mutual+discovery.json  %{_samples}
install -m 644 samples/tpg+mutual+discovery+mutual.json  %{_samples}
install -m 644 samples/tpg+mutual.json  %{_samples}


%pre
%service_add_pre lrbd.service 

%post
%service_add_post lrbd.service 
%fillup_and_insserv

%preun
%service_del_preun lrbd.service 

%postun
%service_del_postun lrbd.service 

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
/var/adm/fillup-templates/sysconfig.lrbd
/usr/sbin/lrbd
/usr/sbin/rclrbd
%{_mandir}/man8/lrbd.8.gz
/usr/lib/systemd/system/lrbd.service
%dir %attr(-, root, root) %{_docdir}/%{name}
%dir %attr(-, root, root) %{_docdir}/%{name}/samples
%{_docdir}/%{name}/samples/*

%changelog

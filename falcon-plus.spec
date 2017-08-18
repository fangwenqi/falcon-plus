Name:           falcon-plus
Version:        0.2.0
Release:        6%{?dist}
Summary:        An open-source and enterprise-level monitoring system which is designed for modern distributed systems
Group:          Applications/Internet
License:        Apache
URL:            https://github.com/open-falcon/falcon-plus
Source:         %{name}-%{version}.tgz
Source1:        %{name}-wdconfig.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  go >= 1.4.2

%define __spec_install_post %{nil}
%define debug_package %{nil}

%define falcon_user falcon

%define packname open-falcon
%define instdir /data/falcon

%define falcon_modules 'agent aggregator alarm api gateway graph hbs judge nodata transfer'

%description
An open-source and enterprise-level monitoring system which is designed for modern distributed systems.

%prep
%setup -T -c -n go/src/github.com/open-falcon/falcon-plus
tar --strip-components=1 -x -f %{SOURCE0}
tar --strip-components=1 -x -f %{SOURCE1}

%build
export GOPATH=%{_builddir}/go
make clean
cp -pr %{_builddir}/go/src/github.com/open-falcon/falcon-plus/vendor/golang.org %{_builddir}/go/src/
make
make pack

%install
rm -rf %{buildroot}
mkdir out
tar -x -f %{packname}-v%{version}.tar.gz -C out

install -d %{buildroot}/usr/local/bin
install out/open-falcon  %{buildroot}/usr/local/bin/
for i in `echo %{falcon_modules}`; do
    install -d %{buildroot}/var/log/falcon/$i
    install -d %{buildroot}/etc/falcon/$i
    install out/$i/config/cfg.json %{buildroot}/etc/falcon/$i/
    install out/$i/bin/falcon-$i %{buildroot}/usr/local/bin/
done

install -d %{buildroot}/var/lib/falcon/agent/
install -d %{buildroot}/var/lib/falcon/agent/plugins
cp -pr out/agent/public %{buildroot}/var/lib/falcon/agent/
install wdconfig/agent.cfg.json %{buildroot}/etc/falcon/agent/cfg.json

install -d %{buildroot}/var/lib/falcon/api/
cp -pr out/api/data %{buildroot}/var/lib/falcon/api/

install -d %{buildroot}/var/lib/falcon/graph/
cp -pr out/graph/data %{buildroot}/var/lib/falcon/graph/

install -d %{buildroot}/var/run/falcon/

install -d %{buildroot}/etc/rc.d/init.d/
install -v init.d/* %{buildroot}/etc/rc.d/init.d/
rm -v %{buildroot}/etc/rc.d/init.d/falcon_dashboard

sed -i -e 's@"storage.*@"storage": "/var/lib/falcon/graph/data/6070"@g' %{buildroot}/etc/falcon/graph/cfg.json
sed -i -e 's@"metric_list_file.*@"metric_list_file": "/var/lib/falcon/api/data/metric",@g' %{buildroot}/etc/falcon/api/cfg.json

%clean
rm -rf %{buildroot}

%files
%defattr(-,%{falcon_user},%{falcon_user},-)
/usr/local/bin/open-falcon

%pre
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}


%define falcon_mod agent

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/run/falcon
/var/lib/falcon/agent/public
/var/lib/falcon/agent/plugins
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%define falcon_mod aggregator

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/run/falcon
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%define falcon_mod alarm

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/run/falcon
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%define falcon_mod api

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/lib/falcon/%{falcon_mod}
/var/lib/falcon/%{falcon_mod}/data
/var/run/falcon
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%define falcon_mod gateway

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/run/falcon
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%define falcon_mod graph

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/lib/falcon/%{falcon_mod}
/var/lib/falcon/%{falcon_mod}/data
/var/run/falcon
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%define falcon_mod hbs

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/run/falcon
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%define falcon_mod judge

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/run/falcon
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%define falcon_mod nodata

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/run/falcon
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%define falcon_mod transfer

%package %{falcon_mod}
Summary: falcon-plus %{falcon_mod}
%description %{falcon_mod}
falcon-plus %{falcon_mod} module
%files %{falcon_mod}
%defattr(-,falcon,falcon,-)
/etc/falcon/%{falcon_mod}
/usr/local/bin/falcon-%{falcon_mod}
/var/log/falcon/%{falcon_mod}
/var/run/falcon
%attr(755,root,root) /etc/rc.d/init.d/falcon_%{falcon_mod}

%pre %{falcon_mod}
getent group %{falcon_user} > /dev/null || groupadd -r %{falcon_user}
getent passwd %{falcon_user} > /dev/null || \
    useradd -r -g %{falcon_user} -d /var/lib/%{falcon_user} -s /sbin/nologin \
        -c "Falcon Monitoring System" %{falcon_user}

%post %{falcon_mod}
chkconfig --add falcon_%{falcon_mod}

%preun %{falcon_mod}
if [ "$1" = 0 ]; then
    service falcon_%{falcon_mod} stop
    chkconfig --del falcon_%{falcon_mod}
fi
:


%changelog
* Fri Jun 30 2017 Fang Wenqi <fangwenqi@wanda.cn> 0.2.0-6
- agent: monut point filter "/var/lib/docker" and "net:["

* Thu Jun 29 2017 Fang Wenqi <fangwenqi@wanda.cn> 0.2.0-5
- agent: run as user falcon instead of root for agent service

* Wed Jun 28 2017 Fang Wenqi <fangwenqi@wanda.cn> 0.2.0-4
- Add agent config for production

* Mon Jun 26 2017 Fang Wenqi <fangwenqi@wanda.cn> 0.2.0-3
- Merge various branch and upstream v0.2.0 release: support etcd, health-check, email content.

* Tue Jun 20 2017 Fang Wenqi <fangwenqi@wanda.cn> 0.2.0-2
- Install the module files in various directories according to the Linux convention.

* Mon Jun 19 2017 Fang Wenqi <fangwenqi@wanda.cn> 0.2.0-1
- Initial build.

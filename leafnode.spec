Summary:	NNTP server for small sites
Summary(pl):	Serwer NNTP dla ma�ych host�w
Name:		leafnode
Version:	1.9.18
Release:	1
License:	Distributable
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://wpxx02.toxi.uni-wuerzburg.de/pub/%{name}-%{version}.tar.gz
Source1:	%{name}.texpire
Source2:	%{name}.config
Source3:	%{name}.filters
Source4:	%{name}.rc-inetd
Patch0:		%{name}-noroot.patch
Patch1:		%{name}-use_system_pcre.patch
URL:		http://www.leafnode.org/
Requires:	inetdaemon
Prereq:		rc-inetd
Provides:	nntpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Leafnode is a USENET package intended for small sites, where there are
few users and little disk space, but where a large number of groups is
desired.

The design of leafnode is intended to self-repair after problems, and
to require no manual maintenance.

%description -l pl
Leafnode to serwer USENET przeznaczony dla ma�ych host�w, gdzie jest
niewielu u�ytkownik�w i ma�o miejsca na dyskach ale du�a liczba grup
usenet jest po��dana.

leafnode jest zaprojektowany jako samo-naprawiaj�cy si� i nie
wymagaj�cy r�cznego zarz�dzania.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
autoconf
%configure \
	--with-ipv6

%{__make} LIBDIR=%{_sysconfdir}/%{name} \
	LOCKFILE=%{_var}/lock/news/fetch.lck \
	DEBUG="%{!?debug:$RPM_OPT_FLAGS}%{?debug:-O0 -g}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{{cron.daily,%{_name}},sysconfig/rc-inetd}

%{__make} install \
	PREFIX_USR=$RPM_BUILD_ROOT%{_prefix} \
	PREFIX_VAR=$RPM_BUILD_ROOT%{_var} \
	LIBDIR=$RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	LOCKFILE=$RPM_BUILD_ROOT%{_var}/lock/news/fetch.lck \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install %SOURCE1 $RPM_BUILD_ROOT/etc/cron.daily/texpire
install %SOURCE2 $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/config
install %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/filters
install %SOURCE4 $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/leafnode

gzip -9nf CHANGES README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc *.gz tools/archivefaq.pl update.sh
%attr(755,root,root) /etc/cron.daily/texpire
%attr(755,news,news) %dir %{_sysconfdir}/%{name}
%attr(600,news,news) %config %{_sysconfdir}/%{name}/config
%attr(600,news,news) %config %{_sysconfdir}/%{name}/filters
%attr(640,root,root) /etc/sysconfig/rc-inetd/leafnode
%attr(644,root,root) %{_mandir}/man*/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%attr(755,news,news) %dir  %{_var}/lock/news
%attr(2775,news,news) %dir %{_var}/spool/news
%attr(775,news,news) %dir  %{_var}/spool/news/*
%attr(775,news,news) %dir  %{_var}/spool/news/message.id/*

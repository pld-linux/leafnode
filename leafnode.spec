Summary:	NNTP server for small sites
Summary(pl):	Serwer NNTP dla ma³ych hostów
Name:		leafnode
Version:	1.9.9
Release:	1
URL:		http://wpxx02.toxi.uni-wuerzburg.de/~krasel/leafnode.html
Source0:	ftp://wpxx02.toxi.uni-wuerzburg.de/pub/%{name}-%{version}.tar.gz
Source1:	%{name}.texpire
Source2:	%{name}.config
Source3:	%{name}.filters
Source4:	%{name}.rc-inetd
Patch0:		%{name}-noroot.patch
#Patch1:	%{name}-headers.patch
#Patch2:	http://www.misiek.eu.org/ipv6/leafnode-1.9.4-ipv6fix-220899.patch.gz
Copyright:	distributable
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
group(pl):	Sieciowe/Serwery
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	nntpserver
Requires:	inetdaemon
Requires:	rc-inetd

%description
Leafnode is a USENET package intended for small sites, where there are
few users and little disk space, but where a large number of groups is
desired.

The design of leafnode is intended to self-repair after problems, and
to require no manual maintenance.

%description -l pl
Leafnode to serwer USENET przeznaczony dla ma³ych hostów, gdzie jest
niewielu u¿ytkowników i ma³o miejsca na dyskach ale du¿a liczba grup
usenet jest po¿±dana.

leafnode jest zaprojektowany jako samo-naprawiaj±cy siê i nie
wymagaj±cy rêcznego zarz±dzania.

%prep
%setup -q

%patch0 -p1

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS" ./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--with-ipv6

make libpcre.a 

make LIBDIR=%{_sysconfdir}/%{name} \
     LOCKFILE=%{_var}/lock/news/fetch.lck \
     DEBUG="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{{cron.daily,%{_name}},sysconfig/rc-inetd}

make PREFIX_USR=$RPM_BUILD_ROOT%{_prefix} \
     PREFIX_VAR=$RPM_BUILD_ROOT%{_var} \
LIBDIR=$RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
     LOCKFILE=$RPM_BUILD_ROOT%{_var}/lock/news/fetch.lck \
     MANDIR=$RPM_BUILD_ROOT%{_mandir} \
     install

install %SOURCE1 $RPM_BUILD_ROOT/etc/cron.daily/texpire
install %SOURCE2 $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/config
install %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/filters
install %SOURCE4 $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/leafnode

strip		$RPM_BUILD_ROOT{%{_bindir}/*,%{_sbindir}/*} || :
gzip -9nf -9nf	$RPM_BUILD_ROOT%{_mandir}/man*/* CHANGES INSTALL README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {CHANGES,INSTALL,README,TODO}.gz tools/archivefaq.pl update.sh
%attr(755,root,root) /etc/cron.daily/texpire
%attr(755,news,news) %dir %{_sysconfdir}/%{name}
%attr(600,news,news) %config %{_sysconfdir}/%{name}/config
%attr(600,news,news) %config %{_sysconfdir}/%{name}/filters
%attr(640,root,root) /etc/sysconfig/rc-inetd/leafnode
%attr(644,root,root) %{_mandir}/man*/*
%attr(750,root,root) %{_sbindir}/*
%attr(750,root,root) %{_bindir}/*
%attr(755,news,news) %dir  %{_var}/lock/news
%attr(2775,news,news) %dir  %{_var}/spool/news
%attr(775,news,news) %dir  %{_var}/spool/news/*
%attr(775,news,news) %dir  %{_var}/spool/news/message.id/*

Summary:	NNTP server for small sites
Summary(pl):	Serwer NNTP dla ma³ych hostów
Name:		leafnode
Version:	1.9.4
Release:	1
URL:		http://wpxx02.toxi.uni-wuerzburg.de/~krasel/leafnode.html
Source0:	ftp://wpxx02.toxi.uni-wuerzburg.de/pub/%{name}-%{version}.tar.gz
Source1:	leafnode.texpire
Source2:	leafnode.config
Source3:	leafnode.filters
Patch0:		leafnode-noroot.patch
Patch1:		leafnode-headers.patch
Patch2:		http://www.misiek.eu.org/ipv6/leafnode-1.9.4-ipv6fix-220899.patch.gz
Copyright:	distributable
Group:		Networking/Daemons
group(pl):	Sieciowe/Serwery
BuildRoot:	/tmp/%{name}-%{version}-root
Conflicts:	inn

%description
Leafnode is a USENET package intended for small sites, where
there are few users and little disk space, but where a large
number of groups is desired.

The  design  of  leafnode is intended to self-repair after
problems, and to require no manual maintenance.

%description -l pl
Leafnode to serwer USENET przeznaczony dla ma³ych hostów, gdzie
niewielu jest niewielu u¿ytkowników i ma³o miejsca na dyskach
ale du¿a liczba grup usenet jest po¿±dana.

leafnode jest zaprojektowany jako samo-naprawiaj±cy siê
i nie wymagaj±cy rêcznego zarz±dzania.

%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
autoconf
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--enable-ipv6

make libpcre.a CFLAGS="$RPM_OPT_FLAGS"

make LIBDIR=/etc/%{name} \
     LOCKFILE=%{_var}/lock/news/fetch.lck \
     DEBUG="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{cron.daily,%{_name}}

make PREFIX_USR=$RPM_BUILD_ROOT%{_prefix} \
     PREFIX_VAR=$RPM_BUILD_ROOT%{_var} \
     LIBDIR=$RPM_BUILD_ROOT/etc/%{name} \
     LOCKFILE=$RPM_BUILD_ROOT%{_var}/lock/news/fetch.lck \
     MANDIR=$RPM_BUILD_ROOT%{_mandir} \
     install

install %SOURCE1 $RPM_BUILD_ROOT/etc/cron.daily/texpire
install %SOURCE2 $RPM_BUILD_ROOT/etc/leafnode/config
install %SOURCE3 $RPM_BUILD_ROOT/etc/leafnode/filters

strip		$RPM_BUILD_ROOT{%{_bindir}/*,%{_sbindir}/*} || :
gzip -9nf	$RPM_BUILD_ROOT%{_mandir}/man*/* CHANGES INSTALL README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {CHANGES,INSTALL,README,TODO}.gz tools/archivefaq.pl update.sh
%attr(755,root,root)  /etc/cron.daily/texpire
%attr(755,news,news)  %dir /etc/%{name}
%attr(600,news,news)  %config /etc/%{name}/config
%attr(600,news,news)  %config /etc/%{name}/filters
%attr(644,root,root)  %{_mandir}/man*/*
%attr(750,news,news)  %{_sbindir}/*
%attr(750,news,news)  %{_bindir}/*
%attr(755,news,news)  %dir  %{_var}/lock/news
%attr(2775,news,news) %dir  %{_var}/spool/news
%attr(775,news,news)  %dir  %{_var}/spool/news/*
%attr(775,news,news)  %dir  %{_var}/spool/news/message.id/*

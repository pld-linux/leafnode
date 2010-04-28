Summary:	NNTP server for small sites
Summary(pl.UTF-8):	Serwer NNTP dla małych hostów
Summary(pt_BR.UTF-8):	Cliente / Servidor USENET para pequenos sites
Name:		leafnode
Version:	1.11.7
Release:	1
License:	distributable
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/leafnode/%{name}-%{version}.tar.bz2
# Source0-md5:	e5e8ac28386c59df0b14ddbfcbe78509
Source1:	%{name}.texpire
Source2:	%{name}.config
Source3:	%{name}.filters
Source4:	%{name}.rc-inetd
Patch0:		%{name}-config.patch
URL:		http://www.leafnode.org/
BuildRequires:	autoconf >= 2.54
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	inetdaemon
Requires:	rc-inetd
Provides:	nntpserver
Obsoletes:	leafnode+
Conflicts:	inn
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Leafnode is a USENET package intended for small sites, where there are
few users and little disk space, but where a large number of groups is
desired.

The design of leafnode is intended to self-repair after problems, and
to require no manual maintenance.

%description -l de.UTF-8
Leafnode ist ein offline-Newsserver, der vor allem für den typischen
Einzelnutzer-Rechner ohne permanente Internetanbindung geeignet ist.
Leafnode bezieht automatisch die Newsgroups, die der oder die Nutzer
regelmaessig lesen, vom Newsserver des Providers.

%description -l pl.UTF-8
Leafnode to serwer USENET przeznaczony dla małych hostów, gdzie jest
niewielu użytkowników i mało miejsca na dyskach ale duża liczba grup
usenet jest pożądana.

leafnode jest zaprojektowany jako samo-naprawiający się i nie
wymagający ręcznego zarządzania.

%description -l pt_BR.UTF-8
O Leafnode é um software desenvolvido para disponibilizar acesso à
USENET para pequenos sites rodando qualquer tipo de Unix, com pocas
dezenas de leitores e um pequeno link para a net.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
%configure \
	--with-ipv6 \
	--sysconfdir=%{_sysconfdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{cron.daily,%{name},sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_var}/lock/news \
	$RPM_BUILD_ROOT%{_var}/log/news

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/texpire
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/config
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/filters
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/leafnode

# unused stuff
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/Makefile.dist
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/config.example
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/filters.example

# daemontools stuff
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/UNINSTALL-daemontools
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/nntp.rules.dist
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/run.tcpd.dist
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/run.tcpserver.dist

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README tools/archivefaq.pl update.sh
%attr(755,root,root) /etc/cron.daily/texpire
%attr(755,news,news) %dir %{_sysconfdir}/%{name}
%attr(600,news,news) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/config
%attr(600,news,news) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/filters
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/leafnode
%{_mandir}/man*/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%attr(755,news,news) %dir  %{_var}/lock/news
%attr(2775,news,news) %dir %{_var}/spool/news
%attr(775,news,news) %dir  %{_var}/spool/news/*
%attr(775,news,news) %dir  %{_var}/spool/news/message.id
%attr(775,news,news) %dir  %{_var}/log/news

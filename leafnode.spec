Summary:	NNTP server for small sites
Summary(pl.UTF-8):	Serwer NNTP dla małych hostów
Summary(pt_BR.UTF-8):	Cliente / Servidor USENET para pequenos sites
Name:		leafnode
Version:	1.12.0
Release:	1
License:	distributable
Group:		Networking/Daemons
Source0:	https://downloads.sourceforge.net/leafnode/%{name}-%{version}.tar.xz
# Source0-md5:	0fe11436e77158b0cc03cd1808366d3c
Source1:	%{name}.texpire
Source2:	%{name}.config
Source3:	%{name}.filters
Source4:	%{name}.rc-inetd
Patch0:		%{name}-config.patch
URL:		https://www.leafnode.org/
BuildRequires:	autoconf >= 2.69
BuildRequires:	pcre2-8-devel >= 10.0
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	inetdaemon
Requires:	pcre2-8 >= 10.0
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
%patch -P0 -p1

%build
%{__autoconf}
%configure \
	--sysconfdir=%{_sysconfdir}/leafnode \
	--with-ipv6

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{cron.daily,%{name},sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_var}/lock/news \
	$RPM_BUILD_ROOT%{_var}/log/news

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/texpire
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/config
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/filters
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/leafnode

# unused stuff
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/config.example
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/filters.example

# daemontools stuff
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/UNINSTALL-daemontools

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
%attr(755,news,news) %dir %{_sysconfdir}/leafnode
%attr(600,news,news) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/leafnode/config
%attr(600,news,news) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/leafnode/filters
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/leafnode
%{_mandir}/man1/leafnode-version.1*
%{_mandir}/man1/newsq.1*
%{_mandir}/man8/applyfilter.8*
%{_mandir}/man8/checkgroups.8*
%{_mandir}/man8/fetchnews.8*
%{_mandir}/man8/leafnode.8*
%{_mandir}/man8/texpire.8*
%attr(755,root,root) %{_bindir}/leafnode-version
%attr(755,root,root) %{_bindir}/newsq
%attr(755,root,root) %{_sbindir}/applyfilter
%attr(755,root,root) %{_sbindir}/checkgroups
%attr(755,root,root) %{_sbindir}/fetchnews
%attr(755,root,root) %{_sbindir}/leafnode
%attr(755,root,root) %{_sbindir}/texpire
%attr(755,news,news) %dir  %{_var}/lock/news
%attr(775,news,news) %dir  %{_var}/log/news
%attr(2775,news,news) %dir %{_var}/spool/news
%attr(775,news,news) %dir  %{_var}/spool/news/failed.postings
%attr(775,news,news) %dir  %{_var}/spool/news/interesting.groups
%attr(775,news,news) %dir  %{_var}/spool/news/leaf.node
%attr(775,news,news) %dir  %{_var}/spool/news/message.id
%attr(775,news,news) %dir  %{_var}/spool/news/out.going
%attr(775,news,news) %dir  %{_var}/spool/news/temp.files

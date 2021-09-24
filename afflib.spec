# TODO:
# - build against system lzma if possible
# - some bundled qemu source?
#
# Conditional build:
%bcond_without	fuse		# FUSE support
%bcond_without	python		# Python support
%bcond_with	system_lzma	# building against system lzma instead of local copy
%bcond_without	static_libs	# static library
%bcond_without	s3		# Amazon S3 support
%bcond_without	qemu		# QEMU support
#
Summary:	Library to support the Advanced Forensic Format
Summary(pl.UTF-8):	Biblioteka do obsługi firmatu plików AFF (Advanced Forensic Format)
Name:		afflib
Version:	3.7.19
Release:	3
License:	BSD with advertising
Group:		Libraries
#Source0Download: https://github.com/sshock/AFFLIBv3/releases/
Source0:	https://github.com/sshock/AFFLIBv3/archive/v%{version}/AFFLIBv3-%{version}.tar.gz
# Source0-md5:	83b2b89e23090930905547e7e47f9e09
Patch0:		%{name}-no-libmd.patch
Patch1:		%{name}-x32-x64.patch
URL:		https://github.com/sshock/AFFLIBv3
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%if %{with s3}
BuildRequires:	curl-devel
BuildRequires:	expat-devel >= 1.95
%endif
BuildRequires:	intltool
%if %{with fuse}
BuildRequires:	libfuse3-devel
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
%if %{with system_lzma}
BuildRequires:	lzma-devel
%endif
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
%{?with_python:BuildRequires:	python-devel >= 2}
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AFF(R) is an open and extensible file format designed to store disk
images and associated metadata. afflib is library for support of the
Advanced Forensic Format (AFF).

%description -l pl.UTF-8
AFF(R) to otwarty i rozszerzalny format pliku zaprojektowany do zapisu
obrazów dysków i powiązanych metadanych. afflib to biblioteka do
obsługi formatu AFF (Advanced Forensic Format).

%package -n afftools
Summary:	Utilities for AFFLIB library
Summary(pl.UTF-8):	Narzędzia do biblioteki AFFLIB
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}

%description -n afftools
This package contains utilities for using AFFLIB library.

%description -n afftools -l pl.UTF-8
Ten pakiet zawiera narzędzia korzystające z biblioteki AFFLIB.

%package devel
Summary:	Development files for AFFLIB
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AFFLIB
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel

%description devel
This package contains the header files for developing applications
that use AFFLIB library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę AFFLIB.

%package static
Summary:	Static AFFLIB library
Summary(pl.UTF-8):	Statyczna biblioteka AFFLIB
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static AFFLIB library.

%description static -l pl.UTF-8
Statyczna biblioteka AFFLIB.

%package python
Summary:	Python bindings for AFFLIB
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki AFFLIB
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description python
These bindings currently support a read-only file-like interface to
AFFLIB and basic metadata accessor functions. The binding is not
currently complete.

%description python -l pl.UTF-8
Te wiązania obecnie obsługują zbliżony do plików interfejs tylko do
odczytu do biblioteki AFFLIB oraz podstawowe funkcje dostępu do
metadanych. Wiązania nie są jeszcze kompletne.

%prep:
%setup -q -n AFFLIBv3-%{version}
%patch0 -p1
%patch1 -p1

%if %{with system_lzma}
	# prevent internal lzma to be built - testing
	#rm -rf lzma443
%else
	#fix spurious permissions with lzma443
	find lzma443 -type f -exec chmod 0644 {} ';'
%endif

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable fuse} \
	%{__enable_disable python} \
	%{__enable_disable s3} \
	%{__enable_disable qemu}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%if %{with python}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGLIST.txt COPYING ChangeLog NEWS README doc/announce_2.2.txt
%attr(755,root,root) %{_libdir}/libafflib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libafflib.so.0

%files -n afftools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aff*
%{_mandir}/man1/aff*.1.*

%files devel
%defattr(644,root,root,755)
%doc doc/crypto_design.txt doc/crypto_doc.txt
%attr(755,root,root) %{_libdir}/libafflib.so
%{_includedir}/afflib
%{_pkgconfigdir}/afflib.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libafflib.a
%endif

%if %{with python}
%files python
%defattr(644,root,root,755)
%doc pyaff/README
%attr(755,root,root) %{py_sitedir}/pyaff.so
%{py_sitedir}/PyAFF-0.1-py*.egg-info
%endif

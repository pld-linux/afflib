# TODO:
# - build against system lzma if possible
# - some bundled qemu source?
#
# Conditional build:
%bcond_without	fuse		# without FUSE support
%bcond_without	python		# without Python support
%bcond_with	system_lzma	# building against system lzma instead of local copy
%bcond_without	static_libs	# don't build static libraries
%bcond_without	s3		# without Amazon S3
%bcond_without	qemu		# without QEMU support
#
Summary:	Library to support the Advanced Forensic Format
Name:		afflib
Version:	3.7.18
Release:	1
License:	BSD with advertising
Group:		Libraries
Source0:	https://github.com/sshock/AFFLIBv3/archive/v%{version}.tar.gz
# Source0-md5:	079f7ff418a853d5e7462d09113bbe2f
Patch0:		Sanity-check-size-passed-to-malloc.patch
Patch1:		%{name}-x32-x64.patch
URL:		https://github.com/sshock/AFFLIBv3
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with s3}
BuildRequires:	curl-devel
BuildRequires:	expat-devel
%endif
BuildRequires:	intltool
%if %{with fuse}
BuildRequires:	libfuse3-devel
%endif
BuildRequires:	libmd-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
%if %{with system_lzma}
BuildRequires:	lzma-devel
%endif
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AFF® is an open and extensible file format designed to store disk
images and associated metadata. afflib is library for support of the
Advanced Forensic Format (AFF).

%package -n     afftools
Summary:	Utilities for %{name}
Requires:	%{name} = %{version}-%{release}

%description -n afftools
The %{name}-utils package contains utilities for using %{name}.

%package        devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel
Requires:	pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package python
Summary:	Python bindings for AFFLIB
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description python
These bindings currently support a read-only file-like interface to
AFFLIB and basic metadata accessor functions. The binding is not
currently complete.

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
%{__aclocal}
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

%if %{with python}
%py_postclean
rm -rf $RPM_BUILD_ROOT%{py_sitedir}/*.egg-info/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGLIST.txt ChangeLog NEWS README doc/announce_2.2.txt COPYING
%attr(755,root,root) %{_libdir}/libafflib.so.*

%files -n afftools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aff*
%{_mandir}/man1/aff*.1.*

%files devel
%defattr(644,root,root,755)
%doc doc/crypto_design.txt doc/crypto_doc.txt
%attr(755,root,root) %{_libdir}/libafflib.so
%{_libdir}/*.la
%{_includedir}/afflib/
%{_pkgconfigdir}/afflib.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libafflib.a
%endif

%files python
%defattr(644,root,root,755)
%doc pyaff/README
%attr(755,root,root) %{py_sitedir}/pyaff.so

# TODO:
# - python, amazon s3, lzma, fuse, qemu bconds
# - build against system lzma if possible
#
Summary:	Library to support the Advanced Forensic Format
Name:		afflib
Version:	3.7.16
Release:	0.1
License:	BSD with advertising
Group:		Libraries
Source0:	https://github.com/sshock/AFFLIBv3/archive/v%{version}.tar.gz
# Source0-md5:	776f09e1c98a63e1e7a16a52f56146fe
Patch0:		Sanity-check-size-passed-to-malloc.patch
URL:		https://github.com/sshock/AFFLIBv3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	expat-devel
BuildRequires:	intltool
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	lzma-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
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

%prep:
%setup -q -n AFFLIBv3-%{version}
%patch0 -p1

# prevent internal lzma to be built - testing
#rm -rf lzma443

#fix spurious permissions with lzma443
find lzma443 -type f -exec chmod 0644 {} ';'

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGLIST.txt ChangeLog NEWS README doc/announce_2.2.txt COPYING
%attr(755,root,root) %{_libdir}/*.so.*

%files -n afftools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aff*
%{_mandir}/man1/aff*.1.*

%files devel
%defattr(644,root,root,755)
%doc doc/crypto_design.txt doc/crypto_doc.txt
%{_includedir}/afflib/
%{_libdir}/*.so
%{_libdir}/*.la
%{_pkgconfigdir}/afflib.pc

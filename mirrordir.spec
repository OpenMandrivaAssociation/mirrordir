#
# (fg) 20010112 Library stuff...
#

%define name2 diffie
%define libname2 %mklibname %name2 1

Name: mirrordir
Summary: Easy to use ftp mirroring package
Version: 0.10.49
Release: %mkrel 9
Source: ftp://ftp.obsidian.co.za/pub/mirrordir/mirrordir-%{version}.tar.bz2
Patch0: mirrordir-0.10.49-confpath.patch
Patch1: mirrordir-zlib-1.1.3-zfree.patch
Patch2: mirrordir-0.10.49-varargs.patch
Patch3: mirrordir-0.10.49-64bit-fixes.patch
Patch4: mirrordir-0.10.49-pam_pwdb.patch
# (tv) use system zlib:
Patch5: mirrordir-use-system-libs.patch
BuildRequires: automake1.4, autoconf2.5 zlib-devel
Group: Networking/File transfer 
URL: ftp://ftp.obsidian.co.za/pub/mirrordir/
BuildRoot: %_tmppath/%name-%version-root
License: GPL
Prefix: %{_prefix}
Requires: %libname2 = %version

%description
Easy to use ftp mirroring package - simply use
mirrordir ftp://some.where.com/dir /some/local/dir

%package -n %libname2
Summary: The diffie library, necessary to run mirrordir.
Group: System/Libraries

%description -n %libname2
The diffie library, necessary to run mirrordir.

%package -n %{libname2}-devel
Summary: Static version of the diffie library
Group: Development/C
Requires: %libname2 = %{version}
Provides: lib%{name2}-devel

%description -n %{libname2}-devel
Static version of the diffie library

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q
%patch0 -p1 -b .confpath
%patch1 -p1 -b .zfree
%patch2 -p1 -b .varargs
%patch3 -p1 -b .64bit-fixes
%patch4 -p1 -b .pam_pwdb
%patch5 -p1 -b .sys_libs
# XXX workaround another abelism concerning autoconf (aka,
# WANT_AUTOCONF_2_5 is a no-op nowadays...)
echo "AC_PREREQ(2.50)" > configure.ac
cat configure.in >> configure.ac
rm -f configure.in
rm -f ltmain.sh 
libtoolize -c
aclocal-1.4
automake-1.4
autoconf

%build
%configure --enable-zlib
%make


%install
rm -rf $RPM_BUILD_ROOT

perl -p -i -e 's/-f \$\(bindir\)\/mirrordir \$/-f \$\(bindir\)\/mirrordir \$\(DESTDIR\)\$/' src/Makefile
make install DESTDIR=$RPM_BUILD_ROOT 


%post -n %libname2 -p /sbin/ldconfig

%postun -n %libname2 -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT 

%files 
%defattr(-,root,root,755)
%doc AUTHORS BUGS COPYING README NEWS THANKS TODO
%{_bindir}/*
%dir %{_sysconfdir}/mirrordir
%config(noreplace) %{_sysconfdir}/mirrordir
%config(noreplace) %{_sysconfdir}/secure*
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_mandir}/man*/*

%files -n %libname2
%defattr(-,root,root,755)
%doc AUTHORS BUGS COPYING README NEWS THANKS TODO
%{_libdir}/lib%{name2}.so.*

%files -n %{libname2}-devel
%defattr(-,root,root,755)
%doc AUTHORS BUGS COPYING README NEWS THANKS TODO
%{_libdir}/lib%{name2}.so
%{_libdir}/lib%{name2}.a
%{_libdir}/lib%{name2}.la


#
# (fg) 20010112 Library stuff...
#

%define name2 diffie
%define libname2 %mklibname %name2 1
%define develname %mklibname -d %name2

Name: mirrordir
Summary: Easy to use ftp mirroring package
Version: 0.10.49
Release: 19
Source: ftp://ftp.obsidian.co.za/pub/mirrordir/mirrordir-%{version}.tar.bz2
Patch0: mirrordir-0.10.49-confpath.patch
Patch1: mirrordir-zlib-1.1.3-zfree.patch
Patch2: mirrordir-0.10.49-varargs.patch
Patch3: mirrordir-0.10.49-64bit-fixes.patch
Patch4: mirrordir-0.10.49-pam_pwdb.patch
# (tv) use system zlib:
Patch5: mirrordir-use-system-libs.patch
Patch6: mirrordir-0.10.49-fix-str-fmt.patch
Patch7: mirrordir-0.10.49-fix-install.patch
Patch8: mirrordir-automake-1.13.patch
BuildRequires: automake autoconf zlib-devel
Group: Networking/File transfer 
URL: ftp://ftp.obsidian.co.za/pub/mirrordir/
License: GPLv2+
Requires: %libname2 = %version

%description
Easy to use ftp mirroring package - simply use
mirrordir ftp://some.where.com/dir /some/local/dir

%package -n %libname2
Summary: The diffie library, necessary to run mirrordir
Group: System/Libraries

%description -n %libname2
The diffie library, necessary to run mirrordir.

%package -n %{develname}
Summary: Static version of the diffie library
Group: Development/C
Requires: %libname2 = %{version}
Provides: lib%{name2}-devel = %version
Provides: %name-devel = %version
Obsoletes: %{mklibname -d %name2 1}

%description -n %{develname}
Static version of the diffie library

%prep
%setup -q
%apply_patches

%build
autoreconf -fi
# Forcing BFD to prevent mirrordir and forward from getting the same build ID
%configure2_5x --enable-zlib \
	CFLAGS="%optflags -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -fuse-ld=bfd"
%make

%install

%makeinstall_std

%files 
%defattr(-,root,root,755)
%doc AUTHORS BUGS COPYING README NEWS THANKS TODO
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/mirrordir
%config(noreplace) %{_sysconfdir}/secure*
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_mandir}/man*/*

%files -n %libname2
%defattr(-,root,root,755)
%doc AUTHORS BUGS COPYING README NEWS THANKS TODO
%{_libdir}/lib%{name2}.so.*

%files -n %{develname}
%defattr(-,root,root,755)
%doc AUTHORS BUGS COPYING README NEWS THANKS TODO
%{_libdir}/lib%{name2}.so
%{_libdir}/lib%{name2}.a


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.49-17mdv2011.0
+ Revision: 666430
- mass rebuild

* Tue Jul 13 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.10.49-16mdv2011.0
+ Revision: 552372
- enable largefile support, should fix (mdv#60119)

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.49-15mdv2010.1
+ Revision: 523320
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.10.49-14mdv2010.0
+ Revision: 426145
- rebuild

* Fri Apr 10 2009 Funda Wang <fwang@mandriva.org> 0.10.49-13mdv2009.1
+ Revision: 365863
- fix str fmt
- fix symbolic link install

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Mon Sep 08 2008 Funda Wang <fwang@mandriva.org> 0.10.49-12mdv2009.0
+ Revision: 282435
- New devel package policy

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.10.49-11mdv2008.1
+ Revision: 153099
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Aug 17 2007 Thierry Vignaud <tv@mandriva.org> 0.10.49-9mdv2008.0
+ Revision: 64797
- patch 5: use system zlib
- fix build
- fix summary


* Tue Jan 31 2006 Olivier Blin <oblin@mandriva.com> 0.10.49-8mdk
- use pam_unix instead of obsolete pam_pwdb (Patch4)
- fix configuration path (i.e. fix Pathc0, sorry for fixing the
  program, it seems this one hasn't been tried for four years)

* Tue Aug 23 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.10.49-7mdk
- varargs, 64-bit, includes & libtool fixes

* Mon Sep 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.10.49-6mdk
- use mklibname

* Thu Jul 17 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.10.49-5mdk
- rebuild


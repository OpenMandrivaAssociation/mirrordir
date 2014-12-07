%define lname	diffie
%define major	1
%define libname	%mklibname %{lname} %{major}
%define devname	%mklibname -d %{lname}

Summary:	Easy to use ftp mirroring package
Name:		mirrordir
Version:	0.10.49
Release:	27
Group:		Networking/File transfer 
License:	GPLv2+
Url:		ftp://ftp.obsidian.co.za/pub/mirrordir/
Source0:	ftp://ftp.obsidian.co.za/pub/mirrordir/%{name}-%{version}.tar.bz2
Patch0:		mirrordir-0.10.49-confpath.patch
Patch1:		mirrordir-zlib-1.1.3-zfree.patch
Patch2:		mirrordir-0.10.49-varargs.patch
Patch3:		mirrordir-0.10.49-64bit-fixes.patch
Patch4:		mirrordir-0.10.49-pam_pwdb.patch
# (tv) use system zlib:
Patch5:		mirrordir-use-system-libs.patch
Patch6:		mirrordir-0.10.49-fix-str-fmt.patch
Patch7:		mirrordir-0.10.49-fix-install.patch
Patch8:		mirrordir-automake-1.13.patch
BuildRequires:	pkgconfig(zlib)

%description
Easy to use ftp mirroring package - simply use
mirrordir ftp://some.where.com/dir /some/local/dir

%package -n %{libname}
Summary:	The diffie library, necessary to run mirrordir
Group:		System/Libraries

%description -n %{libname}
The diffie library, necessary to run mirrordir.

%package -n %{devname}
Summary:	Development files of the diffie library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{lname}-devel = %{version}-%{release}

%description -n %{devname}
This pacakge includes the development files for %{name}.

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
# Forcing BFD to prevent mirrordir and forward from getting the same build ID
%configure2_5x \
	--disable-static \
	--enable-zlib \
	CFLAGS="%optflags -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -fuse-ld=bfd"
%make

%install
%makeinstall_std

%files 
%doc AUTHORS BUGS COPYING README NEWS THANKS TODO
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/mirrordir
%config(noreplace) %{_sysconfdir}/secure*
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_mandir}/man*/*

%files -n %{libname}
%{_libdir}/lib%{lname}.so.%{major}*

%files -n %{devname}
%{_libdir}/lib%{lname}.so


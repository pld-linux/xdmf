# TODO: MPI
# fix utils:
# - installs libmetis conflicting with system metis
# - wants preinstalled libvtk{NetCDF,exoIIc} or installs own versions
# - installs headers to /usr/include/utils/Xdmf* (too generic dir name)
#
# Conditional build:
%bcond_with	mpi	# MPI support
%bcond_with	utils	# build XdmfUtils (see TODO above)
#
%define		rel 5
Summary:	eXtensible Data Model and Format library
Summary(pl.UTF-8):	Biblioteka rozszerzalnego modelu i formatu danych (XDMF)
Name:		xdmf
# Debian says 2.1, but no version information anywhere in sources/CVS
Version:	0
%define	snap	20100330
Release:	0.%{snap}.%{rel}
# specified in libsrc/{gzstream,bz2stream}.*
License:	LGPL v2.1+
Group:		Libraries
# cvs -d :pserver:anonymous:xdmf@public.kitware.com:/cvsroot/Xdmf co Xdmf
Source0:	%{name}.tar.xz
# Source0-md5:	63f99d11bea8d56d4185cb8facd44ca2
Patch0:		%{name}-include.patch
Patch1:		%{name}-soname.patch
Patch2:		%{name}-log2.patch
Patch3:		%{name}-destdir.patch
Patch4:		%{name}-format.patch
Patch5:		%{name}-lib.patch
URL:		http://www.xdmf.org/
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 2.4
BuildRequires:	hdf5-devel >= 1.8
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2
BuildRequires:	python-devel >= 2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
eXtensible Data Model and Format library.

%description -l pl.UTF-8
Biblioteka rozszerzalnego modelu i formatu danych (XDMF - eXtensible
Data Model and Format).

%package devel
Summary:	Header files for Xdmf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Xdmf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	bzip2-devel
Requires:	zlib-devel

%description devel
Header files for Xdmf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Xdmf.

%package -n python-xdmf
Summary:	Python binding for Xdmf library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki Xdmf
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-xdmf
Python binding for Xdmf library.

%description -n python-xdmf -l pl.UTF-8
Pythonowy interfejs do biblioteki Xdmf.

%prep
%setup -q -n Xdmf
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
mkdir build
cd build
%cmake .. \
	-DPythonLibs_FIND_VERSION=2 \
	-DPythonLibs_FIND_VERSION_MAJOR=2 \
	%{!?with_mpi:-DXDMF_BUILD_MPI=OFF} \
	%{?with_utils:-DXDMF_BUILD_UTILS=ON} \
	-DXDMF_SYSTEM_HDF5=ON \
	-DXDMF_SYSTEM_LIBXML2=ON \
	-DXDMF_SYSTEM_ZLIB=ON \
	-DXDMF_USE_RPATH=OFF \
	-DXDMF_WRAP_PYTHON=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# cmake compiles only to .pyc
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXdmf.so.2
%if %{with utils}
%attr(755,root,root) %{_libdir}/libXdmfUtils.so
%attr(755,root,root) %{_libdir}/libmetis.so
%attr(755,root,root) %{_libdir}/libvtkNetCDF.so
%attr(755,root,root) %{_libdir}/libvtkexoIIc.so
%attr(755,root,root) %{_bindir}/XdmfDiff
%attr(755,root,root) %{_bindir}/XdmfExodusConverter
%attr(755,root,root) %{_bindir}/XdmfPartitioner
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXdmf.so
%{_libdir}/XdmfCMake
%{_includedir}/Xdmf*.h
%{_includedir}/bz2stream.h
%{_includedir}/gzstream.h
%if %{with utils}
%{_includedir}/XdmfSTLConverter.txx
# FIXME: too generic dir
%dir %{_includedir}/utils
%{_includedir}/utils/Xdmf*.h
# FIXME: conflict with system metis
%{_includedir}/metis
%{_includedir}/vtkexodus2
%{_includedir}/vtknetcdf
%endif

%files -n python-xdmf
%defattr(644,root,root,755)
%dir %{py_sitedir}/Xdmf
%attr(755,root,root) %{py_sitedir}/Xdmf/_Xdmf.so
%{py_sitedir}/Xdmf/Xdmf.py[co]
%{py_sitedir}/Xdmf/__init__.py[co]
%if %{with utils}
%attr(755,root,root) %{py_sitedir}/Xdmf/_XdmfUtils.so
%{py_sitedir}/Xdmf/XdmfUtils.py[co]
%endif

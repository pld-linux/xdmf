# TODO: parallel (MPI, MPI4PY, H5FDdsm)?
# - use exodusii
# - python3 module
# - system loki library?
#
# Conditional build:
%bcond_without	apidocs	# Doxygen docs
%bcond_without	fortran	# Fortran support in XdmfUtils
%bcond_without	metis	# Metis partitioner in XdmfUtils
%bcond_with	mpi	# MPI support
%bcond_without	java	# Java wrappers
%bcond_without	python	# Python wrappers
#
Summary:	eXtensible Data Model and Format library
Summary(pl.UTF-8):	Biblioteka rozszerzalnego modelu i formatu danych (XDMF)
Name:		xdmf
# see CMakeLists.txt /XDMF_VERSION
Version:	3.0.0
%define	gitref	8d9c98081d89ac77a132d56bc8bef53581db4078
%define	snap	20190115
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	BSD-like
Group:		Libraries
Source0:	https://gitlab.kitware.com/xdmf/xdmf/-/archive/%{gitref}/xdmf-%{snap}.tar.bz2
# Source0-md5:	32fbbd1f6b584e27bb5a30945f6b787a
Patch0:		%{name}-swig.patch
URL:		http://www.xdmf.org/
BuildRequires:	bzip2-devel
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.4
BuildRequires:	hdf5-devel >= 1.8
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxml2-devel >= 2
%{?with_python:BuildRequires:	python-devel >= 2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_java:BuildRequires:	swig >= 2.0.0}
%{?with_python:BuildRequires:	swig-python >= 2.0.0}
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

%package -n java-xdmf
Summary:	Java binding for Xdmf library
Summary(pl.UTF-8):	Interfejs Javy do biblioteki Xdmf
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n java-xdmf
Java binding for Xdmf library.

%description -n java-xdmf -l pl.UTF-8
Interfejs Javy do biblioteki Xdmf.

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
%setup -q -n %{name}-%{gitref}
%patch0 -p1

%build
mkdir build
cd build
%cmake .. \
	-DREQUESTED_PYTHON_VERSION=2 \
	%{?with_apidocs:-DXDMF_BUILD_DOCUMENTATION=ON} \
	%{?with_fortran:-DXDMF_BUILD_FORTRAN=ON} \
	%{!?with_mpi:-DXDMF_BUILD_MPI=OFF} \
	%{?with_metis:-DXDMF_BUILD_PARTITIONER=ON} \
	-DXDMF_BUILD_UTILS=ON \
	-DXDMF_SYSTEM_HDF5=ON \
	-DXDMF_SYSTEM_LIBXML2=ON \
	-DXDMF_SYSTEM_ZLIB=ON \
	-DXDMF_USE_RPATH=OFF \
	%{?with_java:-DXDMF_WRAP_JAVA=ON} \
	%{?with_python:-DXDMF_WRAP_PYTHON=ON}
# TODO: -DXDMF_BUILD_EXODUS_IO=ON BR: Exodus-devel

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Copyright.txt README.md
%if %{with metis}
%attr(755,root,root) %{_bindir}/XdmfPartitioner
%endif
%attr(755,root,root) %{_libdir}/libXdmf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libXdmf.so.3
%attr(755,root,root) %{_libdir}/libXdmfCore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libXdmfCore.so.3
%attr(755,root,root) %{_libdir}/libXdmfUtils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libXdmfUtils.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXdmf.so
%attr(755,root,root) %{_libdir}/libXdmfCore.so
%attr(755,root,root) %{_libdir}/libXdmfUtils.so
%{_libdir}/cmake/Xdmf
%{_includedir}/ProjectVersion.hpp
%{_includedir}/Xdmf*.hpp
%{_includedir}/Xdmf*.i
%{_includedir}/XdmfArray.tpp
%{_includedir}/loki
%if %{with fortran}
%{_includedir}/Xdmf.f
%endif

%if %{with java}
%files -n java-xdmf
%defattr(644,root,root,755)
%{_libdir}/java/Xdmf.jar
%{_libdir}/java/XdmfCore.jar
%{_libdir}/java/XdmfUtils.jar
%attr(755,root,root) %{_libdir}/java/libXdmfJava.so
%attr(755,root,root) %{_libdir}/java/libXdmfCoreJava.so
%attr(755,root,root) %{_libdir}/java/libXdmfUtilsJava.so
%endif

%if %{with python}
%files -n python-xdmf
%defattr(644,root,root,755)
%dir %{py_sitedir}/xdmf
%attr(755,root,root) %{py_sitedir}/xdmf/_Xdmf.so
%attr(755,root,root) %{py_sitedir}/xdmf/_XdmfCore.so
%attr(755,root,root) %{py_sitedir}/xdmf/_XdmfUtils.so
%{py_sitedir}/xdmf/Xdmf.py[co]
%{py_sitedir}/xdmf/XdmfCore.py[co]
%{py_sitedir}/xdmf/XdmfUtils.py[co]
%endif

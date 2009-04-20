%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           funcshell
Version:        0.0.1
Release:        1%{?dist}
Summary:        A shell interface to Func

Group:          Development/Languages
License:        MIT
URL:            http://www.silassewell.com/projects/funcshell
Source0:        http://cloud.github.com/downloads/silas/funcshell/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       func
Requires:       python-cly

%description
funchshell is a shell interface to Func.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/%{name}
%{python_sitelib}/%{name}

%changelog
* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build

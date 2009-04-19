%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           funcshell
Version:        0.0.1
Release:        1%{?dist}
Summary:        A CLI interface to Func

Group:          Development/Languages
License:        MIT
URL:            http://code.google.com/p/silassewell/wiki/funcshell
Source0:        http://silassewell.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       func
Requires:       python-cly
Requires:       python-setuptools

%description
funchshell is a CLI interface to Func.

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
%{python_sitelib}/%{name}-%{version}-*.egg-info

%changelog
* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
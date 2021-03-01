#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Read resources from Python packages
Summary(pl.UTF-8):	Odczyt zasobów z pakietów Pythona
Name:		python3-importlib_resources
Version:	5.1.0
Release:	3
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/importlib-resources/
Source0:	https://files.pythonhosted.org/packages/source/i/importlib-resources/importlib_resources-%{version}.tar.gz
# Source0-md5:	a3ca1dce486f7fba1691938124e54133
Patch0:		%{name}-no_wheel.patch
URL:		https://pypi.org/project/importlib-resources/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:42
BuildRequires:	python3-setuptools_scm >= 5.0.1-2
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-black >= 0.3.7
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-flake8
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-zipp >= 0.4
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-jaraco.packaging >= 8.2
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
importlib_resources is a backport of Python standard library
importlib.resources module for older Pythons. Users of Python 3.9 and
beyond should use the standard library module, since for these
versions, importlib_resources just delegates to that module.

The key goal of this module is to replace parts of pkg_resources with
a solution in Python's stdlib that relies on well-defined APIs. This
makes reading resources included in packages easier, with more stable
and consistent semantics.

%description -l pl.UTF-8
importlib_resources to backport modułu importlib.resources z
biblioteki standardowej Pythona przeznaczony dla starszych wersji
Pythona. Użytkownicy Pythona 3.9 i nowszego powinni używać modułu z
biblioteki standardowej.

Głównym celem tego modułu jest zastąpienie części pkg_resources
rozwiązaniem obecnym w bibliotece standardowej Pythona, opartym na
dobrze zdefiniowanym API. Czyni to czytanie zasobów z pakietów
łatwiejszym, z bardziej stabilną i spójną semantyką.

%package apidocs
Summary:	API documentation for Python importlib_resources module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona importlib_resources
Group:		Documentation

%description apidocs
API documentation for Python importlib_resources module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona importlib_resources.

%prep
%setup -q -n importlib_resources-%{version}
%patch0 -p1

%build
%py3_build

%if %{with tests}
%{__python3} -m unittest discover
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/importlib_resources
%{py3_sitescriptdir}/importlib_resources-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif

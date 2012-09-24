%global gem_name simple_form

Name: rubygem-%{gem_name}
Version: 2.0.2
Release: 1%{?dist}
Summary: Flexible and powerful components to create forms

Group: Development/Languages
License: MIT
URL: https://github.com/plataformatec/%{gem_name}
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem

Provides: rubygem(%{gem_name}) = %{version}
BuildArch: noarch
BuildRequires: rubygems-devel
# Test needs mocha
#BuildRequires: rubygem(mocha)

%if 0%{?fedora} > 16
Requires: ruby(abi) = 1.9.1
%else
Requires: ruby(abi) = 1.8
%endif


%description
SimpleForm aims to be as flexible as possible while helping you with powerful
components to create your forms. The basic goal of SimpleForm is to not touch
your way of defining the layout, letting you find the better design for your
eyes.


%package doc
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Summary: Documentation for %{name}


%description doc
This package contains documentation %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Replace UTF chars in gemspec
sed -i -e 's/\\u{e9}/e/' -e 's/\\u{f4}/o/' -e 's/\\u{e7}/c/' %{gem_name}.gemspec


%build
mkdir -p .%{gem_dir}

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in %%install
gem install -V \
         --local \
         --install-dir ./%{gem_dir} \
         --bindir ./%{_bindir} \
         --force \
         --rdoc \
         %{gem_name}-%{version}.gem


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/


# The test suite needs rubygem-country_select which is not packaged for Fedora
# so commenting it out
#%check
#pushd ./%{gem_instdir}
#rspec -I test/*.rb
#popd


%files
%dir %{gem_instdir}
%{gem_instdir}/lib
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README.md
%exclude %{gem_cache}
%exclude %{gem_instdir}/.yardoc/
%{gem_spec}


%files doc
%{gem_instdir}/test
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_docdir}/rdoc
%doc %{gem_docdir}/ri

%changelog
* Fri Sep 21 2012 Imre Farkas <ifarkas@redhat.com> - 2.0.2-1
- Initial package

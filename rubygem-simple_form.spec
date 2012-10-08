%global gem_name simple_form

Name: rubygem-%{gem_name}
Version: 2.0.3
Release: 1%{?dist}
Summary: Flexible and powerful components to create forms

Group: Development/Languages
License: MIT
URL: https://github.com/plataformatec/%{gem_name}
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem

Provides: rubygem(%{gem_name}) = %{version}
BuildArch: noarch
BuildRequires: rubygems-devel
# Test suite needs the following dependencies
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(railties)
BuildRequires: rubygem(tzinfo)

%if 0%{?fedora} > 16
Requires: ruby(abi) = 1.9.1
%else
Requires: ruby(abi) = 1.8
%endif

Requires: rubygems
Requires: rubygem(activemodel) >= 3.0
Requires: rubygem(actionpack) >= 3.0


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


%build
mkdir -p .%{gem_dir}

# Create the gem as gem install only works on a gem file
LANG=en_US.utf8 gem build %{gem_name}.gemspec

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

# Removing file which is not under source control. For further details check out:
# https://github.com/plataformatec/simple_form/issues/673
%{__rm} %{buildroot}%{gem_instdir}/test/form_builder/general_test.rb.orig


%check
# Get rid of Bundler.
sed -i "/require 'bundler\/setup'/d" test/test_helper.rb
# The following test cases require rubygem-country_select which is not packaged
# for Fedora, so commenting it out
sed -i "/require 'country_select'/d" test/test_helper.rb
sed -i '103,106 s|^|#|' test/form_builder/general_test.rb
sed -i '113,116 s|^|#|' test/form_builder/general_test.rb
sed -i '5,17 s|^|#|' test/inputs/priority_input_test.rb
sed -i '38,42 s|^|#|' test/inputs/priority_input_test.rb
find ./test -name *_test.rb | xargs testrb -Itest


%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README.md
%exclude %{gem_cache}
%exclude %{gem_instdir}/.yardoc/
%{gem_spec}


%files doc
%{gem_instdir}/test
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_docdir}


%changelog
* Fri Sep 21 2012 Imre Farkas <ifarkas@redhat.com> - 2.0.3-1
- Initial package

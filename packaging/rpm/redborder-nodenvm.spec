%define debug_package %{nil}

%global nvm_dir %{__nvm_dir}
%global nvm_version %{__nvmversion}
%global node_version %{__nodeversion}
%undefine __brp_mangle_shebangs

Name: redborder-nodenvm
Version: %{__version}
Release: %{__release}%{?dist}
License: MIT
ExclusiveArch: x86_64
Summary: NVM and Node.js for redborder platform

Source0: nvm-%{nvm_version}.tar.gz
Source1: node-v%{node_version}-linux-x64.tar.xz

BuildRequires: gcc-c++ make tar xz git python openssl-devel readline-devel zlib-devel
Requires: sed grep tar gzip bzip2 make file dialog

%description
NVM with Node.js, packaged as an RPM for redborder platform.
System level install. Versions: nvm-%{nvm_version}, node-%{node_version}.

%prep
%setup -q -n nvm-%{nvm_version}

%build
# Extract nvm
mkdir -p %{nvm_dir}
tar -xzf %{SOURCE0} -C %{nvm_dir} --strip-components=1

# Extract node.js to the NVM directory structure
mkdir -p %{nvm_dir}/versions/node/v%{node_version}
tar -xf %{SOURCE1} -C %{nvm_dir}/versions/node/v%{node_version} --strip-components=1

# Create nvmrc
echo "
umask u=rwx,g=rwx,o=rx
nvm_path=\"%{nvm_dir}\"
" > /etc/nvmrc

# Set up default node version
export NVM_DIR="%{nvm_dir}"
. %{nvm_dir}/nvm.sh
nvm use v%{node_version}
nvm alias default v%{node_version}

%install
rm -rf $RPM_BUILD_ROOT/*
mkdir -p $RPM_BUILD_ROOT%{nvm_dir}
mkdir -p $RPM_BUILD_ROOT/etc/profile.d

cp -rf %{nvm_dir}/* $RPM_BUILD_ROOT%{nvm_dir}/
cp /etc/nvmrc $RPM_BUILD_ROOT/etc/nvmrc
# Create /etc/profile.d/nvm.sh to set up the NVM environment for all users
echo 'export NVM_DIR="%{nvm_dir}"' > $RPM_BUILD_ROOT/etc/profile.d/nvm.sh
# Ensure NVM is loaded into new shell sessions
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> $RPM_BUILD_ROOT/etc/profile.d/nvm.sh

# Set permissions
chgrp -R root $RPM_BUILD_ROOT%{nvm_dir}
chmod -R g+wxr $RPM_BUILD_ROOT%{nvm_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Set up nvm environment
echo 'export NVM_DIR="%{nvm_dir}"' > /etc/profile.d/nvm.sh
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /etc/profile.d/nvm.sh

%files
%{nvm_dir}
/etc/nvmrc
/etc/profile.d/nvm.sh

%changelog
* Thu Aug 01 2024 Daniel Castro <dcastro@redborder.com> - 1.1-1
- Create SPEC file and change nvm installation path
* Wed Jul 24 2024 Daniel Castro <dcastro@redborder.com> - 1.0-1
- Initial package for NVM and Node.js

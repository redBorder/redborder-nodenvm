#!/bin/bash

NVM_VERSION=${NVM_VERSION:="0.39.1"}
NODE_VERSION=${NODE_VERSION:="16.13.0"}
NVM_DIR=${NVM_DIR:="root/.nvm"}

mkdir -p SOURCES

# Download nvm
if [ ! -f SOURCES/nvm-${NVM_VERSION}.tar.gz ]; then
  wget --no-check-certificate https://github.com/nvm-sh/nvm/archive/v${NVM_VERSION}.tar.gz -O SOURCES/nvm-${NVM_VERSION}.tar.gz
fi

# Download Node.js binary
if [ ! -f SOURCES/node-v${NODE_VERSION}-linux-x64.tar.xz ]; then
  wget --no-check-certificate https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz -O SOURCES/node-v${NODE_VERSION}-linux-x64.tar.xz
fi

exit 0
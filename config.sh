#!/bin/bash

mkdir -pv install
mkdir -pv build
installdir="`pwd`/install"
echo $installdir

cd ./build

cmake .. \
  -DSCOREC_PREFIX=$SCOREC_PREFIX \
  -DCMAKE_CXX_COMPILER="mpicxx" \
  -DCMAKE_CXX_FLAGS="-O0 -g -Wall -std=c++11 -fPIC" \
  -DBUILD_SHARED_LIBS=True \
  -DCMAKE_INSTALL_PREFIX=$installdir

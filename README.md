# rastervectoranalysis

The goal of this project is to demonstrate various forms of raster and
vector analysis using Python.

## Installation

### Install GDAL python module via APT

sudo apt -y install python-dev libgdal-dev python-gdal python3-gdal

### Install GDAL python module via pip

1. sudo apt -y install python-dev libgdal-dev python-gdal python3-gdal
2. export CPLUS_INCLUDE_PATH=/usr/include/gdal
3. export C_INCLUDE_PATH=/usr/include/gdal
4. pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==$(gdal-config --version)

### Install Cython via APT

sudo apt -y install cython

## License

Apache License Version 2.0
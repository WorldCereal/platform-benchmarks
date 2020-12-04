#!/bin/bash
set -x

export OTB_APPLICATION_PATH=/opt/orfeo-toolbox/lib/otb/applications/
export PYTHONPATH=/opt/orfeo-toolbox/lib/otb/python/
export LD_LIBRARY_PATH=/opt/orfeo-toolbox/lib


# Test orfeo script with mounted filesystem
time python3 orfeo-test02.py /eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff  orfeo-test02-out-eodata.tiff


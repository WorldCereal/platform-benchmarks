# CREODIAS test
#test reading via S3 (object storage)
time CPL_DEBUG=OFF gdal_translate -CO COMPRESS=LZW /vsis3/eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff out.tiff
#test reading via mounted filesystem
time CPL_DEBUG=OFF gdal_translate -CO COMPRESS=LZW /eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff out2.tiff
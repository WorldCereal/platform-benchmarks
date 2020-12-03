## Read access CreoDIAS

This benchmark uses a simple gdal_translate to assess basic read access. CreoDIAS allows reading through object storage
directly, or by mounting the object storage as a file system.

Benchmark was performed 3 times in a row, reading through object storage was stable around 27 seconds, file system accessed varied from 19 to 24 seconds.

GDAL 3.1.0, released 2020/05/03
```
root@openeo-geotrellis-driver:/opt/spark/work-dir# time CPL_DEBUG=OFF gdal_translate -CO COMPRESS=LZW /vsis3/eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff out.tiff
Input file size is 26648, 16681
ERROR 1: PROJ: proj_create_from_database: ellipsoid not found
proj_create_from_database: ellipsoid not found
0...10...20...30...40...50...60...70...80...90...100 - done.

real    0m27.827s
user    0m15.737s
sys     0m3.096s
root@openeo-geotrellis-driver:/opt/spark/work-dir# time CPL_DEBUG=OFF gdal_translate -CO COMPRESS=LZW /eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff out2.tiff
Input file size is 26648, 16681
ERROR 1: PROJ: proj_create_from_database: ellipsoid not found
proj_create_from_database: ellipsoid not found
0...10...20...30...40...50...60...70...80...90...100 - done.

real    0m24.861s
user    0m13.766s
sys     0m1.416s
```

### Conclusions
In this basic test, reading through the filesystem API was faster compared to object storage. This is good, because Orfeo toolbox
may not support the object storage interface.

### Possible improvements
- Run benchmark multiple times?
- GDAL tuning to improve object storage results?
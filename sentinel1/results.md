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

## Sentinel-2 Reading

For Sentinel-2 reading, these are important parameters:
- Kakadu vs open source JPEG2000
- Object storage vs mounted object storage
- Kakadu allows configuring a number of threads

```
root@openeo-geotrellis-driver:/opt/spark/work-dir# time CPL_DEBUG=OFF gdal_translate -CO TILED=TRUE -CO COMPRESS=LZW /vsis3/eodata/Sentinel-2/MSI/L2A/2019/01/01/S2A_MSIL2A_20190101T082331_N0211_R121_T36SYC_20190101T094029.SAFE/GRANULE/L2A_T36SYC_A018422_20190101T082935/IMG_DATA/R10m/T36SYC_20190101T082331_B02_10m.jp2 out.tif
Input file size is 10980, 10980
0...10...20...30...40...50...60...70...80...90...100 - done.

real    1m11.969s
user    0m41.652s
sys     0m1.352s


root@openeo-geotrellis-driver:/opt/spark/work-dir# time CPL_DEBUG=OFF gdal_translate -CO TILED=TRUE -CO COMPRESS=LZW /eodata/Sentinel-2/MSI/L2A/2019/01/01/S2A_MSIL2A_20190101T082331_N0211_R121_T36SYC_20190101T094029.SAFE/GRANULE/L2A_T36SYC_A018422_20190101T082935/IMG_DATA/R10m/T36SYC_20190101T082331_B02_10m.jp2 out.tif
Input file size is 10980, 10980
0...10...20...30...40...50...60...70...80...90...100 - done.

real    0m23.439s
user    0m38.565s
sys     0m0.949s

##check if number of threads is important
root@openeo-geotrellis-driver:/opt/spark/work-dir# time JP2KAK_THREADS=4 CPL_DEBUG=OFF gdal_translate -CO TILED=TRUE -CO COMPRESS=LZW /eodata/Sentinel-2/MSI/L2A/2019/01/01/S2A_MSIL2A_20190101T082331_N0211_R121_T36SYC_20190101T094029.SAFE/GRANULE/L2A_T36SYC_A018422_20190101T082935/IMG_DATA/R10m/T36SYC_20190101T082331_B02_10m.jp2 out.tif
Input file size is 10980, 10980
0...10...20...30...40...50...60...70...80...90...100 - done.

real    0m22.608s
user    0m38.246s
sys     0m0.987s

root@openeo-geotrellis-driver:/opt/spark/work-dir# time JP2KAK_THREADS=4 CPL_DEBUG=OFF gdal_translate -CO TILED=TRUE -CO COMPRESS=LZW /vsis3/eodata/Sentinel-2/MSI/L2A/2019/01/01/S2A_MSIL2A_20190101T082331_N0211_R121_T36SYC_20190101T094029.SAFE/GRANULE/L2A_T36SYC_A018422_20190101T082935/IMG_DATA/R10m/T36SYC_20190101T082331_B02_10m.jp2 out.tif
Input file size is 10980, 10980
0...10...20...30...40...50...60...70...80...90...100 - done.

real    1m7.773s
user    0m41.764s
sys     0m1.418s

root@openeo-geotrellis-driver:/opt/spark/work-dir# time JP2KAK_THREADS=1 CPL_DEBUG=OFF gdal_translate -CO TILED=TRUE -CO COMPRESS=LZW /eodata/Sentinel-2/MSI/L2A/2019/01/01/S2A_MSIL2A_20190101T082331_N0211_R121_T36SYC_20190101T094029.SAFE/GRANULE/L2A_T36SYC_A018422_20190101T082935/IMG_DATA/R10m/T36SYC_20190101T082331_B02_10m.jp2 out.tif
Input file size is 10980, 10980
0...10...20...30...40...50...60...70...80...90...100 - done.

real    0m29.366s
user    0m38.265s
sys     0m0.906s

```

### Conclusion
Reading from mount is a significantly faster for reading with Kakadu. Need to compare with regular jp2 driver.
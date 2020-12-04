# orfeo-test02

Build and execute `ExtractROI`-`SARCalibration`-`OrthoRectification` pipeline.

## Using direct filesystem

    root@openeo-geotrellis-driver:/opt/spark/work-dir# time python3 orfeo-test02.py /eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff  orfeo-test02-out-eodata.tiff
    INFO:root:test file /eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff
    INFO:root:bbox (3.15, 51.3, 3.25, 51.37)
    INFO:root:Setting up ExtractROI application
    GDAL: GDALOpen(/eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff, this=0x1afc6d0) succeeds as GTiff.
    GDAL: GDALDefaultOverviews::OverviewScan()
    ERROR 1: PROJ: proj_create_from_database: ellipsoid not found
    proj_create_from_database: ellipsoid not found
    2020-12-04 09:17:48 (INFO): Loading kwl metadata from official product in file /eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff
    INFO:root:Setting up SARCalibration application
    INFO:root:Setting up OrthoRectification application
    2020-12-04 09:17:48 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    2020-12-04 09:17:48 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    2020-12-04 09:17:48 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    2020-12-04 09:17:48 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    2020-12-04 09:17:48 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    2020-12-04 09:17:48 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    2020-12-04 09:17:49 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    2020-12-04 09:17:49 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    2020-12-04 09:17:49 (INFO) OrthoRectification: Generating output with size = [694, 982]
    2020-12-04 09:17:49 (INFO) OrthoRectification: Generating output with pixel spacing = [10, -10]
    2020-12-04 09:17:49 (INFO) OrthoRectification: Generating output with origin = [510460, 5.69201e+06]
    2020-12-04 09:17:49 (INFO) OrthoRectification: Area outside input image bounds will have a pixel value of [0]
    2020-12-04 09:17:49 (INFO) OrthoRectification: Using a deformation grid with a physical spacing of 40
    2020-12-04 09:17:49 (INFO) OrthoRectification: Using a deformation grid of size [173.5, 245.5]
    2020-12-04 09:17:49 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    INFO:root:ExecuteAndWriteOutput
    2020-12-04 09:17:49 (INFO) OrthoRectification: Default RAM limit for OTB is 256 MB
    GDAL: GDAL_CACHEMAX = 286 MB
    2020-12-04 09:17:49 (INFO) OrthoRectification: GDAL maximum cache size is 286 MB
    2020-12-04 09:17:49 (INFO) OrthoRectification: OTB will use at most 4 threads
    2020-12-04 09:17:49 (INFO) OrthoRectification: Elevation management: setting default height above ellipsoid to 0 meters
    2020-12-04 09:17:49 (INFO) OrthoRectification: Generating output with size = [694, 982]
    2020-12-04 09:17:49 (INFO) OrthoRectification: Generating output with pixel spacing = [10, -10]
    2020-12-04 09:17:49 (INFO) OrthoRectification: Generating output with origin = [510460, 5.69201e+06]
    2020-12-04 09:17:49 (INFO) OrthoRectification: Area outside input image bounds will have a pixel value of [0]
    2020-12-04 09:17:49 (INFO) OrthoRectification: Using a deformation grid with a physical spacing of 40
    2020-12-04 09:17:49 (INFO) OrthoRectification: Using a deformation grid of size [173.5, 245.5]
    2020-12-04 09:17:49 (INFO): Estimated memory for full processing: 57.0731MB (avail.: 512 MB), optimal image partitioning: 1 blocks
    2020-12-04 09:17:49 (INFO): File orfeo-test02-out-eodata.tiff will be written in 1 blocks of 694x982 pixels
    Writing orfeo-test02-out-eodata.tiff...: 100% [**************************************************]GDAL: QuietDelete(orfeo-test02-out-eodata.tiff) invoking Delete()
    GDAL: GDALOpen(orfeo-test02-out-eodata.tiff, this=0x30edd50) succeeds as GTiff.
    GDAL: GDALDefaultOverviews::OverviewScan()
    GDAL: GDALClose(orfeo-test02-out-eodata.tiff, this=0x30edd50)
    GDAL: GDALDriver::Create(GTiff,orfeo-test02-out-eodata.tiff,694,982,1,Float32,(nil))
    GDAL: Flushing dirty blocks: 0...10...20...30...40...50...60...70...80...90...100 - done.
    GDAL: GDALClose(orfeo-test02-out-eodata.tiff, this=0x30edd50)
     (0s)
    GDAL: GDALClose(/eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff, this=0x1afc6d0)
    
    real	0m6.323s
    user	0m2.441s
    sys	0m0.425s


### Result
    
    root@openeo-geotrellis-driver:/opt/spark/work-dir# gdalinfo orfeo-test02-out-eodata.tiff 
    GDAL: GDALOpen(orfeo-test02-out-eodata.tiff, this=0x5594b82b1d90) succeeds as GTiff.
    Driver: GTiff/GeoTIFF
    GDAL: GDALDefaultOverviews::OverviewScan()
    Files: orfeo-test02-out-eodata.tiff
    Size is 694, 982
    Coordinate System is:
    PROJCRS["WGS 84 / UTM zone 31N",
        BASEGEOGCRS["WGS 84",
            DATUM["World Geodetic System 1984",
                ELLIPSOID["WGS 84",6378137,298.257223563,
                    LENGTHUNIT["metre",1]]],
            PRIMEM["Greenwich",0,
                ANGLEUNIT["degree",0.0174532925199433]],
            ID["EPSG",4326]],
        CONVERSION["UTM zone 31N",
            METHOD["Transverse Mercator",
                ID["EPSG",9807]],
            PARAMETER["Latitude of natural origin",0,
                ANGLEUNIT["degree",0.0174532925199433],
                ID["EPSG",8801]],
            PARAMETER["Longitude of natural origin",3,
                ANGLEUNIT["degree",0.0174532925199433],
                ID["EPSG",8802]],
            PARAMETER["Scale factor at natural origin",0.9996,
                SCALEUNIT["unity",1],
                ID["EPSG",8805]],
            PARAMETER["False easting",500000,
                LENGTHUNIT["metre",1],
                ID["EPSG",8806]],
            PARAMETER["False northing",0,
                LENGTHUNIT["metre",1],
                ID["EPSG",8807]]],
        CS[Cartesian,2],
            AXIS["(E)",east,
                ORDER[1],
                LENGTHUNIT["metre",1]],
            AXIS["(N)",north,
                ORDER[2],
                LENGTHUNIT["metre",1]],
        USAGE[
            SCOPE["unknown"],
            AREA["World - N hemisphere - 0°E to 6°E - by country"],
            BBOX[0,0,84,6]],
        ID["EPSG",32631]]
    Data axis to CRS axis mapping: 1,2
    Origin = (510455.000000000000000,5692019.500000000000000)
    Pixel Size = (10.000000000000000,-10.000000000000000)
    Metadata:
      AREA_OR_POINT=Area
      TIFFTAG_DATETIME=2020:10:04 08:52:16
      TIFFTAG_IMAGEDESCRIPTION=Sentinel-1A IW GRD HR L1
      TIFFTAG_SOFTWARE=Sentinel-1 IPF 003.31
    Image Structure Metadata:
      INTERLEAVE=BAND
    Corner Coordinates:
    Upper Left  (  510455.000, 5692019.500) (  3d 9' 0.81"E, 51d22'45.58"N)
    Lower Left  (  510455.000, 5682199.500) (  3d 8'59.77"E, 51d17'27.69"N)
    Upper Right (  517395.000, 5692019.500) (  3d14'59.79"E, 51d22'44.96"N)
    Lower Right (  517395.000, 5682199.500) (  3d14'58.06"E, 51d17'27.08"N)
    Center      (  513925.000, 5687109.500) (  3d11'59.61"E, 51d20' 6.37"N)
    Band 1 Block=694x2 Type=Float32, ColorInterp=Gray
      NoData Value=0
    GDAL: GDALClose(orfeo-test02-out-eodata.tiff, this=0x5594b82b1d90)
    GDAL: In GDALDestroy - unloading GDAL shared library.

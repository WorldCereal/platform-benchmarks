# Comparison of Kakadu and OpenJPEG-2000 drivers in different environments

This study was conducted in order to assess which driver is more suitable for future cloud deployments.
The report is broken into three different performance analises:

* using files from a local hard drive
* using a collection on CreoDIAS
* using SentinelHub on Amazon AWS

## local computer performance

For this purpose a stripped down NDVI calculator was borrowed:

* simple Python code, uses gdal directly
* NDVI code is replaced by simple average calculation of two image files
* timings were separately measured for read/process/write

The testbed simulated ideal conditions (which was the laptop of the author): fast access SSD hard drive/16GB RAM/quad core CPU.
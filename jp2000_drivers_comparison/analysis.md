# Comparison of Kakadu and OpenJPEG-2000 drivers in different environments

This study was conducted in order to assess which driver is more suitable for future cloud deployments.
The report is broken into three different performance analises:

* using files from a local hard drive
* using a collection on CreoDIAS
* using SentinelHub on Amazon AWS

Global conditions:

* the same docker image was used in all scenarios to ensure the exact same versions of Kakadu, OpenJPEG, GDAL, ...

## local computer performance

For this purpose a stripped down NDVI calculator was borrowed:

* simple Python code, uses gdal directly
* NDVI code is replaced by simple calculation of returning half of the source image 
* timings were separately measured for read/process/write
* read/write is aligned with the block size
* Kakadu writer is forced to use the same block sizes as the input (did not have noticable effect at the end)

The testbed simulated ideal conditions (which was the laptop of the author): fast access SSD hard drive/16GB RAM/quad core CPU.

Three consecutive runs gave consistent results both for Kakadu (JP2KAK):

	root@4838e2e5bdf5:/data# python3 sum2bands_gdal.py JP2KAK
	INFO:__main__:running: JP2KAK 1
	INFO:__main__:running: JP2KAK 2
	INFO:__main__:running: JP2KAK 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [9.775216579437256, 6.576526403427124, 0, 4.595564842224121]
	INFO:__main__:proc: [0.423048734664917, 0.45554208755493164, 0, 0.4442315101623535]
	INFO:__main__:write:[17.652412176132202, 17.160632133483887, 0, 17.12736439704895]
	INFO:__main__:FINISHED
	root@4838e2e5bdf5:/data# python3 sum2bands_gdal.py JP2KAK
	INFO:__main__:running: JP2KAK 1
	INFO:__main__:running: JP2KAK 2
	INFO:__main__:running: JP2KAK 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [9.852328300476074, 6.983541011810303, 0, 4.881054162979126]
	INFO:__main__:proc: [0.44239234924316406, 0.5028300285339355, 0, 0.4695894718170166]
	INFO:__main__:write:[17.562596321105957, 18.113033294677734, 0, 17.070745944976807]
	INFO:__main__:FINISHED
	root@4838e2e5bdf5:/data# python3 sum2bands_gdal.py JP2KAK
	INFO:__main__:running: JP2KAK 1
	INFO:__main__:running: JP2KAK 2
	INFO:__main__:running: JP2KAK 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [9.686598062515259, 6.559106826782227, 0, 4.493874549865723]
	INFO:__main__:proc: [0.41961193084716797, 0.4347701072692871, 0, 0.4294300079345703]
	INFO:__main__:write:[16.76154589653015, 16.831286907196045, 0, 16.80756664276123]
	INFO:__main__:FINISHED

 and Open JPEG (JP2OpenJPEG):
 
	root@4838e2e5bdf5:/data# python3 sum2bands_gdal.py JP2OpenJPEG
	INFO:__main__:running: JP2OpenJPEG 1
	INFO:__main__:running: JP2OpenJPEG 2
	INFO:__main__:running: JP2OpenJPEG 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [19.491449117660522, 10.025968551635742, 0, 5.437419176101685]
	INFO:__main__:proc: [0.48427605628967285, 0.482715368270874, 0, 0.4499695301055908]
	INFO:__main__:write:[28.30368995666504, 27.99168825149536, 0, 28.526732921600342]
	INFO:__main__:FINISHED
	root@4838e2e5bdf5:/data# python3 sum2bands_gdal.py JP2OpenJPEG
	INFO:__main__:running: JP2OpenJPEG 1
	INFO:__main__:running: JP2OpenJPEG 2
	INFO:__main__:running: JP2OpenJPEG 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [19.471473455429077, 10.254300355911255, 0, 5.665111064910889]
	INFO:__main__:proc: [0.5035903453826904, 0.5051546096801758, 0, 0.44912099838256836]
	INFO:__main__:write:[28.65628719329834, 28.745816946029663, 0, 29.007409811019897]
	INFO:__main__:FINISHED
	root@4838e2e5bdf5:/data# python3 sum2bands_gdal.py JP2OpenJPEG
	INFO:__main__:running: JP2OpenJPEG 1
	INFO:__main__:running: JP2OpenJPEG 2
	INFO:__main__:running: JP2OpenJPEG 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [19.58059859275818, 9.911508798599243, 0, 5.525509595870972]
	INFO:__main__:proc: [0.5140869617462158, 0.4688699245452881, 0, 0.4384160041809082]
	INFO:__main__:write:[28.41798186302185, 28.325867652893066, 0, 29.18376398086548]
	INFO:__main__:FINISHED
 
 Results:
 
 * Reading: it is parallelized in both cases. 
   * JP2KAK is faster but the scaling is non-linear. 
   * JP2OpenJPG scales linearly but slower up to 4 cores, when it catches up with JP2KAK.
   * TBD: investigate if on 8/16 cores JP2OpenJPEG catches up with JP2KAK or both converges to a constant time.
 * Processing: JP2KAK is slightly faster
   * Since in this case processing is virtually just providing numpy arrays through GDAL, it is believed that this difference is negligible during a real scenario (when business logic incurs CPU load GDAL).  
 * Writing: JP2KAK is consistently 2x faster, however both drivers implement serial save.
 
 
 
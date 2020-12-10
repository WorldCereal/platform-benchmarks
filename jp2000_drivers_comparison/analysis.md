# Comparison of Kakadu and OpenJPEG-2000 drivers in different environments

This study was conducted in order to assess which driver is more suitable for future cloud deployments. 
The primary interest is estimate best approach to read jpeg2000 images.

The report is broken into three different performance analises:

* using files from a local hard drive
* using a collection on CreoDIAS
* using SentinelHub on Amazon AWS

Global conditions:

* the same docker image was used in all scenarios to ensure the exact same versions of Kakadu, OpenJPEG, GDAL, ...
* the same bash and python codes (with minor changes due to the environments) were used, all committed in this repository. 
* all machines/instances had 4 cores

## local computer performance

For this purpose a stripped down NDVI calculator was borrowed:

* simple Python code, uses gdal directly
* NDVI code is replaced by simple calculation of returning half of the source image 
* timings were separately measured for read/process/write
* read/write is aligned with the block size
* Kakadu writer is forced to use the same block sizes as the input (did not have noticable effect at the end)

The testbed simulated ideal conditions (which was the laptop of the author): fast access SSD hard drive/16GB RAM/quad core CPU.

Consecutive runs gave consistent results both for Kakadu (JP2KAK), these are representative results:

	root@4838e2e5bdf5:/data# python3 perf.py JP2KAK
	INFO:__main__:running: JP2KAK 1
	INFO:__main__:running: JP2KAK 2
	INFO:__main__:running: JP2KAK 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [9.775216579437256, 6.576526403427124, 0, 4.595564842224121]
	INFO:__main__:proc: [0.423048734664917, 0.45554208755493164, 0, 0.4442315101623535]
	INFO:__main__:write:[17.652412176132202, 17.160632133483887, 0, 17.12736439704895]
	INFO:__main__:FINISHED

 and Open JPEG (JP2OpenJPEG):
 
	root@4838e2e5bdf5:/data# python3 perf.py JP2OpenJPEG
	INFO:__main__:running: JP2OpenJPEG 1
	INFO:__main__:running: JP2OpenJPEG 2
	INFO:__main__:running: JP2OpenJPEG 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [19.58059859275818, 9.911508798599243, 0, 5.525509595870972]
	INFO:__main__:proc: [0.5140869617462158, 0.4688699245452881, 0, 0.4384160041809082]
	INFO:__main__:write:[28.41798186302185, 28.325867652893066, 0, 29.18376398086548]
	INFO:__main__:FINISHED
 
 Interpetation:
 
 * Reading: it is parallelized in both cases. 
   * JP2KAK is faster but the scaling is non-linear. 
   * JP2OpenJPG scales linearly but slower up to 4 cores, when it catches up with JP2KAK.
   * TBD: investigate if on 8/16 cores JP2OpenJPEG catches up with JP2KAK or both converges to a constant time.
 * Processing: JP2KAK is slightly faster
   * Since in this case processing is virtually just providing numpy arrays through GDAL, it is believed that this difference is negligible during a real scenario (when business logic incurs CPU load GDAL).  
 * Writing: JP2KAK is consistently 2x faster, however both drivers implement serial save. Save times are constant ~17s for JP2KAK and ~28s for JP2OpenJPEG
  
## Performance measurements on CreoDIAS

Two ways of accessing data was investigated:

* access object storage via S3 protocol (using /vsis3)
* access the same data through a fuse.s3fs mount
* source data was from CreoDIAS's own collection

The timing of gdal_translate commands were measured and corrected by the results of the python measurements.
The permustaions of using 1,2,4 theads and 1,2,4 consurrent gdal_translate calls were investigated.

### Eliminating write times

Since write times were nicely constant (independent of threads) for 'local' tests, the same approach was chosen. 

JP2KAK from mount:

	/data# python3 perf_mount.py JP2KAK
	INFO:__main__:running: JP2KAK 1
	INFO:__main__:running: JP2KAK 2
	INFO:__main__:running: JP2KAK 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [13.995077848434448, 9.45662784576416, 0, 7.963407516479492]
	INFO:__main__:proc: [0.664431095123291, 0.6446657180786133, 0, 0.6607530117034912]
	INFO:__main__:write:[20.82645583152771, 20.948495626449585, 0, 20.98254942893982]
	INFO:__main__:FINISHED
	
JP2KAK from S3:

	/data# python3 perf_s3.py JP2KAK
	INFO:__main__:running: JP2KAK 1
	INFO:__main__:running: JP2KAK 2
	INFO:__main__:running: JP2KAK 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [49.955512285232544, 32.89512586593628, 0, 35.25094676017761]
	INFO:__main__:proc: [0.676001787185669, 0.6587626934051514, 0, 0.6573667526245117]
	INFO:__main__:write:[21.176208019256592, 20.99274468421936, 0, 20.960272789001465]
	INFO:__main__:FINISHED
	
JP2OpenJPEG from mount:
	
	/data# python3 perf_mount.py JP2OpenJPEG
	INFO:__main__:running: JP2OpenJPEG 1
	INFO:__main__:running: JP2OpenJPEG 2
	INFO:__main__:running: JP2OpenJPEG 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [25.959946155548096, 13.44413423538208, 0, 8.327358484268188]
	INFO:__main__:proc: [0.8336594104766846, 0.8033757209777832, 0, 0.6825559139251709]
	INFO:__main__:write:[40.807082176208496, 40.64276385307312, 0, 40.397971868515015]
	INFO:__main__:FINISHED

JP2OpenJPEG from S3:

	/data# python3 perf_s3.py JP2OpenJPEG
	INFO:__main__:running: JP2OpenJPEG 1
	INFO:__main__:running: JP2OpenJPEG 2
	INFO:__main__:running: JP2OpenJPEG 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [36.577035665512085, 21.045676946640015, 0, 12.480378150939941]
	INFO:__main__:proc: [0.8308145999908447, 0.6931614875793457, 0, 0.6582307815551758]
	INFO:__main__:write:[40.72155237197876, 40.918639183044434, 0, 40.61796855926514]
	INFO:__main__:FINISHED

Interpretation:

* reading from mount is always faster than S3
* both JP2KAK and JP2OpenJPEG scales with number of threads from mount, but only openjpeg scales linearly
* JP2KAK has very degraded read performance from S3 (note that the above tests were executed multiple times, this is not a one-off but a consistently repeatable result)
* JP2OpenJPEG scales (non-linear) from S3, but the performance is also worse compared to read from mount
* write times are constant ~21s for JP2KAK and ~41s for JP2OpenJPEG

The constant write times are confirmed and it will makes eliminating write times from gdal_translate calls easy.

### gdal_translate comparison from mount

As mentioned before, permustaions of using multiple threads and consurrent calls were investigated, the column titles represent:

* [0-9]t: number of threads
* [0-9]c: concurrent gdal calls

JP2KAK:

	KAK_1t_1c, OJP_1t_1c, KAK_2t_1c, OJP_2t_1c, KAK_4t_1c, OJP_4t_1c, KAK_1t_2c, OJP_1t_2c, KAK_2t_2c, OJP_2t_2c, KAK_4t_2c, OJP_4t_2c, KAK_1t_4c, OJP_1t_4c, KAK_2t_4c, OJP_2t_4c, KAK_4t_4c, OJP_4t_4c, dummy
	38, 72, 35, 60, 34, 56, 39, 73, 36, 62, 39, 59, 56, 77, 56, 77, 54, 78, -1
	39, 72, 35, 59, 34, 55, 40, 74, 39, 60, 38, 60, 56, 77, 55, 77, 57, 80, -1
	40, 73, 36, 63, 36, 56, 43, 72, 37, 60, 38, 61, 56, 78, 54, 76, 55, 74, -1
	39, 71, 35, 60, 34, 55, 46, 74, 41, 64, 42, 62, 60, 77, 56, 75, 56, 75, -1
	39, 72, 35, 59, 34, 54, 39, 72, 38, 62, 38, 60, 56, 75, 53, 75, 57, 75, -1

JP2OpenJPEG:

	KAK_1t_1c, OJP_1t_1c, KAK_2t_1c, OJP_2t_1c, KAK_4t_1c, OJP_4t_1c, KAK_1t_2c, OJP_1t_2c, KAK_2t_2c, OJP_2t_2c, KAK_4t_2c, OJP_4t_2c, KAK_1t_4c, OJP_1t_4c, KAK_2t_4c, OJP_2t_4c, KAK_4t_4c, OJP_4t_4c, dummy
	47, 80, 42, 69, 40, 62, 50, 80, 44, 71, 45, 68, 58, 88, 59, 83, 57, 82, -1
	45, 77, 39, 70, 42, 66, 45, 84, 44, 68, 44, 68, 57, 90, 59, 88, 59, 86, -1
	57, 86, 41, 78, 40, 68, 46, 94, 47, 86, 49, 70, 63, 93, 60, 88, 57, 80, -1
	44, 77, 40, 76, 43, 60, 43, 81, 41, 71, 43, 67, 57, 84, 56, 80, 57, 89, -1
	43, 80, 40, 66, 41, 62, 44, 80, 42, 83, 43, 78, 57, 84, 56, 98, 60, 80, -1

### Intepretation

By substrating the respective write times and taking average:

Method|KAK_1t_1c|OJP_1t_1c|KAK_2t_1c|OJP_2t_1c|KAK_4t_1c|OJP_4t_1c|KAK_1t_2c|OJP_1t_2c|KAK_2t_2c|OJP_2t_2c|KAK_4t_2c|OJP_4t_2c|KAK_1t_4c|OJP_1t_4c|KAK_2t_4c|OJP_2t_4c|KAK_4t_4c|OJP_4t_4c
---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---
mount|18|31|14.2|19.2|13.4|14.2|20.4|32|17.2|20.6|18|19.4|35.8|35.8|33.8|35|34.8|35.4
s3|26.2|39|19.4|30.8|20.2|22.6|24.6|42.8|22.6|34.8|23.8|29.2|37.4|46.8|37|46.4|37|42.4

These are the approximate read times. Interpretation:

* reading from mount is always faster
* JP2KAK is always faster, however at high concurrency scenarios the performances converge to each other. It is believed to be the saturation of the network bandwidth.

Note 1.: on Creo it seems to be very important to control the number of threads being used.

Note 2.: although the mount approach looks more advantegous, but it can be easily overloaded (by experience using 8 or more concurrent executions). 
In that case the mount freezes indefinitely. With S3 approach this was tested up to 32 concurrent processes and it proved stable (but increasingly slow of course).

## Performance measurements on CreoDIAS

The same techniques was used as for Creo, except only S3 access was investigated.

Source data was from Sinergise S3 buckets, accessing from an instance in the same region (EU-1 Frankfurt).

Python timings for write elmination with JP2KAK and JP2OpenJPEG (~18s and ~30s):

	/data# python3 perf.py JP2OpenJPEG
	INFO:__main__:running: JP2OpenJPEG 1
	INFO:__main__:running: JP2OpenJPEG 2
	INFO:__main__:running: JP2OpenJPEG 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [24.968525409698486, 13.470046281814575, 0, 10.258373975753784]
	INFO:__main__:proc: [0.4264047145843506, 0.3739304542541504, 0, 0.34997129440307617]
	INFO:__main__:write:[30.17921733856201, 30.167754411697388, 0, 30.139368534088135]
	INFO:__main__:FINISHED

	/data# python3 perf.py JP2KAK
	INFO:__main__:running: JP2KAK 1
	INFO:__main__:running: JP2KAK 2
	INFO:__main__:running: JP2KAK 4
	INFO:__main__:threads: [1, 2, 0, 4]
	INFO:__main__:read: [24.376023054122925, 21.33298921585083, 0, 20.435287475585938]
	INFO:__main__:proc: [0.36097192764282227, 0.36220383644104004, 0, 0.3582289218902588]
	INFO:__main__:write:[18.171226978302002, 18.17037320137024, 0, 18.168445825576782]
	INFO:__main__:FINISHED

With the same permutation leading to:

	KAK_1t_1c, OJP_1t_1c, KAK_2t_1c, OJP_2t_1c, KAK_4t_1c, OJP_4t_1c, KAK_1t_2c, OJP_1t_2c, KAK_2t_2c, OJP_2t_2c, KAK_4t_2c, OJP_4t_2c, KAK_1t_4c, OJP_1t_4c, KAK_2t_4c, OJP_2t_4c, KAK_4t_4c, OJP_4t_4c, dummy
	34, 59, 33, 48, 32, 45, 38, 60, 37, 53, 38, 51, 59, 80, 59, 80, 60, 80, -1
	35, 59, 33, 48, 33, 45, 38, 59, 37, 54, 38, 51, 59, 81, 59, 81, 60, 81, -1
	34, 59, 32, 50, 31, 46, 38, 60, 37, 53, 38, 51, 59, 82, 59, 80, 60, 80, -1
	35, 59, 32, 49, 32, 46, 38, 59, 37, 52, 38, 51, 59, 81, 59, 80, 59, 79, -1
	34, 58, 33, 49, 32, 45, 38, 60, 37, 53, 37, 52, 59, 81, 59, 78, 60, 80, -1

And the corrected (write substract) average:

Method|KAK_1t_1c|OJP_1t_1c|KAK_2t_1c|OJP_2t_1c|KAK_4t_1c|OJP_4t_1c|KAK_1t_2c|OJP_1t_2c|KAK_2t_2c|OJP_2t_2c|KAK_4t_2c|OJP_4t_2c|KAK_1t_4c|OJP_1t_4c|KAK_2t_4c|OJP_2t_4c|KAK_4t_4c|OJP_4t_4c
---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---
AWS/S3|16.4|28.8|14.6|18.8|14|15.4|20|29.6|19|23|19.8|21.2|41|51|41|49.8|41.8|50

Interpretation:

* same conclusions as for Creo/mount

## Summary

Putting the the timings of the read operations (pulling the same jpeg-2000 image from Sentinel-2 collection on different clouds) together:

Method|KAK_1t_1c|OJP_1t_1c|KAK_2t_1c|OJP_2t_1c|KAK_4t_1c|OJP_4t_1c|KAK_1t_2c|OJP_1t_2c|KAK_2t_2c|OJP_2t_2c|KAK_4t_2c|OJP_4t_2c|KAK_1t_4c|OJP_1t_4c|KAK_2t_4c|OJP_2t_4c|KAK_4t_4c|OJP_4t_4c
---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---
Creo/mount|18|31|14.2|19.2|13.4|14.2|20.4|32|17.2|20.6|18|19.4|35.8|35.8|33.8|35|34.8|35.4
Creo/S3|26.2|39|19.4|30.8|20.2|22.6|24.6|42.8|22.6|34.8|23.8|29.2|37.4|46.8|37|46.4|37|42.4
AWS/S3|16.4|28.8|14.6|18.8|14|15.4|20|29.6|19|23|19.8|21.2|41|51|41|49.8|41.8|50

Interpretation:

* AWS S3 is in par with Creo mount, sometimes higher, sometimes lower 
* CreoDIAS S3 is very slow, probable reason: CreoDIAS uses an older SWIFT backend to serve S3
* Kakadu seems to be faster when using one thread per core, however JP2OpenJPEG is better parallelized for multithreading.

Todo:

* Check bandwidth saturation/more concurrency on bigger instances
* What happens when attaching more network interfaces



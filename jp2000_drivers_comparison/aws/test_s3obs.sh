#!/bin/bash

$1: sublogfilename
$2: use_driver
$3: gdal_skip
$4: threads
$5: nconcurrent
function measure_gdal_translate(){

  echo "$@"  

  export AWS_REQUEST_PAYER=requester

  logfile=$1
  echo -n "" > $logfile
  shift

  driver=$1
  echo "DRIVER=$driver" >> $logfile
  shift

  export GDAL_SKIP=$1
  shift

  export JP2KAK_THREADS=$1
  export GDAL_NUM_THREADS=$1
  shift

  env | grep _THREADS >> $logfile
  env | grep _SKIP >> $logfile

  nconcurrent=$1
  shift
  echo "NUM_CONCURRENT_GDAL_TRANSLATES=$nconcurrent" >> $logfile

  #srcfile=/vsis3/eodata/Sentinel-2/MSI/L2A/2019/01/01/S2A_MSIL2A_20190101T082331_N0211_R121_T36SYC_20190101T094029.SAFE/GRANULE/L2A_T36SYC_A018422_20190101T082935/IMG_DATA/R10m/T36SYC_20190101T082331_B02_10m.jp2
  srcfile=/vsis3/sentinel-s2-l2a/tiles/36/S/YC/2018/1/11/0/R10m/B02.jp2

  start=$(date +%s)
  for (( iproc=1; iproc<=$nconcurrent; iproc++ )) ; do  
    if (( "$iproc" == "$nconcurrent" )) ; then 
      echo "PROC $iproc REPORTS IN" >> $logfile
      gdal_translate -co BLOCKXSIZE=1024 -co BLOCKYSIZE=1024 -of $driver $srcfile out_$iproc.jp2 >> $logfile 2>&1
    else
      echo "PROC $iproc REPORTS IN" >> $logfile
      gdal_translate -co BLOCKXSIZE=1024 -co BLOCKYSIZE=1024 -of $driver $srcfile out_$iproc.jp2 >> $logfile 2>&1 &
    fi
  done
  end=$(date +%s)
  echo -n "$(( $end - $start )), " >> timings_s3obs.csv

  echo "FINISHED IN $(( $end - $start )) SECONDS" >> $logfile
}

echo -n "" > timings_s3obs.csv
echo -n "KAK_1t_1c, OJP_1t_1c, KAK_2t_1c, OJP_2t_1c, KAK_4t_1c, OJP_4t_1c, " >> timings_s3obs.csv
echo -n "KAK_1t_2c, OJP_1t_2c, KAK_2t_2c, OJP_2t_2c, KAK_4t_2c, OJP_4t_2c, " >> timings_s3obs.csv
echo -n "KAK_1t_4c, OJP_1t_4c, KAK_2t_4c, OJP_2t_4c, KAK_4t_4c, OJP_4t_4c, " >> timings_s3obs.csv
#echo -n "KAK_1t_8c, OJP_1t_8c, KAK_1t_16c, OJP_1t_16c, " >> timings_s3obs.csv
echo "dummy" >> timings_s3obs.csv

for i in {1..5} ; do

  # source file is 130MB for network speed
  # note the opposite driver needs to be passed in because that is the option which driver to blacklist
  measure_gdal_translate log_s3_kakadu_1thread_1concurrent.txt JP2KAK      JP2OpenJPEG 1 1
  measure_gdal_translate log_s3_openjp_1thread_1concurrent.txt JP2OpenJPEG JP2KAK      1 1

  measure_gdal_translate log_s3_kakadu_2thread_1concurrent.txt JP2KAK      JP2OpenJPEG 2 1
  measure_gdal_translate log_s3_openjp_2thread_1concurrent.txt JP2OpenJPEG JP2KAK      2 1
  measure_gdal_translate log_s3_kakadu_4thread_1concurrent.txt JP2KAK      JP2OpenJPEG 4 1
  measure_gdal_translate log_s3_openjp_4thread_1concurrent.txt JP2OpenJPEG JP2KAK      4 1

  measure_gdal_translate log_s3_kakadu_1thread_2concurrent.txt JP2KAK      JP2OpenJPEG 1 2
  measure_gdal_translate log_s3_openjp_1thread_2concurrent.txt JP2OpenJPEG JP2KAK      1 2
  measure_gdal_translate log_s3_kakadu_2thread_2concurrent.txt JP2KAK      JP2OpenJPEG 2 2
  measure_gdal_translate log_s3_openjp_2thread_2concurrent.txt JP2OpenJPEG JP2KAK      2 2
  measure_gdal_translate log_s3_kakadu_4thread_2concurrent.txt JP2KAK      JP2OpenJPEG 4 2
  measure_gdal_translate log_s3_openjp_4thread_2concurrent.txt JP2OpenJPEG JP2KAK      4 2

  measure_gdal_translate log_s3_kakadu_1thread_4concurrent.txt JP2KAK      JP2OpenJPEG 1 4
  measure_gdal_translate log_s3_openjp_1thread_4concurrent.txt JP2OpenJPEG JP2KAK      1 4
  measure_gdal_translate log_s3_kakadu_2thread_4concurrent.txt JP2KAK      JP2OpenJPEG 2 4
  measure_gdal_translate log_s3_openjp_2thread_4concurrent.txt JP2OpenJPEG JP2KAK      2 4
  measure_gdal_translate log_s3_kakadu_4thread_4concurrent.txt JP2KAK      JP2OpenJPEG 4 4
  measure_gdal_translate log_s3_openjp_4thread_4concurrent.txt JP2OpenJPEG JP2KAK      4 4

  echo "-1" >> timings_s3obs.csv

done

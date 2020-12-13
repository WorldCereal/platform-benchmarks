#!/bin/bash

$1: sublogfilename
$4: threads
$5: nconcurrent
function measure_kdu_expand(){

  echo "$@"  

  #export AWS_REQUEST_PAYER=requester
  export CPL_DEBUG=OFF
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../kakadu-8.0.3/lib/Linux-x86-64-gcc
  export PATH=$PATH:../kakadu-8.0.3/bin/Linux-x86-64-gcc

  logfile=$1
  echo -n "" > $logfile
  shift

  nthreads=$1
  export JP2KAK_THREADS=$1
  export GDAL_NUM_THREADS=$1
  shift

  env | grep _THREADS >> $logfile
  env | grep _SKIP >> $logfile

  nconcurrent=$1
  shift
  echo "NUM_CONCURRENT_kdu_expandS=$nconcurrent" >> $logfile

  srcfile=/eodata/Sentinel-2/MSI/L2A/2019/01/01/S2A_MSIL2A_20190101T082331_N0211_R121_T36SYC_20190101T094029.SAFE/GRANULE/L2A_T36SYC_A018422_20190101T082935/IMG_DATA/R10m/T36SYC_20190101T082331_B02_10m.jp2
  #srcfile=/vsis3/eodata/Sentinel-2/MSI/L2A/2019/01/01/S2A_MSIL2A_20190101T082331_N0211_R121_T36SYC_20190101T094029.SAFE/GRANULE/L2A_T36SYC_A018422_20190101T082935/IMG_DATA/R10m/T36SYC_20190101T082331_B02_10m.jp2
  #srcfile=/vsis3/sentinel-s2-l2a/tiles/36/S/YC/2018/1/11/0/R10m/B02.jp2

  start=$(date +%s)
  for (( iproc=1; iproc<=$nconcurrent; iproc++ )) ; do  
    if (( "$iproc" == "$nconcurrent" )) ; then 
      echo "PROC $iproc REPORTS IN" >> $logfile
      kdu_buffered_expand -i $srcfile -cpu -num_threads $nthreads >> $logfile 2>&1
    else
      echo "PROC $iproc REPORTS IN" >> $logfile
      kdu_buffered_expand -i $srcfile -cpu -num_threads $nthreads >> $logfile 2>&1 &
    fi
  done
  end=$(date +%s)
  echo -n "$(( $end - $start )), " >> timings_kdu_mounted.csv

 # cat $logfile | grep End-to-end | sed -E 's/.* ([0-9]+\.[0-9]+).*/\1/g' | head -n 1 >> timings_kdu_mounted.csv
  #cat $logfile | grep End-to-end | sed -E 's/.* ([0-9]+\.[0-9]+).*/\1/g' | tail -n 1 >> timings_kdu_mounted.csv

  echo "FINISHED IN $(( $end - $start )) SECONDS" >> $logfile
}

echo -n "" > timings_kdu_mounted.csv
echo -n "KAK_MIN_1t_1c, KAK_MAX_1t_1c, KAK_MIN_2t_1c, KAK_MAX_2t_1c, KAK_MIN_4t_1c, KAK_MAX_4t_1c, " >> timings_kdu_mounted.csv
echo -n "KAK_MIN_1t_2c, KAK_MAX_1t_2c, KAK_MIN_2t_2c, KAK_MAX_2t_2c, KAK_MIN_4t_2c, KAK_MAX_4t_2c, " >> timings_kdu_mounted.csv
echo -n "KAK_MIN_1t_4c, KAK_MAX_1t_4c, KAK_MIN_2t_4c, KAK_MAX_2t_4c, KAK_MIN_4t_4c, KAK_MAX_4t_4c, " >> timings_kdu_mounted.csv
#echo -n "KAK_MIN_1t_8c, KAK_MAX_1t_8c, KAK_MIN_1t_16c, KAK_MAX_1t_16c, " >> timings_kdu_mounted.csv
echo "dummy" >> timings_kdu_mounted.csv

for i in {1..5} ; do

  # source file is 130MB for network speed
  # note the opposite driver needs to be passed in because that is the option which driver to blacklist
  measure_kdu_expand log_kdu_mounted_native_1thread_1concurrent_$i.txt 1 1
  measure_kdu_expand log_kdu_mounted_native_2thread_1concurrent_$i.txt 2 1
  measure_kdu_expand log_kdu_mounted_native_4thread_1concurrent_$i.txt 4 1

  measure_kdu_expand log_kdu_mounted_native_1thread_2concurrent_$i.txt 1 2
  measure_kdu_expand log_kdu_mounted_native_2thread_2concurrent_$i.txt 2 2
  measure_kdu_expand log_kdu_mounted_native_4thread_2concurrent_$i.txt 4 2

  measure_kdu_expand log_kdu_mounted_native_1thread_4concurrent_$i.txt 1 4
  measure_kdu_expand log_kdu_mounted_native_2thread_4concurrent_$i.txt 2 4
  measure_kdu_expand log_kdu_mounted_native_4thread_4concurrent_$i.txt 4 4

# THIS BREAKS THE MOUNT
#  measure_kdu_expand log_kdu_mounted_native_1thread_8concurrent_$i.txt JP2KAK      JP2OpenJPEG 1 8
#  measure_kdu_expand log_kdu_mounted_native_1thread_16concurrent_$i.txt JP2KAK      JP2OpenJPEG 2 16

  echo "-1" >> timings_kdu_mounted.csv

done

from pathlib import Path
import time
import numpy as np
import openeo
import geopandas as gpd
from ast import literal_eval
connection = openeo.connect("https://openeo-dev.vito.be")
connection.authenticate_basic("driesj","driesj123")

samplespath = Path(__file__).parent.parent / "testdata" / "31UFS_LPISsamples.geojson"

samples_df = gpd.read_file(samplespath)

cube = connection.load_collection("TERRASCOPE_S2_TOC_V2",temporal_extent=["2018-09-01T00:00:00Z","2019-11-30T00:00:00Z"],bands=['TOC-B02_10M','TOC-B03_10M','TOC-B04_10M'])
timings = np.array([],dtype=np.float)
for row in samples_df.iterrows():

    start = time.time()
    bounds = literal_eval(row[1].bounds)
    epsg = row[1].epsg
    print(row[1].sampleID)
    cube.filter_bbox(west=float(bounds[0]),east=float(bounds[2]),north=float(bounds[3]),south=float(bounds[1]),crs="EPSG:" + str(epsg))\
     .download("S2_L2A_10m_%s_%s_2018-09-01_2019-11-30.nc"%(row[1].sampleID,str(epsg)),format="NetCDF",options={"tiled":False})
    end = time.time()
    elapsed = end - start
    timings = np.append(timings, [elapsed])
    print("%.1f - average: %.1f " %(elapsed,np.average(timings)))

    with open('timinigs.csv','a') as t:
        t.write(str(elapsed) + '\n')




#cube.download("out.nc",format="NetCDF")

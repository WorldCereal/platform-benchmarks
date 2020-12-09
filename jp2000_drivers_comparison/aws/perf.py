'''
Created on Dec 8, 2020

@author: banyait
'''
import logging
import time
import uuid
from osgeo import gdal
from osgeo import gdalnumeric
from osgeo import gdalconst
from osgeo.gdalconst import GDT_UInt16
import sys


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    use_driver=sys.argv[1] #'JP2OpenJPEG','JP2KAK'

    red_filename='/vsis3/sentinel-s2-l2a/tiles/36/S/YC/2018/1/11/0/R10m/B02.jp2'
    out_filename='out_'+uuid.uuid4().hex+".tif"
    
    ncores=[0]*4
    tread=[0]*4
    tprocess=[0]*4
    twrite=[0]*4

    drivers=set(('JP2OpenJPEG','JPEG','JPEG2000','JP2KAK'))
    drivers.remove(use_driver)
    for idriver in drivers:
        idr=gdal.GetDriverByName(idriver)
        if idr is not None:
            idr.Deregister()
    gdal.SetConfigOption('CPL_DEBUG', 'OFF')


    for nthread in [1,2,4]:

        ncores[nthread-1]=nthread

        logger.info("running: "+use_driver+" "+str(nthread))
    
        gdal.SetConfigOption('JP2KAK_THREADS', str(nthread))
        gdal.SetConfigOption('GDAL_NUM_THREADS', str(nthread))

        t0=time.time()
    
        red_ds = gdal.Open(red_filename)
        red_band = red_ds.GetRasterBand(1)
        red_xbs,red_ybs = red_band.GetBlockSize()
        
    #    driver = gdal.GetDriverByName(use_driver)
    #     ndvi_ds = driver.Create(out_filename,
    #                             red_ds.RasterXSize, red_ds.RasterYSize,
    #                             1, gdal.GDT_Byte,
    #                             options=['COMPRESS=DEFLATE', 'TILED=YES'])
        ndvi_ds = gdal.GetDriverByName('MEM').Create('',
                                red_ds.RasterXSize, red_ds.RasterYSize,
                                1, GDT_UInt16) 
    
        ndvi_band = ndvi_ds.GetRasterBand(1)
                    
        xbs=(int)(red_xbs)
        ybs=(int)(red_ybs)
        xsize=(int)(red_ds.RasterXSize)
        ysize=(int)(red_ds.RasterYSize)
        tilesx = (int)(xsize//xbs)
        if (tilesx*xbs!=xsize): tilesx=tilesx+1
        tilesy = (int)(ysize//ybs)
        if (tilesy*ybs!=ysize): tilesy=tilesy+1
        
        t1=time.time()
        
        tread[nthread-1]+=t1-t0
        
        for itx in range(0,tilesx*xbs,xbs):
            for ity in range(0,tilesy*ybs,ybs):
                _xbs=xbs if itx+xbs<xsize else xsize-itx
                _ybs=ybs if ity+ybs<ysize else ysize-ity
                
                t2=time.time()
                
                red_array = gdalnumeric.BandReadAsArray(red_band, 
                    xoff=itx,
                    yoff=ity,
                    win_xsize=_xbs,
                    win_ysize=_ybs,
                    buf_type=gdalconst.GDT_UInt16)
    
                t3=time.time()
    
                ndvi_array = red_array*0.5 
                
                ndvi_band.WriteArray(ndvi_array, xoff=itx, yoff=ity)
    
                ndvi_array = None
    
                t4=time.time()
                
                tread[nthread-1]+=t3-t2
                tprocess[nthread-1]+=t4-t3
    
        t5=time.time()
                
        ndvi_ds.SetGeoTransform(red_ds.GetGeoTransform())
        ndvi_ds.SetProjection(red_ds.GetProjection())
        ndvi_ds.FlushCache()
        
    #     if (data.create_cog):
    #         # create COG
    #         subprocess.call(["gdaladdo", '-r', 'average', out_filename, '2', '4', '8', '16', '32'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #         # in order to generate a valid COG, we need to add this GDAL translate step:
    #         # https://trac.osgeo.org/gdal/wiki/CloudOptimizedGeoTIFF
    #         ds = gdal.Open(out_filename)
    #         ds = gdal.Translate(out_file, ds, creationOptions=['COMPRESS=DEFLATE', 'TILED=YES', 'COPY_SRC_OVERVIEWS=YES'])
    #         ds = None
    
    
        t6=time.time()
    
        tprocess[nthread-1]+=t6-t5
    
        gdal.GetDriverByName(use_driver).CreateCopy(out_filename, ndvi_ds, options=['BLOCKXSIZE='+str(xbs),'BLOCKYSIZE='+str(ybs)])
    
    
        t7=time.time()
        
        twrite[nthread-1]+=t7-t6
        
    logger.info('threads: '+str(ncores))
    logger.info('read: '+str(tread))
    logger.info('proc: '+str(tprocess))
    logger.info('write:'+str(twrite))
    logger.info('FINISHED')

        
          
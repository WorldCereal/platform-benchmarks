import json
import logging
import pathlib
import sys
import time
from pprint import pprint

import otbApplication as otb
import rasterio

TEST_FILE = "/eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff"

basename = pathlib.Path(__file__).stem
log = logging.getLogger(basename)


def process(input_file, output_file, bbox):
    log.info("input file {t}".format(t=input_file))
    log.info("bbox {b}".format(b=bbox))
    west, south, east, north = bbox

    log.info("Setting up ExtractROI application")
    extractROI = otb.Registry.CreateApplication("ExtractROI")
    extractROI.SetParameterString("in", input_file)
    extractROI.SetParameterString("mode", "extent")
    extractROI.SetParameterString("mode.extent.unit", "lonlat")
    extractROI.SetParameterFloat("mode.extent.ulx", west)
    extractROI.SetParameterFloat("mode.extent.uly", south)
    extractROI.SetParameterFloat("mode.extent.lrx", east)
    extractROI.SetParameterFloat("mode.extent.lry", north)
    extractROI.Execute()

    log.info("Setting up SARCalibration application")
    SARCalibration = otb.Registry.CreateApplication('SARCalibration')
    SARCalibration.SetParameterInputImage("in", extractROI.GetParameterOutputImage("out"))
    SARCalibration.SetParameterValue('noise', True)
    SARCalibration.SetParameterInt('ram', 512)
    SARCalibration.Execute()

    log.info("Setting up OrthoRectification application")
    OrthoRect = otb.Registry.CreateApplication('OrthoRectification')
    OrthoRect.SetParameterInputImage("io.in", SARCalibration.GetParameterOutputImage("out"))
    # TODO?
    # OrthoRect.SetParameterString("elev.dem", "/home/driesj/dems")
    # OrthoRect.SetParameterString("elev.geoid", "/home/driesj/egm96.grd")
    OrthoRect.SetParameterValue("map.utm.northhem", True)
    OrthoRect.SetParameterInt("map.epsg.code", 32631)
    OrthoRect.SetParameterFloat("outputs.spacingx", 10.0)
    OrthoRect.SetParameterFloat("outputs.spacingy", -10.0)
    OrthoRect.SetParameterString("interpolator", "nn")
    OrthoRect.SetParameterFloat("opt.gridspacing", 40.0)
    OrthoRect.SetParameterInt("opt.ram", 512)
    OrthoRect.Execute()
    OrthoRect.SetParameterString("io.out", output_file)

    log.info("ExecuteAndWriteOutput")
    OrthoRect.ExecuteAndWriteOutput()
    return output_file


def get_image_size(filename):
    with rasterio.open(filename) as ds:
        return ds.width, ds.height


def main():
    logging.basicConfig(level=logging.INFO)

    input_file = TEST_FILE

    west, south, east, north = 2, 50, 5, 52
    N = 8
    # west, south, east, north = 3, 50.5, 4, 51.5
    # N = 3

    bboxes = [
        (west + u * (east - west), south + u * (north - south), east - u * (east - west), north - u * (north - south))
        for u in [n / (2.0 * N) for n in range(N)]
    ]
    log.info("bounding boxes: {b}".format(b=bboxes))

    all_stats = []
    for bbox in bboxes:
        output_file = basename + "-%.3f-%.3f-%.3f-%.3f.tiff" % bbox
        log.info("bbox {b} output file {o}".format(b=bbox, o=output_file))

        start = time.time()
        process(input_file=input_file, output_file=output_file, bbox=bbox)
        end = time.time()

        elapsed = end - start
        size = get_image_size(output_file)
        stats = {"bbox": bbox, "size": size, "elapsed": elapsed}
        print("stats", stats)
        all_stats.append(stats)

    print("All stats:")
    pprint(all_stats)
    json.dump(all_stats, fp=sys.stdout)


if __name__ == '__main__':
    main()

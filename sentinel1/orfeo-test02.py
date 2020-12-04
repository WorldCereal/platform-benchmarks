import logging
import sys

import otbApplication as otb

TEST_FILE = "/eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff"

log = logging.getLogger("")


def main(test_file=TEST_FILE, output_file="orfeo-test02.tiff"):
    logging.basicConfig(level=logging.INFO)
    log.info("test file {t}".format(t=test_file))
    # http://bboxfinder.com/#51.300000,3.150000,51.370000,3.250000
    west, south, east, north = 3.15, 51.3, 3.25, 51.37
    log.info("bbox {b}".format(b=(west, south, east, north)))

    log.info("Setting up ExtractROI application")
    extractROI = otb.Registry.CreateApplication("ExtractROI")
    extractROI.SetParameterString("in", test_file)
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


if __name__ == '__main__':
    main(*sys.argv[1:])

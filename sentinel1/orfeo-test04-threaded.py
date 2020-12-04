import logging
import threading
import time

import otbApplication as otb

log = logging.getLogger()


def process(input_file, output_file, bbox):
    log.info("process: input file {t}".format(t=input_file))
    log.info("process: output file {t}".format(t=output_file))
    log.info("process: bbox {b}".format(b=bbox))
    west, south, east, north = bbox

    start = time.time()
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

    extractROI.SetParameterString("out", output_file)
    extractROI.ExecuteAndWriteOutput()
    end = time.time()

    return {"output_file": output_file, "bbox": bbox, "elapsed": end - start}


class ProcessThread(threading.Thread):
    def __init__(self, input_file, bbox):
        super().__init__()
        self.input_file = input_file
        self.bbox = bbox

    def run(self):
        output_file = "orfeo-test04-%.3f-%.3f-%.3f-%.3f.tiff" % self.bbox
        return process(input_file=self.input_file, output_file=output_file, bbox=self.bbox)


def main():
    logging.basicConfig(level=logging.INFO)

    input_file = "/eodata/Sentinel-1/SAR/GRD/2020/10/04/S1B_IW_GRDH_1SDV_20201004T060621_20201004T060646_023659_02CF3D_593D.SAFE/measurement/s1b-iw-grd-vh-20201004t060621-20201004t060646-023659-02cf3d-002.tiff"

    log.info("Creating thread 1")
    thread1 = ProcessThread(input_file=input_file, bbox=(3, 50, 4, 50.5))

    log.info("Creating thread 2")
    thread2 = ProcessThread(input_file=input_file, bbox=(3, 51, 4, 51.5))

    log.info("Starting thead1")
    thread1.start()
    log.info("Starting thread2")
    thread2.start()

    log.info("sleep")
    time.sleep(5)

    log.info("Join thead1")
    thread1.join()
    log.info("Join thread2")
    thread2.join()


if __name__ == '__main__':
    main()

import numpy as np
import andor_wrapper as aw

aw.initialize('/usr/local/etc/andor')
aw.setAcquisitionMode(1)
aw.setExposureTime(0.1)

dim = aw.getDetector()

aw.setShutter(1, 0, 50, 50)
aw.setImage(1, 1, 1, dim[0], 1, dim[1])

aw.startAcquisition()

camera_status = aw.getStatus()
while (status == 20072):
    camera_status = aw.getStatus()

image_data = aw.getAcquiredData(dim)

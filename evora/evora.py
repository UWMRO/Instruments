from evora import andor

class Evora(object):
    """
    This class executes the driver code through the "andor" import which is "swigged" C++ code.

    Replace all the prints with a safe call method.
    """
    def __init__(self):
        self.num = 0
        # parse config
        # self.config = ConfigParser.ConfigParser()
        # self.config.read(config_path)

    def getStatus(self):
        """
        No input needed. Returns an integer value representing the camera status.  E.g. 20075 means
        the camera is uninitialized.
        """
        # if the first status[0] is 20075 then the camera is not initialized yet and
        # one needs to run the startup method.
        status = andor.GetStatus()
        return "status " + str(status[0]) + "," + str(status[1])

    def startup(self):
        """
        20002 is the magic number.  Any different number and it didn't work.
        """
        # logger.debug(str(andor.GetAvailableCameras()))
        andor.GetAvailableCameras()
        camHandle = andor.GetCameraHandle(0)
        # logger.debug(str(camHandle))

        # logger.debug('set camera: ' + str(andor.SetCurrentCamera(camHandle[1])))
        andor.SetCurrentCamera(camHandle[1])

        init = andor.Initialize("/usr/local/etc/andor")

        # logger.debug('Init: ' + str(init))

        state = andor.GetStatus()

        # logger.debug('Status: ' + str(state))

        # logger.debug('SetAcquisitionMode: ' + str(andor.SetAcquisitionMode(1)))
        andor.SetAcquisitionMode(1)

        # logger.debug('SetShutter: ' + str(andor.SetShutter(1, 0, 50, 50)))
        andor.SetShutter(1, 0, 50, 50)

        # make sure cooling is off when it first starts
        # logger.debug('SetTemperature: ' + str(andor.SetTemperature(0)))
        andor.SetTemperature(0)
        # logger.debug('SetFan ' + str(andor.SetFanMode(0)))
        andor.SetFanMode(0)
        # logger.debug('SetCooler ' + str(andor.CoolerOFF()))
        andor.CoolerOFF()

        return "connect " + str(init)

    def getTEC(self):
        """
        Gets the TEC status by calling andor.GetTemperatureF
        """
        # index on [result[0] - andor.DRV_TEMPERATURE_OFF]
        coolerStatusNames = ('Off', 'NotStabilized', 'Stabilized',
                             'NotReached', 'OutOfRange', 'NotSupported',
                             'WasStableNowDrifting')

        # 20037 is NotReached
        # 20035 is NotStabalized
        # 20036 is Stabalized
        # 20034 is Off

        result = andor.GetTemperatureF()
        # res = coolerStatusNames[result[0] - andor.DRV_TEMPERATURE_OFF]
        # logger.debug(
        #   str(coolerStatusNames[result[0] - andor.DRV_TEMPERATURE_OFF]) + " " + str(result[1]))

        return_res = "getTEC " + str(result[0]) + "," + str(result[1])
        return return_res

    def setTEC(self, setPoint=None):
        """
        Turns on TEC and sets the temperature with andor.SetTemperature
        """
        result = andor.GetTemperatureF()
        # logger.debug(str(result))

        # logger.debug(str(setPoint))

        if setPoint is not None:
            if result[0] == andor.DRV_TEMPERATURE_OFF:
                andor.CoolerON()
            # logger.debug(str(andor.SetTemperature(int(setPoint))))
        return "setTEC " + str(setPoint)

    def warmup(self):
        """
        Pre: Used to warmup camera.
        Post: Sets the temperature to 0 and turns the fan to 0 then turns the cooler off and
        returns 1 that everything worked.
        """
        # setTemp = andor.SetTemperature(0)
        setFan = andor.SetFanMode(0)
        setCooler = andor.CoolerOFF()

        results = 1
        if setFan != andor.DRV_SUCCESS or setCooler != andor.DRV_SUCCESS:
            results = 0
        return "warmup " + str(results)

    def getTemp(self):
        """
        Used to get the temperature as well as other status.
        """
        # 20037 is NotReached
        # 20035 is NotStabalized
        # 20036 is Stabalized
        # 20034 is Off
        temperature_status_names = ['sensor', 'target', 'ambient']
        cooling_status, *temperature_statuses = andor.GetTemperatureStatus()
        temperatures_by_name = dict(zip(temperature_status_names, temperature_statuses))
        temperature_measurement = andor.GetTemperatureF()
        temperatures_by_name['detector'] = temperature_measurement[1]
        return {
            'cooling_status': temperature_measurement[0],
            'temperatures': temperatures_by_name
        }

    def getTempRange(self):
        """
        Used to get the range of temperature, in C, that the hardware allows.
        """
        stats = andor.GetTemperatureRange()
        result = stats[0]
        mintemp = stats[1]
        maxtemp = stats[2]
        return "tempRange " + "%s,%s,%s" % (result, mintemp, maxtemp)

    def shutdown(self):
        """
        Warms up camera by turning off the cooler and then shuts down the camera.
        Future versions should have it wait till the camera is warmed up to 0 C at least.
        """

        self.warmup()
        res = self.getTemp()
        res = res.split(" ")[1].split(",")
        """
        while float(res[2]) < 0:
            time.sleep(5)
            res = self.getTemp()
            res = res.split(" ")[1].split(",")
            print('waiting: %s' % str(res[2]))
        """
        # logger.info('closing down camera connection')
        andor.ShutDown()
        return "shutdown 1"

    def getTimings(self):
        """
        Used to get the actual time in seconds the exposure will take.
        """
        # retval, width, height = andor.GetDetector()
        # print retval, width, height
        expTime, accTime, kTime = andor.GetAcquisitionTimings()
        # logger.debug(str(expTime) + " " + str(accTime) + " " + str(kTime))

        return "timings"

    def verticalSpeedStats(self, index):
        """
        Gets the vertical readout speed stats.
        """
        # logger.debug("GetNumberVSSpeeds: " + str(andor.GetNumberVSSpeeds()))
        # logger.debug("GetNumberVSAmplitudes: " + str(andor.GetNumberVSAmplitudes()))
        # logger.debug("GetVSSpeed: " + str(andor.GetVSSpeed(index)))
        # logger.debug("GetFastestRecommendedVSSpeed: " + str(andor.GetFastestRecommendedVSSpeed()))

    def horizontalSpeedStats(self, channel, type, index):
        """
        Gets the stats of the horizontal readout speed.
        """
        # logger.debug("GetNumberHSSpeeds: " + str(andor.GetNumberHSSpeeds(channel, type)))
        # logger.debug("GetHSSpeed: " + str(andor.GetHSSpeed(channel, type, index)))

    def abort(self):
        """
        This will abort the exposure and throw it out.
        """
        global isAborted
        isAborted = True
        self.isAbort = True
        # logger.debug("Aborted: " + str(andor.AbortAcquisition()))
        andor.AbortAcquisition()
        return 'abort 1'

    def getHeader(self, attributes):
        """
        Pre: Takes in a list of attributes: [imType, binning, itime]
        Post: Returns an AstroPy header object to be used for writing to.
        """
        imType, binning, itime, filter = attributes[0], attributes[
            1], attributes[2], attributes[3]
        # make new fits header object
        header = fits.Header()
        ut_time = time.gmtime()  # get UT time
        dateObs = time.strftime("%Y-%m-%dT%H:%M:%S", ut_time)
        ut_str = time.strftime("%H:%M:%S", ut_time)
        header.append(card=("DATE-OBS", dateObs, "Time at start of exposure"))
        header.append(card=("UT", ut_str, "UT time at start of exposure"))
        header.append(card=("OBSERVAT", "mro", "per the iraf list"))
        header.append(card=("IMAGETYP", imType))
        header.append(card=("FILTER", filter))
        header.append(card=("BINX", binning, "Horizontal Binning"))
        header.append(card=("BINY", binning, "Vertical Binning"))
        header.append(card=("EXPTIME", itime, "Total exposure time"))
        header.append(card=("ACQMODE", "Single Scan", "Acquisition mode"))
        header.append(card=("READMODE", "Image", "Readout mode"))
        header.append(card=("INSTRUME", "evora",
                            "Instrument used for imaging"))
        header.append(card=("LATITUDE", 46.9511,
                            "Decimal degrees of MRO latitude"))
        header.append(card=("LONGITUD", -120.7245,
                            "Decimal degress of MRO longitude"))

        # get readout time and temp
        temp = andor.GetTemperatureStatus()[1]
        readTime = andor.GetAcquisitionTimings()[3] - itime
        header.append(card=("TEMP", temp, "Temperature"))
        header.append(card=("READTIME", readTime, "Pixel readout time"))

        return header

    def getHeader_2(self, attributes, tcc):
        """
        Pre: Takes in a list of attributes: [imType, binning, itime], tcc is ether 'gtcc' or 'heimdall'
        Post: Returns an AstroPy header object to be used for writing to.
        """
        imType, binning, itime, filter = attributes[0], attributes[
            1], attributes[2], attributes[3]
        # make new fits header object
        header = fits.Header()
        ut_time = time.gmtime()  # get UT time
        dateObs = time.strftime("%Y-%m-%dT%H:%M:%S", ut_time)
        ut_str = time.strftime("%H:%M:%S", ut_time)
        header.append(card=("DATE-OBS", dateObs, "Time at start of exposure"))
        header.append(card=("UT", ut_str, "UT time at start of exposure"))
        header.append(card=("OBSERVAT", "mro", "per the iraf list"))
        header.append(card=("IMAGETYP", imType))
        header.append(card=("FILTER", filter))
        header.append(card=("BINX", binning, "Horizontal Binning"))
        header.append(card=("BINY", binning, "Vertical Binning"))
        header.append(card=("EXPTIME", itime, "Total exposure time"))
        header.append(card=("ACQMODE", "Single Scan", "Acquisition mode"))
        header.append(card=("READMODE", "Image", "Readout mode"))
        header.append(card=("INSTRUME", "evora",
                            "Instrument used for imaging"))
        header.append(card=("LONGITUD", -120.7245,
                            "Decimal degrees of MRO latitude"))
        header.append(card=("LATITUDE", 46.9511,
                            "Decimal degress of MRO longitude"))

        # get readout time and temp
        temp = andor.GetTemperatureStatus()[1]
        readTime = andor.GetAcquisitionTimings()[3] - itime
        header.append(card=("TEMP", temp, "Temperature"))
        header.append(card=("READTIME", readTime, "Pixel readout time"))

        # NEEDED header keywords
        # Done RA / Right Ascension
        # Done DEC / Declination
        # Done EPOCH / Epoch for RA and Dec (years)
        # Done ST / local sidereal time (hours)
        # Done HA / Hour Angle
        # Done ZD / Zenith Angle
        # AIRMASS
        # UTMIDDLE
        # JD
        # HJD
        # LJD
        if tcc == "heimdall":
            obsTime = time.strptime(dateObs + " UTC", "%Y-%m-%dT%H:%M:%S %Z")
            logFileList = glob.glob(
                "/home/mro/storage/tcc_data/positionlogs/*.txt")
            file = self.heimdallChooseLogFile(logFileList, obsTime)
            if file is not None:
                results = self.heimdallParseLogFile(file, obsTime)
                if results is not None:
                    ra, dec, epoch, lst, ha, za = results

                    airmass = 1.0 / np.cos(np.radians(za))
                    # airmass = 1.0 / np.sin(np.radians((90-za) + 244/(165+47*(90-za)**1.1)))

                    astroTime = Time(dateObs, scale='utc')
                    print("FROM HEIMDALL LOGS:", results)

                    header.append(card=("RA", ra, "Right Ascension"))
                    header.append(card=("DEC", dec, "Declination"))
                    header.append(card=("EPOCH", epoch,
                                        "Epoch for RA and Dec (years)"))
                    header.append(card=("ST", lst,
                                        "local sidereal time (hours)"))
                    header.append(card=("HA", ha, "Hour Angle"))
                    header.append(card=("ZD", za, "Zenith Angle"))
                    header.append(card=("AIRMASS", airmass,
                                        "Airmass (X = sec z)"))
                    header.append(card=("JD", str(astroTime.jd),
                                        "Julian Date"))
                    header.append(card=("MJD", str(astroTime.mjd),
                                        "Modified Julian Date"))

        else:  # gtcc
            print("ACCESSING LOG FILES")
            LogfileList = glob.glob("/home/mro/mnt/gtcc" + '/????-??-??T??:??:??')
            print("FOUND %d LOGS" % len(LogfileList))
            ObsTime = time.strptime(dateObs + ' UTC', "%Y-%m-%dT%H:%M:%S %Z")
            LogfileName = self.ChooseLogfile(LogfileList, ObsTime)
            if LogfileName is not None:
                print("LOG FILE NAME:", LogfileName)
                ra, dec, epoch, lst, ha, za = self.ParseLogfile(
                    LogfileName, ObsTime)
                print(ra, dec, epoch, lst, ha, za)

                header.append(card=("RA", ra, "Right Ascension"))
                header.append(card=("DEC", dec, "Declination"))
                header.append(card=("EPOCH", epoch,
                                    "Epoch for RA and Dec (years)"))
                header.append(card=("ST", lst, "local sidereal time (hours)"))
                header.append(card=("HA", ha, "Hour Angle"))
                header.append(card=("ZD", za, "Zenith Angle"))

        return header

    def heimdallChooseLogFile(self, logFileList, obsTime):
        """
        Parameters
        ----------
        logFileList : list
                      List of path names to log files.  Log file names should be the UT date in {year/month/day}.txt
        obsTime : time object
                  This is time object of the header keyword OBS-TIME.

        Returns
        -------
        string : Returns the path to the log file that corresponds to the obsTime date.
                 OR if an index wasn't found then None is returned.
        """
        # print(obsTime)
        dateFile = str(obsTime.tm_year) + str(obsTime.tm_mon) + str(
            obsTime.tm_mday) + ".txt"
        # dateFile = time.strftime("%Y%m%d", obsTime) + ".log"
        # print(dateFile)

        logFileList = np.asarray(logFileList)
        files_nopaths = np.asarray([f.split("/")[-1] for f in logFileList])

        try:
            idx = np.where(files_nopaths == dateFile)[0][0]
            return logFileList[idx]
        except IndexError:
            return None

    def heimdallParseLogFile(self, logFile, obsTime):
        """ This file takes a log file reads it and finds the closest time to the obsTime and will output the following:
        RA, DEC, Epoch, LST, HA, ZA, Airmass, HJD, and MJD

        Parameters
        ----------
        logFile : string
                  Full path to the TCC log file.
        obsTime : time object
                  Contains the observation time in a flexible format

        Return
        ------
        tuple : (ra, dec, epoch, lst, ha)
                If no best time is found then None is returned.
        """
        log = pd.read_csv(logFile,
                          delim_whitespace=True,
                          header=None,
                          names=['time', 'ra', 'dec', 'epoch', 'lst', 'za'])

        # Create array of decimal time values
        times = [
            time.strptime(curr_time + " UTC", "%Y%m%dT%H:%M:%S %Z")
            for curr_time in log['time'].values
        ]
        times_deci = np.asarray([time.mktime(t) for t in times])
        obsTime_deci = time.mktime(obsTime)
        # print(times[0])
        # print(time.strftime("%Y%m%dT%H:%M:%S %Z",times[0]))
        # print(times_deci)
        # print(obsTime_deci)
        dif = times_deci - obsTime_deci
        val = dif[dif <= 0][-1]

        try:
            idx = np.where(dif == val)[0][0]
            # print(dif)
            # print(idx)
            # print(dif[idx])

            # now that we have the best idx we grab the relevant data
            ra = log['ra'][idx]
            dec = log['dec'][idx]
            epoch = log['epoch'][idx]
            lst = log['lst'][idx]
            za = log['za'][idx]
            ha = lst - ra
            print(log['time'][idx], ra, dec, epoch, lst, ha, za)

            return (ra, dec, epoch, lst, ha, za)
        except IndexError:
            return None

    def ChooseLogfile(self, LogfileList, ObsTime):
        """
        Code provided by add_headers v4.1 written by Oliver Frasier

        Choose the right logfile for the time of the observation,
        The logfiles are named according to their creation date, but they don't
        necessarilly come though in order. We'll return the name of the last
        one made before the exposure.
        """
        nlogs = len(LogfileList)
        ObsTime = time.mktime(ObsTime)  # convert to float representation
        besttime = -ObsTime  # set a start time way in the past
        bestindex = 0
        for i in range(nlogs):
            # make a time from the logfile name
            LogfileTime = time.mktime(
                time.strptime(
                    os.path.basename(LogfileList[i]) + ' UTC',
                    "%Y-%m-%dT%H:%M:%S %Z"  # this is the format
                ))
            # what's the delta between this and the observation
            delTime = LogfileTime - ObsTime
            # choose the largest negative delLogfileTime as the right logfile
            # that is, the closest negative number to zero
            if delTime > besttime and delTime < 0:
                print("DIFFERENCE IN TIME:", delTime)
                besttime = delTime
                bestindex = i
        # whew! finally got the logfile we want
        if besttime > -1800:  # difference of 30 minutes
            return LogfileList[bestindex]
        else:
            return None

    def ParseLogfile(self, LogfileName, ObsTime):
        """
        Code provided by add_headers v4.1 written by Oliver Frasier

        Find the line in the logfile closest in time to the observation,
        parse it, and return it.
        Logfile format is:

        UTDate&Time RA Dec Epoch LST Hour-angle Zenith-angle fslide:position

        We treat everything as a string.
        """
        Log = open(LogfileName)
        # now we need to find the smallest time increment between
        # Obstime and the time recorded on each line of the logfile
        # we'll read each line in, then compare
        data = Log.readline().split()
        Time = time.strptime(data[0] + ' UTC', "%Y-%m-%dT%H:%M:%S %Z")
        delTime = abs(time.mktime(Time) - time.mktime(ObsTime))
        # move through and compare each line of the logfile
        for newline in Log:
            newdata = newline.split()
            newTime = time.strptime(newdata[0] + ' UTC',
                                    "%Y-%m-%dT%H:%M:%S %Z")
            newdelTime = abs(time.mktime(newTime) - time.mktime(ObsTime))
            # this newdelTime should be smaller than delTime
            # since we should be moving closer to the right line.
            # if it's not, then we've gone too far
            if newdelTime > delTime:
                break
            delTime = newdelTime
            data = newdata
        # filter = data[7].rsplit(':',1)[1] # pull out just the filter number
        return data[1], data[2], data[3], data[4], data[5], data[6]  # , filter

    def expose(self,
               imType=None,
               expnum=None,
               itime=2,
               binning=1,
               filter="",
               readTime=3):
        """
        expNum is deprecated and should be removed.
        This handles a single exposure and no more.  Inputs are the image type integration time, binning type
        filter type, as a string, and the index for the specified horizontal readout time.
        """
        elapse_time = 0 - time.clock()
        if expnum is None:
            self.num += 1
            expnum = self.num
        else:
            self.num = expnum

        if imType is None:  # if the image type is not specified it defaults to object
            imType = "object"

        retval, width, height = andor.GetDetector()
        # logger.debug('GetDetector: ' + str(retval) + " " + str(width) + " " + str(height))
        # print 'SetImage:', andor.SetImage(1,1,1,width,1,height)
        # logger.debug('SetReadMode: ' + str(andor.SetReadMode(4)))
        andor.SetReadMode(4)
        # logger.debug('SetAcquisitionMode: ' + str(andor.SetAcquisitionMode(1)))
        andor.SetAcquisitionMode(1)
        # logger.debug(
        #    'SetImage: ' + str(andor.SetImage(binning, binning, 1, width, 1, height)))
        andor.SetImage(binning, binning, 1, width, 1, height)
        # logger.debug('GetDetector (again): ' + str(andor.GetDetector()))

        if imType == "bias":
            andor.SetShutter(
                1, 2, 0, 0
            )  # TLL mode high, shutter mode Permanently Closed, 0 millisec open/close
            # logger.debug('SetExposureTime: ' + str(andor.SetExposureTime(0)))
            andor.SetExposureTime(0)
        else:
            if imType in ['flat', 'object']:
                andor.SetShutter(1, 0, 5, 5)
            else:
                andor.SetShutter(1, 2, 0, 0)
            # logger.debug(
            #     'SetExposureTime: ' + str(andor.SetExposureTime(itime))
            andor.SetExposureTime(itime)
            # )  # TLL mode high, shutter mode Fully Auto, 5 millisec open/close

        # set Readout speeds 0, 1, 2, or 3
        # print("SetVSSpeed:", andor.SetVSSpeed(3))
        # logger.debug(
        #    "SetHSSpeed: " + str(andor.SetHSSpeed(0, readTime))
        andor.SetHSSpeed(0, readTime)
        #)  # default readTime is index 3 which is 0.5 MHz or ~6 sec

        results, expTime, accTime, kTime = andor.GetAcquisitionTimings()
        # logger.debug("Adjusted Exposure Time: " + str([results, expTime, accTime, kTime]))

        attributes = [imType, binning, itime, filter]
        # header = self.getHeader(attributes)
        header = self.getHeader_2(attributes, 'heimdall')

        # logger.debug('StartAcquisition: ' + str(andor.StartAcquisition()))
        andor.StartAcquisition()

        status = andor.GetStatus()
        # logger.debug(str(status))
        while status[1] == andor.DRV_ACQUIRING:
            status = andor.GetStatus()

        data = np.zeros(width // binning * height // binning, dtype='uint16')
        # logger.debug(str(data.shape))
        result = andor.GetAcquiredData16(data)

        success = None
        if result == 20002:
            success = 1  # for true
        else:
            success = 0  # for false

        # logger.debug(str(result) + 'success={}'.format(result == 20002))
        filename = None
        if success == 1:
            data = data.reshape(width // binning, height // binning)
            #data = np.fliplr(data)
            # logger.debug(str(data.shape) + " " + str(data.dtype))
            hdu = fits.PrimaryHDU(data,
                                  do_not_scale_image_data=True,
                                  uint=True,
                                  header=header)
            # filename = time.strftime('/data/forTCC/image_%Y%m%d_%H%M%S.fits')
            filename = fits_utils.get_image_path('expose')
            hdu.writeto(filename, clobber=True)
            # logger.debug("wrote: {}".format(filename))
        elapse_time += time.clock()
        print("Took %.3f seconds." % elapse_time)
        return "expose " + str(success) + "," + str(filename) + "," + str(
            itime)

    def realTimeExposure(self, protocol, imType, itime, binning=1):
        """
        Inputs are the Evora server protocol, the image type, the integration time, and the binning size.
        Runs camera in RunTillAbort mode.
        """
        # global acquired
        retval, width, height = andor.GetDetector()
        # logger.debug('GetDetector: ' + str(retval) + " " + str(width) + " " + str(height))

        # logger.debug("SetAcquisitionMode: " + str(andor.SetAcquisitionMode(5)))
        andor.SetAcquisitionMode(5)
        # logger.debug('SetReadMode: ' + str(andor.SetReadMode(4)))
        andor.SetReadMode(4)

        # logger.debug(
        #    'SetImage: ' + str(andor.SetImage(binning, binning, 1, width, 1, height)))
        andor.SetImage(binning, binning, 1, width, 1, height)
        # logger.debug('GetDetector (again): ' + str(andor.GetDetector()))

        # logger.debug('SetExposureTime: ' + str(andor.SetExposureTime(itime)))
        andor.SetExposureTime(itime)
        # logger.debug('SetKineticTime: ' + str(andor.SetKineticCycleTime(0)))
        andor.SetKineticCycleTime(0)

        if imType == "bias":
            andor.SetShutter(
                1, 2, 0, 0
            )  # TLL mode high, shutter mode Permanently Closed, 0 millisec open/close
            # logger.debug('SetExposureTime: ' + str(andor.SetExposureTime(0)))
            andor.SetExposureTime(0)
        else:
            if imType in ['flat', 'object']:
                andor.SetShutter(1, 0, 5, 5)
            else:
                andor.SetShutter(1, 2, 0, 0)
            # logger.debug(
            #    'SetExposureTime: ' + str(andor.SetExposureTime(itime))
            # )  # TLL mode high, shutter mode Fully Auto, 5 millisec open/close
            andor.SetExposureTime(itime)

        data = np.zeros(width // binning * height // binning, dtype='uint16')
        # logger.debug(
        #    "SetHSSpeed: " + str(andor.SetHSSpeed(0, 1))
        # )  # read time on real is fast because they aren't science images
        andor.SetHSSpeed(0, 1)
        # logger.debug('StartAcquisition: ' + str(andor.StartAcquisition()))
        andor.StartAcquisition()

        status = andor.GetStatus()
        # logger.debug(str(status))
        workingImNum = 1
        start = time.time()
        end = 0
        while status[1] == andor.DRV_ACQUIRING:

            progress = andor.GetAcquisitionProgress()
            currImNum = progress[
                2]  # won't update until an acquisition is done
            status = andor.GetStatus()

            if status[1] == andor.DRV_ACQUIRING and currImNum == workingImNum:
                # logger.debug("Progress: " + str(andor.GetAcquisitionProgress()))
                results = andor.GetMostRecentImage16(data)  # store image data
                # logger.debug(
                #    str(results) + 'success={}'.format(results == 20002)
                # )  # print if the results were successful

                if results == andor.DRV_SUCCESS:  # if the array filled store successfully
                    data = data.reshape(width // binning, height // binning)  # reshape into image
                    # logger.debug(str(data.shape) + " " + str(data.dtype))
                    hdu = fits.PrimaryHDU(data,
                                          do_not_scale_image_data=True,
                                          uint=True)
                    # filename = time.strftime('/tmp/image_%Y%m%d_%H%M%S.fits')
                    filename = fits_utils.get_image_path('real')
                    hdu.writeto(filename, clobber=True)
                    # logger.debug("wrote: {}".format(filename))
                    data = np.zeros(width // binning * height // binning,
                                    dtype='uint16')

                    protocol.sendData("realSent %s" % filename)
                    # print("Sending", "realSent%d" % (workingImNum))
                    workingImNum += 1
                    end = time.time()
                    # logger.debug("Took %f seconds" % (end - start))
                    start = time.time()

        return "real 1"  # exits with 1 for success

    def kseriesExposure(self,
                        protocol,
                        imType,
                        itime,
                        filter="",
                        readTime=3,
                        numexp=1,
                        binning=1,
                        numAccum=1,
                        accumCycleTime=0,
                        kCycleTime=0):
        """
        This handles multiple image acquisition using the camera kinetic series capability.  The basic arguements are
        the passed in protocol, the image type, integration time, filter type, readout index, number of exposures, and binning type.

        In the future this function could be modified to include accumulations or add time the kinetic cycle time.  Accumulations
        are how many images should be readout as one, and kCycleTime can add time between each exposure that is taken.
        """
        global isAborted
        isAborted = False
        retval, width, height = andor.GetDetector()
        # logger.debug('GetDetector: ' + str(retval) + " " + str(width) + " " + str(height))

        # logger.debug("SetAcquisitionMode: " + str(andor.SetAcquisitionMode(3)))
        andor.SetAcquisitionMode(3)
        # logger.debug('SetReadMode: ' + str(andor.SetReadMode(4)))
        andor.SetReadMode(4)

        # logger.debug(
        #    'SetImage: ' + str(andor.SetImage(binning, binning, 1, width, 1, height)))
        andor.SetImage(binning, binning, 1, width, 1, height)
        # logger.debug('GetDetector (again): ' + str(andor.GetDetector()))

        if imType == "bias":
            itime = 0
            andor.SetShutter(
                1, 2, 0, 0
            )  # TLL mode high, shutter mode Permanently Closed, 0 millisec open/close
            # logger.debug('SetExposureTime: ' + str(andor.SetExposureTime(0)))
            andor.SetExposureTime(0)
        else:
            if imType in ['flat', 'object']:
                andor.SetShutter(1, 0, 5, 5)
            else:
                andor.SetShutter(1, 2, 0, 0)
            # logger.debug(
                'SetExposureTime: ' + str(andor.SetExposureTime(itime))
            # )  # TLL mode high, shutter mode Fully Auto, 5 millisec open/close

        # logger.debug("SetNumberOfAccumulations: " + str(andor.SetNumberAccumulations(numAccum)))  # number of exposures to be combined
        andor.SetNumberAccumulations(numAccum)
        # logger.debug("SetAccumulationTime: " + str(andor.SetAccumulationCycleTime(accumCycleTime)))
        andor.SetAccumulationCycleTime(accumCycleTime)
        # logger.debug("SetNumberOfKinetics: " + str(andor.SetNumberKinetics(numexp)))  # this is the number of exposures the user wants
        andor.SetNumberKinetics(numexp)
        # logger.debug('SetKineticTime: ' + str(andor.SetKineticCycleTime(accumCycleTime)))
        andor.SetKineticCycleTime(accumCycleTime)
        # logger.debug("SetTriggerMode: " + str(andor.SetTriggerMode(0)))
        andor.SetTriggerMode(0)
        # logger.debug("Timings: " + str(andor.GetAcquisitionTimings()))
        # logger.debug("SetHSSpeed: " + str(andor.SetHSSpeed(0, readTime)))  # default readTime is index 3 which is 0.5 MHz or ~6 sec
        andor.SetHSSpeed(0, readTime)

        # write headers
        attributes = [imType, binning, itime, filter]
        # header = self.getHeader(attributes)
        header = self.getHeader_2(attributes, 'heimdall')

        # logger.debug('StartAcquisition: ' + str(andor.StartAcquisition()))
        andor.StartAcquisition()

        status = andor.GetStatus()
        # logger.debug(str(status))

        imageAcquired = False

        counter = 1
        while status[1] == andor.DRV_ACQUIRING:
            status = andor.GetStatus()
            progress = andor.GetAcquisitionProgress()

            runtime = 0
            if progress[2] == counter or (not isAborted and progress[2] == 0 and imageAcquired):
                runtime -= time.clock()
                data = np.zeros(width // binning * height // binning,
                                dtype='uint16')  # reserve room for image
                results = andor.GetMostRecentImage16(data)  # store image data
                # logger.debug(
                #    str(results) + " " + 'success={}'.format(results == 20002)
                # )  # print if the results were successful
                # logger.debug('image number: ' + str(progress[2]))

                if results == andor.DRV_SUCCESS:  # if the array filled store successfully
                    data = data.reshape(width // binning, height // binning)  # reshape into image
                    # logger.debug(str(data.shape) + " " + str(data.dtype))

                    hdu = fits.PrimaryHDU(data,
                                          do_not_scale_image_data=True,
                                          uint=True,
                                          header=header)
                    # filename = time.strftime('/data/forTCC/image_%Y%m%d_%H%M%S.fits')
                    filename = fits_utils.get_image_path('series')
                    hdu.writeto(filename, clobber=True)

                    # logger.debug("wrote: {}".format(filename))

                    protocol.sendData("seriesSent" + str(counter) + " " + str(counter) + "," + str(itime) + "," + filename)
                    # make a new header and write time to it for new exposure.
                    # header = self.getHeader(attributes)
                    header = self.getHeader_2(attributes, 'heimdall')

                    if counter == numexp:
                        # logger.info("entered abort")
                        isAborted = True

                    imageAcquired = True
                    counter += 1
                runtime += time.clock()
                # logger.debug("Took %f seconds to write." % runtime)
        return "series 1," + str(counter)  # exits with 1 for success

    # deprecated to kseriesExposure

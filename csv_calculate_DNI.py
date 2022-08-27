import time
import os
import pandas as pd
import numpy as np
import pytz

import math


def dateparse(timestamp):
    #return pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    print(timestamp)
    return pd.datetime.strptime(timestamp, '%Y/%m/%d %H:%M')


def read_csv(file):
    # os.chdir(path)
    # filename_list = os.listdir(path)
    data = pd.read_csv(file, encoding = 'gbk', date_parser=dateparse, header=0) # 从csv文件中读出对应的列, header None 或者 0
    #data.columns = ['TIME', 'measured value', 'predicted value', 'weighted value']
    data.columns = ['TIME', 'measured value', 'predicted value']
    print(data)
    #exit()
    return data


def ephemeris(time, latitude, longitude, pressure=101325, temperature=12):
    """
    Python-native solar position calculator.
    The accuracy of this code is not guaranteed.
    Consider using the built-in spa_c code or the PyEphem library.

    Parameters
    ----------
    time : pandas.DatetimeIndex
        Must be localized or UTC will be assumed.
    latitude : float
        Latitude in decimal degrees. Positive north of equator, negative
        to south.
    longitude : float
        Longitude in decimal degrees. Positive east of prime meridian,
        negative to west.
    pressure : float or Series, default 101325
        Ambient pressure (Pascals)
    temperature : float or Series, default 12
        Ambient temperature (C)

    Returns
    -------

    DataFrame with the following columns:

        * apparent_elevation : apparent sun elevation accounting for
          atmospheric refraction.
        * elevation : actual elevation (not accounting for refraction)
          of the sun in decimal degrees, 0 = on horizon.
          The complement of the zenith angle.
        * azimuth : Azimuth of the sun in decimal degrees East of North.
          This is the complement of the apparent zenith angle.
        * apparent_zenith : apparent sun zenith accounting for atmospheric
          refraction.
        * zenith : Solar zenith angle
        * solar_time : Solar time in decimal hours (solar noon is 12.00).

    References
    -----------

    .. [1] Grover Hughes' class and related class materials on Engineering
       Astronomy at Sandia National Laboratories, 1985.

    See also
    --------
    pyephem, spa_c, spa_python

    """

    # Added by Rob Andrews (@Calama-Consulting), Calama Consulting, 2014
    # Edited by Will Holmgren (@wholmgren), University of Arizona, 2014

    # Most comments in this function are from PVLIB_MATLAB or from
    # pvlib-python's attempt to understand and fix problems with the
    # algorithm. The comments are *not* based on the reference material.
    # This helps a little bit:
    # http://www.cv.nrao.edu/~rfisher/Ephemerides/times.html

    # the inversion of longitude is due to the fact that this code was
    # originally written for the convention that positive longitude were for
    # locations west of the prime meridian. However, the correct convention (as
    # of 2009) is to use negative longitudes for locations west of the prime
    # meridian. Therefore, the user should input longitude values under the
    # correct convention (e.g. Albuquerque is at -106 longitude), but it needs
    # to be inverted for use in the code.

    Latitude = latitude
    Longitude = -1 * longitude

    Abber = 20 / 3600.
    LatR = np.radians(Latitude)

    # the SPA algorithm needs time to be expressed in terms of
    # decimal UTC hours of the day of the year.

    # if localized, convert to UTC. otherwise, assume UTC.
    try:
        time_utc = time.tz_convert('UTC')
    except TypeError:
        time_utc = time

    # strip out the day of the year and calculate the decimal hour
    DayOfYear = time_utc.dayofyear
    DecHours = (time_utc.hour + time_utc.minute/60. + time_utc.second/3600. +
                time_utc.microsecond/3600.e6)

    # np.array needed for pandas > 0.20
    UnivDate = np.array(DayOfYear)
    UnivHr = np.array(DecHours)

    Yr = np.array(time_utc.year) - 1900
    YrBegin = 365 * Yr + np.floor((Yr - 1) / 4.) - 0.5

    Ezero = YrBegin + UnivDate
    T = Ezero / 36525.

    # Calculate Greenwich Mean Sidereal Time (GMST)
    GMST0 = 6 / 24. + 38 / 1440. + (
        45.836 + 8640184.542 * T + 0.0929 * T ** 2) / 86400.
    GMST0 = 360 * (GMST0 - np.floor(GMST0))
    GMSTi = np.mod(GMST0 + 360 * (1.0027379093 * UnivHr / 24.), 360)

    # Local apparent sidereal time
    LocAST = np.mod((360 + GMSTi - Longitude), 360)

    EpochDate = Ezero + UnivHr / 24.
    T1 = EpochDate / 36525.

    ObliquityR = np.radians(
        23.452294 - 0.0130125 * T1 - 1.64e-06 * T1 ** 2 + 5.03e-07 * T1 ** 3)
    MlPerigee = 281.22083 + 4.70684e-05 * EpochDate + 0.000453 * T1 ** 2 + (
        3e-06 * T1 ** 3)
    MeanAnom = np.mod((358.47583 + 0.985600267 * EpochDate - 0.00015 *
                       T1 ** 2 - 3e-06 * T1 ** 3), 360)
    Eccen = 0.01675104 - 4.18e-05 * T1 - 1.26e-07 * T1 ** 2
    EccenAnom = MeanAnom
    E = 0

    while np.max(abs(EccenAnom - E)) > 0.0001:
        E = EccenAnom
        EccenAnom = MeanAnom + np.degrees(Eccen)*np.sin(np.radians(E))

    TrueAnom = (
        2 * np.mod(np.degrees(np.arctan2(((1 + Eccen) / (1 - Eccen)) ** 0.5 *
                   np.tan(np.radians(EccenAnom) / 2.), 1)), 360))
    EcLon = np.mod(MlPerigee + TrueAnom, 360) - Abber
    EcLonR = np.radians(EcLon)
    DecR = np.arcsin(np.sin(ObliquityR)*np.sin(EcLonR))

    RtAscen = np.degrees(np.arctan2(np.cos(ObliquityR)*np.sin(EcLonR),
                                    np.cos(EcLonR)))

    HrAngle = LocAST - RtAscen
    HrAngleR = np.radians(HrAngle)
    HrAngle = HrAngle - (360 * (abs(HrAngle) > 180))

    SunAz = np.degrees(np.arctan2(-np.sin(HrAngleR),
                                  np.cos(LatR)*np.tan(DecR) -
                                  np.sin(LatR)*np.cos(HrAngleR)))
    SunAz[SunAz < 0] += 360

    SunEl = np.degrees(np.arcsin(
        np.cos(LatR) * np.cos(DecR) * np.cos(HrAngleR) +
        np.sin(LatR) * np.sin(DecR)))

    SolarTime = (180 + HrAngle) / 15.

    # Calculate refraction correction
    Elevation = SunEl
    TanEl = pd.Series(np.tan(np.radians(Elevation)), index=time_utc)
    Refract = pd.Series(0, index=time_utc)

    Refract[(Elevation > 5) & (Elevation <= 85)] = (
        58.1/TanEl - 0.07/(TanEl**3) + 8.6e-05/(TanEl**5))

    Refract[(Elevation > -0.575) & (Elevation <= 5)] = (
        Elevation *
        (-518.2 + Elevation*(103.4 + Elevation*(-12.79 + Elevation*0.711))) +
        1735)

    Refract[(Elevation > -1) & (Elevation <= -0.575)] = -20.774 / TanEl

    Refract *= (283/(273. + temperature)) * (pressure/101325.) / 3600.

    ApparentSunEl = SunEl + Refract

    # make output DataFrame
    DFOut = pd.DataFrame(index=time_utc)
    DFOut['apparent_elevation'] = ApparentSunEl
    DFOut['elevation'] = SunEl
    DFOut['azimuth'] = SunAz
    DFOut['apparent_zenith'] = 90 - ApparentSunEl
    DFOut['zenith'] = 90 - SunEl
    DFOut['solar_time'] = SolarTime
    DFOut.index = time

    return DFOut

def execute(path):
    os.chdir(path)
    filename_list = os.listdir(path)
    ghi_file = ''
    dhi_file = ''
    for file in filename_list:
        if file.find('ghi') >= 0:
            ghi_file = file
        elif file.find('dhi') >= 0:
            dhi_file = file
    print("{}, {}".format(ghi_file, dhi_file))
    # name = csv_to_xls(os.path.join(path, file))
    ghi_data = read_csv(ghi_file)
    dhi_data = read_csv(dhi_file)

    ghi_data['TIME']= pd.to_datetime(ghi_data['TIME'])
    dhi_data['TIME']= pd.to_datetime(dhi_data['TIME'])
    

    timezone = pytz.timezone('Asia/Shanghai')

    t1=pd.DatetimeIndex(ghi_data['TIME'], tz = timezone)

    latitude = 31.29 
    longitude = 121.2085
    #time = '2021-07-01 17:29:30'

    #apparent_elevation = pvlib.solarposition.ephemeris(t1, latitude, longitude, pressure=101325.0, temperature=16.0)
    apparent_elevation = ephemeris(t1, latitude, longitude, pressure=101325.0, temperature=16.0)

    print(apparent_elevation)

    degree = (90 - np.array(apparent_elevation['apparent_elevation'])) * np.pi/180 #转化为弧度

    #numpy.around(a,decimals)

    dni_m = np.true_divide(np.array(ghi_data['measured value'] - dhi_data['measured value']), np.cos(degree))
    dni_m = np.around(dni_m, decimals = 2)
    print(dni_m)
    

    dni_p = np.true_divide(np.array(ghi_data['predicted value'] - dhi_data['predicted value']), np.cos(degree))
    dni_p = np.around(dni_p, decimals = 2)
    print(dni_p)

    # dni = np.concatenate((dni_m, dni_p))
    result = pd.DataFrame()
    result['TIME'] = ghi_data['TIME']
    result['dni_m'] = dni_m
    result['dni_p'] = dni_p
    # result = pd.DataFrame(dni_m, dni_p)
    file_name = ghi_file.replace('ghi', 'dni')
    result.to_csv(file_name, header=0,index=0)
    ghi_data.to_csv(ghi_file, header=0,index=0)
    dhi_data.to_csv(dhi_file, header=0,index=0)

    #return ghi_data['TIME'], ghi_data['predicted value'], dhi_data['predicted value'], result['dni_p']
    #return ghi_data['TIME'], ghi_data['measured value'], dhi_data['measured value'], result['dni_m']

    
    
    # apparent_elevation.to_csv("apparent_elevation.csv")


def main():
    path=r'C:\Users\lucky_wang\OneDrive\automation\result\cal'
    os.chdir(path)
    execute(path)


if __name__ == "__main__":
    main()

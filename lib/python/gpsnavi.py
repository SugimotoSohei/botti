#!coding:utf-8

import serial
import math
import pynmea2
from pyproj import Geod
import logging


class gpsparser(object):

    def __init__(self, portname=None, baudrate=9600, goal=[[138.75665666666666, 35.68582166666667]], debugmode=False):
        self.debugmode = debugmode
        self.goal = goal
        if portname is not None:
            self.ser = serial.Serial(port=portname, baudrate=baudrate)
            logging.info("open SerialPort")

    def gpsupdate(self, debuggpsvalue=None):
        readline = ""
        if debuggpsvalue is None:
            while True:
                self.ser.flushInput()
                self.ser.flushOutput()
                try:
                    readline = str(self.ser.readline(), 'utf-8').split('\r')[0]
                    self.ser.flushInput()
                    self.ser.flushOutput()
                    self.gpsdata = self.NMEAanAlysis(readline)
                except:
                    pass
                if self.gpsdata is not None:
                    break
        else:
            readline = debuggpsvalue
            print(readline)
            self.gpsdata = self.NMEAanAlysis(readline)
        logging.info(readline)
        logging.info("gpsupdate")

    def NMEAanAlysis(self, data):
        try:
            parsedata = pynmea2.parse(data)
            return parsedata
        except:
            return None

    def timestamp(self):
        return self.gpsdata.timestamp

    def lat(self):
        logging.info(str(self.gpsdata.lat))
        return float(self.gpsdata.lat)

    def latitude(self):
        logging.info(str(self.gpsdata.latitude))
        return float(self.gpsdata.latitude)

    def lon(self):
        logging.info(str(self.gpsdata.lon))
        return float(self.gpsdata.lon)

    def longitude(self):
        logging.info(str(self.gpsdata.longitude))
        return float(self.gpsdata.longitude)

    def sat_receivejudge(self):
        if int(self.gpsdata.num_sats) >= 3:
            logging.info("OKGpsnum:"+str(self.gpsdata.num_sats))
            print("OKGpsnum:"+str(self.gpsdata.num_sats))
            return True
        else:
            logging.info("NoGpsnum:"+str(self.gpsdata.num_sats))
            print("NoGpsnum:"+str(self.gpsdata.num_sats))
            return False

    def altitude(self):
        return float(self.gpsdata.geo_sep)

    def goalcalc(self):
        nowpos = [self.longitude(), self.latitude()]
        g = Geod(ellps='WGS84')
        self.goalaz, self.goalbackaz, self.goaldist = g.inv(nowpos[0], nowpos[1], self.goal[0][0], self.goal[0][1])

    def goaldistance(self):
        logging.info("goaldistance:"+str(self.goaldist))
        return self.goaldist

    def goalhorizontaldistance(self):
        logging.info("goalhorizontaldistance:"+str(math.cos(self.goalazimath())*self.goaldistance()))
        return math.cos(self.goalazimath())*self.goaldistance()

    def goalverticaldistance(self):
        logging.info("goalverticaldistance:"+str(math.sin(self.goalazimath())*self.goaldistance()))
        return math.sin(self.goalazimath())*self.goaldistance()

    def goalazimath(self):
        logging.info("goalAzimath:"+str(self.goalaz))
        return float(self.goalaz)

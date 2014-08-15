#!coding:utf-8
import os
import sys
import math
import time
if os.getlogin() == 'pi':
    import RPi.GPIO as IO
else:
    sys.path.append(os.path.dirname(__file__))
    from RpiTest import GPIO as IO

import go_f
import logging


class GPIO:  # GPIOをTurtleに

    def __init__(self, leftmotor=[22, 23], rightmotor=[24, 25], goalpos=[], gps=None, ratio=96.0, rate=0.0164):
        gof = go_f.getdistance()
        gof.goal = goalpos
        self.gps = gps
        self.rate = rate
        self.ratio = ratio
        self.leftmotor = leftmotor
        self.rightmotor = rightmotor
        IO.setmode(IO.BCM)
        IO.setup(self.leftmotor[0], IO.OUT)
        IO.setup(self.leftmotor[1], IO.OUT)
        IO.setup(self.rightmotor[0], IO.OUT)
        IO.setup(self.rightmotor[1], IO.OUT)
        logging.info("GPIOInit")

    def forward(self, distance):
        start = time.time()
        while True:
            IO.output(self.leftmotor[0], False)
            IO.output(self.leftmotor[1], True)
            IO.output(self.rightmotor[0], False)
            IO.output(self.rightmotor[1], True)
            if time.time() - start >= math.fabs(distance)/self.rate:
                break
        time.sleep(0.01)
        logging.info("Forward")

    def back(self, distance):
        start = time.time()
        while True:
            IO.output(self.leftmotor[0], True)
            IO.output(self.leftmotor[1], False)
            IO.output(self.rightmotor[0], True)
            IO.output(self.rightmotor[1], False)
            if time.time() - start >= math.fabs(distance)/self.rate:
                break
        time.sleep(0.01)
        logging.info("back")

    def left(self, azimath):
        start = time.time()
        while True:
            IO.output(self.leftmotor[0], True)
            IO.output(self.leftmotor[1], False)
            IO.output(self.rightmotor[0], False)
            IO.output(self.rightmotor[1], True)
            if time.time() - start >= math.fabs(azimath)/self.ratio:
                break
        time.sleep(0.01)
        logging.info("left")

    def right(self, azimath):
        start = time.time()
        while True:
            IO.output(self.leftmotor[0], False)
            IO.output(self.leftmotor[1], True)
            IO.output(self.rightmotor[0], True)
            IO.output(self.rightmotor[1], False)
            if time.time() - start >= math.fabs(azimath)/self.ratio:
                break
        time.sleep(0.01)
        logging.info("right")

    def goaldistance(self):
        logging.info("goaldistance:"+str(self.gps.goaldistance()))
        return self.gps.goaldistance()

    def _bump(self, before, after):
        if before == after:
            self.back(1)
            self.left(30)
            time.sleep(0.01)
            logging.info("bomp")
            return True
        else:
            return False

    def first(self, distance1, distance2):
        if distance1 == distance2:
            return True
        else:
            return False

    def angle(self):
        print(self.gapazimath)
        if self.gapazimath > 0:
            self.left(math.fabs(self.gapazimath))
            print("left")
        elif self.gapazimath < 0:
            self.right(math.fabs(self.gapazimath))
            print("right")

    def turn(self, gapazimath):
        self.gapazimath = gapazimath
        if self.gps.goaldistance() >= 10:
            #self.first()
            self.angle()
            self.forward(8)

        if 10 > self.gps.goaldistance() > 3:
            #self.first()
            self.angle()
            self.forward(1)
            self.gps.goal.pop(0)

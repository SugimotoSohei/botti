#!coding:utf-8

import os
import sys
import time
import unittest
if os.getlogin() == 'pi':
    import RPi.GPIO as IO
else:
    sys.path.append(os.path.dirname(__file__))
    from RpiTest import GPIO as IO


class gpiotest(unittest.TestCase):
    def testIO(self):
        IO.setmode(IO.BCM)
        IO.setup(18, IO.OUT)
        IO.output(18, IO.HIGH)
        time.sleep(1)
        IO.output(18, IO.LOW)
        time.sleep(1)

if __name__ == '__main__':
    unittest.main()

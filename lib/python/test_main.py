#!coding:utf-8

import unittest
import main
import os


class test_main(unittest.TestCase):

    def testmain(self):
        #goal = [[141.24374166666666,43.123776666666664],[141.24319666666668,43.123131666666666]]

        goal=[[141.24981666666667, 43.13435],[141.24963333333332, 43.13462666666667]]
        #goal = [[43.123776666666664,141.24374166666666]]
        self.testmain = main.Main(goal=goal,groundalt=36.7)
        f = open(os.path.dirname(__file__)+'/test/gen_test_main.txt')
        gpgga = []
        for data in f.readlines():
            if 'GPGGA' in data:
                gpgga.append(data.split('\n')[0])
        self.testmain.gpsdebugvalue = gpgga
        f.close()

        self.testmain.run()

if __name__ == '__main__':
    unittest.main()

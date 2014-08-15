from PIL import Image
import numpy as np
import subprocess
import datetime
import time
import logging


class flagcapture(object):

    def capture(self):
        self.imagename = None
        try:
            self.imagename = str(time.strftime('%H-%M-%S', datetime.datetime.now().timetuple()))+".png"
            subprocess.call("raspistill -o " + self.imagename + " -t 0")
            logging.info("capture:"+str(self.imagename))
            return True
        except:
            self.imagename = None
            logging.info("capture:Failed")
            return False

    def judge(self, selectcolor='red', selectcolor_judge=110, othercolor1_judge=100, othercolor2_judge=100):
        if self.imagename is not None:
            judgeimage = self.JudgeGoal(filename=self.imagename, selectcolor_judge=selectcolor_judge, othercolor1_judge=othercolor1_judge, othercolor2_judge=othercolor2_judge)
            judgeimage.loadimage()
            judgeimage.objectselect(colorname=selectcolor)
            logging.info("judge")
            return judgeimage.objectdirection()
        else:
            return [None, '0']

    class JudgeGoal():

        def __init__(self, filename=None, selectcolor_judge=110, othercolor1_judge=100, othercolor2_judge=100):
            self.filename = filename
            self.selectcolor_judge = selectcolor_judge
            self.othercolor1_judge = othercolor1_judge
            self.othercolor2_judge = othercolor2_judge

        def loadimage(self, filename=None):
            if filename is None:
                self.im = Image.open(self.filename)
            else:
                self.im = Image.open(filename)
            self.width, self.height = self.im.size
            rgbimg = self.im.convert("RGB")
            self.rgb = list(rgbimg.getdata())

        def objectselect(self, colorname='red'):
            self.data = np.zeros((self.height, self.width, 3), 'uint8')
            count = 0
            for i in range(self.height):
                for j in range(self.width):
                    if colorname == 'red':
                        selectcolor = self.rgb[count][0]
                        othercolor1 = self.rgb[count][1]
                        othercolor2 = self.rgb[count][2]
                    if colorname == 'green':
                        othercolor1 = self.rgb[count][0]
                        selectcolor = self.rgb[count][1]
                        othercolor2 = self.rgb[count][2]
                    if colorname == 'blue':
                        othercolor1 = self.rgb[count][0]
                        othercolor2 = self.rgb[count][1]
                        selectcolor = self.rgb[count][2]
                    if (selectcolor > self.selectcolor_judge and othercolor1 < self.othercolor1_judge and othercolor2 < self.othercolor2_judge):
                        self.data[i][j][0] = 250
                        self.data[i][j][1] = 250
                        self.data[i][j][2] = 250
                    else:
                        self.data[i][j][0] = 0
                        self.data[i][j][1] = 0
                        self.data[i][j][2] = 0
                    count += 1

        def objectdirection(self):
            leftcount = 0
            centercount = 0
            rightcount = 0
            left = self.width/3
            center = (self.width/3)*2
            for i in range(self.height):
                for j in range(self.width):
                    if self.data[i][j][0] == 250:
                        if j < left:
                            leftcount = leftcount+1
                        if j > left and j < center:
                            centercount = centercount+1
                        if j > center:
                            rightcount = rightcount+1
            if leftcount > centercount and leftcount > rightcount:
                    print("leftcount:"+str(leftcount))
                    logging.info("objectdirection:"+"leftcount:"+str(leftcount))
                    return ["left", str(leftcount)]
            if centercount > rightcount and centercount > leftcount:
                    print("centercount:"+str(centercount))
                    logging.info("objectdirection:"+"centercount:"+str(centercount))
                    return ["center", str(centercount)]
            if rightcount > centercount and rightcount > leftcount:
                    print("rightcount:"+str(rightcount))
                    logging.info("objectdirection:"+"rightcount:"+str(rightcount))
                    return ["right", str(rightcount)]

"""
In this example, we demonstrate how to create simple camera viewer using Opencv3 and PyQt5

Author: Berrouba.A
Last edited: 21 Feb 2018
"""

# import system module
import sys
import math
# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWidgets import QWidget,QMessageBox
from PyQt5.QtGui import QImage, QCursor
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from insertUser import createUser
from insertUser import login
from Coordinates_Insertion import createPoint
import jwt
import argparse
import imutils
import time
import cv2
from imutils.video import FPS

#from GUI_Code import Ui_Form

# import Opencv module
import cv2

from ui_main_window import *

class MainWindow(QDialog):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.pos1 = [0,0]
        self.pos2 = [0,0]
        self.pos3 = [0,0]
        self.first = 0
        self.second = 0
        self.third = 0
        self.fourth = 0
        self.logic = 2
        self.image = 0
        self.tdl = False
        self.start = []
        self.end = []
        self.linecorr = [] 
        self.rectcorr = [] 
        self.drawing=False
        self.movement = False
        self.tracker = cv2.TrackerTLD_create()
        self.initBB = None
        self.fps=None
        self.ui.rectangle.clicked.connect(self.Rectangle1)
        self.ui.line.clicked.connect(self.Line1)
        self.ui.Undo.clicked.connect(self.Undo1)
        self.ui.save.clicked.connect(self.Save1)
        self.ui.Reset.clicked.connect(self.Reset1)
        self.ui.TDL.clicked.connect(self.TDL)
        self.ui.Next.clicked.connect(self.Next)
        self.ui.Prev.clicked.connect(self.Prev)
        self.ipAdd = 0
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)
    # view camera
    def common_data(self,list1, list2): 
        result = False
  
        # traverse in the 1st list 
        for x in list1: 
  
        # traverse in the 2nd list 
            for y in list2: 
    
                # if one common 
                if x == y: 
                    result = True
                    return result  
                  
        return result 

    def viewCam(self):
        # read image in BGR format
        ret, self.image = self.cap.read()
            
        if self.tdl:
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
		    # initBB = cv2.selectROI("Frame", self.image, fromCenter=False,showCrosshair=True)
            self.initBB = cv2.selectROI("Cam View",self.image, fromCenter=False,showCrosshair=True)
            cv2.destroyWindow("Cam View")
		    # start OpenCV object tracker using the supplied bounding box
		    # coordinates,then start the FPS throug hput estimator as well
		    #tracker.init(frame, initBB)
            self.tracker.init(self.image, self.initBB)
		    #fps = FPS().start()
            self.fps = FPS().start()
            self.tdl=False
        if self.initBB is not None:
		    #(success, box) = tracker.update(self.image)
            (success, box) = self.tracker.update(self.image)
		    # check to see if the tracking was a success
		    # if success:
            if success:
			    # (x, y, w, h) = [int(v) for v in box]
                (x, y, w, h) = [int(v) for v in box]
			    # cv2.rectangle(self.image, (x, y), (x + w, y + h),(0, 255, 0), 2)
                cv2.rectangle(self.image, (x, y), (x + w, y + h),(0, 255, 0), 2)
                if self.logic==3:
                    loints = []
                    x1, y1, x2, y2 = x, y, x + w, y + h
                    for l in range(y1,y2+1):
                        loints.append((x1,l))
                        loints.append((x2,l))
                    for l in range(x1,x2+1):
                        loints.append((l,y1))
                        loints.append((l,y2))
                    if self.common_data(loints,self.linecorr):
                        cv2.putText(self.image, 'ALARAM IS ON', (40,40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA) 
                    
                    #box1 = self.image[x:x + w,y:y+h]
                    #print(
		    # fps.update()
            self.fps.update()
            self.fps.stop()
        if self.logic==2:
            color = (255, 0, 0) 
            thickness = 2
            self.middlepoint = (self.pos3[0], self.pos3[1])
            self.start_point = (self.pos1[0], self.pos1[1])
            self.end_point = (self.pos2[0], self.pos2[1]) 
            if self.movement:
                self.image = cv2.rectangle(self.image, self.start_point, self.middlepoint, color, thickness)  
            i=0
            for i in range(len(self.start)):
                cv2.rectangle(self.image, self.start[i], self.end[i], color, thickness)
        if self.logic==3:
            QApplication.setOverrideCursor(QCursor(QtCore.Qt.CrossCursor))
            color = (255, 0, 0) 
            thickness = 2
            self.start_point = (self.pos1[0], self.pos1[1])
            self.end_point = (self.pos2[0], self.pos2[1])
            self.middlepoint = (self.pos3[0], self.pos3[1])
            if self.movement:
                cv2.line(self.image, self.start_point, self.middlepoint, color, thickness)
            i=0
            for i in range(len(self.start)):
                cv2.line(self.image, self.start[i], self.end[i], color, thickness)
                #self.image[self.start_point,self.end_point] = self.image2[self.start_point,self.end_point]
        # if self.logic == 4:
        #     color = (255, 0, 0) 
        #     thickness = 2
        #     # radius = int(math.hypot(x - x1, y - y1))
        #     self.start_point = (self.pos1[0], self.pos1[1])
        
        #convert image to RGB format
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = self.image.shape
        step = channel * width
        # create QImage from image
        self.ui.image_label.setGeometry(QtCore.QRect(10, 10, width, height))
        qImg = QImage(self.image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
        # self.ui.image_label.setScaledContents(True)
        # self.ui.image_label.setSizePolicy(True,True)
    def Next(self):
        if self.timer.isActive():
            self.ipAdd = self.ipAdd + 1 
            self.cap = cv2.VideoCapture("C:\\Users\\Krunal parikh\\Desktop\\pyqt5\\P1044012.mp4")
            print(self.ipAdd)   
    def Prev(self):
        if self.timer.isActive():
            self.ipAdd = self.ipAdd + 1 
            self.cap = cv2.VideoCapture("C:\\Users\\Krunal parikh\\Desktop\\pyqt5\\video.mp4")
            print(self.ipAdd)   
    def TDL(self):
        print("TDL TRACKER")
        self.tdl = True
    def Rectangle1(self):
        self.logic = 2
    def Line1(self):
        self.logic = 3
        self.start = []
        self.end = []
    def Undo1(self):
        self.start = self.start[:-1]
        self.end = self.end[:-1]    
    def Reset1(self):
        self.start = []
        self.end = []    
    def Save1(self):
        if self.logic == 2:
            self.first = self.start_point
            self.second = (self.start_point[0],self.end_point[1])
            self.third = (self.start_point[1],self.end_point[0])
            self.fourth = self.end_point
            print(self.first,self.second,self.third,self.fourth,"rectangle coordinates are saved")
        if self.logic == 3:
            i=0
            s=101
            state = "Vadodadara"
            print(len(self.start))
            for i in range(len(self.start)):
                self.X1=self.start[i][0]
                self.Y1=self.start[i][1]
                self.X2=self.end[i][0]
                self.Y2=self.end[i][1]
                print(self.X1 ,self.Y1 ,self.X2 ,self.Y2,state,s)
                coordinate = createPoint(self.X1 ,self.Y1 ,self.X2 ,self.Y2,state,s)
                s = s+1
                print(coordinate)
    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            print('hy')
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")
    
    def mousePressEvent(self, event):
        self.pos1[0], self.pos1[1] = self.ui.image_label.mapFromParent(event.pos()).x(), self.ui.image_label.mapFromParent(event.pos()).y()
        self.drawing=True
        self.pos4, self.pos5 = event.pos().x(), event.pos().y()
        print(self.pos1[0], self.pos1[1])
        if self.logic==3:
            self.linecorr.append((self.pos1[0], self.pos1[1]))
        if self.logic==2:
            self.rectcorr.append((self.pos1[0], self.pos1[1]))
        print("clicked")
    def mouseMoveEvent(self,event):
        self.pos3[0], self.pos3[1] = self.ui.image_label.mapFromParent(event.pos()).x(), self.ui.image_label.mapFromParent(event.pos()).y()
        self.movement = True
        if self.logic==3:
            self.linecorr.append((self.pos3[0], self.pos3[1]))
    def mouseReleaseEvent(self, event):
        self.pos2[0], self.pos2[1] = self.ui.image_label.mapFromParent(event.pos()).x(), self.ui.image_label.mapFromParent(event.pos()).y()
        print("released")
        self.movement=False
        self.end.append((self.pos2[0],self.pos2[1]))
        self.start.append((self.pos1[0],self.pos1[1]))
        if self.logic==3:
            self.linecorr.append((self.pos2[0], self.pos2[1]))
        if self.logic==2:
            self.rectcorr.append((self.pos2[0], self.pos2[1]))
        self.drawing=True
        self.update()


class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui1 = Ui_Form1()
        self.ui1.setupUi(self)
        self.ui1.pushButton.clicked.connect(self.Login)
        self.ui1.pushButton1.clicked.connect(self.Register)
        self.show()  

    def Login(self):
        print("Clicked Enter")
        email=self.ui1.lineEdit_1.text()
        username=self.ui1.lineEdit_2.text()
        password = self.ui1.lineEdit_3.text()
        if (len(username) == 0 or len(email) == 0 or len(password) == 0):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("No Field Can Be Left Blank")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return
        message = login(username, email, password)
        print(message)
        self.cams = MainWindow()
        self.cams.show()
        self.close()
    def Register(self):
        self.cams = SignUp_Window()
        self.cams.show()
        self.close()
class SignUp_Window(QDialog):
    def __init__(self):
        super().__init__()
        self.ui2 = Ui_Form2()
        self.ui2.setupUi(self)
        self.ui2.pushButton.clicked.connect(self.Register)
        self.ui2.pushButton1.clicked.connect(self.Login)
        self.show()  
    def Login(self):
        self.cams = AppWindow()
        self.cams.show()
        self.close()

    def Register(self):
        name = self.ui2.lineEdit_1.text()
        email = self.ui2.lineEdit_2.text()
        username = self.ui2.lineEdit_3.text()
        password = self.ui2.lineEdit_4.text()
        print(username)
        if (len(name) == 0 or len(username) == 0 or len(email) == 0 or len(password) == 0):
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("No Field Can Be Left Blank")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                return
        else:
            print("faa")
            message = createUser(name, username, email, password)
            if message == "User Created":
                print(message)
        self.cams = MainWindow()
        self.cams.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
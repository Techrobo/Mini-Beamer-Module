import FreeCAD as App
import PySide
from PySide import QtCore, QtGui
import csv
import os.path
import os
from stat import S_ISDIR

from .cad import make_parts, close_document, save_parts
#from doe_config_main.laser import suggest_laser


global switch ; switch = 0

csv_filename = 'testdatei_write.csv'


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
 
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)



class Ui_MainWindow(object):
     def __init__(self):
         self.params = None
    
     def setupUi(self, MainWindow):
         self.window = MainWindow
         global switch
 
         MainWindow.setObjectName(_fromUtf8("MainWindow"))
         MainWindow.resize(700, 500)
         #MainWindow.setMinimumSize(QtCore.QSize(600, 300))
         MainWindow.setMaximumSize(QtCore.QSize(700, 500))
         self.widget = QtGui.QWidget(MainWindow)
         self.widget.setObjectName(_fromUtf8("widget"))
 
         #Font
         font = QtGui.QFont()          # see http://doc.qt.io/qt-4.8/qfont.html              # label text displayed and colored in red
         font.setFamily("Times New Roman")                                                   # font used (Windows)
         font.setPointSize(10)                                                               # font PointSize
         font.setWeight(10)                                                                  # font Weight
         font.setBold(True)                                                                  # Bolt True or False 

         #Labeling 
         #label 1 for Width parameter
         self.label_1 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
         self.label_1.setGeometry(QtCore.QRect(30, 62, 190, 45))                           # label coordinates 
         self.label_1.setObjectName(_fromUtf8("label_1"))                                    # label name                                   # Color text
         self.label_1.setText(_translate("MainWindow", "Beamer Width [mm]", None))                 # same resultt with "<b>Hello world</b>"

         #label 2 for Height parameter

         self.label_2 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
         self.label_2.setGeometry(QtCore.QRect(30, 110, 150, 25))                           # label coordinates 
         self.label_2.setObjectName(_fromUtf8("label_2"))                                    # label name                                   # Color text
         self.label_2.setText(_translate("MainWindow", "Beamer Length [mm]", None))                 # same resultt with "<b>Hello world</b>"

         #label 3 for Depth parameter

         self.label_3 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
         self.label_3.setGeometry(QtCore.QRect(30, 145, 150, 25))                           # label coordinates 
         self.label_3.setObjectName(_fromUtf8("label_3"))                                    # label name                                   # Color text
         self.label_3.setText(_translate("MainWindow", "Beamer Depth [mm]", None))                 # same resultt with "<b>Hello world</b>"
         
         #label 4 for Beamer Selection parameter

         self.label_4 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
         self.label_4.setGeometry(QtCore.QRect(30, 30, 150, 25))                           # label coordinates 
         self.label_4.setObjectName(_fromUtf8("label_4"))                                    # label name                                   # Color text
         self.label_4.setText(_translate("MainWindow", "Beamer Selection", None))     

         #label 5 for Lens horizontal distance parameter

         self.label_5 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
         self.label_5.setGeometry(QtCore.QRect(30, 185, 150, 45))                           # label coordinates 
         self.label_5.setObjectName(_fromUtf8("label_5"))                                    # label name                                   # Color text
         self.label_5.setText(_translate("MainWindow", "Lens Horizontal\nDistance [mm]", None)) 
         #label 6 for Lens Vertical distance parameter

         self.label_6 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
         self.label_6.setGeometry(QtCore.QRect(30, 225, 150, 45))                           # label coordinates 
         self.label_6.setObjectName(_fromUtf8("label_6"))                                    # label name                                   # Color text
         self.label_6.setText(_translate("MainWindow", "Lens Vertical\nDistance [mm]", None))            

         self.label_7 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
         self.label_7.setGeometry(QtCore.QRect(30, 275, 150, 45))                           # label coordinates 
         self.label_7.setObjectName(_fromUtf8("label_7"))                                    # label name                                   # Color text
         self.label_7.setText(_translate("MainWindow", "Comp. Location", None))                 # same resultt with "<b>Hello world</b>"
        
         self.label_8 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
         self.label_8.setGeometry(QtCore.QRect(220, 295, 150, 45))                           # label coordinates 
         self.label_8.setObjectName(_fromUtf8("label_8"))                                    # label name                                   # Color text
         self.label_8.setFont(font)
         self.label_8.setText(_translate("MainWindow", "e.g.: C:/Users/ITO/Desktop/Testdatei", None))                 # same resultt with "<b>Hello world</b>"

         self.label_9 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
         self.label_9.setGeometry(QtCore.QRect(465, 295, 150, 45))                           # label coordinates 
         self.label_9.setObjectName(_fromUtf8("label_9"))                                    # label name                                   # Color text
         self.label_9.setFont(font)
         self.label_9.setText(_translate("MainWindow", "file format", None))                 # same resultt with "<b>Hello world</b>"
        
         #section comboBox1 (Drop Down Menu)
         self.cb1 = QtGui.QComboBox(self.widget)
         self.cb1.setGeometry(QtCore.QRect(205, 30, 300, 25))
         #self.cb1.setCurrentText("Select")  
         self.cb1.addItem("KODAK Ultra Mini 75 (RODPJS75)")
         self.cb1.addItem("EZCast J2 Mini Beamer (B08R85YJK2)")
         self.cb1.addItem("ACER AOpen PV12 Mini Beamer (MR.JU611.00E)")
         self.cb1.addItem("CUSTOM BEAMER")
         #self.cb1.currentIndexChanged.connect(self.read_parameters)
         self.cb1.currentIndexChanged.connect(self.selectionchange1)
         

         #section comboBox2
         self.cb2 = QtGui.QComboBox(self.widget)
         self.cb2.setGeometry(QtCore.QRect(465, 287, 110, 18))
         self.cb2.addItem(".stl")
         self.cb2.addItem(".step")
         self.cb2.addItems([".FreeCAD"])
         self.cb2.currentIndexChanged.connect(self.selectionchange2)

         #Horizontal Slider 1 for Width parameter
         #section horizontalSlider 
         self.horizontalSlider1 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
         self.horizontalSlider1.setRange(500, 1200)                                                 #value*10 to get to get one decimal digit
         self.horizontalSlider1.setGeometry(QtCore.QRect(205, 75, 230, 18))                     # coordinates position
         self.horizontalSlider1.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
         self.horizontalSlider1.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
         self.horizontalSlider1.setObjectName(_fromUtf8("horizontalSlider1"))                  # object Name
         self.horizontalSlider1.valueChanged.connect(self.on_horizontal_slider1)               # connect on "def on_horizontal_slider:" for execute action

         #Horizontal Slider 2 for Height parameter 
         self.horizontalSlider2 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
         self.horizontalSlider2.setRange(500, 1200)                                                 #value*10 to get to get one decimal digit
         self.horizontalSlider2.setGeometry(QtCore.QRect(205, 112, 230, 18))                     # coordinates position
         self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
         self.horizontalSlider2.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
         self.horizontalSlider2.setObjectName(_fromUtf8("horizontalSlider2"))                  # object Name
         self.horizontalSlider2.valueChanged.connect(self.on_horizontal_slider2)               # connect on "def on_horizontal_slider:" for execute action

         #Horizontal Slider 3 for Depth parameter 
         self.horizontalSlider3 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
         self.horizontalSlider3.setRange(150, 450)                                                 #value*10 to get to get one decimal digit
         self.horizontalSlider3.setGeometry(QtCore.QRect(205, 147, 230, 18))                     # coordinates position
         self.horizontalSlider3.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
         self.horizontalSlider3.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
         self.horizontalSlider3.setObjectName(_fromUtf8("horizontalSlider3"))                  # object Name
         self.horizontalSlider3.valueChanged.connect(self.on_horizontal_slider3)               # connect on "def on_horizontal_slider:" for execute action

         #Horizontal Slider 4 for Lens Horizontal Distance parameter 
         self.horizontalSlider4 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
         self.horizontalSlider4.setRange(75, 1125)                                                 #value*10 to get to get one decimal digit
         self.horizontalSlider4.setGeometry(QtCore.QRect(205, 197, 230, 18))                     # coordinates position
         self.horizontalSlider4.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
         self.horizontalSlider4.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
         self.horizontalSlider4.setObjectName(_fromUtf8("horizontalSlider4"))                  # object Name
         self.horizontalSlider4.valueChanged.connect(self.on_horizontal_slider4)               # connect on "def on_horizontal_slider:" for execute action

         #Horizontal Slider 5 for Lens Veritical Distance parameter 
         self.horizontalSlider5 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
         self.horizontalSlider5.setRange(45, 405)                                                 #value*10 to get to get one decimal digit
         self.horizontalSlider5.setGeometry(QtCore.QRect(205, 237, 230, 18))                     # coordinates position
         self.horizontalSlider5.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
         self.horizontalSlider5.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
         self.horizontalSlider5.setObjectName(_fromUtf8("horizontalSlider5"))                  # object Name
         self.horizontalSlider5.valueChanged.connect(self.on_horizontal_slider5)               # connect on "def on_horizontal_slider:" for execute action

         #section pushButton 1
         self.pushButton_1 = QtGui.QPushButton(self.widget)                                  # create object PushButton_1
         self.pushButton_1.setGeometry(QtCore.QRect(260, 380, 75, 30))                        # coordinates position
         self.pushButton_1.setObjectName(_fromUtf8("pushButton_1"))                          # name of object
         self.pushButton_1.clicked.connect(self.on_pushButton_1_clicked)                     # connect on def "on_pushButton_1_clicked"
 
         #section pushButton 2
         self.pushButton_2 = QtGui.QPushButton(self.widget)                                  # create object pushButton_2
         self.pushButton_2.setGeometry(QtCore.QRect(420, 380, 75, 30))                       # coordinates position
         self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))                          # name of object
         self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)                     # connect on def "on_pushButton_2_clicked"

         #section pushButton 3
         self.pushButton_3 = QtGui.QPushButton(self.widget)                                  # create object pushButton_2
         self.pushButton_3.setGeometry(QtCore.QRect(100, 380, 75, 30))                       # coordinates position
         self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))                          # name of object
         self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)                     # connect on def "on_pushButton_2_clicked"

         #section lineEdit 1
         #Line edit to input value of the width parameter through slider
         self.lineEdit_1 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_1
         self.lineEdit_1.setGeometry(QtCore.QRect(465, 75, 120, 22))                          # coordinates position
         self.lineEdit_1.setObjectName(_fromUtf8("lineEdit_1"))                              # name of object
         self.lineEdit_1.setText("50.0")                                                        # text by default
         self.lineEdit_1.returnPressed.connect(self.on_lineEdit_1_Pressed)                  # connect on def "on_lineEdit_1_Pressed" for execute actionn   # for validate the data with press on return touch
         #self.lineEdit_1.textChanged.connect(self.on_lineEdit_1_Pressed)                     # connect on def "on_lineEdit_1_Pressed" for execute actionn   # with tips key char by char
        
         #section lineEdit 2
         #Line edit to input value of the height parameter through slider
         self.lineEdit_2 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_3
         self.lineEdit_2.setGeometry(QtCore.QRect(465, 110, 120, 22))                          # coordinates position
         self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))                              # name of object
         self.lineEdit_2.setText("50.0")                                                        # text by default
         self.lineEdit_2.returnPressed.connect(self.on_lineEdit_2_Pressed)                  # connect on def "on_lineEdit_3_Pressed" for execute actionn   # for validate the data with press on return touch
         #self.lineEdit_3.textChanged.connect(self.on_lineEdit_3_Pressed)                     # connect on def "on_lineEdit_3_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects
         #section lineEdit 3
         #Line edit to input value of the depth parameter through slider
         self.lineEdit_3 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_3
         self.lineEdit_3.setGeometry(QtCore.QRect(465, 145, 120, 22))                          # coordinates position
         self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))                              # name of object
         self.lineEdit_3.setText("15.0")                                                        # text by default
         self.lineEdit_3.returnPressed.connect(self.on_lineEdit_3_Pressed)                  # connect on def "on_lineEdit_3_Pressed" for execute actionn   # for validate the data with press on return touch
         #self.lineEdit_3.textChanged.connect(self.on_lineEdit_3_Pressed)                     # connect on def "on_lineEdit_3_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

         #section lineEdit 4
         #Line edit to input value of the Lens Horizontal distance parameter through slider
         self.lineEdit_4 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_3
         self.lineEdit_4.setGeometry(QtCore.QRect(465, 195, 120, 22))                          # coordinates position
         self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))                              # name of object
         self.lineEdit_4.setText("7.5")                                                        # text by default
         self.lineEdit_4.returnPressed.connect(self.on_lineEdit_4_Pressed)                  # connect on def "on_lineEdit_3_Pressed" for execute actionn   # for validate the data with press on return touch
         #self.lineEdit_3.textChanged.connect(self.on_lineEdit_3_Pressed)                     # connect on def "on_lineEdit_3_Pressed" for execute actionn   # with tips key char by char

         #section lineEdit 5
         #Line edit to input value of the depth parameter through slider
         self.lineEdit_5 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_3
         self.lineEdit_5.setGeometry(QtCore.QRect(465, 235, 120, 22))                          # coordinates position
         self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))                              # name of object
         self.lineEdit_5.setText("4.5")                                                        # text by default
         self.lineEdit_5.returnPressed.connect(self.on_lineEdit_5_Pressed)                  # connect on def "on_lineEdit_3_Pressed" for execute actionn   # for validate the data with press on return touch
         #self.lineEdit_3.textChanged.connect(self.on_lineEdit_3_Pressed)                     # connect on def "on_lineEdit_3_Pressed" for execute actionn   # with tips key char by char

         #section lineEdit 6
         self.lineEdit_6 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
         self.lineEdit_6.setGeometry(QtCore.QRect(210, 285, 230, 22))                          # coordinates position
         self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))                              # name of object
         self.lineEdit_6.setText("")                                                        # text by default
         self.lineEdit_6.returnPressed.connect(self.on_lineEdit_6_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
         #self.lineEdit_2.textChanged.connect(self.on_lineEdit_2_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

############################################################################

         font = QtGui.QFont()          # see http://doc.qt.io/qt-4.8/qfont.html              # label text displayed and colored in red
         font.setFamily("Calibri")                                                   # font used (Windows)
         font.setPointSize(13)                                                               # font PointSize
         font.setWeight(10)                                                                  # font Weight
         font.setBold(True)                                                                  # Bolt True or False 
        
         #set font of our labels
         self.label_1.setFont(font)  
         self.label_2.setFont(font) 
         self.label_3.setFont(font)
         self.label_4.setFont(font)
         self.label_5.setFont(font)
         self.label_6.setFont(font)
         self.label_7.setFont(font)
         self.label_8.setFont(font)
         self.label_9.setFont(font)        

         font3 = QtGui.QFont()          # see http://doc.qt.io/qt-4.8/qfont.html              # label text displayed and colored in red
         font3.setFamily("Calibri")                                                   # font used (Windows)
         font3.setPointSize(12)                                                               # font PointSize
         font3.setWeight(10)                                                                  # font Weight
         font3.setBold(True)  

         #set font of our push buttons
         self.pushButton_1.setFont(font3)
         self.pushButton_2.setFont(font3)
         self.pushButton_3.setFont(font3)
       
         font4 = QtGui.QFont()          # see http://doc.qt.io/qt-4.8/qfont.html              # label text displayed and colored in red
         font4.setFamily("Calibri")                                                   # font used (Windows)
         font4.setPointSize(8)                                                               # font PointSize
         font4.setWeight(10)                                                                  # font Weight
         font4.setBold(False)

         #set font of our lineedit values
         self.lineEdit_1.setFont(font4)
         self.lineEdit_2.setFont(font4)  
         self.lineEdit_3.setFont(font4) 
         self.lineEdit_4.setFont(font4) 
         self.lineEdit_5.setFont(font4) 
         self.lineEdit_6.setFont(font4) 

############################################################################
         ### ---graphicsView---
         MainWindow.setCentralWidget(self.widget)
         self.menuBar = QtGui.QMenuBar(MainWindow)
         self.menuBar.setGeometry(QtCore.QRect(0, 0, 500, 26))
         self.menuBar.setObjectName(_fromUtf8("menuBar"))
         MainWindow.setMenuBar(self.menuBar)
         self.mainToolBar = QtGui.QToolBar(MainWindow)
         self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
         MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
         self.statusBar = QtGui.QStatusBar(MainWindow)
         self.statusBar.setObjectName(_fromUtf8("statusBar"))
         MainWindow.setStatusBar(self.statusBar)
         self.statusbar = QtGui.QStatusBar(MainWindow)
         self.statusbar.setObjectName(_fromUtf8("statusbar"))
         MainWindow.setStatusBar(self.statusbar)
 
         self.retranslateUi(MainWindow)
         QtCore.QMetaObject.connectSlotsByName(MainWindow)

         #Initial DEFAULT VALUES
         self.lineEdit_1.setText("50.0")
         self.lineEdit_2.setText("50.0")                                                        # gives the value "0" to the lineEdit_1
         self.lineEdit_3.setText("15.0")                                                        # gives the value "0" to the lineEdit_1
         self.lineEdit_4.setText("7.5")  
         self.lineEdit_5.setText("4.5")
         self.horizontalSlider1.setValue(500)
         self.horizontalSlider2.setValue(500)                                                  # gives the value "0" to the horizontalSlider
         self.horizontalSlider3.setValue(150)                                                  # gives the value "0" to the horizontalSlider
         self.horizontalSlider4.setValue(75)                                                  # gives the value "0" to the horizontalSlider
         self.horizontalSlider5.setValue(45) 
         self.cb1.setCurrentText("CUSTOM BEAMER")  

     def retranslateUi(self, MainWindow):
         MainWindow.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)                   # this function turns the front window (stay to hint)
         MainWindow.setWindowTitle(_translate("MainWindow", "MINI BEAMER MODULE", None))            # title main window
                                
         self.pushButton_1.setToolTip(_translate("MainWindow", "pushButton_1", None))
         self.pushButton_1.setText(_translate("MainWindow", "Reset", None))
                
         self.pushButton_2.setToolTip(_translate("MainWindow", "pushButton_2", None))
         self.pushButton_2.setText(_translate("MainWindow", "Apply", None))     

         self.pushButton_3.setToolTip(_translate("MainWindow", "pushButton_3", None))
         self.pushButton_3.setText(_translate("MainWindow", "Save", None))    
          
         #For conversion of the values entered in height and width and Depth
     def affectation_X (self,val_X0):                                                        # connection affectation_X
         val_X = float(val_X0)                                                              # extract the value and transform it in float
         #
         #here your code
         #
         print( val_X0)
         return (float(val_X))
         #
     def affectation_Y (self,val_Y0):                                                        # connection affectation_X
         val_Y = float(val_Y0)                                                              # extract the value and transform it in float
         #
         #here your code
         #
         print( val_Y0)
         return (float(val_Y))
         #
     def affectation_Z (self,val_Z0):                                                        # connection affectation_X
         val_Z = float(val_Z0)                                                              # extract the value and transform it in float
         #
         #here your code
         #
         print( val_Z0)
         return (float(val_Z))
         #
 
        ########################################################################

     def selectionchange1 (self):
         index = self.cb1.currentIndex() #index of the drop down menu
        
         if index==0:
             global switch
             self.lineEdit_1.setText("78.7")
             self.lineEdit_2.setText("78.7")                                                        # gives the value "0" to the lineEdit_1
             self.lineEdit_3.setText("22.1")                                                        # gives the value "0" to the lineEdit_1
             self.lineEdit_4.setText("7.5")  
             self.lineEdit_5.setText("4.5")  
             self.horizontalSlider1.setValue(787)
             self.horizontalSlider2.setValue(787)                                                  # gives the value "0" to the horizontalSlider
             self.horizontalSlider3.setValue(221)
             self.horizontalSlider4.setValue(75)
             self.horizontalSlider5.setValue(45)
             self.horizontalSlider1.setEnabled(False)
             self.horizontalSlider2.setEnabled(False) 
             self.horizontalSlider3.setEnabled(False)
             self.lineEdit_1.setEnabled(False)
             self.lineEdit_2.setEnabled(False)
             self.lineEdit_3.setEnabled(False)
           
         elif index==1:
             global switch
             self.lineEdit_1.setText("115.0")
             self.lineEdit_2.setText("115.0")                                                        # gives the value "0" to the lineEdit_1
             self.lineEdit_3.setText("32.0")                                                        # gives the value "0" to the lineEdit_1
             self.lineEdit_4.setText("7.5")  
             self.lineEdit_5.setText("4.5") 
             self.horizontalSlider1.setValue(1150)
             self.horizontalSlider2.setValue(1150)                                                  # gives the value "0" to the horizontalSlider
             self.horizontalSlider3.setValue(320)
             self.horizontalSlider4.setValue(75)
             self.horizontalSlider5.setValue(45)
             self.horizontalSlider1.setEnabled(False)
             self.horizontalSlider2.setEnabled(False) 
             self.horizontalSlider3.setEnabled(False)
             self.lineEdit_1.setEnabled(False)
             self.lineEdit_2.setEnabled(False)
             self.lineEdit_3.setEnabled(False)
         
         elif index==2:
             global switch
             self.lineEdit_1.setText("115.0")
             self.lineEdit_2.setText("115.0")                                                        # gives the value "0" to the lineEdit_1
             self.lineEdit_3.setText("42.0")                                                        # gives the value "0" to the lineEdit_1
             self.lineEdit_4.setText("7.5")  
             self.lineEdit_5.setText("4.5")
             self.horizontalSlider1.setValue(1150)
             self.horizontalSlider2.setValue(1150)                                                  # gives the value "0" to the horizontalSlider
             self.horizontalSlider3.setValue(420)
             self.horizontalSlider4.setValue(75)
             self.horizontalSlider5.setValue(45)
             self.horizontalSlider1.setEnabled(False)
             self.horizontalSlider2.setEnabled(False) 
             self.horizontalSlider3.setEnabled(False)
             self.lineEdit_1.setEnabled(False)
             self.lineEdit_2.setEnabled(False)
             self.lineEdit_3.setEnabled(False)
  
         elif index==3:
             self.horizontalSlider1.setEnabled(True)
             self.horizontalSlider2.setEnabled(True) 
             self.horizontalSlider3.setEnabled(True)
             self.lineEdit_1.setEnabled(True)
             self.lineEdit_2.setEnabled(True)
             self.lineEdit_3.setEnabled(True)

   
     def selectionchange2 (self):
        pass  
        ########################################################################
        
     def on_horizontal_slider1(self, val_X):                                                  # connection on_horizontal_slider
         #connect horizonal slider to line edit 1 value of width

      
         self.lineEdit_1.setText(str(val_X/10))
         self.affectation_X(val_X)
         
         #self.Darstellung(val_X)
         #self.label_6.setText(_translate("MainWindow",str(val_X), None))     # display in the label_6 (red)
 
         print( "on_horizontal_slider1" )   
                                                    # displayed on View repport
     def on_horizontal_slider2(self, val_Y):                                                  # connection on_horizontal_slider
         #connect horizonal slider to line edit 3 value of width

         self.lineEdit_2.setText(str(val_Y/10))
         self.affectation_Y(val_Y)
         #self.Darstellung(val_Y)

         print( "on_horizontal_slider2" )    
    
     def on_horizontal_slider3(self, val_Z):                                                  # connection on_horizontal_slider
         #connect horizonal slider to line edit 3 value of width

         self.lineEdit_3.setText(str(val_Z/10))
         self.affectation_Z(val_Z)
         #self.Darstellung(val_Y)

         print( "on_horizontal_slider3" )                                                

     def on_horizontal_slider4(self, val_Z):                                                  # connection on_horizontal_slider
         #connect horizonal slider to line edit 3 value of width

         self.lineEdit_4.setText(str(val_Z/10))
         self.affectation_Z(val_Z)
         #self.Darstellung(val_Y)

         print( "on_horizontal_slider4" )    

     def on_horizontal_slider5(self, val_Z):                                                  # connection on_horizontal_slider
         #connect horizonal slider to line edit 3 value of width

         self.lineEdit_5.setText(str(val_Z/10))
         self.affectation_Z(val_Z)
         #self.Darstellung(val_Y)

         print( "on_horizontal_slider5" )    

         #lineEdit to connect height value with slider change
     def on_lineEdit_1_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
         val_X = float(self.lineEdit_1.text())                                                      # extract the string in the lineEdit
         val_X = round(val_X, 1)
         self.lineEdit_1.setText(str(val_X))
         #
         #here your code
         #
         self.affectation_X(float(val_X))
         try:
             self.horizontalSlider1.setValue(val_X*10)                                      # affect the value "val_X" on horizontalSlider and modify this
         except Exception:                                                                   # if error
             self.horizontalSlider1.setValue(int(0))                                          # affect the value "0" on horizontalSlider and modify this
             val_X = "0"
         print( val_X)
         #
         #lineEdit to connect width value with slider change
     def on_lineEdit_2_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
         val_Y = float(self.lineEdit_2.text())                                                      # extract the string in the lineEdit
         val_Y = round(val_Y, 1)
         self.lineEdit_2.setText(str(val_Y))
         #
         #here your code
         #
         self.affectation_Y(float(val_Y))
         try:
             self.horizontalSlider2.setValue(val_Y*10)                                      # affect the value "val_X" on horizontalSlider and modify this
         except Exception:                                                                   # if error
             self.horizontalSlider2.setValue(int(0))                                          # affect the value "0" on horizontalSlider and modify this
             val_Y = "0"
         print( val_Y)
         #

         #lineEdit to connect width value with slider change
     def on_lineEdit_3_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
         val_Z = float(self.lineEdit_3.text())                                                      # extract the string in the lineEdit
         val_Z = round(val_Z, 1)
         self.lineEdit_3.setText(str(val_Z))
         #
         #here your code
         #
         self.affectation_Z(float(val_Z))
         try:
             self.horizontalSlider3.setValue(val_Z*10)                                      # affect the value "val_X" on horizontalSlider and modify this
         except Exception:                                                                   # if error
             self.horizontalSlider3.setValue(int(0))                                          # affect the value "0" on horizontalSlider and modify this
             val_Z = "0"
         print( val_Z)
         #

     def on_lineEdit_4_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
         val_Z = float(self.lineEdit_4.text())                                                      # extract the string in the lineEdit
         val_Z = round(val_Z, 1)
         self.lineEdit_4.setText(str(val_Z))
         #
         #here your code
         #
         self.affectation_Z(float(val_Z))
         try:
             self.horizontalSlider4.setValue(val_Z*10)                                      # affect the value "val_X" on horizontalSlider and modify this
         except Exception:                                                                   # if error
             self.horizontalSlider4.setValue(int(0))                                          # affect the value "0" on horizontalSlider and modify this
             val_Z = "0"
         print( val_Z)
         #

     def on_lineEdit_5_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
         val_Z = float(self.lineEdit_5.text())                                                      # extract the string in the lineEdit
         val_Z = round(val_Z, 1)
         self.lineEdit_5.setText(str(val_Z))
         #
         #here your code
         #
         self.affectation_Z(float(val_Z))
         try:
             self.horizontalSlider5.setValue(val_Z*10)                                      # affect the value "val_X" on horizontalSlider and modify this
         except Exception:                                                                   # if error
             self.horizontalSlider5.setValue(int(0))                                          # affect the value "0" on horizontalSlider and modify this
             val_Z = "0"
         print( val_Z)
         #

     def on_lineEdit_6_Pressed(self):                                                        # connection on_lineEdit_2_Pressed
        comp = self.lineEdit_6.text()                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.lineEdit_6.setText(str(comp))
        #self.affectation_X(comp)
        #print(comp)
        #return(comp)
        #
 
     def save_parameters(self, filename):
         Width, Height, Depth = self.params
         with open(filename,"w", newline='') as csvdatei:
             csv_writer = csv.writer(csvdatei, delimiter=';')
             csv_writer.writerow(["Holder Hole Width","Holder Hole Height","Holder Hole Depth","Lens Horizontal Distance","Lens Vertical Distance"])
             csv_writer.writerow([Height,Width,Depth,Lens_x,Lens_y])
    
     def read_parameters(self):
         
         Height = float(self.lineEdit_1.text())
         #Height = round(Height,1)
         Width = float(self.lineEdit_2.text())
         #Width = round(Width,1)
         Depth = float(self.lineEdit_3.text())
         #Depth = round(Depth,1)
         Lens_x = float(self.lineEdit_4.text())
         Lens_y = float(self.lineEdit_5.text())
         new_params = ( 
                 Width,
                 Height,
                 Depth,
                 Lens_x,
                 Lens_y
                 )
         params_changed = not (self.params == new_params)
         self.params = new_params
         return params_changed

    
         # Buttons
     def on_pushButton_3_clicked(self):    # Button Save                                     # connection on_pushButton_3_clicked
         changed = self.read_parameters()
         if changed:
            # Only recompute parts if parameters changed
             make_parts(params=self.params)

         format_ = self.cb2.currentIndex()
         dest = self.lineEdit_6.text()
         self.lineEdit_6.setText(str(dest))
         try:
             mode = os.stat(dest).st_mode
         except FileNotFoundError:
             print('Folder "{}" not found.'.format(dest))
             return
         if S_ISDIR(mode):
             self.save_parameters(os.path.join(dest, csv_filename))
             save_parts(format_,dest)
         else:
             print('"{}" is not a valid folder.'.format(dest))

         self.pushButton_3.setStyleSheet("background-color: QPalette.Base")                  # origin system color pushButton_1
         App.Console.PrintMessage("Save\r\n")
         #self.window.hide()                                                                  # hide the window and close the macro
         #

     def on_pushButton_1_clicked(self):    # Button Reset                                    # connection on_pushButton_1_clicked
        
         
         self.lineEdit_1.setText("50.0")
         self.lineEdit_2.setText("50.0")                                                        # gives the value "0" to the lineEdit_1
         self.lineEdit_3.setText("15.0")                                                        # gives the value "0" to the lineEdit_1
         self.lineEdit_4.setText("7.5")  
         self.lineEdit_5.setText("4.5")  
         self.horizontalSlider1.setValue(50)
         self.horizontalSlider2.setValue(50)                                                  # gives the value "0" to the horizontalSlider
         self.horizontalSlider3.setValue(15)                                                  # gives the value "0" to the horizontalSlider
         self.horizontalSlider4.setValue(75)  
         self.horizontalSlider5.setValue(45)  
         self.cb1.setCurrentText("CUSTOM BEAMER")  
         global switch
         
         print(self.lineEdit_1.text())
         print(self.lineEdit_2.text())
         print(self.lineEdit_3.text())
         print(self.lineEdit_4.text())
         print(self.lineEdit_5.text())
         print(self.horizontalSlider1.value)
         print(self.horizontalSlider2.value)
         print(self.horizontalSlider3.value)
         print(self.horizontalSlider4.value)
         print(self.horizontalSlider5.value)
         print( "Reset")
         make_parts(params=self.params)


     def on_pushButton_2_clicked(self):    # Button Apply connection on_pushButton_2_clicked

         #here your code
         #
         print( "Apply")
         changed = self.read_parameters()
         if changed:
             # Only recompute parts if parameters changed
             print("change")
             make_parts(params=self.params)


MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
#MainWindow.show()

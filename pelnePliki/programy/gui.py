import sys
sys.coinit_flags = 2
import pythoncom
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLineEdit, QMessageBox, QLabel, QVBoxLayout, \
    QListWidget, QComboBox, QListWidgetItem, QTableWidget, QTableWidgetItem, QGridLayout, QHeaderView, QMainWindow, \
    QFileDialog, QRadioButton,QCheckBox,QProgressBar
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPalette, QPixmap
import os
import cv2
from structuredLight import StructeredLight
from linearScan import LinearScanner


class CreateFromLinearScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Metoda skanera liniowego')
        self.filePath =None
        self.pclvis=False
        self.bpavis=False
        self.delaunayvis=False
        self.linearHook=None
        self.clipingHeight=-0.03
        self.topLeft=[300,200]
        self.bottomRight=[200,200]
        self.distanceFromCenter=0.49
        self.width=600
        self.height=600
        self.setWidgetHandles()
        self.initUI()
    def setWidgetHandles(self):
        self.pickFileButton = QPushButton('Wybierz plik', self)
        self.startButton = QPushButton('Start', self)
        self.bpaRadiusInput = QLineEdit(self)
        self.bpaRadiusInput.setText("3")
        self.fpsInput = QLineEdit(self)
        self.fpsInput.setText("15")
        
        
        self.inputSetTopLeft= QLineEdit(self)
        self.inputSetTopLeft.setText("340,213")
        self.inputSetBottomRight= QLineEdit(self)
        self.inputSetBottomRight.setText("486,291")
        self.distanceInput= QLineEdit(self)
        self.distanceInput.setText(str(self.distanceFromCenter))
        
        self.bpaRadiusLabel = QLabel(self)
        self.bpaRadiusLabel.setText("Mnożnik długości promienia")
        

        self.labelSetDistance = QLabel(self)
        self.labelSetDistance.setText("Wpisz odległość od środka [m]")
        self.labelfpsInput = QLabel(self)
        self.labelfpsInput.setText("Wpisz wartość FPS")
        self.labelSetTopLeft = QLabel(self)
        self.labelSetTopLeft.setText("Wpisz lewy górny róg X,Y")
        self.labelSetBottomRight = QLabel(self)
        self.labelSetBottomRight.setText("Wpisz prawy dolny róg X,Y")
        
        self.labelFileName = QLabel(self)
        self.labelFileName.setText("Wybierz plik")
        
        self.pointCloudVis=QCheckBox("PCLVis",self)
        self.pointCloudVis.setText("Chmura punktów widoczna")
        self.pointCloudVis.toggled.connect(self.setPclVisibility)
        self.ballpivotVis=QCheckBox("BPAVis",self)
        self.ballpivotVis.setText("BPA widoczne")
        self.ballpivotVis.toggled.connect(self.setBpaVisibility)
        self.delauVis=QCheckBox("BPAVis",self)
        self.delauVis.setText("Triangulacja Delaunay'a widoczna")
        self.delauVis.toggled.connect(self.setDelaunayVisibility)
        self.labelProgressBar = QLabel(self)
        self.labelProgressBar.setText("Ładowanie")
        self.labelProgressBar.hide()
        self.progressBar=QProgressBar(self)
        self.progressBar.hide()


    def setPclVisibility(self):
        self.pclvis=not self.pclvis
    def setBpaVisibility(self):
        self.bpavis=not self.bpavis
    def setDelaunayVisibility(self):
        self.delaunayvis=not self.delaunayvis

    def perToPix(self, percent, axis):
        if axis == 'w':
            return percent * self.width / 100
        else:
            return percent * self.height / 100

    def resizeEvent(self, event):
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.update()

    def update(self):
        self.startButton.resize(self.perToPix(30, 'w'), self.perToPix(10, 'h'))
        self.startButton.move(self.perToPix(5, 'w'), self.perToPix(2, 'h'))


        self.pickFileButton.resize(self.perToPix(20, 'w'), self.perToPix(5, 'h'))
        self.pickFileButton.move(self.perToPix(55, 'w'), self.perToPix(2, 'h'))
        self.labelFileName.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelFileName.move(self.perToPix(55, 'w'), self.perToPix(6, 'h'))

        self.labelSetTopLeft.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelSetTopLeft.move(self.perToPix(55, 'w'), self.perToPix(10, 'h'))
        self.inputSetTopLeft.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.inputSetTopLeft.move(self.perToPix(55, 'w'), self.perToPix(15, 'h'))

        self.labelSetBottomRight.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelSetBottomRight.move(self.perToPix(55, 'w'), self.perToPix(18, 'h'))
        self.inputSetBottomRight.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.inputSetBottomRight.move(self.perToPix(55, 'w'), self.perToPix(23, 'h'))

        self.labelfpsInput.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelfpsInput.move(self.perToPix(55, 'w'), self.perToPix(26, 'h'))
        self.fpsInput.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.fpsInput.move(self.perToPix(55, 'w'), self.perToPix(31, 'h'))


        
        

        self.labelSetDistance.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelSetDistance.move(self.perToPix(55, 'w'), self.perToPix(34, 'h'))
        self.distanceInput.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.distanceInput.move(self.perToPix(55, 'w'), self.perToPix(39, 'h'))



        self.pointCloudVis.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.pointCloudVis.move(self.perToPix(55, 'w'), self.perToPix(45, 'h'))

        self.delauVis.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.delauVis.move(self.perToPix(55, 'w'), self.perToPix(49, 'h'))


        self.ballpivotVis.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.ballpivotVis.move(self.perToPix(55, 'w'), self.perToPix(53, 'h'))
        self.bpaRadiusLabel.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.bpaRadiusLabel.move(self.perToPix(55, 'w'), self.perToPix(58, 'h'))
        self.bpaRadiusInput.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.bpaRadiusInput.move(self.perToPix(55, 'w'), self.perToPix(63, 'h'))




        self.labelProgressBar.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelProgressBar.move(self.perToPix(25, 'w'), self.perToPix(42, 'h'))
        self.progressBar.resize(self.perToPix(40, 'w'), self.perToPix(10, 'h'))
        self.progressBar.move(self.perToPix(10, 'w'), self.perToPix(50, 'h'))


    def initUI(self):
        button_style = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        self.startButton.clicked.connect(self.startProgram)
        self.startButton.setFont(button_style)
        self.pickFileButton.clicked.connect(self.openFile)
        self.pickFileButton.setFont(button_style)
        self.pickFileButton.setStyleSheet("background-color : yellow")
        self.setGeometry(300, 200, 900, 800)
        self.update()
        self.show()
    def openFile(self):
        data_path = QFileDialog.getOpenFileName(None, 'Otwórz plik')
        if data_path:

            myPath = data_path[0].replace(os.sep, '/')
            self.filePath = myPath
            self.labelFileName.setText(myPath)
            self.update()
    def setProgressBarValues(self,value,actionName):
        self.progressBar.setValue(value)
        self.labelProgressBar.setText(str(actionName))
    def startProgram(self):
        self.labelProgressBar.setVisible(True)
        self.progressBar.setVisible(True)

        topLeftPoint=self.inputSetTopLeft.text().split(',')
        convertedTopLeft=(int(topLeftPoint[0]),int(topLeftPoint[1]))
        bottomRightPoint=self.inputSetBottomRight.text().split(',')
        convertedBottomRight=(int(bottomRightPoint[0]),int(bottomRightPoint[1]))
        if self.linearHook:
            self.linearHook.updateVals(convertedTopLeft,convertedBottomRight,self.labelFileName.text(),float(self.distanceInput.text()),self.pclvis,self.bpavis,self.delaunayvis,float(self.bpaRadiusInput.text()),int(self.fpsInput.text()),self.setProgressBarValues)
            self.linearHook.createFromVideo()
        else:
            self.linearHook=LinearScanner(convertedTopLeft,convertedBottomRight,self.labelFileName.text(),float(self.distanceInput.text()),self.pclvis,self.bpavis,self.delaunayvis,float(self.bpaRadiusInput.text()),int(self.fpsInput.text()),self.setProgressBarValues)
            self.linearHook.createFromVideo()
        self.labelProgressBar.hide()
        self.progressBar.hide()
class CreateFromPCL(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Metoda światła strukturalnego')
        self.directory =None
        self.imageName = None
        self.pclvis=False
        self.bpavis=False
        self.delaunayvis=False
        self.angleList=[{"angle":"22.5","frameNumber":16},{"angle":"45","frameNumber":8},{"angle":"90","frameNumber":4}]
        self.chosenFrameNumber=16
        self.clipingHeight=-0.03
        self.beginFileName="nowa_"
        self.distanceUpperBoundry=0.465
        self.distanceLowerBoundry=0.35
        self.distanceFromCenter=0.5
        self.startingFrameValue=309
        self.width=600
        self.height=600
        self.setWidgetHandles()
        self.initUI()
    def setWidgetHandles(self):
        self.pickFolderButton = QPushButton('Wybierz folder', self)
        self.startButton = QPushButton('Start', self)
        self.fileNameInput = QLineEdit(self)
        self.bpaRadiusInput = QLineEdit(self)
        self.bpaRadiusInput.setText("3")
        self.fileNameInput.setText(self.beginFileName)
        
        self.distanceInput= QLineEdit(self)
        self.distanceInput.setText(str(self.distanceFromCenter))
        self.startingFrame = QLineEdit(self)
        self.startingFrame.setText(str(self.startingFrameValue))
        self.clipingHeightInput = QLineEdit(self)
        self.clipingHeightInput.setText(str(self.clipingHeight))
        
        self.distanceInputUpperBoundry = QLineEdit(self)
        self.distanceInputUpperBoundry.setText(str(self.distanceUpperBoundry))
        self.distanceInputLowerBoundry = QLineEdit(self)
        self.distanceInputLowerBoundry.setText(str(self.distanceLowerBoundry))
        
        self.labelFileName = QLabel(self)
        self.labelFileName.setText("Wpisz nazwę początku pliku")
        self.bpaRadiusLabel = QLabel(self)
        self.bpaRadiusLabel.setText("Mnożnik długości promienia")
        
        self.labelSetClipingHeight = QLabel(self)
        self.labelSetClipingHeight.setText("Minimalna wartość Y")
        self.angleDropdownLabel = QLabel(self)
        self.angleDropdownLabel.setText("Wybierz kąt pomiaru")
        self.labelSetDistanceUpperBoundry = QLabel(self)
        self.labelSetDistanceUpperBoundry.setText("Górna granica odległości")
        self.labelSetDistanceLowerBoundry = QLabel(self)
        self.labelSetDistanceLowerBoundry.setText("Dolna granica odległości")
        
        self.labelSetDistance = QLabel(self)
        self.labelSetDistance.setText("Wpisz odległość od środka [m]")
        self.labelStartingFrame=QLabel(self)
        self.labelStartingFrame.setText("Numer początkowej klatki")
        self.labelFolderName = QLabel(self)
        self.labelFolderName.setText("Ścieżka do folderu")
        self.pointCloudVis=QCheckBox("PCLVis",self)
        self.pointCloudVis.setText("Chmura punktów widoczna")
        self.pointCloudVis.toggled.connect(self.setPclVisibility)
        self.ballpivotVis=QCheckBox("BPAVis",self)
        self.ballpivotVis.setText("BPA widoczne")
        self.ballpivotVis.toggled.connect(self.setBpaVisibility)
        self.delauVis=QCheckBox("BPAVis",self)
        self.delauVis.setText("Triangulacja Delaunay'a widoczna")
        self.delauVis.toggled.connect(self.setDelaunayVisibility)
        self.labelProgressBar = QLabel(self)
        self.labelProgressBar.setText("Ładowanie")
        self.labelProgressBar.hide()
        self.progressBar=QProgressBar(self)
        self.progressBar.hide()
        self.angleDropDown = QComboBox(self)
        for item in self.angleList:
            self.angleDropDown.addItem(item['angle'])

    def setPclVisibility(self):
        self.pclvis=not self.pclvis
    def setBpaVisibility(self):
        self.bpavis=not self.bpavis
    def setDelaunayVisibility(self):
        self.delaunayvis=not self.delaunayvis

    def perToPix(self, percent, axis):
        if axis == 'w':
            return percent * self.width / 100
        else:
            return percent * self.height / 100

    def resizeEvent(self, event):
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.update()

    def update(self):
        self.startButton.resize(self.perToPix(30, 'w'), self.perToPix(10, 'h'))
        self.startButton.move(self.perToPix(5, 'w'), self.perToPix(2, 'h'))


        self.pickFolderButton.resize(self.perToPix(20, 'w'), self.perToPix(5, 'h'))
        self.pickFolderButton.move(self.perToPix(55, 'w'), self.perToPix(2, 'h'))
        self.labelFolderName.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelFolderName.move(self.perToPix(55, 'w'), self.perToPix(6, 'h'))
        

        self.labelFileName.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelFileName.move(self.perToPix(55, 'w'), self.perToPix(12, 'h'))
        self.fileNameInput.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.fileNameInput.move(self.perToPix(55, 'w'), self.perToPix(17, 'h'))


        

        self.labelStartingFrame.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelStartingFrame.move(self.perToPix(55, 'w'), self.perToPix(20, 'h'))
        self.startingFrame.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.startingFrame.move(self.perToPix(55, 'w'), self.perToPix(25, 'h'))

        self.labelSetDistance.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelSetDistance.move(self.perToPix(55, 'w'), self.perToPix(28, 'h'))
        self.distanceInput.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.distanceInput.move(self.perToPix(55, 'w'), self.perToPix(33, 'h'))

        self.labelSetDistanceUpperBoundry.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelSetDistanceUpperBoundry.move(self.perToPix(55, 'w'), self.perToPix(36, 'h'))
        self.distanceInputUpperBoundry.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.distanceInputUpperBoundry.move(self.perToPix(55, 'w'), self.perToPix(41, 'h'))

        self.labelSetDistanceLowerBoundry.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelSetDistanceLowerBoundry.move(self.perToPix(55, 'w'), self.perToPix(44, 'h'))
        self.distanceInputLowerBoundry.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.distanceInputLowerBoundry.move(self.perToPix(55, 'w'), self.perToPix(49, 'h'))

        self.labelSetClipingHeight.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelSetClipingHeight.move(self.perToPix(55, 'w'), self.perToPix(52, 'h'))
        self.clipingHeightInput.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.clipingHeightInput.move(self.perToPix(55, 'w'), self.perToPix(57, 'h'))

        self.angleDropdownLabel.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.angleDropdownLabel.move(self.perToPix(55, 'w'), self.perToPix(60, 'h'))
        self.angleDropDown.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.angleDropDown.move(self.perToPix(55, 'w'), self.perToPix(65, 'h'))

        self.pointCloudVis.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.pointCloudVis.move(self.perToPix(55, 'w'), self.perToPix(70, 'h'))

        self.delauVis.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.delauVis.move(self.perToPix(55, 'w'), self.perToPix(73, 'h'))

        self.ballpivotVis.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.ballpivotVis.move(self.perToPix(55, 'w'), self.perToPix(76, 'h'))

        self.bpaRadiusLabel.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.bpaRadiusLabel.move(self.perToPix(55, 'w'), self.perToPix(80, 'h'))
        self.bpaRadiusInput.resize(self.perToPix(30, 'w'), self.perToPix(5, 'h'))
        self.bpaRadiusInput.move(self.perToPix(55, 'w'), self.perToPix(85, 'h'))




        self.labelProgressBar.resize(self.perToPix(30, 'w'), self.perToPix(6, 'h'))
        self.labelProgressBar.move(self.perToPix(25, 'w'), self.perToPix(42, 'h'))
        self.progressBar.resize(self.perToPix(40, 'w'), self.perToPix(10, 'h'))
        self.progressBar.move(self.perToPix(10, 'w'), self.perToPix(50, 'h'))


    def initUI(self):
        button_style = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        self.startButton.clicked.connect(self.startProgram)
        self.startButton.setFont(button_style)
        self.angleDropDown.setStyleSheet("background-color : blue")
        self.angleDropDown.activated.connect(self.changeAngle)
        self.pickFolderButton.clicked.connect(self.openFolder)
        self.pickFolderButton.setFont(button_style)
        self.pickFolderButton.setStyleSheet("background-color : yellow")
        self.setGeometry(300, 200, 900, 800)
        self.update()
        self.show()
    def changeAngle(self,angle):
        self.chosenFrameNumber=self.angleList[angle]['frameNumber']
    def openFolder(self):
        print("tutaj")
        data_path = QFileDialog.getExistingDirectory(None, 'Otwórz folder')
        if data_path:
            myPath = data_path.replace(os.sep, '/')
            self.directory = myPath
            self.labelFolderName.setText(myPath)
            self.update()
    def setProgressBarValues(self,value,actionName):
        self.progressBar.setValue(value)
        self.labelProgressBar.setText(str(actionName))
    def startProgram(self):
        self.labelProgressBar.setVisible(True)
        self.progressBar.setVisible(True)
        structuredHook=StructeredLight(self.fileNameInput.text(),self.directory,float(self.clipingHeightInput.text()),float(self.distanceInput.text()),float(self.distanceInputLowerBoundry.text()),
            float(self.distanceInputUpperBoundry.text()),int(self.startingFrame.text()),self.chosenFrameNumber,self.pclvis,self.bpavis,self.delaunayvis,float(self.bpaRadiusInput.text()),self.setProgressBarValues)
        structuredHook.createAllFromPLY()
        self.labelProgressBar.hide()
        self.progressBar.hide()
class GUI(QWidget):
    def __init__(self, w, h):
        super().__init__()
        self.createFromPCLButton = QPushButton('Światło strukturalne', self)
        self.createFromLinear = QPushButton('Skaner liniowy', self)
        
        self.width = w
        self.height = h
        self.imagePath = None
        self.imageName = None
        self.initUI()

    def perToPix(self, percent, axis):
        if axis == 'w':
            return percent * self.width / 100
        else:
            return percent * self.height / 100

    def resizeEvent(self, event):
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.update()

    def update(self):
        self.createFromLinear.resize(self.perToPix(30, 'w'), self.perToPix(10, 'h'))
        self.createFromLinear.move(self.perToPix(20, 'w'), self.perToPix(20, 'h'))

        self.createFromPCLButton.resize(self.perToPix(30, 'w'), self.perToPix(10, 'h'))
        self.createFromPCLButton.move(self.perToPix(55, 'w'), self.perToPix(20, 'h'))

    def initUI(self):
        button_style = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        self.createFromLinear.clicked.connect(self.openCreateFromLinear)
        self.createFromLinear.setFont(button_style)

        self.createFromPCLButton.clicked.connect(self.openCreateFromPointcloud)
        self.createFromPCLButton.setFont(button_style)
        self.setGeometry(300, 200, 900, 800)
        self.setWindowTitle('Główne okno')
        self.update()
        self.show()
    def openCreateFromPointcloud(self):
        self.fromcldHandle=CreateFromPCL()
    def openCreateFromLinear(self):
        self.linearHandle=CreateFromLinearScanner()
    
    def openFiles(self):
        data_path, _ = QFileDialog.getOpenFileName(None, 'Otwórz plik')
        if data_path:
            myPath = data_path.replace(os.sep, '/')
            self.imagePath = myPath
            myImage = QPixmap(myPath)
            self.imageLabel.setPixmap(myImage)
            self.imageLabel.setScaledContents(True)
            self.processedImageLabel.clear()
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Button, QtCore.Qt.green)
    app.setPalette(palette)
    sz = app.primaryScreen().size()
    ex = GUI(sz.width(), sz.height())
    sys.exit(app.exec_())

from PyQt5 import QtCore, QtGui, QtWidgets
import notifications
from VADetector import VADetector

#global lists to store user's stats
AROUSAL = list()
VALENCE = list()
HEART_RATE = list()

def anaylsis(valence,arousal):
    statue=" "
    if(0>=valence>0.2):# neutral
        if(-0.3>arousal>=0):
            statue="neutral"
        if(arousal>0.2):
            statue="interested"
        else:
            statue="relaxed"    
    if(valence>0.2):# good feelings
        if(arousal>0):
            statue="interested"
        else:
            statue="relaxed"
    else:#valence < 0 bad feelings
        if(arousal>0):
            statue="nervous"
        else:
            statue="tired"
    return statue
def heartRate_anaylsis(heartRate):
    statue=" "
    if(heartRate<50):
        statue="too low"
    if(60>heartRate>50):
        statue="under normal"
    if(76>heartRate>66):
        statue="normal"
    if(90>heartRate>76):
        statue="above normal"
    if(heartRate>90):
        statue="dangerouse"            
    return statue
  
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(280, 200)
        # MainWindow.setMinimumSize(QtCore.QSize(240, 170))
        # MainWindow.setMaximumSize(QtCore.QSize(300, 220))

        #window style
        background_color = "#15202b"
        font_color = "white"
        font = QtGui.QFont()
        font.setWeight(57)

        MainWindow.setFixedSize(280,200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet('QWidget { Background-color: '+background_color+';}')
        #vertical layout for the main window
        self.verticalWindow = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalWindow.setContentsMargins(10, 20, 10, 10)
        self.verticalWindow.setObjectName("verticalWindow")
        #vertical layout for user's input
        self.config_VLayout = QtWidgets.QVBoxLayout()
        self.config_VLayout.setSpacing(0)
        self.config_VLayout.setObjectName("config_VLayout")
        #horizontal layout for period input
        self.time_HLayout = QtWidgets.QHBoxLayout()
        self.time_HLayout.setContentsMargins(20, -1, -1, -1)
        self.time_HLayout.setSpacing(0)
        self.time_HLayout.setObjectName("time_HLayout")
        #period_label
        self.period_lbl = QtWidgets.QLabel(self.centralwidget)
        self.period_lbl.setMaximumSize(QtCore.QSize(16777215, 25))
        self.period_lbl.setObjectName("period_lbl")
        self.period_lbl.setStyleSheet("QLabel { color:"+font_color+";}")
        self.period_lbl.setFont(font)
        self.time_HLayout.addWidget(self.period_lbl)

        #spin box for choosing the period time
        self.period_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.period_spin.setMaximumSize(QtCore.QSize(70, 25))
        self.period_spin.setObjectName("period_spin")
        self.period_spin.setMinimum(1)
        self.period_spin.setMaximum(180)
        self.period_spin.setStyleSheet("QSpinBox { color:"+font_color+";}")
        self.time_HLayout.addWidget(self.period_spin)

        self.config_VLayout.addLayout(self.time_HLayout)
        #horizontal layout for heart rate input
        self.rate_HLayout = QtWidgets.QHBoxLayout()
        self.rate_HLayout.setContentsMargins(20, -1, -1, -1)
        self.rate_HLayout.setObjectName("rate_HLayout")
        #check box to enable the heart rate
        self.heart_rate = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.heart_rate.sizePolicy().hasHeightForWidth())
        self.heart_rate.setSizePolicy(sizePolicy)
        self.heart_rate.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.heart_rate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.heart_rate.setObjectName("heart_rate")
        self.heart_rate.setFont(font)
        self.heart_rate.setStyleSheet("QCheckBox { color:"+font_color+";}")
        self.rate_HLayout.addWidget(self.heart_rate)

        self.config_VLayout.addLayout(self.rate_HLayout)

        self.verticalWindow.addLayout(self.config_VLayout)
        #start button
        self.start = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy)
        self.start.setMinimumSize(QtCore.QSize(100, 20))
        self.start.setMaximumSize(QtCore.QSize(16777215, 40))
        self.start.setObjectName("start")
        self.start.setStyleSheet('QPushButton { color: '+font_color+'; Background-color:#17bf63; border-radius: 15px;}')
        font = QtGui.QFont()
        font.setBold(True)
        self.start.setFont(font)
        self.verticalWindow.addWidget(self.start, 0, QtCore.Qt.AlignHCenter)

        #initialize timer and call the model periodically (but start the timer when start button is clicked)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.model_wrapper)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("QStatusBar { Background-color: "+background_color+";}")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dave"))
        self.period_lbl.setText(_translate("MainWindow", "Time Period (min)"))
        self.heart_rate.setText(_translate("MainWindow", "Heart Rate"))
        self.start.setText(_translate("MainWindow", "START"))
        self.start.clicked.connect(self.switch)

    def switch(self):
        _translate = QtCore.QCoreApplication.translate
        status = self.start.text()
        if status == "START":
            self.start.setText(_translate("MainWindow", "STOP"))
            self.start.setStyleSheet('QPushButton { color: white; Background-color:#ff0000;border-radius: 15px;}')
            period = self.period_spin.value()
            #setting the timer period
            self.timer.setInterval(1000*60*int(period))
            self.timer.start()
            self.model = VADetector()
            print("Model loaded!")
        if status == "STOP":
            self.start.setStyleSheet('QPushButton { color: white; Background-color:#17bf63; border-radius: 15px;}')
            self.start.setText(_translate("MainWindow", "START"))
            #stop the timer
            self.timer.stop()
  
    def model_wrapper(self):
        heart_enabled = self.heart_rate.checkState()
        #To be removed
        arousal, valence, heart_rate = 10,10,10
        mood = "Distructed"
        print("capturing...")
        arousal, valence = self.model(capture_period=15)
        print("captured!")
        # if heart_enabled:
            # heart_rate = model()

        mood = anaylsis(valence,arousal)

        AROUSAL.append(arousal)
        VALENCE.append(valence)
        HEART_RATE.append(heart_rate)
        #pop-up notifications
        notifications.show_notification(self, mood, AROUSAL, VALENCE, HEART_RATE)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


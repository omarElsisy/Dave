from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class Ui_ReportWindow(object):
    def __init__(self, arousal, valence, heart_rate, mood):
        #initialize user stats
        self.arousal = arousal
        self.valence = valence
        self.heart_rate = heart_rate
        self.Umood = mood
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        #window style
        background_color = "#15202b"
        font_color = "white"
        font = QtGui.QFont()
        font.setWeight(80)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #set background and font colors for the main window
        self.centralwidget.setStyleSheet('QWidget { Background-color:'+background_color+'; color:'+font_color+';}')

        #gridLayout for the main window
        self.gridWindow = QtWidgets.QGridLayout(self.centralwidget)
        self.gridWindow.setObjectName("gridWindow")
        # set the second row (plots row) to fill up twice the height of empty space taken by the first row (labels row)
        self.gridWindow.setRowStretch(0, 1)
        self.gridWindow.setRowStretch(1, 5)

        #grid layout for user's data (heart rate & mood)
        self.gridLabels = QtWidgets.QGridLayout()
        self.gridLabels.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLabels.setObjectName("gridLabels")
        #add left and top padding to the grid layout
        self.gridLabels.setContentsMargins(QtCore.QMargins(10,10,0,0))

        #configure heart rate label
        self.rate = QtWidgets.QLabel(self.centralwidget)
        self.rate.setMaximumSize(QtCore.QSize(77, 16777215))
        self.rate.setObjectName("rate")
        self.rate.setFont(font)
        self.gridLabels.addWidget(self.rate, 0, 0, 1, 1)

        #configure user's heart rate (number) label
        self.current_rate = QtWidgets.QLabel(self.centralwidget)
        self.current_rate.setObjectName("current_rate")
        self.current_rate.setFont(font)
        self.gridLabels.addWidget(self.current_rate, 0, 1, 1, 1)

        #configure mood label
        self.mood = QtWidgets.QLabel(self.centralwidget)
        self.mood.setMaximumSize(QtCore.QSize(77, 16777215))
        self.mood.setObjectName("mood")
        self.mood.setFont(font)
        self.gridLabels.addWidget(self.mood, 2, 0, 1, 1)

        #configure user's mood label
        self.current_mood = QtWidgets.QLabel(self.centralwidget)
        self.current_mood.setObjectName("current_mood")
        self.current_mood.setFont(font)
        self.gridLabels.addWidget(self.current_mood, 2, 1, 1, 1)

        #add gridLabels (gridLayout) to the main grid layout
        self.gridWindow.addLayout(self.gridLabels, 0, 0, 1, 1)

        #grid layout for the three plots
        self.gridPlots = QtWidgets.QGridLayout()
        self.gridPlots.setObjectName("gridPlots")

        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.figure.set_facecolor(background_color)
        self.figure.clf()
        # with matplotlib.rc_context({'axes.edgecolor':'orange', 'xtick.color':'red', 'ytick.color':'green', 'figure.facecolor':'white'}):
        valence_graph = self.figure.add_subplot(221, xlabel="Periods", ylabel="Valence")
        self.canvas.draw_idle()

        x1 = range(1, len(self.valence) + 1)
        y1 = self.valence
        valence_graph.plot(x1, y1, 'b.-')

        arousal_graph = self.figure.add_subplot(222, xlabel="Periods", ylabel="Arousal")
        x2 = range(1, len(self.arousal) + 1)
        y2 = self.arousal
        arousal_graph.plot(x2, y2, 'b.-')

        rate_graph = self.figure.add_subplot(212, fc = "white", xlabel="Periods", ylabel="Heart rate (bpm)")
        x3 = range(1, len(self.heart_rate) + 1)
        y3 = self.heart_rate
        rate_graph.plot(x3, y3, 'b.-')

        self.figure.tight_layout(pad=3)
        self.canvas.draw_idle()

        self.gridPlots.addWidget(self.canvas, 0, 0, 1, 1)
        self.gridWindow.addLayout(self.gridPlots, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("QStatusBar { Background-color:"+background_color+";}")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Report"))
        self.current_mood.setText(_translate("MainWindow", str(self.Umood)))
        self.mood.setText(_translate("MainWindow", "Mood:"))
        self.rate.setText(_translate("MainWindow", "Heart rate:"))
        if len(self.heart_rate) > 0:
            rate = str(self.heart_rate[len(self.heart_rate) - 1])
        else:
            rate = "0"
        self.current_rate.setText(_translate("MainWindow", rate))

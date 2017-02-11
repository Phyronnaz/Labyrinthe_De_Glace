import numpy as np
from PyQt5 import QtCore, QtWidgets
from qlabyrintheview import QLabyrintheView
from main import genere_grille, deplacement, grille_vierge


class Ui_MainWindow(object):
    def __init__(self, n, p, fin, direction):
        self.grille, self.debut, T, self.chemin = genere_grille(n, p, fin, direction)
        print('Done')

        self.position = self.debut

        x = fin[0] + [-1, 1, 0, 0][direction]
        y = fin[1] + [0, 0, -1, 1][direction]
        self.fin = x, y

        self.textes = T
        self.colors = np.zeros((n, p), dtype=object)

        T_tmp = T.copy()
        T_tmp[T_tmp == np.inf] = -np.inf
        m = T_tmp.max()
        for i in range(n):
            for j in range(p):
                x = T[i, j] / m
                r = 255
                g = 0
                b = 0
                a = min(x * 200, 255)
                self.colors[i, j] = r, g, b, a

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(852, 467)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QLabyrintheView(self.grille, self.debut, self.fin, self.chemin, self.textes, self.colors,
                                            self.centralWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButtonUp = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonUp.setObjectName("pushButtonUp")
        self.verticalLayout.addWidget(self.pushButtonUp)
        self.pushButtonDown = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonDown.setObjectName("pushButtonDown")
        self.verticalLayout.addWidget(self.pushButtonDown)
        self.pushButtonLeft = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonLeft.setObjectName("pushButtonLeft")
        self.verticalLayout.addWidget(self.pushButtonLeft)
        self.pushButtonRight = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonRight.setObjectName("pushButtonRight")
        self.verticalLayout.addWidget(self.pushButtonRight)
        self.pushButtonRestart = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonRestart.setObjectName("pushButtonRestart")
        self.verticalLayout.addWidget(self.pushButtonRestart)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 852, 19))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButtonDown.clicked.connect(self.down)
        self.pushButtonUp.clicked.connect(self.up)
        self.pushButtonLeft.clicked.connect(self.left)
        self.pushButtonRight.clicked.connect(self.right)
        self.pushButtonRestart.clicked.connect(self.restart)
        self.pushButtonDown.setShortcut("down")
        self.pushButtonUp.setShortcut("up")
        self.pushButtonLeft.setShortcut("left")
        self.pushButtonRight.setShortcut("right")
        self.pushButtonRestart.setShortcut("Space")

    def restart(self):
        self.position = self.debut
        self.graphicsView.move(self.position)

    def down(self):
        self.position = deplacement(self.grille, self.position, 2)
        self.graphicsView.move(self.position)

    def up(self):
        self.position = deplacement(self.grille, self.position, 0)
        self.graphicsView.move(self.position)

    def left(self):
        self.position = deplacement(self.grille, self.position, 3)
        self.graphicsView.move(self.position)

    def right(self):
        self.position = deplacement(self.grille, self.position, 1)
        self.graphicsView.move(self.position)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonUp.setText(_translate("MainWindow", "Up"))
        self.pushButtonDown.setText(_translate("MainWindow", "Down"))
        self.pushButtonLeft.setText(_translate("MainWindow", "Left"))
        self.pushButtonRight.setText(_translate("MainWindow", "Right"))
        self.pushButtonRestart.setText(_translate("MainWindow", "Restart"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    n, p = 5, 5
    fin = 0, 2
    direction = 0
    ui = Ui_MainWindow(n, p, fin, direction)
    ui.setupUi(MainWindow, )
    MainWindow.showMaximized()
    sys.exit(app.exec_())

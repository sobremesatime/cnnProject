from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(572, 572)


        self.label1 = QtWidgets.QLabel()
        self.label1.setObjectName("draw_window")
        self.label1.setFrameShape(QtWidgets.QFrame.Panel)
        self.label1.setText("")
        self.label1.setMinimumSize(400, 400)
        palette_white = QtGui.QPalette()
        palette_white.setColor(QtGui.QPalette.Window, QtCore.Qt.black)
        self.label1.setPalette(palette_white)

        self.label2 = QtWidgets.QLabel()
        self.label2.setObjectName("result_label")
        self.label2.setText("结果：")
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setMaximumSize(60, 30)

        self.label3 = QtWidgets.QLabel()
        self.label3.setFrameShape(QtWidgets.QFrame.Box)
        self.label3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label3.setObjectName("reslut_num")
        self.label3.setText("")
        self.label3.setMaximumSize(60, 30)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayout0 = QtWidgets.QHBoxLayout()
        self.horizontalLayout0.addWidget(self.label2)
        self.horizontalLayout0.addWidget(self.label3)

        self.horizontalLayout1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout1.addLayout(self.horizontalLayout0)
        self.horizontalLayout1.addWidget(self.label1)



        self.pushButton1 = QtWidgets.QPushButton()
        self.pushButton1.setObjectName("recognition")
        self.pushButton1.setText("识别")
        self.pushButton2 = QtWidgets.QPushButton()
        self.pushButton2.setObjectName("clear")
        self.pushButton2.setText("清空")
        self.pushButton3 = QtWidgets.QPushButton()
        self.pushButton3.setObjectName("close")
        self.pushButton3.setText("关闭")
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.addWidget(self.pushButton1)
        self.horizontalLayout2.addWidget(self.pushButton2)
        self.horizontalLayout2.addWidget(self.pushButton3)


        self.verticalLayout_top = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_top.addLayout(self.horizontalLayout1)
        self.verticalLayout_top.addLayout(self.horizontalLayout2)

        self.setLayout(self.verticalLayout_top)
        self.setGeometry(400, 400, 600, 300)






        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "手写数字识别"))
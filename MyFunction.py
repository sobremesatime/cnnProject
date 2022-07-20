from MyGui import Ui_Form
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtGui import QPainter,QColor,QFont, QPen
from PyQt5.QtCore import Qt
from PIL import ImageGrab, Image
import PIL
from CnnModel import LeNet_5
import torch
import numpy as np
import matplotlib.pyplot as plt

class myFunction(QWidget, Ui_Form):
    def __init__(self):
        super(myFunction, self).__init__()  #初始化父类
        self.setupUi(self)

        # setMouseTracking设置为False，否则不按下鼠标时也会跟踪鼠标事件
        self.setMouseTracking(False)

        self.pos_xy = []
        self.label_range = [0, 0, 0, 0]

        self.pushButton1.clicked.connect(self.btn_recognize_on_clicked)
        self.pushButton2.clicked.connect(self.btn_clear_on_clicked)
        self.pushButton3.clicked.connect(self.btn_close_on_clicked)


        # init model
        with torch.no_grad():
            # self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.device = 'cpu'
            self.model = LeNet_5().to(self.device)
            self.model.eval()
            self.ckpt_path = 'models/LeNet+.pth'
            self.model=torch.load(self.ckpt_path, map_location=self.device)


    def test(self):
        print(super(myFunction, self).width(), self.x(), self.label1.x(), self.label1.width())
        print(self.label_range)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 10, Qt.SolidLine)
        painter.setPen(pen)


        if len(self.pos_xy) > 1:
            point_start = self.pos_xy[0]
            for pos_tmp in self.pos_xy:
                point_end = pos_tmp

                # 判断是否是断点
                if point_end == (-1, -1):
                    point_start = (-1, -1)
                    continue
                if point_start == (-1, -1):
                    point_start = point_end
                    continue

                painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end
        painter.end()

    def range_limit(self, x, y):

        if (x < self.label_range[0]) or (x > self.label_range[2]):
            pos_x = -1
            pos_y = -1

        elif (y < self.label_range[1]) or (y > self.label_range[3]):
            pos_x = -1
            pos_y = -1
        else:
            pos_x = x
            pos_y = y

        return (pos_x, pos_y)

    def get_limit_range(self, offset=20):
        self.label_range = [self.label1.x() + offset,
                            self.label1.y() + offset,
                            self.label1.x() + self.label1.width() - offset,
                            self.label1.y() + self.label1.height() - offset]

    def mouseMoveEvent(self, event):
        '''
            按住鼠标移动事件：将当前点添加到pos_xy列表中
        '''

        self.get_limit_range()
        #中间变量pos_tmp提取当前点
        pos_tmp = self.range_limit(event.pos().x(), event.pos().y())
        #pos_tmp添加到self.pos_xy中
        self.pos_xy.append(pos_tmp)

        self.update()

    def mouseReleaseEvent(self, event):
        '''
            鼠标按住后松开的事件
            在每次松开后向pos_xy列表中添加一个断点(-1, -1)
        '''
        pos_test = (-1, -1)
        self.pos_xy.append(pos_test)

        self.update()

    def btn_recognize_on_clicked(self):
        self.get_limit_range()
        im_range = [self.label_range[0] + self.x(),
                    self.label_range[1] + self.y() + 30,
                    self.label_range[2] + self.x(),
                    self.label_range[3] + self.y() + 30]
        im = ImageGrab.grab(im_range)  # 截屏，手写数字部分
        im = im.convert('L')
        im = im.resize((28, 28), Image.ANTIALIAS)  # 将截图转换成 28 * 28 像素
        im = np.array(im).astype(np.float32)
        self.get_img2bin(im, threshlod=200)
        # print(im)
        # plt.imshow(im)
        # plt.show()
        recognize_result = self.recognize_img(im)  # 调用识别函数
        self.label3.setText(str(recognize_result))  # 显示识别结果
        self.update()

    def get_img2bin(self, img, threshlod=200):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j] > threshlod:
                    img[i, j] = 0
                else:
                    img[i, j] = 1

    def recognize_img(self, img):
        with torch.no_grad():
            x = torch.from_numpy(img).to(self.device).unsqueeze(0).unsqueeze(0)
            y = self.model(x).cpu().numpy()
            pred = np.argmax(y)
        return pred

    def btn_clear_on_clicked(self):
        self.pos_xy = []
        self.label3.setText('')
        self.update()

    def btn_close_on_clicked(self):
        self.close()
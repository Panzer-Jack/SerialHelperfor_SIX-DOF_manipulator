import sys
import time
from robArm import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import serial
import threading
import numpy as np
import xlwt
import xlrd

res1 = "34"
res2 = "104"
res3 = "106"
res4 = "166"
res5 = "100"
res6 = "157"
com = ""
msgGlobal = ""
msgGlobalOld = ""
gjzText = 0


class serial_frameGJZ(QThread):
    def __init__(self, parent=None, ser=None):
        super(serial_frameGJZ, self).__init__(parent)
        self.ser = ser

    def serial_C(self):
        worksheet2 = xlrd.open_workbook("机械臂关键帧-确认表.xlsx")
        sheet = worksheet2.sheet_by_index(0)
        # self.ser = serial.Serial(com, 9600, timeout=0.5)

        while 1:
            i = int(gjzText)
            print(i)
            if i == -1:
                break
            self.ser.write(
                f"{str(sheet.row_values(i)[0])} {str(sheet.row_values(i)[1])} {str(sheet.row_values(i)[2])} {str(sheet.row_values(i)[3])} {str(sheet.row_values(i)[4])} {str(sheet.row_values(i)[5])} 90".encode())
            msg = self.ser.readlines()
            # print()
            if msg:
                print(msg)
            #     break
            time.sleep(2)
        pass

    def run(self):
        self.serial_C()


class serial_frameTest(QThread):
    def __init__(self, parent=None, ser=None):
        super(serial_frameTest, self).__init__(parent)
        self.ser = ser

    def serial_C(self):
        worksheet2 = xlrd.open_workbook("机械臂关键帧-确认表.xlsx")
        sheet = worksheet2.sheet_by_index(0)
        # self.ser = serial.Serial(com, 9600, timeout=0.5)

        for i in range(0, sheet.nrows):
            while 1:
                self.ser.write(
                    f"{str(sheet.row_values(i)[0])} {str(sheet.row_values(i)[1])} {str(sheet.row_values(i)[2])} {str(sheet.row_values(i)[3])} {str(sheet.row_values(i)[4])} {str(sheet.row_values(i)[5])} 90".encode())
                msg = self.ser.readlines()
                if msg:
                    print(msg)
                    break
                time.sleep(5)
            print(sheet.row_values(i))
        pass

    def run(self):
        self.serial_C()


class serial_control(QThread):
    update_date = pyqtSignal(str)

    def __init__(self, parent=None, ser=None):
        super(serial_control, self).__init__(parent)
        self.ser = ser

    def serial_C(self, ser):
        global res1, res2, res3, res4, res5, res6, msgGlobal, msgGlobalOld
        while 1:
            ser.write(
                f"{res1} {res2} {res3} {res4} {res5} {res6} 90".encode())
            msg = ser.readlines()
            if msg:
                msgGlobal = msg
                print(msg)
                if msgGlobal != msgGlobalOld:
                    msgGlobalOld = msgGlobal
                    self.update_date.emit('update')
                break
            time.sleep(0.1)

    def run(self):
        # ser = serial.Serial(com, 9600, timeout=0.5)
        while 1:
            self.serial_C(self.ser)


class mainWin(QMainWindow, Ui_ETC_UI_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowIcon(QIcon('qtMain.ico'))

        # 主程序按钮
        self.button_close.clicked.connect(self.evt_close)
        self.button_small.clicked.connect(self.evt_small)
        self.button_testFrame.clicked.connect(self.run_frameTable)
        self.button_run.clicked.connect(self.run)
        self.recordButton.clicked.connect(self.recordFrame)
        self.gjz_button.clicked.connect(self.gjz_step)
        self.recordButton_2.clicked.connect(self.oc_serial)
        self.flag = 0
        self.row = 0
        self.gjzText = 0
        self.ser = None
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.worksheet = self.workbook.add_sheet("机械臂关键帧-sheet1")

        self.slider.valueChanged.connect(self.valueChange)
        self.slider_2.valueChanged.connect(self.valueChange)
        self.slider_3.valueChanged.connect(self.valueChange)
        self.slider_4.valueChanged.connect(self.valueChange)
        self.slider_5.valueChanged.connect(self.valueChange)
        self.slider_6.valueChanged.connect(self.valueChange)

        self.textSlider.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                f'font-size:18pt; font-weight:100; color:#00ff00;">{res1}</span></p>')
        self.textSlider_2.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res2}</span></p>')
        self.textSlider_3.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res3}</span></p>')
        self.textSlider_4.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res4}</span></p>')
        self.textSlider_5.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res5}</span></p>')
        self.textSlider_6.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res6}</span></p>')

        # 窗口可拖动
        self.mouse_x = self.mouse_y = self.origin_x = self.origin_y = None
        QMessageBox.about(self, '天父的博爱',
                          '“凡事都不可亏欠人，惟有彼此相爱，当常以为亏欠，因为爱人的，就完全了律法。'
                          '像那不可奸淫，不可杀人，不可偷盗，不可贪婪，或有别的诫命，都包在爱人如己这一句话之内的。'
                          '爱是不加害于人的，所以爱就完全了律法。” \n      ------------（《新约·罗马书》第十三章）\n'
                          '所以你们也要爱我，所以当出现新的bug时 先别急着找@我去debug。神是爱你们的，要先想想如何找到天父为你们放置的另一个接口，'
                          '神曰：当上帝关了这扇门，一定会为你打开另一扇门。\n      ------------ 天父 · Panzer_Jack')

    # # 1.鼠标点击事件
    # def mousePressEvent(self, evt):
    #     # 获取鼠标当前的坐标
    #     self.mouse_x = evt.globalX()
    #     self.mouse_y = evt.globalY()
    #
    #     # 获取窗体当前坐标
    #     self.origin_x = self.x()
    #     self.origin_y = self.y()
    #
    # # 2.鼠标移动事件
    # def mouseMoveEvent(self, evt):
    #     # 计算鼠标移动的x，y位移
    #     move_x = evt.globalX() - self.mouse_x
    #     move_y = evt.globalY() - self.mouse_y
    #
    #     # 计算窗体更新后的坐标：更新后的坐标 = 原本的坐标 + 鼠标的位移
    #     dest_x = self.origin_x + move_x
    #     dest_y = self.origin_y + move_y
    #
    #     # 移动窗体
    #     self.move(dest_x, dest_y)

    def oc_serial(self):
        global com
        com = self.lineEdit_7.text()
        self.ser = serial.Serial(com, 9600, timeout=0.5)
        self.serial_runFrameTest = serial_frameTest(ser=self.ser)
        self.serial_runFrameGJZ = serial_frameGJZ(ser=self.ser)
        self.serial_run = serial_control(ser=self.ser)
        self.serial_run.update_date.connect(self.get_Info)

    def gjz_step(self):
        global gjzText, com
        com = self.lineEdit_7.text()
        gjzText = self.gjz_line.text()
        print(gjzText)
        if not self.flag:
            self.flag = 1
            self.serial_runFrameGJZ.start()

    def get_Info(self):
        msg = ""
        for i in range(0, len(msgGlobal)):
            msg += msgGlobal[i].decode()
        self.showTable.append(f"{msg}")

    def run_frameTable(self):
        global com
        com = self.lineEdit_7.text()
        self.serial_runFrameTest.start()

    def recordFrame(self):
        self.worksheet.write(self.row, 0, str(res1))
        self.worksheet.write(self.row, 1, str(res2))
        self.worksheet.write(self.row, 2, str(res3))
        self.worksheet.write(self.row, 3, str(res4))
        self.worksheet.write(self.row, 4, str(res5))
        self.worksheet.write(self.row, 5, str(res6))
        self.worksheet.write(self.row, 6, "90")
        self.row += 1

    def valueChange(self):
        global res1, res2, res3, res4, res5, res6
        time.sleep(0.1)
        res1 = self.slider.value()
        res2 = self.slider_2.value()
        res3 = self.slider_3.value()
        res4 = self.slider_4.value()
        res5 = self.slider_5.value()
        res6 = self.slider_6.value()
        # com = self.lineEdit_7.text()

        # print("test:", res1, res2, res3, res4, res5, res6)
        self.textSlider.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                f'font-size:18pt; font-weight:100; color:#00ff00;">{res1}</span></p>')
        self.textSlider_2.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res2}</span></p>')
        self.textSlider_3.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res3}</span></p>')
        self.textSlider_4.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res4}</span></p>')
        self.textSlider_5.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res5}</span></p>')
        self.textSlider_6.setText(f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                  'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                  f'font-size:18pt; font-weight:100; color:#00ff00;">{res6}</span></p>')

    def run(self):
        # global com
        # com = self.lineEdit_7.text()
        self.serial_run.start()

    def go_CV_thread(self):
        self.evt_run.start()

    def evt_small(self):
        self.showMinimized()

    def evt_close(self):
        self.workbook.save("机械臂关键帧-录取表.xlsx")
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = mainWin()
    main_win.show()
    sys.exit(app.exec_())

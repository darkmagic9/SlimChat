# -*- coding: utf-8 -*-

"""
Module implementing Dialog_additem.
"""

from PyQt5.QtCore import pyqtSlot, QPoint, Qt, QEvent
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QPainter
import sys
from Additem_ui import *


class Dialog_additem(QDialog, Ui_Dialog_For_Additem):
    """
    Class documentation goes here.
    """
    def __init__(self, des_id, temp, userslist, self_id, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog_additem, self).__init__(parent)
        self.setupUi(self)
        self.temp = temp
        self.userslist = userslist
        self.des_id = des_id
        self.self_id = self_id
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.closeBt.setIcon(QIcon('img/blueclose.png'))
        self.top.installEventFilter(self)
        #self.flag = False#判断返回的联系人图标是默认的还是自定义的
        #self.iconpath = ''
        self.m_drag = False
        self.m_DragPosition = QPoint()
        self.pbAdd.clicked.connect(self.pbAddClicked)
        self.closeBt.clicked.connect(self.closeBtClicked)
    


    def eventFilter(self, obj, event):
        if obj == self.top:
            if event.type() == QEvent.Paint:
                painter = QPainter(self.top)
                painter.drawPixmap(self.top.rect(), QPixmap('img/top.png'))
        return QWidget.eventFilter(self, obj, event)

    def mousePressEvent(self, event):
        if event.button()== Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False



    '''@pyqtSlot(bool)
    def on_radioButton_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        self.flag = False
        if self.pushButton.isEnabled() == True:
            self.pushButton.setEnabled(False)
    
    @pyqtSlot(bool)
    def on_radioButton_2_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        self.flag = True
        if self.pushButton.isEnabled() == False:
            self.pushButton.setEnabled(True)
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        fname = QFileDialog.getOpenFileName(self, '打开文件','./res/user/',("Images (*.png *.jpg)"))
        if fname[0]:
            self.iconpath = fname[0]
    '''

    @pyqtSlot()
    def pbAddClicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self,'提示','好友姓名为空')
            self.lineEdit.setFocus()
        elif self.lineEdit.text().isdigit() == False:
            QMessageBox.critical(self, '提示', '个人账号应该为数字，请重新输入！')
        else:
            users = []
            for user in self.userslist:
                users.append(user['userid'])
            if int(self.lineEdit.text()) == self.self_id:
                QMessageBox.information(self, '提示', '不能添加自己为好友！')
            elif int(self.lineEdit.text()) in users:
                QMessageBox.information(self, '提示', '联系人已存在好友列表中！')
            else:
                self.des_id[0] = int(self.lineEdit.text())
                self.temp[int(self.lineEdit.text())] =  self.comboBox.currentText()
                self.done(1)#给主窗口的返回值
    
    @pyqtSlot()
    def closeBtClicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        self.done(-1)

    '''
    def geticonpath(self):
        if self.flag == True:
            return self.iconpath
        else:
            return "./res/user/default.jpg"
    '''
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     xx = Dialog_additem()
#     xx.show()
#     sys.exit(app.exec_())
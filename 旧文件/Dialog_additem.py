# -*- coding: utf-8 -*-

"""
Module implementing Dialog_additem.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
import sys
from Ui_additem_ui import Ui_Dialog


class Dialog_additem(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog_additem, self).__init__(parent)
        self.setupUi(self)
        self.flag = False#判断返回的联系人图标是默认的还是自定义的
        self.iconpath = ''
    
    @pyqtSlot(bool)
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
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self,'提示','好友姓名为空')
            self.lineEdit.setFocus()
        else:
            self.done(1)#给主窗口的返回值
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        self.done(-1)

    def geticonpath(self):
        if self.flag == True:
            return self.iconpath
        else:
            return "./res/user/default.jpg"

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     xx = Dialog_additem()
#     xx.show()
#     sys.exit(app.exec_())
from PyQt5.QtGui import QPainter, QStandardItem
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from PyQt5.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from chat import FeedBackListItem
from Chat_ui import Ui_Form_For_Chat
from record import RecordTextEdit
from PyQt5.QtWidgets import QTextEdit, QLabel, QWidget, QVBoxLayout, QPushButton, QTextEdit,  QListWidget
#class NoFocusDelegate(QStyledItemDelegate):
#   def __init__(self):
#       super().__init__()
#
#   def paint(painter, option, index):
#        itemOption = QStyleOptionViewItem(option)
#        if itemOption.state & QStyle.State_HasFocus:
#            itemOption.state = itemOption.state ^ QStyle.State_HasFocus
#        
#        QStyledItemDelegate.paint(painter, itemOption, index)



class FeedBackUI(QWidget, Ui_Form_For_Chat):
    sendMsgSignal = pyqtSignal(int, str)
    sendPicSignal = pyqtSignal(int, bytes)
    sendFileSignal = pyqtSignal(int, str)
    def __init__(self, self_id, self_head, name, id, head, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.self_head = self_head
        self.name = name
        self.id = id 
        self.self_id = self_id
        self.head = head
        self.wf = 1
        self.hf = 1
        self.initWgt()
        self.closeBt.clicked.connect(self.my_close)
        self.minBt.clicked.connect(self.showMinimized)
        self.s_pic.clicked.connect(self.sendPic)
        self.s_file.clicked.connect(self.sendFile)
        self.cache = ""
        self.m_drag = False
        self.m_DragPosition = QPoint()

        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap('img/background/bg6.jpg')))
        self.setPalette(palette)

        

    def initWgt(self):
        self.lblName.setText(self.name)
        self.lblId.setText(str(self.id))
        image = QImage()
        image.loadFromData(self.head)
        self.lblHead.setScaledContents(True)
        self.lblHead.setPixmap(QPixmap.fromImage(image))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(
                            "QListWidget{"
                                "border:        1px solid #8AA0B8;"
                            "}"
                            "QTextEdit{"
                                "border-top:    0px solid #8AA0B8;"
                                "border-right:  1px solid #8AA0B8;"
                                "border-bottom: 1px solid #8AA0B8;"
                                "border-left:   1px solid #8AA0B8;"
                            "}"
                            "QPushButton{"
                                "background-color:#3F70AB;"
                                "color:white;"
                                "border:0px;"
                            "}"
                            "QPushButton:pressed{"
                                "background-color:#214285;"
                            "}"
                            )


        self.m_textEdt.setPlaceholderText("请在此输入消息:")
        #self.m_textEdt.setFixedHeight(180*self.hf)

        #self.m_mainLayout.setContentsMargins(0,0,0,0)
        #self.m_mainLayout.setSpacing(10)

        self.m_listWgt.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.m_listWgt.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.m_listWgt.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        #//m_listWgt   ->setSelectionMode(QAbstractItemView.NoSelection)
        #//m_listWgt   ->setItemDelegate(new NoFocusDelegate())
        self.m_submitBtn.clicked.connect(self.sltBtnSubmitClicked)
        self.his_msgbt.clicked.connect(self.showHistoryMsg)

    def sendPic(self):
        file = QFileDialog.getOpenFileName(self, '选择图片', './img', ("Images (*.png *.jpg *.bmp)"))
        if file[0]:
            with open(file[0], 'rb') as f:
                pic = f.read()
                self.sendPicSignal.emit(self.id, pic)
                self.showPic(pic, 2)


    def sendFile(self):
        file = QFileDialog.getOpenFileName(self, '选择文件', '.', ("(*.*)"))
        if file[0]:
            self.sendFileSignal.emit(self.id, file[0])


    def my_close(self):
        self.saveTalkHistory()
        self.hide()

    def saveTalkHistory(self):
        file = "records/p_%s_%s.re"%(self.self_id, self.id)
        try:
            with open(file, "a+") as f:
                f.write(self.cache)
                self.cache = ""
        except:
            pass

    def showHistoryMsg(self):
        record = self.readTalkHistory()
        self.textEdit = RecordTextEdit()
        for r in record:
            self.textEdit.append(r)
        self.textEdit.show()


    def readTalkHistory(self):
        file = "records/p_%s_%s.re"%(self.self_id, self.id)
        try:
            with open(file, 'r') as f:
                record = f.read()
        except:
            record = ""
        return record.split("\n")

    def showPic(self, pic, ori):
        #1 is left    2 is right
        #m_bubbleList->addItem(m_textEdt->toPlainText(),qrand()%2+1);
        text = self.m_textEdt.toPlainText()
        self.m_textEdt.clear()
        self.feedItem = FeedBackListItem(self, ori, self.self_head, self.head, 1, pic=pic)#qrand()%2+1
        time = QDateTime.currentDateTime()#//获取系统现在的时间
        str = time.toString("yyyy-MM-dd hh:mm:ss")#设置显示格式
        self.timeLabel = QLabel(self.m_listWgt)
        self.timeLabel.setText(str)
        self.timeLabel.setFixedHeight(30)
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.itemTime = QListWidgetItem(self.m_listWgt)
        self.item = QListWidgetItem(self.m_listWgt)
        self.item.setSizeHint(QSize(self.width() - 10, self.height()))
        self.m_listWgt.setItemWidget(self.itemTime, self.timeLabel)
        self.m_listWgt.setItemWidget(self.item, self.feedItem)

        self.m_listWgt.scrollToBottom()
        self.feedItem.sendItemSize[int,int].connect(self.getItemSize)


    def sltBtnSubmitClicked(self, bool):
        #1 is left    2 is right
        #m_bubbleList->addItem(m_textEdt->toPlainText(),qrand()%2+1);
        text = self.m_textEdt.toPlainText()
        self.m_textEdt.clear()
        self.feedItem = FeedBackListItem(self, 2, self.self_head, self.head, 0, text)#qrand()%2+1
        time = QDateTime.currentDateTime()#//获取系统现在的时间
        str = time.toString("yyyy-MM-dd hh:mm:ss")#设置显示格式
        self.timeLabel = QLabel(self.m_listWgt)
        self.timeLabel.setText(str)
        self.timeLabel.setFixedHeight(30)
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.itemTime = QListWidgetItem(self.m_listWgt)
        self.item = QListWidgetItem(self.m_listWgt)
        self.item.setSizeHint(QSize(self.width() - 10, self.height()))
        self.m_listWgt.setItemWidget(self.itemTime, self.timeLabel)
        self.m_listWgt.setItemWidget(self.item, self.feedItem)

        self.m_listWgt.scrollToBottom()
        self.feedItem.sendItemSize[int,int].connect(self.getItemSize)
        self.sendMsgSignal.emit(self.id, text)

        self.cache += "%s(%s)   %s\n%s\n"%("我", self.self_id, str, text)

    def notOnline(self):
        self.notOnlineLabel = QLabel(self.m_listWgt)
        self.notOnlineLabel.setText("对方不在线上！请在对方在线时再发送信息！")
        self.cache += "对方不在线上！请在对方在线时再发送信息！\n"
        self.notOnlineLabel.setFixedHeight(30)
        self.notOnlineLabel.setAlignment(Qt.AlignCenter)
        self.item = QListWidgetItem(self.m_listWgt)
        self.m_listWgt.setItemWidget(self.item, self.notOnlineLabel)
        self.m_listWgt.scrollToBottom()

    def recvive(self, datas):
        for data in datas:
            if data[0] == 0:
                self.recviveMsg(data[1])
            elif data[0] == 1:
                self.recvivePic(data[1])


    def recvivePic(self, pic):
        self.showPic(pic, 1)


    def recviveMsg(self, msg):
        #if id == self.id:
        #for msg in msgs:
        self.feedItem = FeedBackListItem(self, 1, self.self_head, self.head, 0, text=msg)#qrand()%2+1
        time = QDateTime.currentDateTime()#//获取系统现在的时间
        str = time.toString("yyyy-MM-dd hh:mm:ss")#设置显示格式
        self.timeLabel = QLabel(self.m_listWgt)
        self.timeLabel.setText(str)
        self.timeLabel.setFixedHeight(30)
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.itemTime = QListWidgetItem(self.m_listWgt)
        self.item = QListWidgetItem(self.m_listWgt)
        self.item.setSizeHint(QSize(self.width() - 10, self.height()))
        self.m_listWgt.setItemWidget(self.itemTime, self.timeLabel)
        self.m_listWgt.setItemWidget(self.item, self.feedItem)

        self.m_listWgt.scrollToBottom()
        self.feedItem.sendItemSize[int,int].connect(self.getItemSize)
        self.cache += "%s(%s)   %s\n%s\n"%(self.name, self.id, str, msg)

   # def showWindow(self):
     #   self.show()

    def getItemSize(self, w, h):
        self.w = w
        self.h = h
        self.item.setSizeHint(QSize(w,h))
  
    def resizeEvent(self, event):
        rect = self.rect()
        self.m_submitBtn.setGeometry(rect.right()-77*self.wf,rect.bottom()-39*self.hf,68*self.wf,31*self.hf)
        self.m_listWgt.setGeometry(0,90,self.width(),self.height()-self.m_textEdt.height()-90-45)

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


from PyQt5.QtWidgets import QApplication
import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)
    e = FeedBackUI(''.encode(), 'dfsa', 1234, ''.encode())
    e.show()
    sys.exit(app.exec_())

from PyQt5.QtGui import QPainter, QStandardItem
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from PyQt5.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from chat import FeedBackListItem
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





from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QTextEdit,  QListWidget

StrSubmitSuggestion = "发送"
StrTextEdtPlaceHoderText = "请在此输入消息:"


class FeedBackUI(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.wf = 1
        self.hf = 1
        self.initWgt()

    def initWgt(self):
        self.setMaximumWidth(1200)
        self.setFixedHeight(777)
        self.setFixedWidth(777)
       # this->setWindowFlags(Qt::FramelessWindowHint);

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
        self.m_mainLayout = QVBoxLayout(self)
        self.m_textEdt = QTextEdit(self)
        self.m_submitBtn = QPushButton(self)
        self.m_listWgt = QListWidget(self)

        self.m_mainLayout.addWidget(self.m_listWgt)
        self.m_mainLayout.addWidget(self.m_textEdt)

        self.m_textEdt.setPlaceholderText(StrTextEdtPlaceHoderText)
        self.m_submitBtn.setText(StrSubmitSuggestion)
        self.m_textEdt.setFixedHeight(180*self.hf)

        self.m_mainLayout.setContentsMargins(0,0,0,0)
        self.m_mainLayout.setSpacing(10)

        self.m_listWgt.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.m_listWgt.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.m_listWgt.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        #//m_listWgt   ->setSelectionMode(QAbstractItemView.NoSelection)
        #//m_listWgt   ->setItemDelegate(new NoFocusDelegate())
        self.m_submitBtn.clicked.connect(self.sltBtnSubmitClicked)


    def sltBtnSubmitClicked(self, bool):
        #1 is left    2 is right
        #m_bubbleList->addItem(m_textEdt->toPlainText(),qrand()%2+1);
        text = self.m_textEdt.toPlainText()
        self.feedItem = FeedBackListItem(self, text, qrand()%2+1)
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


    def getItemSize(self, w, h):
        self.item.setSizeHint(QSize(w,h))
  
    def resizeEvent(self, event):
        rect = self.rect();
        self.m_submitBtn.setGeometry(rect.right()-77*self.wf,rect.bottom()-39*self.hf,68*self.wf,31*self.hf);
        self.m_listWgt.setGeometry(0,0,self.width(),self.height()-self.m_textEdt.height());


from PyQt5.QtWidgets import QApplication
import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)
    e = FeedBackUI()
    e.show()
    sys.exit(app.exec_())




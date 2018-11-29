from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QEvent, Qt, QRect
from PyQt5.QtGui import QPalette, QPainter, QPixmap, QImage
###################################头像部分需要修改！！！
class Buddy(QWidget):
	def __init__(self, name, id, headPath, ishide, parent=None):
		super().__init__(parent)
		self.initUI(name, id, headPath, ishide)

	def initUI(self, name, id, headPath, ishide):
		self.headPath = headPath
		self.head = QWidget(self)
		self.name = QLabel(self)
		self.name.setStyleSheet("background-color:rgba(255,255,255,0)")
		self.name.setText(name)
		self.id = QLabel(self)
		self.id.setStyleSheet("background-color:rgba(255,255,255,0)")
		self.id.setText(id)
		self.lblonlinestate = QLabel(self)
		self.lblonlinestate.setStyleSheet("background-color:rgba(255,255,255,0)")
		
		self.head.setFixedSize(40, 40)

		color = QPalette()
		color.setColor(QPalette.Text, Qt.gray)
		self.id.setPalette(color)

		self.head.move(7, 7)
		self.name.move(60, 10)
		self.id.move(60, 27)
		self.lblonlinestate.setGeometry(QRect(310, 10, 30, 30))
		if ishide == 1:
			self.lblonlinestate.setPixmap(QPixmap('img/bullet-grey.png'))
		else:
			self.lblonlinestate.setPixmap(QPixmap('img/bullet_green.png'))


		self.head.installEventFilter(self)


	def eventFilter(self, obj, event):
		if obj == self.head:
			if event.type() == QEvent.Paint:
				image = QImage()
				image.loadFromData(self.headPath)
				painter = QPainter(self.head)
				painter.drawPixmap(self.head.rect(), QPixmap.fromImage(image))#

		return QWidget.eventFilter(self, obj, event)

from PyQt5.QtWidgets import QApplication
import sys
if __name__ == '__main__':
	app = QApplication(sys.argv)
	b = Buddy('hah', 'dfa', 'img/2-1.bmp', 0)
	b.show()
	sys.exit(app.exec_())
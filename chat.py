from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent, QDateTime, Qt, pyqtSignal, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QTransform, QFont, QImage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

COLOR_WHITE = Qt.white 
ITEM_HEIGHT = 40
ITEM_SPACE = 5
HeaderBgColor = QColor(219, 238, 252)
HeaderTextColor = QColor(55, 100, 151)
COLOR_BLACK = Qt.black 
HEAD_W_H = 40


class Orientation:
	None_ = 0
	Left  = 1
	Right = 2


class FeedBackListItem(QWidget):
	sendItemSize = pyqtSignal(int, int)
	def __init__(self, parent,  Ori, self_head, head, flag=0, text="", pic=''.encode('utf-8')):
		super().__init__(parent)
		self.pic = pic
		self.m_text = text
		self.m_width = 0
		self.m_oritation = Ori
		self.m_parent = parent
		self.head = head
		self.self_head = self_head
		self.flag = flag
		self.installEventFilter(self)

	def eventFilter(self, obj, event):
		if obj == self and event.type() == QEvent.Paint:
			painter = QPainter(self)
			painter.setRenderHints(QPainter.HighQualityAntialiasing | QPainter.Antialiasing)
			self.drawBg(painter)
			if self.flag == 0:
				self.drawItems(painter)
			else:
				self.drawPic(painter)
			return QWidget.eventFilter(self, obj, event)
		else:
			return False

	def drawBg(self, painter):
		painter.save()
		painter.setBrush(COLOR_WHITE)
		painter.setPen(COLOR_WHITE)
		painter.drawRect(self.rect())
		painter.restore()


	def getItemSize(self, width, height):
		return QSize(width, height)


	def drawPic(self, painter):
		painter.save()

		nItemY = 0
		#nWidth = self.width()
		nWidth = 755
		nWidth = nWidth if nWidth % 2 == 0 else nWidth + 1

		topLeft = QPointF(0, nItemY+30)
		bottomRight = QPointF(nWidth, nItemY+ITEM_HEIGHT+ITEM_SPACE)
		ItemRect = QRectF(topLeft, bottomRight)

		painter.save()
		t = QTransform()
		t.translate(ItemRect.center().x(), ItemRect.center().y())
		painter.setTransform(t)

		rectTopLeft = QPointF()
		rectBottomRight = QPointF()
		textRect = QRectF(rectTopLeft, rectBottomRight)

		font = QFont('幼圆', 10)
		painter.setFont(font)

		path = QPainterPath()
	

		image = QImage()
		image.loadFromData(self.pic)
		pixmap = QPixmap.fromImage(image)

		pixelsWide = image.width()
		pixelsHigh = image.height()




		#m_wf = nWidth * 2 // 3
		##pixelsHigh = ITEM_HEIGHT if pixelsWide < (m_wf*8//9) else (((pixelsWide // (nWidth // 2)) + 2) * ITEM_HEIGHT*2//5)
		#pixelsWide = pixelsWide if pixelsWide < (m_wf*8//9) else (m_wf*8//9)
		if pixelsWide > 540:
			pixelsWide = 540
			pixelsHigh = int(pixelsHigh * (540 / pixelsWide))


		if Orientation.Right == self.m_oritation:
			painter.save()
			painter.setPen(Qt.NoPen)
			painter.setBrush(HeaderBgColor)
			#绘制边框 头像边框
			painter.drawRoundedRect(nWidth // 2 - 55, -ITEM_HEIGHT // 2, HEAD_W_H, HEAD_W_H, 2, 2)
			painter.setPen(HeaderTextColor)
	        #painter->drawPixmap(nWidth / 2 - 54, -ITEM_HEIGHT / 2 + 1, 48, 48, QPixmap(""));
	        #绘制头像
			image = QImage()
			image.loadFromData(self.self_head)
			painter.drawPixmap(nWidth // 2 - 54, -ITEM_HEIGHT // 2 + 1, HEAD_W_H, HEAD_W_H,QPixmap.fromImage(image))
			painter.restore()

			nX = (nWidth // 2) -85 - pixelsWide
			if nX < 0:
				nX = -pixelsWide - 85 + nWidth // 2
			painter.save()

			textRect = QRectF(nX, -ITEM_HEIGHT // 2, pixelsWide + 20, pixelsHigh)
			path.addRoundedRect(textRect, 3, 3)
			path.moveTo(nWidth // 2 - 65, -ITEM_HEIGHT // 2 + 12)
			path.lineTo(nWidth // 2 - 55, -ITEM_HEIGHT // 2 + 18)
			path.lineTo(nWidth // 2 - 65, -ITEM_HEIGHT // 2 + 21)
			painter.setPen(QColor(140, 170, 202))
			painter.drawPath(path)

			#painter.drawPixmap(nX + 10, -ITEM_HEIGHT / 2,pixelsWide, QPixmap(''))
			painter.restore()
			painter.setPen(Qt.white)
			textRect = QRectF(nX + 10, -ITEM_HEIGHT // 2, pixelsWide, pixelsHigh)

					    #设置text颜色
			painter.setPen(Qt.red)
			painter.drawPixmap(nX + 10, -ITEM_HEIGHT // 2, pixelsWide, pixelsHigh, pixmap) #, 
			painter.restore()

			#increment nItemY    item高度设置
			if pixelsHigh <= HEAD_W_H:
				pixelsHigh = HEAD_W_H
				nItemY += pixelsHigh + ITEM_SPACE   #head height + ITEMSPACING
			else:
				nItemY += pixelsHigh + ITEM_SPACE
			
			#QSize(width(),height)
			#self.sendItemSize.emit(self.width(),pixelsHigh + ITEM_SPACE+30)
			self.sendItemSize.emit(755,pixelsHigh + ITEM_SPACE+30)

		else:
			painter.save();
			textRect = QRectF(-nWidth // 2 + 59, -ITEM_HEIGHT // 2, pixelsWide + 20, pixelsHigh)
			path.addRoundedRect(textRect, 3, 3)
			path.moveTo(-nWidth // 2 + 59, -ITEM_HEIGHT // 2 + 12)
			path.lineTo(-nWidth // 2 + 49, -ITEM_HEIGHT // 2 + 18)
			path.lineTo(-nWidth // 2 + 59, -ITEM_HEIGHT // 2 + 21)
			painter.setPen(QColor(140, 170, 202))
			painter.drawPath(path)
			painter.restore()

	        #绘制头像
			painter.save()
			painter.setPen(Qt.NoPen)
			painter.setBrush(HeaderBgColor)
			leftRect = QRectF(-nWidth // 2 + 5, -ITEM_HEIGHT // 2, HEAD_W_H, HEAD_W_H)
			painter.drawRect(leftRect)
			painter.setPen(HeaderTextColor)

			image = QImage()
			image.loadFromData(self.head)
			painter.drawPixmap(-nWidth // 2 + 5, -ITEM_HEIGHT // 2, HEAD_W_H, HEAD_W_H, QPixmap.fromImage(image))
			painter.restore()

			painter.setPen(COLOR_BLACK);

			textRect = QRectF(-nWidth // 2 + 59 + 10, -ITEM_HEIGHT // 2, pixelsWide, pixelsHigh)
	    

		    #设置text颜色
			painter.setPen(Qt.red)
			painter.drawPixmap(-nWidth // 2 + 59 + 10, -ITEM_HEIGHT // 2, pixelsWide, pixelsHigh, pixmap) #, 
			painter.restore()

			#increment nItemY    item高度设置
			if pixelsHigh <= HEAD_W_H:
				pixelsHigh = HEAD_W_H
				nItemY += pixelsHigh + ITEM_SPACE   #head height + ITEMSPACING
			else:
				nItemY += pixelsHigh + ITEM_SPACE
			
			#QSize(width(),height)
			#self.sendItemSize.emit(self.width(),pixelsHigh + ITEM_SPACE+30)
			self.sendItemSize.emit(755,pixelsHigh + ITEM_SPACE+30)





	def drawItems(self, painter):
		painter.save()

		nItemY = 0
		#nWidth = self.width()
		nWidth = 755
		nWidth = nWidth if nWidth % 2 == 0 else nWidth + 1

		topLeft = QPointF(0, nItemY+30)
		bottomRight = QPointF(nWidth, nItemY+ITEM_HEIGHT+ITEM_SPACE)
		ItemRect = QRectF(topLeft, bottomRight)

		painter.save()
		t = QTransform()
		t.translate(ItemRect.center().x(), ItemRect.center().y())
		painter.setTransform(t)

		rectTopLeft = QPointF()
		rectBottomRight = QPointF()
		textRect = QRectF(rectTopLeft, rectBottomRight)

		font = QFont('幼圆', 10)
		painter.setFont(font)

		path = QPainterPath()
		fm = QFontMetrics(font)
		pixelsWide = fm.width(self.m_text)
		pixelsHigh = fm.height()
		m_wf = nWidth * 2 // 3
		pixelsHigh = ITEM_HEIGHT if pixelsWide < (m_wf*8//9) else (((pixelsWide // (nWidth // 2)) + 2) * ITEM_HEIGHT*2//5)
		pixelsWide = pixelsWide if pixelsWide < (m_wf*8//9) else (m_wf*8//9)

		if Orientation.Right == self.m_oritation:
			painter.save()
			painter.setPen(Qt.NoPen)
			painter.setBrush(HeaderBgColor)
			#绘制边框 头像边框
			painter.drawRoundedRect(nWidth // 2 - 55, -ITEM_HEIGHT // 2, HEAD_W_H, HEAD_W_H, 2, 2)
			painter.setPen(HeaderTextColor)
	        #painter->drawPixmap(nWidth / 2 - 54, -ITEM_HEIGHT / 2 + 1, 48, 48, QPixmap(""));
	        #绘制头像
			image = QImage()
			image.loadFromData(self.self_head)
			painter.drawPixmap(nWidth // 2 - 54, -ITEM_HEIGHT // 2 + 1, HEAD_W_H, HEAD_W_H,QPixmap.fromImage(image))
			painter.restore()

			nX = (nWidth // 2) -85 - pixelsWide
			if nX < 0:
				nX = -pixelsWide - 85 + nWidth // 2
			painter.save()

			textRect = QRectF(nX, -ITEM_HEIGHT // 2, pixelsWide + 20, pixelsHigh)
			path.addRoundedRect(textRect, 3, 3)
			path.moveTo(nWidth // 2 - 65, -ITEM_HEIGHT // 2 + 12)
			path.lineTo(nWidth // 2 - 55, -ITEM_HEIGHT // 2 + 18)
			path.lineTo(nWidth // 2 - 65, -ITEM_HEIGHT // 2 + 21)
			painter.setPen(QColor(140, 170, 202))
			painter.drawPath(path)

			#painter.drawPixmap(nX + 10, -ITEM_HEIGHT / 2,pixelsWide, QPixmap(''))
			painter.restore()
			painter.setPen(Qt.white)
			textRect = QRectF(nX + 10, -ITEM_HEIGHT / 2, pixelsWide, pixelsHigh)

		else:
			painter.save();
			textRect = QRectF(-nWidth // 2 + 59, -ITEM_HEIGHT // 2, pixelsWide + 20, pixelsHigh)
			path.addRoundedRect(textRect, 3, 3)
			path.moveTo(-nWidth // 2 + 59, -ITEM_HEIGHT // 2 + 12)
			path.lineTo(-nWidth // 2 + 49, -ITEM_HEIGHT // 2 + 18)
			path.lineTo(-nWidth // 2 + 59, -ITEM_HEIGHT // 2 + 21)
			painter.setPen(QColor(140, 170, 202))
			painter.drawPath(path)
			painter.restore()

	        #绘制头像
			painter.save()
			painter.setPen(Qt.NoPen)
			painter.setBrush(HeaderBgColor)
			leftRect = QRectF(-nWidth // 2 + 5, -ITEM_HEIGHT // 2, HEAD_W_H, HEAD_W_H)
			painter.drawRect(leftRect)
			painter.setPen(HeaderTextColor)

			image = QImage()
			image.loadFromData(self.head)
			painter.drawPixmap(-nWidth // 2 + 5, -ITEM_HEIGHT // 2, HEAD_W_H, HEAD_W_H, QPixmap.fromImage(image))
			painter.restore()

			painter.setPen(COLOR_BLACK);

			textRect = QRectF(-nWidth // 2 + 59 + 10, -ITEM_HEIGHT // 2, pixelsWide, pixelsHigh)
	    

	    #设置text颜色
		painter.setPen(Qt.red)
		painter.drawText(textRect, Qt.AlignVCenter | Qt.AlignLeft, self.m_text) #, 
		painter.restore()

		#increment nItemY    item高度设置
		if pixelsHigh <= HEAD_W_H:
			pixelsHigh = HEAD_W_H
			nItemY += pixelsHigh + ITEM_SPACE   #head height + ITEMSPACING
		else:
			nItemY += pixelsHigh + ITEM_SPACE
		
		#QSize(width(),height)
		#self.sendItemSize.emit(self.width(),pixelsHigh + ITEM_SPACE+30)
		self.sendItemSize.emit(755,pixelsHigh + ITEM_SPACE+30)

from PyQt5.QtWidgets import QApplication
import sys
if __name__ == '__main__':
	app = QApplication(sys.argv)
	e = FeedBackListItem(None, "nihao", 1)
	e.show()
	sys.exit(app.exec_())
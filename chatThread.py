from PyQt5.QtCore import QThread, pyqtSignal

class ChatThread(QThread):
	def __init__(self, chatWindow):
		super().__init__()
		self.chatWindow = chatWindow

	def run(self):
		self.chatWindow.show()

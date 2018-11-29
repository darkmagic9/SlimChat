from PyQt5.QtCore import QThread, pyqtSignal
from protocol import *
import struct
from playsound import playsound
BUFFERSIZE = 1024

class Listener(QThread):
	newSysMsgSignal = pyqtSignal(int, int, bytes)
	newFriendMsgSignal = pyqtSignal(int, int, bytes)
	newGroupMsgSignal = pyqtSignal(int, int, bytes)
	successAddFriendSignal = pyqtSignal(dict, bytes)
	friendOfflineSignal = pyqtSignal(int)
	beDelSignal = pyqtSignal(int)
	friendsOnlineSignal = pyqtSignal(int)
	noExistSignal = pyqtSignal(int)
	offlineSignal = pyqtSignal(int)
	createGroupOkSignal = pyqtSignal(int, bytes)
	addGroupOkSignal = pyqtSignal(int, bytes)
	#refuseAddSignal = pyqtSignal(int)
	def __init__(self, widget, parent=None):
		super().__init__(parent)
		self.widget = widget

	def run(self):
		while True:
			try:
				res = self.widget.client.sock.recv(HEADER_SIZE)
				size, src_id, des_id, type = struct.unpack(HEADER_FORM, res)
				recvd_size = 0
				data = ''.encode('utf-8')
				while recvd_size != size:
					if size - recvd_size > BUFFERSIZE:
						d = self.widget.client.sock.recv(BUFFERSIZE)
					else:
						d = self.widget.client.sock.recv(size - recvd_size)
					recvd_size += len(d)
					data += d
				#完成！
				if type == Type.RF_ADD:
					playsound("sound/system_msg.wav")
					self.newSysMsgSignal.emit(src_id, type, data)

				#完成！
				elif type == Type.AC_ADD:
					playsound("sound/system_msg.wav")
					self.newSysMsgSignal.emit(src_id, type, data)
					friend = {'id' : src_id, 'ishide' : 0}
					friend['name'] = data.split('\n'.encode('utf-8'), 1)[0].decode('utf-8')
					head = data.split('\n'.encode('utf-8'), 1)[1]
					self.successAddFriendSignal.emit(friend, head)

				#待测试
				elif type == Type.FRIEND_ONLINE:
					playsound("sound/friend_online.wav")
					self.friendsOnlineSignal.emit(src_id) #dealFriendOnline

				#完成
				elif type == Type.BE_ADDED:
					playsound("sound/system_msg.wav")
					self.newSysMsgSignal.emit(src_id, type, data)
				#完成
				elif type == Type.NOEXIST:
					self.noExistSignal.emit(src_id)
				#完成
				elif type == Type.OFFLINE:
					self.offlineSignal.emit(src_id)
				#完成
				elif type == Type.BE_DELED:
					playsound("sound/system_msg.wav")
					self.newSysMsgSignal.emit(src_id, type, data)
					self.beDelSignal.emit(src_id)  # dealBeDel
				#待测试
				elif type == Type.TEXT: 
					playsound("sound/friend_msg.wav")
					self.newFriendMsgSignal.emit(src_id, type, data)
				elif type == Type.PIC:
					playsound("sound/friend_msg.wav")
					self.newFriendMsgSignal.emit(src_id, type, data)
				elif type == Type.FILE:
					playsound("sound/file.wav")
					self.newFriendMsgSignal.emit(src_id, type, data)
				#完成
				elif type == Type.FRIEND_OFFLINE:
					playsound("sound/friend_offline.wav")
					self.friendOfflineSignal.emit(src_id) #dealFriendOffline
				elif type == Type.GROUP_TEXT:
					playsound("sound/group_msg.wav")
					self.newGroupMsgSignal.emit(src_id, type, data)
				elif type == Type.GROUP_PIC:
					playsound("sound/group_msg.wav")
					self.newGroupMsgSignal.emit(src_id, type, data)
				elif type == Type.GROUP_CREATE_OK:
					playsound("sound/system_msg.wav")
					self.createGroupOkSignal.emit(src_id, data)
					self.newSysMsgSignal.emit(src_id, type, data)
				elif type == Type.GROUP_ADD_OK:
					playsound("sound/system_msg.wav")
					self.addGroupOkSignal.emit(src_id, data) #########################待完善！
					self.newSysMsgSignal.emit(src_id, type, data)
				elif type == Type.GROUP_NOEXIST:
					playsound("sound/system_msg.wav")
					self.newSysMsgSignal.emit(src_id, type, data)
				elif type == Type.FILE_AC:
					playsound("sound/file.wav")
					self.newFriendMsgSignal.emit(src_id, type, data)
				elif type == Type.FILE_RF:
					playsound("sound/file.wav")
					self.newFriendMsgSignal.emit(src_id, type, data)
			except:
				pass


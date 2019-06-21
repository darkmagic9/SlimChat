import socket
from protocol import *
import json
import struct
from PyQt5.QtWidgets import QMessageBox
import os
HOST_ID = 0
TEMP_ID = -1
BUFFERSIZE = 1024
class Client():
	def __init__(self):
		self.host = '127.0.0.1'
		self.port = 20000
		self.id = -1
		self.name = ''
		with open('img/2-1.bmp', 'rb') as pic:
			self.head = pic.read()


	def setupHostandPort(self, addr, port):
		self.host = addr
		self.port = port

	def connectToServer(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, 30)
		try:
			self.sock.connect((self.host, self.port))
		except:
			QMessageBox.warning(None, 'Error', 'Unable to connect to the server, Please check the configuration file for errors!')
			return False
		return True


	def dealDeleteGroup(self, gid):
		data = str(gid).encode('utf-8')
		protocol = Protocol(len(data), self.id, HOST_ID, Type.DEL_GROUP)
		header = protocol.make_packet_header()
		self.sock.sendall(header+data)


	def dealAcceptFile(self, id, filename):
		data = filename.encode('utf-8')
		protocol = Protocol(len(data), self.id, id, Type.FILE_AC)
		header = protocol.make_packet_header()
		self.sock.sendall(header+data)

	def dealRefuseFile(self, id, filename):
		data = filename.encode('utf-8')
		protocol = Protocol(len(data), self.id, id, Type.FILE_RF)
		header = protocol.make_packet_header()
		self.sock.sendall(header+data)


	def dealCreateGroup(self, gname, ghead):
		data = gname.encode('utf-8')+'\n'.encode('utf-8')+ghead
		protocol = Protocol(len(data), self.id, HOST_ID, Type.CREATE_GROUP)
		header = protocol.make_packet_header()
		self.sock.sendall(header+data)


	def dealJoinGroup(self, gid):
		data = str(gid).encode('utf-8')
		protocol = Protocol(len(data), self.id, HOST_ID, Type.JOIN_GROUP)
		header = protocol.make_packet_header()
		self.sock.sendall(header+data)


	def dealGetGroupMember(self, gid):
		protocol = Protocol(len(str(gid).encode('utf-8')), self.id, HOST_ID, Type.GET_GROUP_MEMBER)
		header = protocol.make_packet_header()
		self.sock.sendall(header+str(gid).encode('utf-8'))

		res_header = self.sock.recv(HEADER_SIZE)
		size, src_id, des_id, type = struct.unpack(HEADER_FORM, res_header)

		recvd_size = 0
		data = ''
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = self.sock.recv(BUFFERSIZE)
			else:
				d = self.sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d.decode('utf-8')
		data = json.loads(data)
		return data



	def dealGetGroupNameAndHead(self, gid):
		protocol = Protocol(len(str(gid).encode('utf-8')), self.id, HOST_ID, Type.GET_GROUP_NAME_HEAD)
		header = protocol.make_packet_header()
		self.sock.sendall(header+str(gid).encode('utf-8'))

		res_header = self.sock.recv(HEADER_SIZE)
		size, src_id, des_id, type = struct.unpack(HEADER_FORM, res_header)

		recvd_size = 0
		data = ''.encode('utf-8')
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = self.sock.recv(BUFFERSIZE)
			else:
				d = self.sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		data = data.split('\n'.encode('utf-8'), 1)
		return (data[0].decode('utf-8'), data[1])


	def dealGetGroupList(self):
		protocol = Protocol(0, self.id, HOST_ID, Type.GET_GROUP_LIST)
		header = protocol.make_packet_header()
		self.sock.sendall(header)

		res_header = self.sock.recv(HEADER_SIZE)
		size, src_id, des_id, type = struct.unpack(HEADER_FORM, res_header)

		recvd_size = 0
		data = ''
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = self.sock.recv(BUFFERSIZE)
			else:
				d = self.sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d.decode('utf-8')
		data = json.loads(data)
		return data

	def dealSendGroupMsg(self, des_id, msg):
		msg = msg.encode('utf-8')
		protocol = Protocol(len(msg), self.id, des_id, Type.GROUP_TEXT)
		header = protocol.make_packet_header()
		self.sock.sendall(header+msg)

	def dealSendGroupPic(self, des_id, pic):
		protocol = Protocol(len(pic), self.id, des_id, Type.GROUP_PIC)
		header = protocol.make_packet_header()
		self.sock.sendall(header+pic)


	def dealSendMsg(self, des_id, msg):
		msg = msg.encode('utf-8')
		protocol = Protocol(len(msg), self.id, des_id, Type.TEXT)
		header = protocol.make_packet_header()
		self.sock.sendall(header+msg)

	def dealSendPic(self, des_id, pic):
		protocol = Protocol(len(pic), self.id, des_id, Type.PIC)
		header = protocol.make_packet_header()
		self.sock.sendall(header+pic)

	def dealSendFile(self, des_id, filename):
		try:
			with open(filename, 'rb') as file:
				data = file.read()
			data = (os.path.basename(filename)).encode('utf-8')+"\n".encode('utf-8') +data
			protocol = Protocol(len(data), self.id, des_id, Type.FILE)
			header = protocol.make_packet_header()
			self.sock.sendall(header+data)
		except:
			pass


	def dealDelFriend(self, id):
		protocol = Protocol(0, self.id, id, Type.DEL_FRIEND)
		header = protocol.make_packet_header()
		self.sock.sendall(header)

	def dealAcceptAdded(self, des_id):
		data = self.name.encode('utf-8')+'\n'.encode('utf-8')+self.head
		protocol = Protocol(len(data), self.id, des_id, Type.AC_ADD)
		header = protocol.make_packet_header()
		self.sock.sendall(header+data)

	def dealRefuseAdded(self, des_id):
		protocol = Protocol(0, self.id, des_id, Type.RF_ADD)
		header = protocol.make_packet_header()
		self.sock.sendall(header)


	#data格式[id，昵称]
	#def dealGetName(self, id):
	#	protocol = Protocol(len(str(id).encode('utf-8')), self.id, HOST_ID, Type.GET_HEAD)
	#	header = protocol.make_packet_header()
	#	self.sock.sendall(header+str(id).encode('utf-8'))
#
#		res_header = self.sock.recv(HEADER_SIZE)
#		size, src_id, des_id, type = struct.unpack(HEADER_FORM, res_header)
#
#		recvd_size = 0
#		data = ''
#		while recvd_size != size:
#			if size - recvd_size > BUFFERSIZE:
#				d = self.sock.recv(BUFFERSIZE)
#			else:
#				d = self.sock.recv(size - recvd_size)
#			recvd_size += len(d)
#			data += d.decode('utf-8')
#		return data

	def dealGetSelfName(self):
		protocol = Protocol(0, self.id, HOST_ID, Type.GET_SELF_NAME)
		header = protocol.make_packet_header()
		self.sock.sendall(header)

		res_header = self.sock.recv(HEADER_SIZE)
		size, src_id, des_id, type = struct.unpack(HEADER_FORM, res_header)

		name = (self.sock.recv(size)).decode('utf-8')
		return name

	def dealGetHead(self, id):
		protocol = Protocol(len(str(id).encode('utf-8')), self.id, HOST_ID, Type.GET_HEAD)
		header = protocol.make_packet_header()
		self.sock.sendall(header+str(id).encode('utf-8'))

		res_header = self.sock.recv(HEADER_SIZE)
		size, src_id, des_id, type = struct.unpack(HEADER_FORM, res_header)

		recvd_size = 0
		data = ''.encode('utf-8')
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = self.sock.recv(BUFFERSIZE)
			else:
				d = self.sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		return data




	#需要验证
	def dealInitGroupInfo(self):
		protocol = Protocol(0, self.id, HOST_ID, Type.GET_GROUP_INFO)
		header = protocol.make_packet_header()
		self.sock.sendall(header)

		res_header = self.sock.recv(HEADER_SIZE)
		size, src_id, des_id, type = struct.unpack(HEADER_FORM, res_header)

		recvd_size = 0
		data = ''
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = self.sock.recv(BUFFERSIZE)
			else:
				d = self.sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d.decode('utf-8')
		data = json.loads(data)
		return data


	def dealLogin(self, id, pwd):
		info = {'id' : id, 'password' : pwd}
		info = json.dumps(info).encode('utf-8')
		protocol = Protocol(len(info), TEMP_ID, HOST_ID, Type.LOGIN)
		header = protocol.make_packet_header()
		self.sock.sendall(header+info)

		data = self.sock.recv(HEADER_SIZE)
		size, src_id, des_id, type = struct.unpack(HEADER_FORM, data)
		if type == Type.OK:
			self.id = des_id
			self.name = self.dealGetSelfName()
			self.head = self.dealGetHead(self.id)                                   ############################处理登录时初始化用户头像！！
		return type

	def dealGetHead(self, id):
		id = str(id).encode('utf-8')
		protocol = Protocol(len(id), self.id, HOST_ID, Type.GET_HEAD)
		header = protocol.make_packet_header()
		self.sock.sendall(header+id)

		data = self.sock.recv(HEADER_SIZE)
		size, src_id, des_id, type = struct.unpack(HEADER_FORM, data)

		data = ''.encode('utf-8')
		recvd_size = 0
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = self.sock.recv(BUFFERSIZE)
			else:
				d = self.sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		return data


	def dealRegister(self, name,pwd):
		info = {'name' : name, 'password' : pwd}
		info = json.dumps(info).encode('utf-8')
		protocol = Protocol(len(info), TEMP_ID, HOST_ID, Type.REGISTER)
		header = protocol.make_packet_header()
		self.sock.sendall(header+info)

		data = self.sock.recv(HEADER_SIZE)
		size, src_id, des_id, type = struct.unpack(HEADER_FORM, data)
		if type == Type.OK:
			self.id = int(des_id)
		return (type, int(des_id))

	def dealUpdate(self, info):
		info = json.dumps(info)
		info = info.encode('utf-8')
		protocol = Protocol(len(info), self.id, HOST_ID, Type.UPDATE)
		header = protocol.make_packet_header()
		self.sock.sendall(header+info)


	def dealQuit(self):
		protocol = Protocol(0, self.id, HOST_ID, Type.QUIT)
		header = protocol.make_packet_header()
		self.sock.sendall(header)
		self.sock.close()

	def dealSetHead(self):
		protocol = Protocol(len(self.head), self.id, HOST_ID, Type.SET_HEAD)
		header = protocol.make_packet_header()
		self.sock.sendall(header+self.head)

	def dealSetName(self):
		name = self.name.encode('utf-8')
		protocol = Protocol(len(name), self.id, HOST_ID, Type.SET_SELF_NAME)
		header = protocol.make_packet_header()
		self.sock.sendall(header+name)

		


#if __name__ == '__main__':
#	c = Client()
#	print(c.host)
#	print(c.port)
#	
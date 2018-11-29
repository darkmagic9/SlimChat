import struct

HEADER_SIZE = struct.calcsize('llll')
HEADER_FORM = 'llll'



class Type:
	LOGIN = 0 #登录
	REGISTER = 1 #注册
	ADD_FRIEND = 2 #添加好友
	DEL_FRIEND = 3 #删除好友
	QUIT = 4 #退出
	BE_ADDED = 5 #被添加
	BE_DELED = 6 #被删除
	FRIEND_ONLINE = 7 #好友上线
	#SEND_TEXT = 8 #发送文本
	#SEND_PIC = 9 #发送图片
	#SEND_FILE = 10 #发送文件
	TEXT = 8
	PIC = 9
	FILE = 10
	CHANGE_GROUP = 11 #改变好友分组
	CHANGE_HEAD = 12 #改变头像
	CHAGNE_SELF_NAME = 13 #改变自己的昵称
	CHANGE_FRI_NAME = 14 #设置好友备注
	GET_GROUP_INFO = 15 #获取分组信息
	RET_GROUP_INFO = 16 #获取好友
	GET_SELF_NAME = 17 #获取自己的信息
	RET_SELF_NAME = 18
	OK = 19
	FAIL = 20
	REPEAT = 21
	NOEXIST = 22
	#AC_TEXT = 23
	#AC_PIC = 24
	#AC_FILE = 25
	GET_HEAD = 26
	RET_HEAD = 27
	SET_HEAD = 28
	SET_SELF_NAME = 29
	AC_ADD = 30
	RF_ADD = 31
	FRIEND_OFFLINE = 32
	OFFLINE = 33
	UPDATE = 34
	GROUP_TEXT = 35
	GROUP_PIC = 36
	CREATE_GROUP = 37
	JOIN_GROUP = 38
	CHAGNE_GROUP_NAME = 39
	LEAVE_GROUP = 40
	GET_GROUP_LIST = 41
	GET_GROUP_NAME_HEAD = 42
	GET_GROUP_MEMBER = 43
	GROUP_CREATE_OK = 44
	GROUP_ADD_OK = 45
	GROUP_NOEXIST = 46
	FILE_AC = 47
	FILE_RF = 48
	DEL_GROUP = 49






class Protocol:
	def __init__(self, size, src_id, des_id, type):
		self.size = size
		self.src_id = src_id
		self.des_id = des_id
		self.type = type

	def make_packet_header(self):
		header = struct.pack(HEADER_FORM, self.size, self.src_id, self.des_id, self.type)
		return header



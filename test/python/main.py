import ctypes
import sys, os
#from pathlib import Path
import struct
import json


#os.environ['path'] += ';D:\\data\\QT\\DLL\\TestDLL'  #python代码根目录，所有库文件放于该目录下

#os.add_dll_directory('D:\\data\\QT\\DLL\\newtest')

def bytes_to_short(bytes):
    # 假设bytes是两个字节的长度
    assert len(bytes) == 2
    # 使用'short'格式符号转换
    #'>h'是格式字符串，其中>表示字节顺序是网络序（大端），h则表示转换成short。如果你的字节顺序是小端，可以使用'<h'格式字符串。
    short_value, = struct.unpack('>h', bytes)
    return short_value

def loadData():
    with open('mydata60004.log', 'rb') as file:
	    content = file.read()
	    if content[0:4].hex() == '5aa56996':
	        dataLenBytes = content[4:8]
	        actual_byte_num_in_frame = dataLenBytes[0]*16777216+ dataLenBytes[1]*65536 + dataLenBytes[2]*256 + dataLenBytes[3]
	        print("OKKKXXX", actual_byte_num_in_frame)

	        if actual_byte_num_in_frame > 12000*4:
	            left_byte_num = 12000*4
	        else:
	            left_byte_num = actual_byte_num_in_frame
	        print('left_byte_num', left_byte_num)
	        data = content[8:left_byte_num+8]

	        length = len(data)
	        listA = []
	        listB = []
	        for i in range(actual_byte_num_in_frame//4):
	            ch0 = bytes_to_short(data[4*i+0:4*i+2])
	            ch1 = bytes_to_short(data[4*i+2:4*i+4])
	            listA.append(ch0)
	            listB.append(ch1)
	    return [listA, listB]


dll = ctypes.CDLL("../../lib/mylib.dll")
#dll.add.argtypes = [ctypes.c_int, ctypes.c_int]
dll.getUUID.restype = ctypes.c_char_p
r = dll.getUUID()
print("UUID")
print(r)


dll.update.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
dll.update.restype = None
# 创建一个float数组
# 初始化一个包含20000个点的数组



#mylist = [1.0,2.0,3.0]
#mylist2 = [4.0,5,]

data = loadData()
mylist = data[0]
mylist2 = data[1]
print(len(mylist2))
#return


array_length = len(mylist)
#array_type = c_double * array_length
array_type = ctypes.c_double * array_length
arra = array_type(*mylist)  # 初始化数组为0到19999
arrb = array_type(*mylist2)  # 初始化数组为0到19999
dll.update(arra, arrb, array_length, array_length)


dll.authorize.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
dll.authorize.restype = ctypes.c_char_p
dll.authorize(b"./license.txt", b"./publicKey.txt")

dll.demodulate.argtypes =[ctypes.c_int, ctypes.c_int]
dll.demodulate(70, 10000)

dll.getDecayCurve.restype = ctypes.c_char_p
r1 = dll.getDecayCurve()
print('Python---')
strr1 = str(r1, encoding="utf-8")
json_obj = json.loads(strr1)
if json_obj['ret'] == 'ok':
	#print('getDecayCurve-json', json_obj)
	strList = [float(i) for i in json_obj['data'].split(',')]
#print(r)

dll.getCompensationCurve.restype = ctypes.c_char_p
r = dll.getCompensationCurve()
print('Python---2')
#print(r)
strr2 = str(r, encoding="utf-8")
json2_obj = json.loads(strr2)
if json2_obj['ret'] == 'ok':
	strList2 = [float(i) for i in json2_obj['data'].split(',')]
	if strList[5000] == strList2[5000]:
		print("ERRR...")
	else:
		print('5000', strList[5000], strList2[5000])

dll.getTemperature.argtypes = [ctypes.c_char_p]
dll.getTemperature.restype = ctypes.c_char_p
r = dll.getTemperature(b"0.36:25,0.7:100")
print('Python---3')
#print(r)
strr3 = str(r, encoding="utf-8")
json3_obj = json.loads(strr3)
if json3_obj['ret'] == 'ok':
	strList3 = [float(i) for i in json3_obj['data'].split(',')]
else:
	print("ERR3", json3_obj['msg'])

# 可视化
import matplotlib.pyplot as plt
plt.figure()
if strList:
	plt.subplot(3, 1, 1)
	plt.ylim(0, 1)
	plt.plot(strList)
	plt.title('R1')

if strList2:
	plt.subplot(3, 1, 2)
	plt.ylim(0, 1)
	plt.plot(strList2)
	plt.title('R2')

if strList3:
	plt.subplot(3, 1, 3)
	plt.ylim(-20, 150)
	plt.plot(strList3)
	plt.title('R3')

plt.show()
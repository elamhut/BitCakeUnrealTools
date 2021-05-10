import datetime
import os

path = os.getcwd()
print("{}\\AgoraVai".format(path))
exist = os.path.isdir("{}\\AgoraVai\\".format(path))
print(exist)
print(datetime.datetime.now().strftime("%y%m%d"))
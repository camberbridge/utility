# coding: utf8
import socket
from socket import socket, AF_INET, SOCK_DGRAM
import subprocess
import csv
import time
import threading

HOST = ""
PORT = 20000

s = socket(AF_INET, SOCK_DGRAM)
s.bind((HOST, PORT))

land_list = []
with open("./landmark.csv", "r") as f:
  reader = csv.reader(f)
  header = next(reader)
  land_list = [row for row in reader]

def get_place(distance):
  for row in land_list:
    row[3] = float(row[3])
    distance = float(distance)
    if row[3] >= distance:
      print(row[3], distance, row[1].decode("utf-8"))
      return row[1].decode("utf-8"), "landmark_en"
  return "日　比　谷", "aaaaaaa_pe"

def str_parser(msg):
  if len(msg) != 73:
    return None
  v_type = msg[11]
  v_num = str(int(msg[12:14]))
  distance = str(int(msg[20:23]))+"."+msg[23:25]
  speed = str(int(msg[48:51]))+"."+msg[51:52]
  yusen = str(msg[7])
  return v_type, v_num, distance, speed, yusen

loop_flag = True
def offset(interval):
  global loop_flag
  global s
  while True:
    time.sleep(interval)
    loop_flag = False
    s.close()
    time.sleep(interval)
    loop_flag = True
    try:
      s = socket(AF_INET, SOCK_DGRAM)
      s.bind((HOST, PORT))
    except:
      pass

def main():
  while True:
    if loop_flag:
      try:
        msg, address = s.recvfrom(8192)
        data = str_parser(msg)

        print(msg)
        if data is not None and data[4] == "1":
          print(data)
          pj, pe = get_place(data[2])
          cmd = "./distributor.sh " + data[0] + " " + data[1] + " " + data[2] + " " + data[3] + " '" + pj + "' " + pe
          process = (subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
          print(process)
      except:
        pass
    else:
      pass

if __name__ == "__main__":
  thread1 = threading.Thread(target=main)
  thread2 = threading.Thread(target=offset, args=([2]))
  thread1.start()
  thread2.start()
  thread1.join()
  thread2.join()

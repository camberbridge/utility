import serial
import serial.tools.list_ports
import sys
import time
baudrate = 9600

# Send sp_read (that is ball speed).
def sender(sp_read):
  if isinstance(sp_read, int):
    if sp_read > 999 or sp_read < 0:
      print("ERR: sp_read is incorrect.")
      return

    # Initialize serial.
    port = serial.tools.list_ports.comports()[-1].device
    with serial.Serial(port, baudrate, parity = serial.PARITY_NONE) as ser:
      # Prepare data.
      sp_str = "00"+str(sp_read)
      data = sp_str[-3]+sp_str[-2]+sp_str[-1]+'\x20\x20\x20\x0d'
      data_a = data.encode('ascii')

      ser.write(data_a)
      # Refer: https://stackoverflow.com/questions/38950613/have-to-use-sleep-with-pyserial-when-opening-com-port-for-arduino-nano
      time.sleep(2)
      print(data_a)
  else:
    print("ERR: input is not integer.")


if __name__=="__main__":
  sender(int(sys.argv[1]))

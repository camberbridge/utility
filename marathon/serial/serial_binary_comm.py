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
      data = ('01' 
        + bin(int(sp_str[-3]))[2:].zfill(2)
        + bin(int(sp_str[-2]))[2:].zfill(4)
        + '0010'
        + bin(int(sp_str[-1]))[2:].zfill(4))

      # Refer: https://stackoverflow.com/questions/2072351/python-conversion-from-binary-string-to-hexadecimal
      #data = hex(int(data, 2))  # bin str->int10->hex string
      #data_a = data.encode('ascii')
      data = int(data, 2)  # bin str->int10
      data_a = data

      ser.write(data_a)
      # Refer: https://stackoverflow.com/questions/38950613/have-to-use-sleep-with-pyserial-when-opening-com-port-for-arduino-nano
      time.sleep(.5)
      print(data_a)
  else:
    print("ERR: input is not integer.")


if __name__=="__main__":
  sender(int(sys.argv[1]))

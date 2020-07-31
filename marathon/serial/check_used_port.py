import serial
import serial.tools.list_ports

def uart_write_read(w_data, r_size):
    ser.write(w_data)
    print('Send: '+ str(w_data))
    r_data = ser.read_until(size=r_size) #Read r_size
    print('Recv: ' + str(r_data))

    return r_data

def search_com_port():
    coms = serial.tools.list_ports.comports()
    comlist = [com.device for com in coms]
    print('Connected COM ports: ' + str(comlist))
    use_port = comlist[-1]
    print('Use COM port: ' + use_port)

    return use_port

if __name__ == '__main__':
    use_port = search_com_port()
    print(f"Use: {use_port}")

    # Init Serial Port Setting
    ser = serial.Serial(use_port)
    ser.baundrate = 9600
    ser.timeout = 5 #sec

    w_data = b'RV\n'
    r_size = 7
    r_data = uart_write_read(w_data, r_size)
    print('Reserved: {}'.format(r_data))

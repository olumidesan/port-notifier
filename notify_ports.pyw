
import time
import serial
import platform

from plyer import notification

if platform.system() == "Linux": 
    import serial.tools.list_ports_posix 


ports_on_startup = []

def list_serial_ports():

    if platform.system() == "Windows":
        _ports = ['COM%s' % (i + 1) for i in range(256)]

    elif platform.system() == "Linux":
        _ports = serial.tools.list_ports_posix.comports()

    else:
        # Other platforms not [yet] supported
        raise EnvironmentError('Unsupported platform')

    ports = []

    for port in _ports:
        try:
            if platform.system() == "Windows":
                s = serial.Serial(port)
                _port = port

            elif platform.system() == "Linux":
                s = serial.Serial(port.device)
                _port = port.device
                
            ports.append(_port) 
            s.close()

        except (OSError, serial.SerialException):
            pass

    return ports

def main():
    ports_on_startup = set(list_serial_ports())

    while True:
        ports = list_serial_ports()

        # Check for new and removed devices
        new_ports = [port for port in ports if port not in ports_on_startup]
        removed_ports = [port for port in ports_on_startup if port not in ports]

        if len(new_ports) > 0:
            for port in new_ports:
                # Send notification (platform independent)
                notification.notify(
                    title="Port of device connected",
                    message=f"{port}",
                    )
                ports_on_startup.add(port)

        if len(removed_ports) > 0:
            for port in removed_ports:
                ports_on_startup.remove(port)

        time.sleep(2)

if __name__ == '__main__':
    main()


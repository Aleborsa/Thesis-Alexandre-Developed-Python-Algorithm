import win_inet_pton
from pyModbusTCP.client import ModbusClient

HOST = "10.20.38.10"
ModBus = ModbusClient(host=HOST, port=502, auto_open=True)


def barrel():
    register = ModBus.read_input_registers(30)
    testBarrel = register[0] and 3

    if testBarrel != 3:
        return 1
    else:
        return 0


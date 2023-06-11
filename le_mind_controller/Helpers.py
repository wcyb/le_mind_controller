from serial.tools import list_ports as lp
from serial import Serial


class Helpers:
    def __init__(self):
        pass

    @staticmethod
    def get_available_ports() -> list[str]:
        available_ports = lp.comports()
        if len(available_ports) == 0:
            return []  # no COM ports available
        return [prt.name for prt in available_ports]

    @staticmethod
    def create_serial(port_name: str, port_baud: int = 115200) -> Serial:
        return Serial(port_name, port_baud, timeout=1)

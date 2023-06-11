from serial.threaded import LineReader
from serial.threaded import ReaderThread


class SerComm(LineReader):
    TERMINATOR = b'\r'

    def __init__(self):
        self.buffer = bytearray()
        self.on_receive = None
        self.on_disconnect = None

    def connection_made(self, transport: ReaderThread):
        super().connection_made(transport)

    def handle_line(self, data: str):
        if self.on_receive is not None:
            self.on_receive(data)

    def connection_lost(self, exc: Exception):
        if self.on_disconnect is not None:
            self.on_disconnect()

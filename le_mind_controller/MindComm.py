import random
import string
import json
from serial.threaded import ReaderThread
from serial import Serial

from .SerComm import SerComm
from .MindData import HubPortName, MindData


class MindComm:
    def __init__(self, port: Serial, mind_data: MindData):
        self.data_received = False

        self.mind_data = mind_data
        self.comm_th = ReaderThread(port, SerComm)
        self.comm_th.start()
        self.transport, self.protocol = self.comm_th.connect()
        self.protocol.on_receive = self.__receive

    @staticmethod
    def __generate_message_id() -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits + "-_", k=4))

    def __receive(self, data: str):
        if self.mind_data is not None:
            self.data_received = self.mind_data.parse_mind_data(data)

    def __send(self, data: dict) -> str:
        message_id = self.__generate_message_id()
        data['i'] = message_id
        self.protocol.write_line(json.dumps(data))
        return message_id

    def cmd_start_command_streaming(self) -> str:
        return self.__send({'i': '',
                            'm': "program_modechange",
                            'p': {"mode": "play"}})

    def cmd_stop_program_execution(self) -> str:
        return self.__send({'i': '',
                            'm': "program_terminate",
                            'p': {}})

    def cmd_reset_program_time(self) -> str:
        return self.__send({'i': '',
                            'm': "reset_program_time",
                            'p': {}})

    def cmd_motor_set_position_value(self, port_name: HubPortName, offset: int) -> str:
        return self.__send({'i': '',
                            'm': "scratch.motor_set_position",
                            'p': {"port": port_name.name, "offset": offset}})

    def cmd_reset_yaw(self) -> str:
        return self.__send({'i': '',
                            'm': "scratch.reset_yaw",
                            'p': {}})

    def cmd_clear_display(self) -> str:
        return self.__send({'i': '',
                            'm': "scratch.display_clear",
                            'p': {}})

    def cmd_motor_turn_on(self, port_name: HubPortName, speed: int = 80, stop_when_stalled: bool = True) -> str:
        return self.__send({'i': '',
                            'm': "scratch.motor_start",
                            'p': {"port": port_name.name, "speed": speed, "stall": stop_when_stalled}})

    def cmd_motor_turn_off(self, port_name: HubPortName) -> str:
        return self.__send({'i': '',
                            'm': "scratch.motor_stop",
                            'p': {"port": port_name.name, "stop": 1}})

    def cmd_motor_double_turn_on_cm(self, port_name1: HubPortName, port_name2: HubPortName, speed1: int = 80, speed2: int = 80, distance_cm: int = 10) -> str:
        degrees = int(20.5 * distance_cm)
        return self.__send({'i': '',
                            'm': "scratch.move_tank_degrees",
                            'p': {"lmotor": port_name1.name, "rmotor": port_name2.name, "lspeed": speed1, "rspeed": speed2, "stop": 1, "degrees": degrees}})

    def cmd_motor_double_turn_on_deg(self, port_name1: HubPortName, port_name2: HubPortName, speed1: int = 80, speed2: int = 80, degrees: int = 10) -> str:
        return self.__send({'i': '',
                            'm': "scratch.move_tank_degrees",
                            'p': {"lmotor": port_name1.name, "rmotor": port_name2.name, "lspeed": speed1, "rspeed": speed2, "stop": 1, "degrees": degrees}})

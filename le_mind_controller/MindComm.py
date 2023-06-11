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

    def __send(self, data: dict):
        self.protocol.write_line(json.dumps(data))

    def cmd_start_command_streaming(self) -> str:
        message_id = self.__generate_message_id()
        self.__send({'i': message_id, 'm': "program_modechange", 'p': {"mode": "play"}})
        return message_id

    def cmd_stop_program_execution(self) -> str:
        message_id = self.__generate_message_id()
        self.__send({'i': message_id, 'm': "program_terminate", 'p': {}})
        return message_id

    def cmd_reset_program_time(self) -> str:
        message_id = self.__generate_message_id()
        self.__send({'i': message_id, 'm': "reset_program_time", 'p': {}})
        return message_id

    def cmd_motor_set_position_value(self, port_name: HubPortName, offset: int) -> str:
        message_id = self.__generate_message_id()
        self.__send({'i': message_id, 'm': "scratch.motor_set_position",
                     'p': {"port": port_name.name, "offset": offset}})
        return message_id

    def cmd_reset_yaw(self) -> str:
        message_id = self.__generate_message_id()
        self.__send({'i': message_id, 'm': "scratch.reset_yaw", 'p': {}})
        return message_id

    def cmd_clear_display(self) -> str:
        message_id = self.__generate_message_id()
        self.__send({'i': message_id, 'm': "scratch.display_clear", 'p': {}})
        return message_id

    def cmd_motor_turn_on(self, port_name: HubPortName, speed: int = 80, stop_when_stalled: bool = True) -> str:
        message_id = self.__generate_message_id()
        self.__send({'i': message_id, 'm': "scratch.motor_start", 'p': {"port": port_name.name, "speed": speed, "stall": stop_when_stalled}})
        return message_id

    def cmd_motor_turn_off(self, port_name: HubPortName) -> str:
        message_id = self.__generate_message_id()
        self.__send({'i': message_id, 'm': "scratch.motor_stop", 'p': {"port": port_name.name, "stop": 1}})
        return message_id

    def cmd_motor_double_turn_on_cm(self, port_name1: HubPortName, port_name2: HubPortName, speed1: int = 80, speed2: int = 80, distance_cm: int = 10) -> str:
        message_id = self.__generate_message_id()
        degrees = int(20.5 * distance_cm)
        self.__send({'i': message_id, 'm': "scratch.move_tank_degrees", 'p': {"lmotor": port_name1.name, "rmotor": port_name2.name, "lspeed": speed1, "rspeed": speed2, "stop": 1, "degrees": degrees}})
        return message_id

    def cmd_motor_double_turn_on_deg(self, port_name1: HubPortName, port_name2: HubPortName, speed1: int = 80, speed2: int = 80, degrees: int = 10) -> str:
        message_id = self.__generate_message_id()
        self.__send({'i': message_id, 'm': "scratch.move_tank_degrees", 'p': {"lmotor": port_name1.name, "rmotor": port_name2.name, "lspeed": speed1, "rspeed": speed2, "stop": 1, "degrees": degrees}})
        return message_id

import json
from collections.abc import Callable
from enum import IntEnum
from typing import Any


class DeviceType(IntEnum):
    LIGHT_SENSOR = 61
    DISTANCE_SENSOR = 62
    MOTOR_MEDIUM = 75


class HubSideFacingUp(IntEnum):
    FRONT = 0
    UP = 1
    RIGHT = 2
    BACK = 3
    DOWN = 4
    LEFT = 5


class Colors(IntEnum):
    OTHER = -1
    BLACK = 0
    VIOLET = 1
    BLUE = 3
    TEAL = 4
    GREEN = 5
    YELLOW = 7
    RED = 9
    WHITE = 10


class HubPortName(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5


class HubPort:
    def __init__(self, name: HubPortName = None, device: DeviceType = None):
        self.port_name = name
        self.connected_device_type = device
        self.port_data = None

    def set_port_data(self, data: list):
        self.port_data = data

    def get_port_data(self) -> list:
        return self.port_data


class MindData:
    def __init__(self, confirmation_callback: Callable[[str], Any] = None):
        self.ports = {HubPortName.A: HubPort(HubPortName.A), HubPortName.B: HubPort(HubPortName.B),
                      HubPortName.C: HubPort(HubPortName.C), HubPortName.D: HubPort(HubPortName.D),
                      HubPortName.E: HubPort(HubPortName.E), HubPortName.F: HubPort(HubPortName.F)}
        self.acceleration = None
        self.gyro = None
        self.tilt_angle = None

        self.battery_voltage = None
        self.battery_level = None

        self.hub_orientation = None

        self.confirmation_callback = confirmation_callback

    def parse_mind_data(self, data: str) -> bool:
        try:
            received_json = json.loads(data)
            if 'r' in received_json:  # response to a previous command
                if self.confirmation_callback is not None:
                    self.confirmation_callback(received_json['i'])  # notify through a callback that the message with given ID was executed by the hub
            elif received_json['m'] == 0 and len(received_json['p']) == 12:  # if we receive status info
                self.ports[HubPortName.A].set_port_data(received_json['p'][0])
                self.ports[HubPortName.B].set_port_data(received_json['p'][1])
                self.ports[HubPortName.C].set_port_data(received_json['p'][2])
                self.ports[HubPortName.D].set_port_data(received_json['p'][3])
                self.ports[HubPortName.E].set_port_data(received_json['p'][4])
                self.ports[HubPortName.F].set_port_data(received_json['p'][5])
                self.acceleration = received_json['p'][6]
                self.gyro = received_json['p'][7]
                self.tilt_angle = received_json['p'][8]
            elif received_json['m'] == 2 and len(received_json['p']) == 3:
                self.battery_voltage = received_json['p'][0]
                self.battery_level = received_json['p'][1]
            elif received_json['m'] == 14:
                self.hub_orientation = HubSideFacingUp(received_json['p'])
            return True
        except Exception as e:
            # print("Error while parsing JSON data")
            return False

    def determine_type_of_connected_devices(self) -> int:
        number_of_devices = 0
        for port_name, port_obj in self.ports.items():
            if port_obj.get_port_data()[0] in iter(DeviceType):
                port_obj.connected_device_type = DeviceType(port_obj.get_port_data()[0])
                number_of_devices += 1
        return number_of_devices

    def get_distance(self) -> (HubPortName, int):
        for port_name, port_obj in self.ports.items():
            if port_obj.connected_device_type is DeviceType.DISTANCE_SENSOR:
                return port_name, port_obj.get_port_data()[1][0]
        return None, None

    def get_color(self) -> (HubPortName, Colors):
        for port_name, port_obj in self.ports.items():
            if port_obj.connected_device_type is DeviceType.LIGHT_SENSOR:
                if port_obj.get_port_data()[1][1] is not None:
                    return port_name, Colors(port_obj.get_port_data()[1][1])
                else:
                    return port_name, Colors.OTHER
        return None, None

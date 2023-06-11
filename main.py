from pynput.keyboard import Key, Listener

from le_mind_controller.MindData import MindData, HubPortName
from le_mind_controller.MindComm import MindComm
from le_mind_controller.Helpers import Helpers


def on_press(key: Key):
    # print("{0} pressed".format(key))
    match key:
        case Key.up:
            mc.cmd_motor_turn_on(HubPortName.B, -70)
        case Key.left:
            mc.cmd_motor_turn_on(HubPortName.A, 50)
        case Key.right:
            mc.cmd_motor_turn_on(HubPortName.A, -50)
        case Key.down:
            mc.cmd_motor_turn_on(HubPortName.B, 70)
        case Key.shift_l:
            mc.cmd_motor_turn_on(HubPortName.C, -35)
        case Key.shift_r:
            mc.cmd_motor_turn_on(HubPortName.C, 35)
        case Key.ctrl_l:
            mc.cmd_motor_turn_on(HubPortName.D, 35)
        case Key.ctrl_r:
            mc.cmd_motor_turn_on(HubPortName.D, -35)
        case Key.f12:
            print("Distance: {0}".format(md.get_distance()[1]))
            print("Color: {0}".format(md.get_color()[1].name))


def on_release(key: Key):
    # print("{0} release".format(key))
    match key:
        case Key.esc:
            print("Exiting...")  # Stop listener
            return False
        case _:
            mc.cmd_stop_program_execution()


def execution_confirmed(message_id: str):
    print("Message with id: {0} was executed by the hub.".format(message_id))


print("Available COM ports:")
for prt in Helpers.get_available_ports():
    print(prt)
port = input("Selected COM port: ")
ser = Helpers.create_serial(port)

md = MindData(execution_confirmed)
mc = MindComm(ser, md)
with Listener(on_press=on_press, on_release=on_release) as listener:
    while not mc.data_received:
        pass
    mc.cmd_start_command_streaming()
    print("Number of devices connected to the hub: {0}".format(md.determine_type_of_connected_devices()))
    listener.join()

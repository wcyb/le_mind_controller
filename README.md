# le_mind_controller
Python library that allows you to control the LEGO 51515 (MINDSTORMS) set.
Includes a demo showing how to use the library on an example of an M.V.P robot control with an added crane.
It is not necessary to install the official bloated LEGO software for this set.
All control and communication handling is done exclusively in Python, so we don't need additional software.
We can use the same functionalities as when programming with Word Blocks or in MicroPython using LEGO software, but not all functionalities have been implemented in this library yet.

Python version 3.11 or higher is required for this to function.

## Structure
* `Helpers.py` - It contains two functions - one allows you to list the available COM ports, and the other is used to create a connection.
* `MindComm.py` - It is responsible for the "high-level" handling of communication with the HUB. This is where the commands that control the HUB are located.
* `MindData.py` - Responsible for processing the data received from the HUB. Here you will find all the data from the sensors that are in the HUB, as well as functions for reading data from attachable modules.
* `SerComm.py` - It is responsible for the "low-level" handling of communication with the HUB. Here you will find the functionality responsible for data transfer and the HUB connectivity events.

## General usage information
No matter how we connect to the HUB (USB cable or Bluetooth), we need to follow certain steps in a certain order before we can control our robot.
1. First, identify the COM port used for communication. In the case of Bluetooth connection on Windows 10, we need to pair our HUB first. After that, we should have two additional COM ports assigned to the Bluetooth device (our HUB). Usually the first one will be the one we need. Sometimes it won't work, in which case we need to choose the second one.
2. Create a connection through the selected serial port - this is made possible by the `create_serial` function from the `Helpers` class.
3. Create an instance of the `MindData` class to process the data received from the HUB. In the constructor call, we can specify what function in our code will be responsible for monitoring the execution status of the commands we send.
4. Create an instance of the `MindComm` class to handle communication with the HUB. In the constructor call, specify the previously created connection to the selected serial port and the created `MindData` object.
5. Now wait for the data to be received from the HUB. When this happens, the `data_received` attribute in the `MindComm` object will be set to `True`.
6. We can now start controlling our HUB. To do this, first send the `cmd_start_command_streaming` command once, as the first one. If we specified in step 3 what function will monitor the execution status of the commands we send, after the HUB executes the command we specified, this specified function will be called with a parameter specifying the ID of the executed command. Such command ID will also be returned to us after calling each `cmd_...` function, so we can keep track of what commands were sent and what commands were executed. This allows us to sequence the execution of commands. If at any time we want to stop the execution of commands by the HUB, send the command `cmd_stop_program_execution`.

## Useful resources
* [The official MicroPython documentation for the LEGO MINDSTORMS Inventor Hub](https://lego.github.io/MINDSTORMS-Robot-Inventor-hub-API/index.html)
* [The format and types of commands](https://github.com/gpdaniels/spike-prime/issues/8)

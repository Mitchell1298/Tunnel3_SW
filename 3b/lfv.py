from pyModbusTCP.client import ModbusClient
from enum import Enum
from struct import *

class LightStatus(Enum):
    OFF = 0
    YELLOW_BLINKING = 1
    YELLOW_SOLID = 2
    RED = 3


class Lfv:
    BARRIER_1 = 41000
    BARRIER_2 = 41006
    BARRIER_POSITION = 1

    CAMERA_1 = 45000
    CAMERA_2 = 45004
    CAMERA_3 = 45008
    CAMERA_PAN = 0
    CAMERA_TILT = 1
    CAMERA_ZOOM = 2
    CAMERA_PRESET = 3

    

    def __init__(self, ip):
        self.modbus = ModbusClient(host=ip, unit_id=1, auto_open=True)

    def close_barrier(self, barrier):
        self.modbus.write_multiple_registers(barrier, [1])

    def open_barrier(self, barrier):
        self.modbus.write_multiple_registers(barrier, [2])

    def stop_barrier(self, barrier):
        self.modbus.write_multiple_registers(barrier, [3])

    def get_barrier_position(self, barrier):
        return self.modbus.read_holding_registers(barrier + BARRIER_POSITION)[0]

    def set_camera_orientation(self, camera, pan, tilt, zoom):
        self.modbus.write_multiple_registers(camera + Lfv.CAMERA_PAN, [pan])
        self.modbus.write_multiple_registers(camera + Lfv.CAMERA_TILT, pack('b', tilt))
        self.modbus.write_multiple_registers(camera + Lfv.CAMERA_ZOOM, [zoom])

    def set_camera_preset(self, camera, preset):
        self.modbus.write_multiple_registers(camera + Lfv.CAMERA_PRESET, [preset])

    def set_lights_level_global(self, level):
        self.modbus.write_multiple_registers(42000, [level])

    def set_lights_level_zone(self, zone, level):
        self.modbus.write_multiple_registers(43000 + 6 * zone, [level])

    def get_lights_level_zone(self, zone):
        return self.modbus.read_holding_registers(43000 + 6 * zone + 2)[0]

    def set_lights_auto(self, zone, auto):
        self.modbus.write_multiple_registers(43000 + 6 * zone + 1, [0 if auto else 1])

    def set_traffic_light_red(self, light):
        self.modbus.write_multiple_registers(40000 + 4 * light, [1])

    def set_traffic_light_off(self, light):
        self.modbus.write_multiple_registers(40000 + 4 * light, [2])

    def get_traffic_light_status(self, light):
        return LightStatus(self.modbus.read_holding_registers(40000 + 4 * light + 1)[0])

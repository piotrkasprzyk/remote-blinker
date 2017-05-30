#!/usr/bin/python3

import serial
import colorsys
import time


class SerialConnector(object):
    def __init__(self, port='/dev/ttyUSB0'):
        self._port = port
        self._conn = serial.Serial(self._port, timeout=1)

    def __del__(self):
        self._conn.close()

    @staticmethod
    def hex_to_palette(hex_string):
        if len(hex_string) != 6:
            return
    
        r, g, b = map(lambda x: int(x, 16) / 255, (hex_string[i:i+2] for i in range(0, len(hex_string), 2)))
        return map(lambda x: int(x * 255), colorsys.rgb_to_hsv(r, g, b))

    def set_hex_color(self, idx, hex_string):
        h, s, v = self.hex_to_palette(hex_string)
        b = bytearray([ord('?'), idx, h, 255, ord('!')])
        self._conn.write(b)


if __name__ == '__main__':
    sc = SerialConnector()
    time.sleep(5)
    sc.set_hex_color(0, 'ff0000')
    sc.set_hex_color(1, '00ff00')
    sc.set_hex_color(2, '0000ff')


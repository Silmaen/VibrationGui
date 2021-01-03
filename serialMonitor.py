#! /usr/bin/env python
# encoding: utf8
"""just a serial monitor"""

import serial
import struct

lines = [
b'4929677 82643.000000 165286.000000 247929.000000 495858.000000 578501.000000 661144.000000\n',
b'4937219 82644.000000 165288.000000 247932.000000 495864.000000 578508.000000 661152.000000\n',
b'4944306 82645.000000 165290.000000 247935.000000 495870.000000 578515.000000 661160.000000\n',
b'4951571 82646.000000 165292.000000 247938.000000 495876.000000 578522.000000 661168.000000\n',
b'4959324 82647.000000 165294.000000 247941.000000 495882.000000 578529.000000 661176.000000\n',
b'4966941 82648.000000 165296.000000 247944.000000 495888.000000 578536.000000 661184.000000\n',
b'4974452 82649.000000 165298.000000 247947.000000 495894.000000 578543.000000 661192.000000\n',
b'4981816 82650.000000 165300.000000 247950.000000 495900.000000 578550.000000 661200.000000\n',
b'4988944 82651.000000 165302.000000 247953.000000 495906.000000 578557.000000 661208.000000\n',
b'4996071 82652.000000 165304.000000 247956.000000 495912.000000 578564.000000 661216.000000\n',
b'5003461 82653.000000 165306.000000 247959.000000 495918.000000 578571.000000 661224.000000\n',
b']\xacE\x00\x00\x00\x00\x00\x00\x9d\x1aH\x00\x9d\x9aH\x80\xeb\xe7H\x80\xebgI`I\x87I\x00\x9d\x9aI\n',
b'L\xadE\x00\x00\x00\x00\x00@\x9d\x1aH@\x9d\x9aH\xe0\xeb\xe7H\xe0\xebgI\x98I\x87I@\x9d\x9aI\n',
b'Q\xaeE\x00\x00\x00\x00\x00\x80\x9d\x1aH\x80\x9d\x9aH@\xec\xe7H@\xecgI\xd0I\x87I\x80\x9d\x9aI7\x9dI\x00\x00\x00\x00\x00\x80\x02 H\x80\x02\xa0H\xc0\x03\xf0H\xc0\x03pI0\x02\x8cI\x80\x02\xa0I\n',
b',\x9eI\x00\x00\x00\x00\x00\xc0\x02 H\xc0\x02\xa0H \x04\xf0H \x04pIh\x02\x8cI\xc0\x02\xa0I\n',
b'\xf7\x9fI\x00\x00\x00\x00\x00\x00\x03 H\x00\x03\xa0H\x80\x04\xf0H\x80\x04pI\xa0\x02\x8cI\x00\x03\xa0I\n',
b'b\xa1I\x00\x00\x00\x00\x00@\x03 H@\x03\xa0H\xe0\x04\xf0H\xe0\x04pI\xd8\x02\x8cI@\x03\xa0I\n',
b'\x00\xa3I\x00\x00\x00\x00\x00\x80\x03 H\x80\x03\xa0H@\x05\xf0H@\x05pI\x10\x03\x8cI\x80\x03\xa0I\n',
b'\x85\xa4I\x00\x00\x00\x00\x00\xc0\x03 H\xc0\x03\xa0H\xa0\x05\xf0H\xa0\x05pIH\x03\x8cI\xc0\x03\xa0I\n',
b'\xc8\xa5I\x00\x00\x00\x00\x00\x00\x04 H\x00\x04\xa0H\x00\x06\xf0H\x00\x06pI\x80\x03\x8cI\x00\x04\xa0I\n',
b'1\xa7I\x00\x00\x00\x00\x00@\x04 H@\x04\xa0H`\x06\xf0H`\x06pI\xb8\x03\x8cI@\x04\xa0I\n',
b't\xa8I\x00\x00\x00\x00\x00\x80\x04 H\x80\x04\xa0H\xc0\x06\xf0H\xc0\x06pI\xf0\x03\x8cI\x80\x04\xa0I\n',
b'+\xaaI\x00\x00\x00\x00\x00\xc0\x04 H\xc0\x04\xa0H \x07\xf0H \x07pI(\x04\x8cI\xc0\x04\xa0I\n',
b'$\xabI\x00\x00\x00\x00\x00\x00\x05 H\x00\x05\xa0H\x80\x07\xf0H\x80\x07pI`\x04\x8cI\x00\x05\xa0I\n',
b'\x1f\xacI\x00\x00\x00\x00\x00@\x05 H@\x05\xa0H\xe0\x07\xf0H\xe0\x07pI\x98\x04\x8cI@\x05\xa0I\n',
b'\x0e\xadI\x00\x00\x00\x00\x00\x80\x05 H\x80\x05\xa0H@\x08\xf0H@\x08pI\xd0\x04\x8cI\x80\x05\xa0I\n',
b'\x08\xaeI\x00\x00\x00\x00\x00\xc0\x05 H\xc0\x05\xa0H\xa0\x08\xf0H\xa0\x08pI\x08\x05\x8cI\xc0\x05\xa0I\n',
b')\xafI\x00\x00\x00\x00\x00\x00\x06 H\x00\x06\xa0H\x00\t\xf0H\x00\tpI@\x05\x8cI\x00\x06\xa0I\n',
b'y\xb0I\x00\x00\x00\x00\x00@\x06 H@\x06\xa0H`\t\xf0H`\tpIx\x05\x8cI@\x06\xa0I\n',
b'\x94\xb2I\x00\x00\x00\x00\x00\x80\x06 H\x80\x06\xa0H\xc0\t\xf0H\xc0\tpI\xb0\x05\x8cI\x80\x06\xa0I\n',
b'&\xb4I\x00\x00\x00\x00\x00\xc0\x06 H\xc0\x06\xa0H \n',
b'\xf0H \n',
b'pI\xe8\x05\x8cI\xc0\x06\xa0I\n',
b'i\xb5I\x00\x00\x00\x00\x00\x00\x07 H\x00\x07\xa0H\x80\n',
b'\xf0H\x80\n',
b'pI \x06\x8cI\x00\x07\xa0I\n',
b'U\xb6I\x00\x00\x00\x00\x00@\x07 H@\x07\xa0H\xe0\n',
b'\xf0H\xe0\n',
b'pIX\x06\x8cI@\x07\xa0I\n',
b'O\xb7I\x00\x00\x00\x00\x00\x80\x07 H\x80\x07\xa0H@\x0b\xf0H@\x0bpI\x90\x06\x8cI\x80\x07\xa0I\n',
b'<\xb8I\x00\x00\x00\x00\x00\xc0\x07 H\xc0\x07\xa0H\xa0\x0b\xf0H\xa0\x0bpI\xc8\x06\x8cI\xc0\x07\xa0I\n',
b'C\xb9I\x00\x00\x00\x00\x00\x00\x08 H\x00\x08\xa0H\x00\x0c\xf0H\x00\x0cpI\x00\x07\x8cI\x00\x08\xa0I\n',
b'/\xbaI\x00\x00\x00\x00\x00@\x08 H@\x08\xa0H`\x0c\xf0H`\x0cpI8\x07\x8cI@\x08\xa0I\n',
b'7\xbbI\x00\x00\x00\x00\x00\x80\x08 H\x80\x08\xa0H\xc0\x0c\xf0H\xc0\x0cpIp\x07\x8cI\x80\x08\xa0I\n',
b'$\xbcI\x00\x00\x00\x00\x00\xc0\x08 H\xc0\x08\xa0H \r\xf0H \rpI\xa8\x07\x8cI\xc0\x08\xa0I\n',
b'+\xbdI\x00\x00\x00\x00\x00\x00\t H\x00\t\xa0H\x80\r\xf0H\x80\rpI\xe0\x07\x8cI\x00\t\xa0I\n',
b'\x18\xbeI\x00\x00\x00\x00\x00@\t H@\t\xa0H\xe0\r\xf0H\xe0\rpI\x18\x08\x8cI@\t\xa0I\n',
b'\x1f\xbfI\x00\x00\x00\x00\x00\x80\t H\x80\t\xa0H@\x0e\xf0H@\x0epIP\x08\x8cI\x80\t\xa0I\n',
b'\x0c\xc0I\x00\x00\x00\x00\x00\xc0\t H\xc0\t\xa0H\xa0\x0e\xf0H\xa0\x0epI\x88\x08\x8cI\xc0\t\xa0I\n',
b'\x12\xc1I\x00\x00\x00\x00\x00\x00\n',
b' H\x00\n',
b'\xa0H\x00\x0f\xf0H\x00\x0fpI\xc0\x08\x8cI\x00\n',
b'\xa0I\n',
b'\x00\xc2I\x00\x00\x00\x00\x00@\n',
b' H@\n',
b'\xa0H`\x0f\xf0H`\x0fpI\xf8\x08\x8cI@\n',
b'\xa0I\n',
b'\x06\xc3I\x00\x00\x00\x00\x00\x80\n',
b' H\x80\n',
b'\xa0H\xc0\x0f\xf0H\xc0\x0fpI0\t\x8cI\x80\n',
b'\xa0I\n',
b'\xf4\xc3I\x00\x00\x00\x00\x00\xc0\n',
b' H\xc0\n',
b'\xa0H \x10\xf0H \x10pIh\t\x8cI\xc0\n',
b'\xa0I\n',
b'\xfa\xc4I\x00\x00\x00\x00\x00\x00\x0b H\x00\x0b\xa0H\x80\x10\xf0H\x80\x10pI\xa0\t\x8cI\x00\x0b\xa0I\n',
b'\xe8\xc5I\x00\x00\x00\x00\x00@\x0b H@\x0b\xa0H\xe0\x10\xf0H\xe0\x10pI\xd8\t\x8cI@\x0b\xa0I\n',
b'\xee\xc6I\x00\x00\x00\x00\x00\x80\x0b H\x80\x0b\xa0H@\x11\xf0H@\x11pI\x10\n',
b'\x8cI\x80\x0b\xa0I\n',
b'\xdc\xc7I\x00\x00\x00\x00\x00\xc0\x0b H\xc0\x0b\xa0H\xa0\x11\xf0H\xa0\x11pIH\n',
b'\x8cI\xc0\x0b\xa0I\n',
b'\xe2\xc8I\x00\x00\x00\x00\x00\x00\x0c H\x00\x0c\xa0H\x00\x12\xf0H\x00\x12pI\x80\n',
b'\x8cI\x00\x0c\xa0I\n',
b'\xdc\xc9I\x00\x00\x00\x00\x00@\x0c H@\x0c\xa0H`\x12\xf0H`\x12pI\xb8\n',
b'\x8cI@\x0c\xa0I\n',
b'\xd6\xcaI\x00\x00\x00\x00\x00\x80\x0c H\x80\x0c\xa0H\xc0\x12\xf0H\xc0\x12pI\xf0\n',
b'\x8cI\x80\x0c\xa0I\n',
b'\xc4\xcbI\x00\x00\x00\x00\x00\xc0\x0c H\xc0\x0c\xa0H \x13\xf0H \x13pI(\x0b\x8cI\xc0\x0c\xa0I\n',
b'\xbe\xccI\x00\x00\x00\x00\x00\x00\r H\x00\r\xa0H\x80\x13\xf0H\x80\x13pI`\x0b\x8cI\x00\r\xa0I\n',
b'\xb8\xcdI\x00\x00\x00\x00\x00@\r H@\r\xa0H\xe0\x13\xf0H\xe0\x13pI\x98\x0b\x8cI@\r\xa0I\n',
b'\xdb\x06J\x00\x00\x00\x00\x00\xc0\x1a H\xc0\x1a\xa0H (\xf0H (pIh\x17\x8cI\xc0\x1a\xa0I\n',
b'\xd6\x07J\x00\x00\x00\x00\x00\x00\x1b H\x00\x1b\xa0H\x80(\xf0H\x80(pI\xa0\x17\x8cI\x00\x1b\xa0I\n',
b'\xd0\x08J\x00\x00\x00\x00\x00@\x1b H@\x1b\xa0H\xe0(\xf0H\xe0(pI\xd8\x17\x8cI@\x1b\xa0I\n',
b'\xca\tJ\x00\x00\x00\x00\x00\x80\x1b H\x80\x1b\xa0H@)\xf0H@)pI\x10\x18\x8cI\x80\x1b\xa0I\n',
b'\xc4\n',
b'J\x00\x00\x00\x00\x00\xc0\x1b H\xc0\x1b\xa0H\xa0)\xf0H\xa0)pIH\x18\x8cI\xc0\x1b\xa0I\n',
b'\xbe\x0bJ\x00\x00\x00\x00\x00\x00\x1c H\x00\x1c\xa0H\x00*\xf0H\x00*pI\x80\x18\x8cI\x00\x1c\xa0I\n',
b'\xb8\x0cJ\x00\x00\x00\x00\x00@\x1c H@\x1c\xa0H`*\xf0H`*pI\xb8\x18\x8cI@\x1c\xa0I\n',
b'\xbe\rJ\x00\x00\x00\x00\x00\x80\x1c H\x80\x1c\xa0H\xc0*\xf0H\xc0*pI\xf0\x18\x8cI\x80\x1c\xa0I\n',
b'\xac\x0eJ\x00\x00\x00\x00\x00\xc0\x1c H\xc0\x1c\xa0H +\xf0H +pI(\x19\x8cI\xc0\x1c\xa0I\n',
b'\xa6\x0fJ\x00\x00\x00\x00\x00\x00\x1d H\x00\x1d\xa0H\x80+\xf0H\x80+pI`\x19\x8cI\x00\x1d\xa0I\n',
b'\xac\x10J\x00\x00\x00\x00\x00@\x1d H@\x1d\xa0H\xe0+\xf0H\xe0+pI\x98\x19\x8cI@\x1d\xa0I\n',
b'\xc9HJ\x00\x00\x00\x00\x00\x80* H\x80*\xa0H\xc0?\xf0H\xc0?pI0%\x8cI\x80*\xa0I\n',
b'\x05JJ\x00\x00\x00\x00\x00\xc0* H\xc0*\xa0H @\xf0H @pIh%\x8cI\xc0*\xa0I\n',
b';KJ\x00\x00\x00\x00\x00\x00+ H\x00+\xa0H\x80@\xf0H\x80@pI\xa0%\x8cI\x00+\xa0I\n',
b'4LJ\x00\x00\x00\x00\x00@+ H@+\xa0H\xe0@\xf0H\xe0@pI\xd8%\x8cI@+\xa0I\n',
b'.MJ\x00\x00\x00\x00\x00\x80+ H\x80+\xa0H@A\xf0H@ApI\x10&\x8cI\x80+\xa0I\n',
b'(NJ\x00\x00\x00\x00\x00\xc0+ H\xc0+\xa0H\xa0A\xf0H\xa0ApIH&\x8cI\xc0+\xa0I\n',
b'"OJ\x00\x00\x00\x00\x00\x00, H\x00,\xa0H\x00B\xf0H\x00BpI\x80&\x8cI\x00,\xa0I\n',
b'\x1cPJ\x00\x00\x00\x00\x00@, H@,\xa0H`B\xf0H`BpI\xb8&\x8cI@,\xa0I\n',
b'\x16QJ\x00\x00\x00\x00\x00\x80, H\x80,\xa0H\xc0B\xf0H\xc0BpI\xf0&\x8cI\x80,\xa0I\n',
b"\x10RJ\x00\x00\x00\x00\x00\xc0, H\xc0,\xa0H C\xf0H CpI('\x8cI\xc0,\xa0I\n",
b'\n',
b"SJ\x00\x00\x00\x00\x00\x00- H\x00-\xa0H\x80C\xf0H\x80CpI`'\x8cI\x00-\xa0I\n",
b"\x04TJ\x00\x00\x00\x00\x00@- H@-\xa0H\xe0C\xf0H\xe0CpI\x98'\x8cI@-\xa0I\n",
b"\xfeTJ\x00\x00\x00\x00\x00\x80- H\x80-\xa0H@D\xf0H@DpI\xd0'\x8cI\x80-\xa0I\n",
b'\x04VJ\x00\x00\x00\x00\x00\xc0- H\xc0-\xa0H\xa0D\xf0H\xa0DpI\x08(\x8cI\xc0-\xa0I\n',
b'\xf2VJ\x00\x00\x00\x00\x00\x00. H\x00.\xa0H\x00E\xf0H\x00EpI@(\x8cI\x00.\xa0I\n',
b'\xecWJ\x00\x00\x00\x00\x00@. H@.\xa0H`E\xf0H`EpIx(\x8cI@.\xa0I\n',
b'_\x03K\x00\x00\x00\x00\x00@V H@V\xa0H`\x81\xf0H`\x81pIxK\x8cI@V\xa0I\n',
b'N\x04K\x00\x00\x00\x00\x00\x80V H\x80V\xa0H\xc0\x81\xf0H\xc0\x81pI\xb0K\x8cI\x80V\xa0I\n',
b'G\x05K\x00\x00\x00\x00\x00\xc0V H\xc0V\xa0H \x82\xf0H \x82pI\xe8K\x8cI\xc0V\xa0I\n',
b'A\x06K\x00\x00\x00\x00\x00\x00W H\x00W\xa0H\x80\x82\xf0H\x80\x82pI L\x8cI\x00W\xa0I\n',
b'<\x07K\x00\x00\x00\x00\x00@W H@W\xa0H\xe0\x82\xf0H\xe0\x82pIXL\x8cI@W\xa0IStatistics:\n'
]

def main():
    com = serial.Serial(port="COM3")
    com.set_buffer_size(rx_size=1000000)
    mode = 0
    while 1:
        if mode == 0:
            byte_line = com.read_until(b'\n')
            print("<<< " + byte_line.decode('ascii').rstrip())
            if b"MESASC" in byte_line:
                mode = 1
                continue
            if b"MESBIN" in byte_line:
                mode = 2
                continue
        if mode == 1:
            byte_line = com.read_until(b'\n')
            if b"RDY" in byte_line:
                mode = 0
                continue
            items = byte_line.decode('ascii').split()
            # print(items)
        if mode == 2:
            byte_line = com.read(40)
            if byte_line == b"0000000000000000000000000000000000000000":
                mode = 0
                continue
            items = [
                struct.unpack("Q", byte_line[0:8])[0],
                # struct.unpack("f", byte_line[8:12])[0],
                struct.unpack("f", byte_line[12:16])[0],
                struct.unpack("f", byte_line[16:20])[0],
                struct.unpack("f", byte_line[20:24])[0],
                struct.unpack("f", byte_line[24:28])[0],
                struct.unpack("f", byte_line[28:32])[0],
                struct.unpack("f", byte_line[32:36])[0],
                # struct.unpack("f", byte_line[36:40])[0],
            ]
            # print(items)


if __name__ == '__main__':
    main()

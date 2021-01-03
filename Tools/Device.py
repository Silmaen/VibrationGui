"""
Module de définition de la classe d'interface avec l'appareil de mesure
"""
import serial
import time
import serial.tools.list_ports
import struct

old_mesure_methode = True


class VibrationDevice:
    """
    classe de gestion d'un périphérique de mesure
    """
    def __init__(self, parent, port):
        self.__isVibDev = False
        self.parent = parent
        self.bin_fmt = False
        if port in [None, ""]:
            return
        try:
            self.com = serial.Serial(port=port, baudrate=250000, timeout=10)
            self.com.set_buffer_size(rx_size=1000000)
            start = time.time()
            rdy = self.__wait_ready(True)
            if rdy:
                self.__write(b"qui_es_tu", True)
                while time.time() - start < 10:  # timeout 10second
                    line = self.__read_line(True)
                    if b"DeviceVibration" in line:
                        self.__isVibDev = True
                        break
        except Exception as err:
            self.parent.log(str(err))

    def __write(self, st: bytes, force=False, trace=False):
        if not self.__isVibDev and not force:
            return False
        if trace:
            self.parent.log(st.decode("ascii"), -1)
        self.com.write(st)
        self.com.flush()
        return self.__wait_ack(force, trace)

    def __read_line(self, force=False, trace=False):
        if not self.__isVibDev and not force:
            return ""
        line = self.com.readline()
        if trace:
            self.parent.log(line.decode("ascii"), -2)
        return line

    def __read_line_fast(self):
        return self.com.readline()

    def __wait_ready(self, force=False, trace=False):
        start = time.time()
        rdy = False
        while time.time() - start < 10:  # timeout 10second
            line = self.__read_line(force, trace)
            if b"RDY" in line:
                rdy = True
                break
        return rdy

    def __wait_ack(self, force=False, trace=False):
        start = time.time()
        rdy = False
        while time.time() - start < 10:  # timeout 10second
            line = self.__read_line(force, trace)
            if b"ACK" in line:
                rdy = True
                break
        return rdy

    def is_vibration_device(self):
        """
        retourne True si le test de communication est concluant
        """
        return self.__isVibDev

    def set_measure_time(self, mes_time):
        """
        Défini le temps de mesure sur le périphérique
        :param mes_time: le temps de mesure en secondes
        """
        self.__write(("set_mtime " + str(mes_time) + "000000\n").encode("ascii"))
        if not self.__wait_ready():
            self.parent.log("Impossible de définir le temps de mesure")

    def set_measure_range(self, mes_range=16):
        """
        Défini l'échelle de mesure
        :param mes_range: l'échelle 0:2g 1:4g 2:8g 3:16g(default)
        """
        if type(mes_range) != int:
            return
        mes_range = min(max(mes_range, 0), 3)
        self.__write(("set_range " + str(mes_range) + "\n").encode("ascii"))
        if not self.__wait_ready():
            self.parent.log("Impossible de définir l'échelle de mesure")

    def set_measure_resolution(self, mes_resolution):
        """
        Défini la résolution de mesure
        :param mes_resolution: 0: LowResolution 1: high resolution(default)
        """
        if type(mes_resolution) != int:
            return
        mes_resolution = min(max(mes_resolution, 0), 1)
        self.__write(("set_resolution " + str(mes_resolution) + "\n").encode("ascii"))
        if not self.__wait_ready():
            self.parent.log("Impossible de définir la résolution")

    def set_motor_delay(self, mot_delay):
        """
        Défini la résolution de mesure
        :param mot_delay: [100-1000] ms (défaut=100)
        """
        if type(mot_delay) != int:
            self.parent.log("Mauvais type de donnée de délai: " + str(type(mot_delay)), 2)
            return
        mot_delay = min(max(mot_delay, 100), 1000)
        self.__write(("set_wait " + str(mot_delay) + "\n").encode("ascii"))
        if not self.__wait_ready():
            self.parent.log("Impossible de définir le délai de moteur")

    def set_motor_throttle(self, mot_throttle):
        """
        Défini la résolution de mesure
        :param mot_throttle: [0-100] % (défaut=20%)
        """
        if type(mot_throttle) != int:
            self.parent.log("Mauvais type de donnée de gaz: " + str(type(mot_throttle)), 2)
            return
        mot_throttle = min(max(mot_throttle, 0), 100)
        self.__write(("set_throttle " + str(mot_throttle) + "\n").encode("ascii"))
        if not self.__wait_ready():
            self.parent.log("Impossible de définir les gaz moteur")

    def set_binary(self, binary: bool):
        """
        Défini le format d'échange des données brute avec le périphérique
        :param binary: TRue: format binaire, sinon, format ascii
        """
        self.bin_fmt = binary
        if self.bin_fmt:
            self.__write(b"set_binary")
            if not self.__wait_ready():
                self.parent.log("Impossible de définir le format binaire")
        else:
            self.__write(b"set_ascii")
            if not self.__wait_ready():
                self.parent.log("Impossible de définir le format ascii")

    def measure(self):
        """
        Lance la commande de mesure
        :return: une liste de ligne de retour.
        """
        if not self.__isVibDev:
            return []
        self.com.flushInput()
        self.__write(b"measure")
        lines = []
        self.parent.log("measuring, please wait...", 3)

        if self.bin_fmt:
            bin_mode = False
            bin_len = 40
            while 1:
                if bin_mode:
                    line = self.com.read(bin_len)
                    if line == b"0" * bin_len:
                        bin_mode = False
                        break
                    items = [
                        struct.unpack("Q", line[0:8])[0],
                        # struct.unpack("f", byte_line[8:12])[0],
                        struct.unpack("f", line[12:16])[0],
                        struct.unpack("f", line[16:20])[0],
                        struct.unpack("f", line[20:24])[0],
                        struct.unpack("f", line[24:28])[0],
                        struct.unpack("f", line[28:32])[0],
                        struct.unpack("f", line[32:36])[0],
                        # struct.unpack("f", byte_line[36:40])[0],
                    ]
                    lines.append(items)
                else:
                    line = self.__read_line().strip()
                    if b"MESBIN" in line:
                        lines = []
                        bin_len = int(line.split()[1])
                        bin_mode = True
                        continue
        else:
            rdy_count = 0
            while 1:
                line = self.__read_line().strip()
                if b"RDY" in line:
                    rdy_count += 1
                    if rdy_count == 3:
                        break
                    continue
                if b"MESASC" in line:
                    lines = []
                    continue
                lines.append(line)
            self.parent.log("measure done", 3)
        return lines


def findDevice(parent):
    """
    Recherche sur les ports série si un périphérique est présent et revoie le premier objet trouvé
    :param parent: l'appelant. doit être une classe ayant une méthode log.
    :return: Un objet device ou None s'il n'a rien trouvé
    """
    arduino_port = [p.device for p in serial.tools.list_ports.comports() if 'arduino' in p.description.lower()]
    if len(arduino_port) < 1:
        parent.log("No device found.")
        return None
    for port in arduino_port:
        dev = VibrationDevice(parent, port)
        if dev.is_vibration_device():
            parent.log("Vibration device found at: " + str(port), 3)
            return dev
    parent.log("No vibration device found.")
    return None

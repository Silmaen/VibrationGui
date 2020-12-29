"""
Module de définition de la classe d'interface avec l'appareil de mesure
"""
import serial
import time
import serial.tools.list_ports

old_mesure_methode = True


class VibrationDevice:
    """
    classe de gestion d'un périphérique de mesure
    """
    def __init__(self, parent, port):
        self.__isVibDev = False
        self.parent = parent
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
        self.__write(("set_mtime " + str(mes_time) + "000000\n").encode("ascii"), trace=True)
        if not self.__wait_ready(trace=True):
            self.parent.log("Impossible de définir le temps de mesure")

    def set_measure_range(self, mes_range=16):
        """
        Défini l'échelle de mesure
        :param mes_range: l'échelle 0:2g 1:4g 2:8g 3:16g(default)
        """
        if type(mes_range) != int:
            return
        mes_range = min(max(mes_range, 0), 3)
        self.__write(("set_range " + str(mes_range) + "\n").encode("ascii"), trace=True)
        if not self.__wait_ready(trace=True):
            self.parent.log("Impossible de définir l'échelle de mesure")

    def set_measure_resolution(self, mes_resolution):
        """
        Défini la résolution de mesure
        :param mes_resolution: 0: LowResolution 1: high resolution(default)
        """
        if type(mes_resolution) != int:
            return
        mes_resolution = min(max(mes_resolution, 0), 1)
        self.__write(("set_resolution " + str(mes_resolution) + "\n").encode("ascii"), trace=True)
        if not self.__wait_ready(trace=True):
            self.parent.log("Impossible de définir la résolution")

    def measure(self):
        """
        Lance la commande de mesure
        :return: une liste de ligne de retour.
        """
        if not self.__isVibDev:
            return []
        self.com.flushInput()
        self.__write(b"measure")
        if old_mesure_methode:
            lines = []
            self.parent.log("measuring, please wait...", 3)
            rdy_count = 0
            while 1:
                line = self.__read_line().strip()
                if b"RDY" in line:
                    rdy_count += 1
                    if rdy_count == 3:
                        break
                    continue
                if b"MES" in line:
                    lines = []
                    continue
                lines.append(line)
            self.parent.log("measure done", 3)
        else:
            raw_data = b""
            self.parent.log("measuring, please wait...", 3)
            while 1:
                raw_line = self.com.read(3)
                raw_data += raw_line
                if b"RDY" in raw_line:
                    break
            self.parent.log("measure done", 3)
            lines = []
            inlines = raw_data.splitlines(keepends=False)
            for inline in inlines:
                if b"MES" in inline:
                    lines = []
                    continue
                if b"RDY" in inline:
                    break
                lines.append(inline)
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

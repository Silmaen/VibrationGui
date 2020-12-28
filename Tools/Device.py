"""
Module de définition de la classe d'interface avec l'appareil de mesure
"""
import serial
import time
import serial.tools.list_ports


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
            self.com = serial.Serial(port=port, baudrate=115200, timeout=10)
            self.com.set_buffer_size(rx_size=1000000)
            start = time.time()
            rdy = self.__wait_ready(True)
            if rdy:
                self.__write(b"quiestu", True)
                while time.time() - start < 10:  # timeout 10second
                    line = self.__read_line(True)
                    if b"DeviceVibration" in line:
                        self.__isVibDev = True
                        break
        except Exception as err:
            self.parent.log(str(err))

    def __write(self, st: bytes, force=False):
        if not self.__isVibDev and not force:
            return False
        self.com.write(st)
        self.com.flush()
        return self.__wait_ack(force)

    def __read_line(self, force=False):
        if not self.__isVibDev and not force:
            return ""
        line = self.com.readline()
        return line

    def __wait_ready(self, force=False):
        start = time.time()
        rdy = False
        while time.time() - start < 10:  # timeout 10second
            line = self.__read_line(force)
            if b"RDY" in line:
                rdy = True
                break
        return rdy

    def __wait_ack(self, force=False):
        start = time.time()
        rdy = False
        while time.time() - start < 10:  # timeout 10second
            line = self.__read_line(force)
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
        self.__write(("setmtime " + str(mes_time*1000000)).encode("utf8"))
        self.__wait_ready()

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

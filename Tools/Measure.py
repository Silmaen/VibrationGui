"""
Module De définition des outils des mesure
"""
from threading import Thread
import queue
from Tools.Device import findDevice
import numpy as np
import scipy.signal as sp

from Tools.utils import compute_period


class MesureManager:
    """
    Classe de gestion des des mesures, permettant de mesurer dans un thread séparé
    """
    def __init__(self, root=None, log_callback=None, post_mesure=None):
        self.root = root
        self.log_callback = log_callback
        self.queue = queue.Queue()
        self.data = None
        self.data_change = False
        self.post_mesure = post_mesure
        self.option_time = 5
        self.option_range = 3
        self.option_resolution = 1
        self.option_motor_delay = 100
        self.option_motor_throttle = 20
        self.option_bin_fmt = False

    def log(self, msg: str, lvl: int = 1):
        """
        fonction de log dans la console
        :param msg: le message à afficher
        :param lvl: le niveau du message (cf. les niveaux de log)
        """
        if self.log_callback:
            self.log_callback(msg, lvl)

    def process_queue(self):
        """
        traitement de la queue des messages
        :return:
        """
        try:
            self.queue.get(False)
            # Show result of the task if needed
            if self.post_mesure is not None:
                self.post_mesure()
        except queue.Empty:
            self.root.after(100, self.process_queue)

    def configure(self, **kw):
        """
        Fonction de configuration (Setter General)
        """
        key = 'option_time'
        if key in kw:
            self.option_time = kw[key]
            del kw[key]
        key = 'option_range'
        if key in kw:
            self.option_range = kw[key]
            del kw[key]
        key = 'option_resolution'
        if key in kw:
            self.option_resolution = kw[key]
            del kw[key]
        key = 'option_motor_delay'
        if key in kw:
            self.option_motor_delay = kw[key]
            del kw[key]
        key = 'option_motor_throttle'
        if key in kw:
            self.option_motor_throttle = kw[key]
            del kw[key]

    def Mesure(self):
        """
        exécute une mesure dans un thread séparé
        """
        self.log('MesureManager.Mesure', 4)
        self.queue = queue.Queue()
        self.ThreadedMesure(self).start()
        self.root.after(100, self.process_queue)

    def set_data(self, data):
        """
        Défini les données
        :param data: les nouvelles données
        """
        self.data = data
        self.data_change = True

    def get_data(self):
        """
        renvoie les données
        :return: les données
        """
        self.data_change = False
        return self.data

    class ThreadedMesure(Thread):
        """
        permet la gestion de la mesure dans un thread séparé
        """
        def __init__(self, parent):
            Thread.__init__(self)
            self.parent = parent
            self.q = parent.queue

        def run(self) -> None:
            """
            Execution de la file d'attente
            """
            device = findDevice(self.parent)
            if not device:
                self.parent.log("Pas trouvé de périphérique compatible, pas de mesure.")
                self.q.put("Task failed")
                return
            device.set_measure_time(self.parent.option_time)
            device.set_measure_range(self.parent.option_range)
            device.set_measure_resolution(self.parent.option_resolution)
            device.set_motor_delay(self.parent.option_motor_delay)
            device.set_motor_throttle(self.parent.option_motor_throttle)
            device.set_binary(self.parent.option_bin_fmt)
            self.parent.set_data(self.mesure(device))
            device.com.close()
            self.parent.log("Mesure Terminée", 3)
            self.q.put("Task finished")

        def mesure(self, device):
            """
            réclame une mesure au périphérique et stocke le retour
            :param device: le périphérique
            :return: les données de retour
            """
            lines = device.measure()
            time = []
            ax = []
            ay = []
            az = []
            v5 = []
            v = []
            i = []
            if device.bin_fmt:
                for line in lines:
                    time.append(line[0]/1.e6)
                    ax.append(line[1])
                    ay.append(line[2])
                    az.append(line[3])
                    v5.append(line[4])
                    v.append(line[5])
                    i.append(line[6])
            else:
                for line in lines:
                    it = line.split()
                    if len(it) != 7:
                        self.parent.log("format de ligne incorrect: '" + line.decode("ascii") + "' " + str(len(it)))
                        continue
                    try:
                        tt = float(it[0])/1.e6
                        tax = float(it[1])
                        tay = float(it[2])
                        taz = float(it[3])
                        tv5 = float(it[4])
                        tv = float(it[5])
                        ti = float(it[6])
                        time.append(tt)
                        ax.append(tax)
                        ay.append(tay)
                        az.append(taz)
                        v5.append(tv5)
                        v.append(tv)
                        i.append(ti)
                    except Exception as err:
                        self.parent.log("Mauvais décodage de la chaine '" + line.decode("ascii") + "' : " + str(err))
            data = {"time": np.array(time), "ax": np.array(ax), "ay": np.array(ay), "az": np.array(az),
                    "v5": np.array(v5), "v": np.array(v), "i": np.array(i)
                    }
            data["ax"] = data["ax"] - data["ax"].mean()
            data["ay"] = data["ay"] - data["ay"].mean()
            data["az"] = data["az"] - data["az"].mean()
            dt, f, std = compute_period(data["time"])
            data["sampling"] = {
                "number": np.size(data["time"]),
                "dt": dt,
                "frequency": f,
                "deviation": std
            }
            self.parent.log("Fréquence d'échantillon: " + str(f), 3)
            # filter frequencies to keep between 1 Hz - 100 Hz
            # sos = sp.butter(10, [0.1, min(150, 0.9 * f/2.0)], 'bandpass', fs=f, output='sos')
            # data["ax"] = sp.sosfilt(sos, data["ax"])
            # data["ay"] = sp.sosfilt(sos, data["ay"])
            # data["az"] = sp.sosfilt(sos, data["az"])
            # data["v5"] = sp.sosfilt(sos, data["v5"])
            # data["v"] = sp.sosfilt(sos, data["v"])
            # data["i"] = sp.sosfilt(sos, data["i"])
            return data

"""
Module De définition des outils des mesure
"""
from threading import Thread
import queue
from Tools.Device import findDevice
import numpy as np


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
                return
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
            for line in lines:
                it = line.split()
                if len(it) != 4:
                    self.parent.log("format de linge incorrect")
                try:
                    tt = float(it[0])/1.e6
                    tax = float(it[1])
                    tay = float(it[2])
                    taz = float(it[3])
                    time.append(tt)
                    ax.append(tax)
                    ay.append(tay)
                    az.append(taz)
                except Exception as err:
                    self.parent.log("Mauvais décodage de la chaine '" + line + "' : " + str(err))
            data = {"time": np.array(time), "ax": np.array(ax), "ay": np.array(ay), "az": np.array(az)}
            data["ax"] = data["ax"] - data["ax"].mean()
            data["ay"] = data["ay"] - data["ay"].mean()
            data["az"] = data["az"] - data["az"].mean()
            return data

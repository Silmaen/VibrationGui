"""
Rassemblement d'outils de calcul
"""


def compute_period(data_t):
    """
    Calcule la période moyen d'une série de timestamps
    :param data_t: la série de timestamps
    :return: (dt, freq, écart type)
    """
    import numpy as np
    if np.size(data_t) < 2:
        return 0, 0, 0
    n = np.size(data_t)
    g = np.zeros(n - 1)
    for i in range(n - 1):
        if i == 0:
            continue
        g[i] = data_t[i] - data_t[i - 1]
    dt = g.mean()
    if dt == 0:
        return 0, 0, 0
    return dt, 1.0 / dt, g.std()


def fftw(input_data):
    """
    Calcul de la transformée de Fourier
    :param input_data: le tableau de données à traiter
    :return: la transformée de Fourier
    """
    import pyfftw
    import numpy as np
    out_length = len(input_data) // 2 + 1
    a = pyfftw.empty_aligned(len(input_data), dtype='float32')
    out_data = pyfftw.empty_aligned(out_length, dtype='complex64')
    fft_obj = pyfftw.FFTW(a, out_data, flags=('FFTW_ESTIMATE',), planning_timelimit=1.0)
    a[:] = np.array(input_data, dtype='float32')
    return fft_obj()


def RMS_curve(data_t, data_x, data_y=None, data_z=None):
    """
    calcule la RMS jusqu'à 3 courbes
    :param data_t: l'échantillonnage en temps
    :param data_x: première courbe
    :param data_y: seconde courbe
    :param data_z: troisième courbe
    """
    import numpy as np
    if np.size(data_t) < 2:
        return None
    d, f, s = compute_period(data_t)
    n = np.size(data_t)
    window = np.int(np.floor(f / 10))
    steps = np.int_(np.floor(n / window))
    t_rms = np.zeros(steps)
    x_rms = np.zeros(steps)
    y_rms = np.zeros(steps)
    z_rms = np.zeros(steps)
    for i in range(0, steps):
        t_rms[i] = np.mean(data_t[(i * window):((i + 1) * window)])
        x_rms[i] = np.sqrt(np.mean(data_x[(i * window):((i + 1) * window)] ** 2))
        if data_y is not None:
            y_rms[i] = np.sqrt(np.mean(data_y[(i * window):((i + 1) * window)] ** 2))
            if data_z is not None:
                z_rms[i] = np.sqrt(np.mean(data_z[(i * window):((i + 1) * window)] ** 2))
    if data_y is None:
        return t_rms, x_rms
    if data_z is None:
        return t_rms, x_rms, y_rms
    return t_rms, x_rms, y_rms, z_rms


def compute_spectrogram(data_t, data_x):
    """
    Calcule le spectrogramme
    :param data_t: échelle de temps
    :param data_x: le signal
    :return: fréquences, temps, intensité
    """
    from scipy import signal
    d, fs, s = compute_period(data_t)
    f, t2, sxx = signal.spectrogram(data_x, fs=fs, nperseg=int(fs), noverlap=int(fs)-1)
    return f, t2, sxx


def compute_PSD(data_t, data_x, data_y=None, data_z=None):
    """
    Calcule la courbe de puissance spectrale
    :param data_t: échelle de temps
    :param data_x: première courbe
    :param data_y: seconde courbe
    :param data_z: troisième courbe
    :return: fréquences, intensité
    """
    from scipy import signal
    d, fs, s = compute_period(data_t)
    f, pxx = signal.welch(data_x, fs=fs, nperseg=int(2*fs), noverlap=int(2*fs)-1)
    f, pyy = signal.welch(data_y, fs=fs, nperseg=int(2*fs), noverlap=int(2*fs)-1)
    f, pzz = signal.welch(data_z, fs=fs, nperseg=int(2*fs), noverlap=int(2*fs)-1)
    if data_y is None:
        return f, pxx
    if data_z is None:
        return f, pxx, pyy
    return f, pxx, pyy, pzz


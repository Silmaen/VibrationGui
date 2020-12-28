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
    N = np.size(data_t)
    g = np.zeros(N - 1)
    for i in range(N-1):
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
    outLength = len(input_data) // 2 + 1
    a = pyfftw.empty_aligned(len(input_data), dtype='float32')
    outData = pyfftw.empty_aligned(outLength, dtype='complex64')
    fft_obj = pyfftw.FFTW(a, outData, flags=('FFTW_ESTIMATE',), planning_timelimit=1.0)
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
    N = np.size(data_t)
    window = np.int(np.floor(f/10))
    steps = np.int_(np.floor(N / window))
    t_RMS = np.zeros(steps)
    x_RMS = np.zeros(steps)
    y_RMS = np.zeros(steps)
    z_RMS = np.zeros(steps)
    for i in range(0, steps):
        t_RMS[i] = np.mean(data_t[(i * window):((i + 1) * window)])
        x_RMS[i] = np.sqrt(np.mean(data_x[(i * window):((i + 1) * window)] ** 2))
        if data_y is not None:
            y_RMS[i] = np.sqrt(np.mean(data_y[(i * window):((i + 1) * window)] ** 2))
            if data_z is not None:
                z_RMS[i] = np.sqrt(np.mean(data_z[(i * window):((i + 1) * window)] ** 2))
    if data_y is None:
        return t_RMS, x_RMS
    if data_z is None:
        return t_RMS, x_RMS, y_RMS
    return t_RMS, x_RMS, y_RMS, z_RMS

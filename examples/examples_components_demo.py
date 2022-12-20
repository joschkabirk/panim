from panim import *
import os
import numpy as np

z = np.linspace(-20, 200, 10000)
# +z_max=100 - nice settings to get three good pulses with stretching

# Pictures of frequency chirpes pulses
os.makedirs("plots", exist_ok=True)
os.makedirs("plots/chirped_pulses", exist_ok=True)
plot_pulses(
    z,
    np.linspace(0, 500, 3),
    nu_center=0.15,
    k_i=[1, 3, 2, 5],
    no_axes=True,
    plotname="./plots/chirped_pulses/pulses",
    figuresize=(11, 1),
    colors=["steelblue", "orange", "forestgreen"],
    spec_width=100,
)

# Spectral components of a pulse
os.makedirs("plots/sum_demonstration", exist_ok=True)
z = np.linspace(-70, 70, 1000)
d = sin_sum(
    z,
    0,
    N_frequencies=4000,
    nu_center=0.15,
    k_i=(1, 3, 2),
    spec_width=100,
    plotting=True,
    figuresize=(11, 1.2),
    savein="./plots/sum_demonstration",
)

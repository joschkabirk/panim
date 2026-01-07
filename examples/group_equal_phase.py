import os

import numpy as np

from panim import *

z = np.linspace(-20, 200, 10000)
# +z_max=100 - nice settings to get three good pulses with stretching
os.makedirs("plots", exist_ok=True)

# Special case without dispersion
z = np.linspace(0, 200, 1000)
p = calc_pulses(
    z,
    t_start=0,
    t_end=2000,
    n_steps=200,
    nu_center=0.02,
    k_i=[10 * 2 * np.pi * 0.02, 10, 0],
    spec_width=600,
)
animate(
    z,
    p,
    ms_between_frames=40,
    figuresize=(14, 4),
    saveas="./plots/group_equal_phase.gif",
)

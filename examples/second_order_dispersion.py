import os

import numpy as np

from panim import animate, calc_pulses

z = np.linspace(-20, 200, 10000)
os.makedirs("plots", exist_ok=True)


# Second order dispersion (group delay dispersion/ group velocity dispersion)
# (see https://www.rp-photonics.com/group_velocity_dispersion.html)
z = np.linspace(-30, 600, 1000)
p = calc_pulses(
    z,
    t_start=0,
    t_end=2500,
    n_steps=50,
    nu_center=0.02,
    k_i=[1, 3, 2],
    spec_width=600,
)
animate(
    z,
    p,
    ms_between_frames=40,
    figuresize=(14, 4),
    saveas="./plots/second_order_dispersion.gif",
)

import os

import numpy as np

from panim import animate, calc_pulses

z = np.linspace(-20, 200, 10000)
os.makedirs("plots", exist_ok=True)

# See here for overview of dispersion terms:
# https://www.rp-photonics.com/chromatic_dispersion.html

# First order dispersion
z = np.linspace(0, 100, 1000)
p = calc_pulses(
    z,
    t_start=0,
    t_end=1000,
    n_steps=200,
    nu_center=0.025,
    k_i=[4, 10, 0],
    spec_width=600,
)
animate(
    z,
    p,
    ms_between_frames=40,
    figuresize=(14, 4),
    saveas="./plots/first_order_dispersion.gif",
)

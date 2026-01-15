"""First order dispersion example.

See: https://www.rp-photonics.com/chromatic_dispersion.html
"""

from pathlib import Path

import numpy as np

from panim import animate, calc_pulses

Path("plots").mkdir(exist_ok=True)

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
    fps=15,
    figuresize=(7, 2.2),
    saveas="./plots/first_order_dispersion.gif",
    dpi=80,
)

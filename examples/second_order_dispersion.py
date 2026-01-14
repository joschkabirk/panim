"""Second order dispersion (group velocity dispersion) example.

See: https://www.rp-photonics.com/group_velocity_dispersion.html
"""

from pathlib import Path

import numpy as np

from panim import animate, calc_pulses

Path("plots").mkdir(exist_ok=True)

# Second order dispersion (group delay dispersion / group velocity dispersion)
z = np.linspace(-30, 180, 1000)
p = calc_pulses(
    z,
    t_start=0,
    t_end=700,
    n_steps=200,
    nu_center=0.02,
    k_i=[1, 3, 7],
    spec_width=600,
)
animate(
    z,
    p,
    fps=15,
    figuresize=(7, 2.2),
    saveas="./plots/second_order_dispersion.gif",
    dpi=80,
)

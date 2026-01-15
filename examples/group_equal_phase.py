"""Group velocity equals phase velocity (no dispersion) example."""

from pathlib import Path

import numpy as np

from panim import animate, calc_pulses

Path("plots").mkdir(exist_ok=True)

# Special case without dispersion: group velocity = phase velocity
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
    fps=15,
    figuresize=(7, 2.2),
    saveas="./plots/group_equal_phase.gif",
    dpi=80,
)

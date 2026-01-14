"""Illustration of the difference between spatial and time domain representation.

This example simulates the propagation of optical pulses through a fibre
and creates an animation that shows both the spatial and time domain views
of the pulses as they evolve along the fibre length.
"""

from pathlib import Path

import numpy as np

from panim import animate_with_time, calc_pulses

Path("plots").mkdir(exist_ok=True)

# Simulate pulse propagation through optical fibre
z = np.linspace(-30, 180, 1000)
p = calc_pulses(
    z,
    t_start=0,
    t_end=900,
    n_steps=200,
    nu_center=0.02,
    k_i=[1, 3, 7],
    spec_width=600,
)

animate_with_time(
    z,
    p,
    fixed_z_1=900,
    fixed_z_2=None,
    figuresize=(7, 4.4),
    fps=20,
    saveas="./plots/spatial_vs_time.gif",
    z_offset=5,
    dpi=80,
)

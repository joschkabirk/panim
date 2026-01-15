"""Optical fibre pulse propagation example.

Visualizes pulse propagation through an optical fibre with:
- Top panel: Spatial pulse propagation along the fibre
- Middle panel: Electric field vs time at the fibre input (z_1)
- Bottom panel: Electric field vs time at the fibre output (z_2)

This demonstrates how dispersion affects the pulse shape as it
travels through the fibre.
"""

from pathlib import Path

import numpy as np

from panim import animate_with_time, calc_pulses

Path("plots").mkdir(exist_ok=True)

# Simulate pulse propagation through optical fibre
z = np.linspace(0, 110, 500)
p = calc_pulses(
    z,
    t_start=-300,
    t_end=2000,
    n_steps=300,
    nu_center=0.02,
    k_i=[10 * 2 * np.pi * 0.02, 10, 20, 0],
    spec_width=500,
)

# Create animation showing spatial propagation and temporal field at two positions
animate_with_time(
    z,
    p,
    fixed_z_1=0,  # Fibre input (refers to the index in the z array)
    fixed_z_2=-1,  # Fibre output (refers to the index in the z array)
    figuresize=(7, 6.6),
    fps=15,
    saveas="./plots/optical_fibre.gif",
    z_offset=5,
    dpi=80,
)

from panim import *
import os
import numpy as np

z = np.linspace(-20, 200, 10000)
# +z_max=100 - nice settings to get three good pulses with stretching

# Pictures of frequency chirpes pulses
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
    saveas="./examples_output/group_equal_phase.gif",
)

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
    saveas="./examples_output/1st_order_dispersion.gif",
)

# Second order dispersion (group delay dispersion/ group velocity dispersion)
# (see https://www.rp-photonics.com/group_velocity_dispersion.html)
z = np.linspace(-30, 600, 1000)
p = calc_pulses(
    z, t_start=0, t_end=2500, n_steps=500, nu_center=0.02, k_i=[1, 3, 2], spec_width=600,
)
animate(
    z,
    p,
    ms_between_frames=40,
    figuresize=(14, 4),
    saveas="./examples_output/group_velocity_dispersion.gif",
)

# Third order dispersion
z = np.linspace(-30, 600, 1000)
p = calc_pulses(
    z,
    t_start=0,
    t_end=2500,
    n_steps=200,
    nu_center=0.02,
    k_i=[1, 3, 2, 6],
    spec_width=600,
)
animate(
    z,
    p,
    ms_between_frames=40,
    figuresize=(14, 4),
    saveas="./examples_output/3rd_order_dispersion.gif",
)

"""Demo of spectral components and chirped pulses."""

from pathlib import Path

import numpy as np

from panim import plot_pulses, plot_spectral_components

z = np.linspace(-20, 200, 10000)
# +z_max=100 - nice settings to get three good pulses with stretching

# Pictures of frequency chirped pulses
Path("plots/chirped_pulses").mkdir(parents=True, exist_ok=True)
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
Path("plots/sum_demonstration").mkdir(parents=True, exist_ok=True)
z = np.linspace(-70, 70, 1000)
plot_spectral_components(
    z,
    t=0,
    n_frequencies=4000,
    nu_center=0.15,
    k_i=[1, 3, 2],
    spec_width=100,
    figuresize=(11, 1.2),
    savedir="./plots/sum_demonstration",
)

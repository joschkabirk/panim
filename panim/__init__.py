"""panim - Pulse Animation Library.

A library for visualizing the construction and propagation of light pulses
as sums of spectral components with frequency-dependent properties.

Examples
--------
Basic usage:

>>> import numpy as np
>>> from panim import calc_pulses, animate
>>> z = np.linspace(0, 100, 500)
>>> pulses = calc_pulses(z, t_start=0, t_end=100, n_steps=50)
>>> animate(z, pulses, saveas="pulse.gif")

"""

from panim._version import __version__
from panim.animation import animate, animate_with_time
from panim.core import (
    c,
    calc_pulses,
    compute_spectral_field,
    wave_vector,
)
from panim.plotting import plot_pulses, plot_spectral_components
from panim.resonator import animate_resonator, resonator_modes

__all__ = [
    # Version
    "__version__",
    # Constants
    "c",
    # Core physics
    "wave_vector",
    "compute_spectral_field",
    "calc_pulses",
    # Animation
    "animate",
    "animate_with_time",
    # Plotting
    "plot_pulses",
    "plot_spectral_components",
    # Resonator
    "resonator_modes",
    "animate_resonator",
]

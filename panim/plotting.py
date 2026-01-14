"""Static plotting functions for pulse visualization.

This module provides functions to create static plots of light pulses
and their spectral components.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.signal import windows

from panim.core import compute_spectral_field, wave_vector

if TYPE_CHECKING:
    from collections.abc import Sequence

    from matplotlib.figure import Figure


def plot_pulses(
    z: NDArray[np.floating],
    times: ArrayLike,
    nu_center: float = 0.5,
    k_i: Sequence[float] | None = None,
    spec_width: float = 400.0,
    no_axes: bool = False,
    plotname: str | Path = "",
    dpi: int = 100,
    figuresize: tuple[float, float] = (11, 4),
    z_arrow: bool = False,
    colors: Sequence[str] | None = None,
) -> Figure:
    """Plot pulses at multiple time points on a single figure.

    Parameters
    ----------
    z : ndarray
        Spatial coordinate array (propagation axis).
    times : array_like
        Time points at which to plot the pulse.
    nu_center : float, optional
        Center frequency of the spectrum. Default is 0.5.
    k_i : sequence of float, optional
        Wave vector coefficients. Default is [1, 10, 0].
    spec_width : float, optional
        Spectral width parameter. Default is 400.0.
    no_axes : bool, optional
        If True, hide axes. Default is False.
    plotname : str or Path, optional
        Base path for saving plots (without extension).
    dpi : int, optional
        Resolution for saved figures. Default is 100.
    figuresize : tuple of float, optional
        Figure size (width, height) in inches. Default is (11, 4).
    z_arrow : bool, optional
        If True, draw an arrow indicating propagation direction.
        Default is False.
    colors : sequence of str, optional
        Colors for each time step. Default is steelblue for all.

    Returns
    -------
    Figure
        The matplotlib figure object.

    Examples
    --------
    >>> import numpy as np
    >>> from panim import plot_pulses
    >>> z = np.linspace(0, 100, 500)
    >>> fig = plot_pulses(z, [0, 5, 10], colors=['blue', 'green', 'red'])
    """
    times_arr = np.asarray(times)
    if k_i is None:
        k_i = [1.0, 10.0, 0.0]
    if colors is None:
        colors = ["steelblue"] * len(times_arr)

    # Compute pulses at each time
    pulses = [
        compute_spectral_field(
            z, float(t), nu_center=nu_center, k_coefficients=k_i, spec_width=spec_width
        )
        for t in times_arr
    ]

    fig, ax = plt.subplots(figsize=figuresize, dpi=dpi, frameon=False)

    ax.set_xlim(z.min(), z.max())
    ymax = pulses[0].max() * 1.1
    ymin = pulses[0].min() * 1.1

    if z_arrow:
        ymin *= 2

    ax.set_ylim(ymin, ymax)

    if no_axes:
        plt.axis("off")
        if z_arrow:
            _draw_z_arrow(ax, z, ymin)

    for i, pulse in enumerate(pulses):
        ax.plot(z, pulse, color=colors[i])

        if plotname:
            plotname_str = str(plotname)
            if len(pulses) > 1:
                plotname_full = f"{plotname_str}_{i + 1}.pdf"
            else:
                plotname_full = f"{plotname_str}.pdf"

            print(f"Saving as {plotname_full}")
            fig.savefig(plotname_full)

    return fig


def plot_spectral_components(
    z: NDArray[np.floating],
    t: float,
    nu_center: float = 1.0,
    nu_min: float = 0.001,
    n_frequencies: int = 4000,
    spec_width: float = 200.0,
    k_i: Sequence[float] | None = None,
    figuresize: tuple[float, float] = (11, 4),
    savedir: str | Path = "",
) -> tuple[Figure, Figure, Figure]:
    """Plot spectral components, resulting pulse, and spectrum.

    Creates three figures showing the decomposition of the pulse
    into spectral components.

    Parameters
    ----------
    z : ndarray
        Spatial coordinate array.
    t : float
        Time at which to calculate the field.
    nu_center : float, optional
        Center frequency. Default is 1.0.
    nu_min : float, optional
        Minimum frequency. Default is 0.001.
    n_frequencies : int, optional
        Number of frequency components. Default is 4000.
    spec_width : float, optional
        Spectral width parameter. Default is 200.0.
    k_i : sequence of float, optional
        Wave vector coefficients. Default is [1, 5, 0].
    figuresize : tuple of float, optional
        Figure size for component and pulse plots. Default is (11, 4).
    savedir : str or Path, optional
        Directory to save plots. If empty, plots are not saved.

    Returns
    -------
    tuple of Figure
        (components_fig, pulse_fig, spectrum_fig)
    """
    if k_i is None:
        k_i = [1.0, 5.0, 0.0]

    # Pad coefficients
    k_coeffs = list(k_i) + [0.0] * (4 - len(k_i))

    # Create frequency array and spectrum
    frequencies = np.linspace(nu_min, nu_center * 2, n_frequencies)
    spectrum = windows.gaussian(len(frequencies), std=spec_width)

    # Compute spectral components
    E_components = np.zeros((len(frequencies), len(z)))
    for i, freq in enumerate(frequencies):
        phi = wave_vector(freq, nu_center, *k_coeffs[:4]) * z
        E_components[i, :] = spectrum[i] * np.sin(2 * np.pi * freq * t - phi)

    E_field = E_components.sum(axis=0)

    # Determine which components to plot
    n_plot_min = int(n_frequencies / 5)
    n_plot_max = int(4 * n_frequencies / 5)
    spacing = 10
    plot_indices = range(n_plot_min, n_plot_max, spacing)

    # Save directory setup
    savedir_path = Path(savedir) if savedir else None
    if savedir_path:
        savedir_path.mkdir(parents=True, exist_ok=True)

    # Plot spectral components
    fig_components, ax_comp = plt.subplots(figsize=figuresize, frameon=False)
    ax_comp.set_xlim(z.min(), z.max())
    ax_comp.set_ylim(E_components.min() * 1.1, E_components.max() * 1.1)
    plt.axis("off")

    for i in plot_indices:
        ax_comp.plot(z, E_components[i])

    if savedir_path:
        fig_components.savefig(savedir_path / "spectral_components.pdf")

    # Plot resulting pulse
    fig_pulse, ax_pulse = plt.subplots(figsize=figuresize, frameon=False)
    ax_pulse.set_xlim(z.min(), z.max())
    ax_pulse.set_ylim(E_field.min() * 2, E_field.max())
    plt.axis("off")
    ax_pulse.plot(z, E_field)

    if savedir_path:
        fig_pulse.savefig(savedir_path / "resulting_pulse.pdf")

    # Plot spectrum
    fig_spectrum, ax_spec = plt.subplots(figsize=(6, 4), frameon=False)
    ax_spec.plot(frequencies, spectrum)
    ax_spec.set_xlabel(r"Frequency $\nu$")
    ax_spec.set_ylabel(r"Spectral amplitude $S(\nu)$")

    if savedir_path:
        fig_spectrum.savefig(savedir_path / "spectrum.pdf")

    return fig_components, fig_pulse, fig_spectrum


def _draw_z_arrow(ax, z: NDArray[np.floating], ymin: float) -> None:
    """Draw a z-direction arrow on the axis."""
    z_mean = z.mean()
    arrow_start = z_mean - 0.2 * z_mean
    arrow_end = z_mean + 0.2 * z_mean
    text_x = z_mean - 0.1 * z_mean

    ax.annotate(
        "",
        xytext=(arrow_start, ymin),
        xy=(arrow_end, ymin),
        arrowprops={"arrowstyle": "->"},
    )
    ax.annotate(
        "position $z$",
        xytext=(text_x, 0.9 * ymin),
        xy=(z_mean, 0.9 * ymin),
    )

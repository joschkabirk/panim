"""Resonator and cavity mode functions.

This module provides functions for calculating and visualizing
optical resonator eigenmodes and mode-locking phenomena.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from matplotlib import animation
from numpy.typing import NDArray
from tqdm import tqdm

if TYPE_CHECKING:
    pass

# Speed of light (normalized)
c: float = 1.0


def resonator_modes(
    t: float,
    z: NDArray[np.floating],
    n_modes: int = 3,
    random_phases: bool = False,
    plot: bool = True,
    figuresize: tuple[float, float] = (10, 4),
    savedir: str | Path = "",
) -> NDArray[np.floating]:
    """Calculate resonator eigenmode decomposition.

    Computes the standing wave modes of an optical cavity and their
    superposition at a given time.

    Parameters
    ----------
    t : float
        Time at which to calculate the modes.
    z : ndarray
        Spatial coordinate array (cavity length).
    n_modes : int, optional
        Number of modes to include. Default is 3.
    random_phases : bool, optional
        If True, assign random phases to each mode. Default is False.
    plot : bool, optional
        If True, create plots of individual modes and sum. Default is True.
    figuresize : tuple of float, optional
        Figure size for plots. Default is (10, 4).
    savedir : str or Path, optional
        Directory to save plots. If empty, plots are shown but not saved.

    Returns
    -------
    E_modes : ndarray
        Array of shape (n_modes, len(z)) containing each mode's field.

    Notes
    -----
    The resonator mode frequencies are determined by:
        delta_nu = c / (2 * L)
    where L is the cavity length (z.max() - z.min()).
    """
    # Cavity length and mode spacing
    length = z.max() - z.min()
    delta_nu = c / (2 * length)
    frequencies = np.array([delta_nu * i for i in range(1, n_modes + 1)])

    # Mode phases
    phases = np.zeros(n_modes)
    if random_phases:
        phases = np.random.uniform(0, 200, n_modes)

    # Uniform spectrum (could be generalized)
    spectrum = np.ones(n_modes)

    # Calculate mode fields
    E_modes = np.zeros((n_modes, len(z)))

    savedir_path = Path(savedir) if savedir else None
    if savedir_path:
        savedir_path.mkdir(parents=True, exist_ok=True)

    if plot:
        fig, axs = plt.subplots(2, 1, figsize=figuresize, dpi=100, frameon=False)
        axs[0].axis("off")
        axs[1].axis("off")
        axs[0].set_xlim(z.min(), z.max())
        axs[1].set_xlim(z.min(), z.max())

    for i in range(n_modes):
        omega = 2 * np.pi * frequencies[i]
        k = omega / c
        E_modes[i, :] = spectrum[i] * np.sin(2 * omega * t - phases[i]) * np.sin(k * z)

        if plot:
            # Individual mode plot
            fig_mode, ax_mode = plt.subplots(figsize=(10, 2), dpi=100, frameon=False)
            ax_mode.set_ylim(-1.1, 1.1)
            ax_mode.axis("off")
            ax_mode.plot(z, E_modes[i])
            axs[0].plot(z, E_modes[i], label=str(i))

            if savedir_path:
                fig_mode.savefig(savedir_path / f"mode_{i}.pdf")
                plt.close(fig_mode)

    if plot:
        E_total = E_modes.sum(axis=0)
        maximum = np.max(np.abs(E_total))
        axs[1].set_ylim(-1.2 * maximum, 1.2 * maximum)
        axs[1].plot(z, E_total)

        # Sum plot
        fig_sum, ax_sum = plt.subplots(figsize=(10, 2), dpi=100, frameon=False)
        ax_sum.axis("off")
        ax_sum.plot(z, E_total)

        if savedir_path:
            fig.savefig(savedir_path / "modes_both.pdf")
            fig_sum.savefig(savedir_path / "modes_sum.pdf")
            plt.close(fig)
            plt.close(fig_sum)

    return E_modes


def animate_resonator(
    z: NDArray[np.floating],
    times: NDArray[np.floating],
    n_modes: int,
    fps: int = 15,
    figuresize: tuple[float, float] = (11, 4),
    saveas: str | Path = "",
    *,
    show_progress: bool = True,
) -> HTML | None:
    """Animate the time evolution of resonator modes.

    Parameters
    ----------
    z : ndarray
        Spatial coordinate array (cavity extent).
    times : ndarray
        Array of time points to animate.
    n_modes : int
        Number of modes to include.
    fps : int, optional
        Frames per second for the animation. Default is 15.
    figuresize : tuple of float, optional
        Figure size. Default is (11, 4).
    saveas : str or Path, optional
        Path to save animation as .gif. If empty, returns HTML.
    show_progress : bool, optional
        Whether to show progress bar. Default is True.

    Returns
    -------
    HTML or None
        HTML5 video for Jupyter if saveas is empty, otherwise None.
    """
    # Calculate modes at all times
    time_iter = tqdm(times) if show_progress else times
    modes = [resonator_modes(t, z, n_modes, plot=False) for t in time_iter]

    sum_iter = tqdm(modes) if show_progress else modes
    pulses = [E_i.sum(axis=0) for E_i in sum_iter]

    fig, ax = plt.subplots(figsize=figuresize)

    ax.set_xlim(z.min(), z.max())
    maximum = np.max(np.abs(np.array(pulses)))
    ax.set_ylim(-1.2 * maximum, 1.2 * maximum)
    ax.set_xlabel(r"position $z$")

    (line,) = ax.plot([], [], color="forestgreen")

    def init() -> tuple:
        line.set_data([], [])
        return (line,)

    def update(frame: int) -> tuple:
        line.set_data(z, pulses[frame])
        return (line,)

    plt.close()

    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        blit=True,
        frames=len(pulses),
        interval=1000 / fps,
    )

    saveas_str = str(saveas)
    if saveas_str:
        fps = int(fps)
        anim.save(saveas_str, writer="imagemagick", fps=fps)
        return None

    return HTML(anim.to_html5_video())

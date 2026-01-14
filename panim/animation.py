"""Animation functions for visualizing pulse propagation.

This module provides functions to create animations of light pulse
propagation and time evolution.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from matplotlib import animation
from numpy.typing import NDArray

if TYPE_CHECKING:
    pass


def animate(
    z: NDArray[np.floating],
    pulses: NDArray[np.floating],
    fps: int = 30,
    figuresize: tuple[float, float] = (11, 4),
    saveas: str | Path = "",
    dpi: int = 72,
) -> HTML | None:
    """Animate the time evolution of a wave packet.

    Creates an animation showing the pulse propagating along the z-axis.

    Parameters
    ----------
    z : ndarray
        Spatial coordinate array (propagation axis).
    pulses : ndarray
        Array of shape (n_steps, len(z)) containing the electric field
        at each time step.
    fps : int, optional
        Frames per second for the animation. Default is 30.
    figuresize : tuple of float, optional
        Figure size (width, height) in inches. Default is (11, 4).
    saveas : str or Path, optional
        Path to save the animation. Supports .mp4 and .gif formats.
        If empty, returns HTML for Jupyter display.
    dpi : int, optional
        Resolution in dots per inch. Lower values reduce file size.
        Default is 72.

    Returns
    -------
    HTML or None
        HTML5 video for Jupyter notebooks if saveas is empty,
        otherwise None (animation is saved to file).

    Examples
    --------
    >>> import numpy as np
    >>> from panim import calc_pulses, animate
    >>> z = np.linspace(0, 100, 500)
    >>> pulses = calc_pulses(z, 0, 100, 50, show_progress=False)
    >>> html = animate(z, pulses)  # Returns HTML for Jupyter
    """
    fig, ax = plt.subplots(figsize=figuresize, dpi=dpi)

    ax.set_xlim(z.min(), z.max())
    ax.set_ylim(1.2 * pulses.min(), 1.2 * pulses.max())
    ax.set_xlabel(r"Position $z$ [a.u.]")
    ax.set_ylabel(r"Electric field $E$ [a.u.]")
    ax.set_yticks([])

    (line,) = ax.plot([], [], color="tab:blue")
    fig.tight_layout()

    def init() -> tuple:
        line.set_data([], [])
        return (line,)

    def update(frame: int) -> tuple:
        line.set_data(z, pulses[frame, :])
        return (line,)

    plt.close()

    interval_ms = 1000 / fps

    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        blit=True,
        frames=len(pulses),
        interval=interval_ms,
    )

    saveas_str = str(saveas)
    if saveas_str:
        _save_animation(anim, saveas_str, fps)
        return None

    return HTML(anim.to_html5_video())


def animate_with_time(
    z: NDArray[np.floating],
    pulses: NDArray[np.floating],
    fps: int = 30,
    figuresize: tuple[float, float] = (11, 4),
    saveas: str | Path = "",
    fixed_z_1: int = 0,
    fixed_z_2: int | None = 1,
    z_offset: float = 0,
    dpi: int = 72,
) -> HTML | None:
    """Animate pulse propagation with temporal field views at fixed positions.

    Creates a 2- or 3-panel animation depending on whether one or two
    observation points are specified:
    - Top: Spatial pulse propagation along z-axis
    - Middle (if fixed_z_2 is not None): Electric field vs time at position z_1
    - Bottom: Electric field vs time at position z_2 (or z_1 if only one point)

    Parameters
    ----------
    z : ndarray
        Spatial coordinate array (propagation axis).
    pulses : ndarray
        Array of shape (n_steps, len(z)) containing the electric field
        at each time step.
    fps : int, optional
        Frames per second for the animation. Default is 30.
    figuresize : tuple of float, optional
        Figure size (width, height) in inches. Default is (11, 4).
    saveas : str or Path, optional
        Path to save the animation. Supports .mp4 and .gif formats.
    fixed_z_1 : int, optional
        Index in z array for first observation point. Default is 0.
    fixed_z_2 : int or None, optional
        Index in z array for second observation point. Default is 1.
        If None, only one observation point is shown (2-panel layout).
    z_offset : float, optional
        Extra margin for z-axis limits. Default is 0.
    dpi : int, optional
        Resolution in dots per inch. Lower values reduce file size.
        Default is 72.

    Returns
    -------
    HTML or None
        HTML5 video for Jupyter notebooks if saveas is empty,
        otherwise None (animation is saved to file).
    """
    # Normalize pulses
    pulses_norm = pulses / pulses.max()

    single_point = fixed_z_2 is None
    n_panels = 2 if single_point else 3

    fig, axs = plt.subplots(n_panels, 1, figsize=figuresize, dpi=dpi)

    # Configure axes
    axs[0].set_xlim(z.min() - z_offset, z.max() + z_offset)
    axs[1].set_xlim(0, len(pulses_norm))
    if not single_point:
        axs[2].set_xlim(0, len(pulses_norm))

    for ax in axs:
        ax.set_ylim(1.2 * pulses_norm.min(), 1.2 * pulses_norm.max())
        ax.set_yticks([])

    axs[0].set_xlabel(r"Position $z$ [a.u.]")
    axs[1].set_xlabel(r"Time $t$ [a.u.]")
    if not single_point:
        axs[2].set_xlabel(r"Time $t$ [a.u.]")

    for ax in axs:
        ax.set_ylabel(r"Electric field $E$ [a.u.]")

    axs[0].set_title(r"Pulse propagation along the $z$-axis")
    if single_point:
        axs[1].set_title(rf"Electric field at position $z = {z[fixed_z_1]:.2f}$")
    else:
        axs[1].set_title(r"Electric field at position $z_1$")
        axs[2].set_title(r"Electric field at position $z_2$")

    # Create line artists
    (line_spatial,) = axs[0].plot([], [], color="tab:blue")
    (line_z1,) = axs[1].plot([], [], color="forestgreen")
    if not single_point:
        (line_z2,) = axs[2].plot([], [], color="darkred")

    # Mark observation points
    axs[0].axvline(z[fixed_z_1], color="forestgreen", lw=5, label=r"$z_1$")
    if not single_point:
        axs[0].axvline(z[fixed_z_2], color="darkred", lw=5, label=r"$z_2$")
        axs[0].legend(loc="upper center", ncol=2)
    else:
        axs[0].legend(loc="upper center", ncol=1)
    fig.tight_layout()

    if single_point:

        def init() -> tuple:
            line_spatial.set_data([], [])
            line_z1.set_data([], [])
            return line_spatial, line_z1

        def update(frame: int) -> tuple:
            line_spatial.set_data(z, pulses_norm[frame, :])
            line_z1.set_data(range(frame), pulses_norm[:frame, fixed_z_1])
            return line_spatial, line_z1

    else:

        def init() -> tuple:
            line_spatial.set_data([], [])
            line_z1.set_data([], [])
            line_z2.set_data([], [])
            return line_spatial, line_z1, line_z2

        def update(frame: int) -> tuple:
            line_spatial.set_data(z, pulses_norm[frame, :])
            line_z1.set_data(range(frame), pulses_norm[:frame, fixed_z_1])
            line_z2.set_data(range(frame), pulses_norm[:frame, fixed_z_2])
            return line_spatial, line_z1, line_z2

    interval_ms = 1000 / fps

    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        blit=False,
        frames=len(pulses_norm),
        interval=interval_ms,
    )
    plt.close()

    saveas_str = str(saveas)
    if saveas_str:
        _save_animation(anim, saveas_str, fps)
        return None

    return HTML(anim.to_html5_video())


def _save_animation(
    anim: animation.FuncAnimation,
    saveas: str,
    fps: int,
) -> None:
    """Save animation to file.

    Parameters
    ----------
    anim : FuncAnimation
        The animation object to save.
    saveas : str
        Output file path.
    fps : int
        Frames per second for the saved animation.
    """
    if saveas.endswith(".mp4"):
        writer = animation.FFMpegWriter(
            fps=fps,
            metadata={"artist": "panim"},
            bitrate=1800,
        )
        print(f"Saving as {saveas}")
        anim.save(saveas, writer=writer)

    elif saveas.endswith(".gif"):
        print(f"Saving as {saveas}")
        anim.save(saveas, writer="imagemagick", fps=fps)

    else:
        # Save both formats
        writer = animation.FFMpegWriter(
            fps=fps,
            metadata={"artist": "panim"},
            bitrate=1800,
        )
        mp4_path = f"{saveas}.mp4"
        gif_path = f"{saveas}.gif"

        print(f"Saving as {mp4_path}")
        anim.save(mp4_path, writer=writer)
        print(f"Saving as {gif_path}")
        anim.save(gif_path, writer="imagemagick", fps=fps)
